from venture.objects.file_type import FileType
import venture.prompts.system_ownership as system_ownership
import venture.prompts.system_summary as system_summary
from venture.objects.parse_result import ParseResult
import venture.logic.model_selector_logic as model_selector_logic
from venture.objects.parsed_doc import ParsedDoc
import venture.logic.token_count_logic as token_count_logic
import venture.casual_utils as casual_utils 
import venture.logic.openai_logic as openai_logic
import venture.logic.loaders_logic as lolo
import venture.logic.function_name_logic as fnlo
from venture.metadata import Metadata
from typing import Dict, Set, Tuple
from venture.config import Config
from pdf2docx import Converter
import docx2txt
import json
import time
import uuid


def index_cosmos__read_file(file_path:str, file_type:FileType):
    # VERIFY THIS IS DOC IS PARSABLE
    if file_type == FileType.DOCX.value:
        text = docx2txt.process(file_path)
        return text
    elif file_type == FileType.PDF.value:
        temp_file_name = str(uuid.uuid4()) + '.docx'
        with open(file_path) as pdf:
            cv = Converter(pdf)      
            cv.convert(casual_utils.get_index_path()+temp_file_name)
            cv.close()
            text = docx2txt.process(casual_utils.get_index_path()+temp_file_name)
            casual_utils.delete_file(casual_utils.get_index_path()+temp_file_name)
            return text
    elif file_type == FileType.TXT.value:
        text = casual_utils.read_text_from_file(file_path)
        return text
    else:
        return None

def index_cosmos__extract_summary_from_doc(metadata:Metadata, file_name_no_suffix:str, doc_as_string: str, processed_doc_token_count:int):
    system_message = system_summary.SYSTEM_MESSAGE
    model_name = model_selector_logic.get_model_name_for_summary_extract(metadata, processed_doc_token_count)
    user_message = f'Input:\n```\n{doc_as_string}\n```'
    output = openai_logic.openai_chat_completion(metadata=metadata,
                                          model_name=model_name,
                                          system=system_message,
                                          user=user_message).assistant_message_content
    return f'{file_name_no_suffix}\n{output}'

def index_cosmos__extract_contact_details_from_doc(metadata:Metadata, doc_as_string: str, processed_doc_token_count:int):
    system_message = system_ownership.SYSTEM_MESSAGE
    model_name = model_selector_logic.get_model_name_for_ownership_extract(metadata, processed_doc_token_count)
    user_message = system_ownership.USER_MESSAGE.format(doc_as_string)
    functions = [system_ownership.OWNERSHIP_HANDLER]
    output = openai_logic.openai_chat_completion(metadata=metadata,
                                          model_name=model_name,
                                            system=system_message,
                                            user=user_message,
                                            functions=functions, 
                                            function_call={'name':system_ownership.OWNERSHIP_HANDLER['name']})
    
    if not output.is_success:
        return ''
    
    if not output.has_function_arguments or output.assistant_function_name is None:
        return ''
    
    if system_ownership.EXPLICIT_CONTACTS_DETAILS not in output.assistant_function_parsed_arguments:
        return ''

    if len(output.assistant_function_parsed_arguments[system_ownership.EXPLICIT_CONTACTS_DETAILS]) == 0:
        return ''

    cd = output.assistant_function_parsed_arguments[system_ownership.EXPLICIT_CONTACTS_DETAILS]
    return cd[0] if isinstance(cd, list) and len(cd) == 1 else str(cd)

