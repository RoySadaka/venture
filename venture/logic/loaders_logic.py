import venture.prompts.system_retrieval_caller as system_retrieval_caller
from venture.objects.token_counts import TokenCounts
from venture.objects.parsed_doc import ParsedDoc
import venture.logic.token_count_logic as token_count_logic
import venture.casual_utils as casual_utils 
from venture.metadata import Metadata
from venture.config import Config
from typing import Dict
import json
import copy

def load_all_docs() -> Dict[str,ParsedDoc]:
    file_name_to_parsed_doc = dict()
    for file_path in casual_utils.loop_file_names_in_directory(Config.INDEX_PATH):
        json_str = casual_utils.read_text_from_file(file_path)
        json_obj = json.loads(json_str)
        parsed_doc = ParsedDoc.from_json(json_obj)
        file_name = casual_utils.doc_name_from_file_path(file_path)
        file_name_to_parsed_doc[file_name] = parsed_doc
    return file_name_to_parsed_doc

def load_retrieval_functions(file_name_to_parsed_doc:Dict[str,ParsedDoc]):
    retrieval_doc_functions = []
    function_name_to_file_name = {}
    
    # FUNCTIONS
    for file_name,parsed_doc in file_name_to_parsed_doc.items():
        function_description = system_retrieval_caller.TEMPLATE_TOPIC_HANDLER['description'].format(parsed_doc.summary)

        function_name = parsed_doc.function_name
        function_name = system_retrieval_caller.TEMPLATE_TOPIC_HANDLER['name'].format(function_name)
        function_name_to_file_name[function_name] = file_name
        f = copy.deepcopy(system_retrieval_caller.TEMPLATE_TOPIC_HANDLER)
        f['name'] = function_name
        f['description'] = function_description
        retrieval_doc_functions.append(f)
    return retrieval_doc_functions, function_name_to_file_name

def load_initial_metadata(metadata:Metadata):
    metadata.file_name_to_parsed_doc = load_all_docs()
    metadata.retrieval_doc_functions, metadata.function_name_to_file_name = load_retrieval_functions(metadata.file_name_to_parsed_doc)
    retrieval_caller_system_count, \
    retrieval_verdict_system_count, \
    explore_all_prompt_token_count, \
    cosmos_function_name_all_prompt_token_count, \
    cosmos_system_summary_count, \
    cosmos_ownership_all_prompt_token_count = token_count_logic.get_system_token_counts()
    retrieval_function_name_to_count = token_count_logic.get_retrieval_function_name_to_token_count(metadata)

    metadata.token_counts = TokenCounts(retrieval_function_name_to_count=retrieval_function_name_to_count,
                                        retrieval_caller_system_count=retrieval_caller_system_count,
                                        retrieval_verdict_system_count=retrieval_verdict_system_count,
                                        explore_all_prompt_token_count = explore_all_prompt_token_count,
                                        cosmos_function_name_all_prompt_count=cosmos_function_name_all_prompt_token_count,
                                        cosmos_system_summary_count=cosmos_system_summary_count,
                                        cosmos_system_ownership_all_prompt_count=cosmos_ownership_all_prompt_token_count)