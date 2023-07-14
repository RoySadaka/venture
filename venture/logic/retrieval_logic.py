from venture.objects.retrieval_output import RetrievalOutput
import venture.prompts.system_retrieval_venture as srv
import venture.logic.model_selector_logic as mslo
import venture.logic.openai_logic as oailo
from venture.metadata import Metadata
from venture.config import Config
from typing import Set


def retrieve_docs(metadata:Metadata, 
                    function_name_to_file_name:dict[str,str], 
                    picked_doc_file_names:Set[str], 
                    user_query:str) -> RetrievalOutput:
    retrieval_functions = metadata.retrieval_functions

    if Config.AUTO_PILOT_NAME not in picked_doc_file_names:
        # AUTO PILOT IS OFF
        return RetrievalOutput(picked_doc_file_names=picked_doc_file_names)
    
    # AUTO PILOT IS ON
    picked_doc_file_names = picked_doc_file_names - {Config.AUTO_PILOT_NAME}
    
    # REMOVE HAND PICKED DOCS FROM OPTIONS TO CHOOSE
    file_name_to_function_name = {v:k for k,v in function_name_to_file_name.items()}
    picked_doc_function_names = {file_name_to_function_name[picked_doc_file_name] for picked_doc_file_name in picked_doc_file_names}
    functions_to_use = [f for f in retrieval_functions if f['name'] not in picked_doc_function_names]

    # CHOOSE BEST DOC FOR AUTO PILOT
    model_name = mslo.get_model_name_for_retrieval(metadata, user_query, functions_to_use)
    
    system_message = srv.SYSTEM_MESSAGE.format(Config.EXTRA_ROLE)
    user_message = f'Input:\n```\n{user_query}\n```\n{srv.USER_REMINDER}'
    output = oailo.openai_chat_completion(metadata=metadata,
                                          model_name=model_name, 
                                            system=system_message,
                                            user=user_message,
                                            functions=functions_to_use, 
                                            function_call='auto')
    
    if not output.is_success:
        return RetrievalOutput(picked_doc_file_names=picked_doc_file_names) \
                if len(picked_doc_file_names) > 0 else RetrievalOutput()
    
    if not output.has_function_arguments:
        return RetrievalOutput(picked_doc_file_names=picked_doc_file_names) \
                if len(picked_doc_file_names) > 0 else RetrievalOutput(response_text=output.assistant_message_content)
    
    # HANDLE FUNCTIONS
    function_name = output.assistant_function_name
    if function_name in srv.NON_TEMPLATE_HANDLER_NAMES:
        return RetrievalOutput(picked_doc_file_names=picked_doc_file_names) \
                if len(picked_doc_file_names) > 0 \
                else RetrievalOutput(response_text=output.assistant_function_parsed_arguments['response'])
    else:
        file_name = function_name_to_file_name[function_name]
        picked_doc_file_names.add(file_name)

    return RetrievalOutput(picked_doc_file_names=picked_doc_file_names)