def index_cosmos_parse_delta(metadata:Metadata, file_name_add_to_file_type: Dict[str,FileType]) -> Dict[str, ParseResult]:
    file_name_to_parsed_doc = metadata.file_name_to_parsed_doc
    all_hashes = {parsed_doc.hash for parsed_doc in file_name_to_parsed_doc.values()}
    file_name_to_result = dict()
    for file_path in casual_utils.loop_file_names_in_directory(casual_utils.get_parsed_files_path()):
        file_name = casual_utils.doc_name_from_file_path(file_path)

        if file_name not in file_name_add_to_file_type:
            continue

        doc_as_string = index_cosmos__read_file(file_path, file_name_add_to_file_type[file_name])

        processed_doc = casual_utils.preprocess_doc(doc_as_string)

        doc_hash = casual_utils.hash_doc(processed_doc)
        if doc_hash in all_hashes:
            file_name_to_result[file_name] = ParseResult.ALREADY_EXISTS
            continue

        processed_doc_token_count = token_count_logic.count_tokens(processed_doc)

        if processed_doc_token_count < Config.MIN_TOKENS_TO_CONSIDER_DOC:
            file_name_to_result[file_name] = ParseResult.TOO_SHORT
            continue
        if processed_doc_token_count > Config.MAX_TOKENS_TO_CONSIDER_DOC:
            file_name_to_result[file_name] = ParseResult.TOO_LONG
            continue

        try:
            summary = index_cosmos__extract_summary_from_doc(metadata, file_name, processed_doc, processed_doc_token_count)
            contact_details = index_cosmos__extract_contact_details_from_doc(metadata, processed_doc, processed_doc_token_count)
            function_name = fnlo.extract_openai_function_name(metadata, file_name, summary)
        except:
            file_name_to_result[file_name] = ParseResult.ERROR
            continue

        all_hashes.add(doc_hash)
        summary_token_count = token_count_logic.count_tokens(summary)
        parsed_doc = ParsedDoc(file_name=file_name,
                               function_name=function_name,
                               content=processed_doc,
                               content_token_count=processed_doc_token_count,
                               hash=doc_hash,
                               summary=summary,
                               summary_token_count=summary_token_count,
                               contact_details=contact_details)
        file_name_to_parsed_doc[file_name] = parsed_doc
        parsed_doc_as_json_str = json.dumps(parsed_doc.to_json(), ensure_ascii=False)
        casual_utils.write_text_to_file(parsed_doc_as_json_str, casual_utils.get_index_path()+file_name)
        file_name_to_result[file_name] = ParseResult.SUCCESS_ADD

    return file_name_to_result

def get_supported_file_types_suffixes():
    return ['.'+suffix for suffix in set(ft.value for ft in FileType)]

def add_new_file_to_cosmos(source_path):
    file_name = casual_utils.doc_name_from_file_path(source_path)

    if '.' not in source_path.split('/')[-1]:
        # CURRENTLY RELYING ON FULL FILE NAME TO RECOGNIZE TYPE 
        return file_name, None, False

    file_type = source_path.split('.')[-1].lower()
    try:
        # VERIFY THIS IS DOC IS PARSABLE
        text = index_cosmos__read_file(source_path, file_type)
        if text is None:
            return file_name, file_type, False
    except:
        return file_name, file_type, False

    casual_utils.copyfile(source_path, casual_utils.get_parsed_files_path()+file_name)
    return file_name, file_type, True

def remove_file_from_cosmos(file_name:str, file_name_to_parsed_doc:Dict[str,ParsedDoc]):
    time.sleep(1) # OTHERWISE THE UI REFRESH TOO FAST AND IT LOOKS LIKE NOTHING HAPPENED
    casual_utils.delete_file(casual_utils.get_parsed_files_path()+file_name)
    was_deleted = casual_utils.file_exists(casual_utils.get_index_path()+file_name)
    casual_utils.delete_file(casual_utils.get_index_path()+file_name)
    file_name_to_parsed_doc.pop(file_name,None)
    return was_deleted

def index_cosmos(metadata:Metadata, file_paths_to_upload, file_names_to_delete):
    skipped = set()
    file_name_add_to_file_type = dict()
    
    if file_paths_to_upload is not None:
        for file_path_to_upload in file_paths_to_upload:
            file_name, file_type, was_added_to_docs = add_new_file_to_cosmos(file_path_to_upload.name)
            if was_added_to_docs:
                file_name_add_to_file_type[file_name] = file_type
            else:
                skipped.add(file_name)

    to_be_deleted = set()
    deleted = set()
    if file_names_to_delete is not None:
        for file_name_to_delete in file_names_to_delete:
            to_be_deleted.add(file_name_to_delete)
            was_deleted = remove_file_from_cosmos(file_name_to_delete, metadata.file_name_to_parsed_doc)
            if was_deleted:
                deleted.add(file_name_to_delete)
            else:
                skipped.add(file_name_to_delete)

    if len(file_name_add_to_file_type) > 0 or len(to_be_deleted) > 0:
        file_name_to_result = index_cosmos_parse_delta(metadata, file_name_add_to_file_type)
        for skipped_file_name in skipped:
            file_name_to_result[skipped_file_name] = ParseResult.UNSUPPORTED_FORMAT
        lolo.load_initial_metadata(metadata)
        for file_name in deleted:
            file_name_to_result[file_name] = ParseResult.SUCCESS_DELETE

        report = '\n'.join([f'{ParseResult.symbol(result)} "{file_name}" : {result}' for file_name, result in file_name_to_result.items()]) if len(file_name_to_result) > 0 else ''
        metadata.cosmos_result = f'Cosmos refresh done!\n{report}'
    else:
        skipped_str = '\n'.join(skipped)
        skipped_str = '' if len(skipped) == 0 else f'\nSkipped unsupported files:\n{skipped_str}'
        metadata.cosmos_result = f'Nothing to do{skipped_str}'