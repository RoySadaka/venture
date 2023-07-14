import venture.prompts.system_function_name as system_function_name
import venture.logic.model_selector_logic as mslo
import venture.logic.token_count_logic as tclo
import venture.logic.openai_logic as oailo
from venture.metadata import Metadata
from venture.config import Config
import re

def try_extract_casual_openai_function_name(file_name:str, force:bool):
    function_name = file_name.replace(' ', '_').lower()
    valid_chars_pattern = '[^a-zA-Z0-9_-]'
    function_name = re.sub(valid_chars_pattern, '', function_name)
    function_name = function_name.replace('project_','') if function_name.startswith('project_') else function_name
    function_name = function_name + Config.OPEN_AI_FUNCTION_TEMPLATE_SUFFIX
    if len(function_name) > Config.OPEN_AI_FUNCTION_MAX_LENGTH:
        if force:
            return function_name[-Config.OPEN_AI_FUNCTION_MAX_LENGTH:]
        return None
    return function_name


def extract_openai_function_name(metadata:Metadata, file_name:str, file_summary:str):
    function_name = try_extract_casual_openai_function_name(file_name, force=False)
    if function_name is not None:
        return function_name
    
    # FUNCTION NAME TOO LONG, EXTRACT SHORTER
    summary_token_count = tclo.count_tokens(file_summary)
    model_name = mslo.get_model_name_for_function_name_extract(metadata, summary_token_count)
    system_message = system_function_name.SYSTEM_MESSAGE
    user_message = system_function_name.USER_MESSAGE_TEMPLATE.format(file_summary)
    functions = [system_function_name.FILE_NAME_HANDLER]
    output = oailo.openai_chat_completion(metadata=metadata,
                                          model_name=model_name,
                                            system=system_message,
                                            user=user_message,
                                            functions=functions, 
                                            function_call={'name':system_function_name.FILE_NAME_HANDLER['name']})
    
    if not output.is_success or \
        not output.has_function_arguments or \
        'file_name' not in output.assistant_function_parsed_arguments:
        return try_extract_casual_openai_function_name(file_name, force=True)

    suggested_file_name = output.assistant_function_parsed_arguments['file_name']
    return try_extract_casual_openai_function_name(suggested_file_name, force=True)