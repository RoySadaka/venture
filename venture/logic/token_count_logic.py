import venture.prompts.system_ownership as system_ownership
import venture.prompts.system_function_name as system_function_name
import venture.prompts.system_summary as system_summary
import venture.prompts.system_retrieval_caller as system_retrieval_caller
import venture.prompts.system_retrieval_verdict as system_retrieval_verdict
import venture.prompts.system_venture as system_venture
from venture.metadata import Metadata
from venture.config import Config
import tiktoken
import json

def count_tokens(text:str):
    tokenizer = tiktoken.get_encoding(Config.TOKENIZER_NAME)
    return len(tokenizer.encode(text))

def get_explore_all_prompt_token_count():
    explore_functions = [system_venture.ANSWER_FOUND_HANDLER, system_venture.MISSING_ANSWER_HANDLER]
    explore_functions_token_count = sum(count_tokens(json.dumps(f)) for f in explore_functions)
    explore_all_prompt_token_count = explore_functions_token_count + count_tokens(system_venture.SYSTEM_MESSAGE) + count_tokens(system_venture.USER_MESSAGE)
    return explore_all_prompt_token_count

def get_cosmos_function_name_all_prompt_token_count():
    cosmos_function_name_all_prompt_token_count = count_tokens(system_function_name.SYSTEM_MESSAGE) + \
                                    count_tokens(system_function_name.USER_MESSAGE_TEMPLATE) + \
                                    count_tokens(json.dumps(system_function_name.FILE_NAME_HANDLER)) 
    return cosmos_function_name_all_prompt_token_count

def get_cosmos_ownership_all_prompt_token_count():
    cosmos_ownership_all_prompt_token_count = count_tokens(system_ownership.SYSTEM_MESSAGE) + \
                                                count_tokens(system_ownership.USER_MESSAGE) + \
                                                count_tokens(json.dumps(system_ownership.OWNERSHIP_HANDLER)) 
    return cosmos_ownership_all_prompt_token_count

def get_system_token_counts():
    retrieval_caller_system_count = count_tokens(system_retrieval_caller.SYSTEM_MESSAGE) + count_tokens(system_retrieval_caller.USER_MESSAGE)
    retrieval_verdict_system_count = count_tokens(system_retrieval_verdict.SYSTEM_MESSAGE) + count_tokens(system_retrieval_verdict.USER_MESSAGE)
    explore_all_prompt_token_count = get_explore_all_prompt_token_count()
    cosmos_function_name_all_prompt_token_count = get_cosmos_function_name_all_prompt_token_count()
    cosmos_system_summary_token_count = count_tokens(system_summary.SYSTEM_MESSAGE)
    cosmos_ownership_all_prompt_token_count = get_cosmos_ownership_all_prompt_token_count()
    return retrieval_caller_system_count, \
            retrieval_verdict_system_count, \
            explore_all_prompt_token_count, \
            cosmos_function_name_all_prompt_token_count, \
            cosmos_system_summary_token_count, \
            cosmos_ownership_all_prompt_token_count

def get_cosmos_ownership_function_to_token_count():
    ownership_functions = [system_ownership.OWNERSHIP_HANDLER]
    ownership_function_name_to_token_count = {f['name']:count_tokens(json.dumps(f)) for f in ownership_functions}
    return ownership_function_name_to_token_count

def get_retrieval_function_name_to_token_count(metadata:Metadata):
    function_name_to_file_name = metadata.function_name_to_file_name
    file_name_to_parsed_doc = metadata.file_name_to_parsed_doc
    system_retrieval_caller.NON_TEMPLATE_FUNCTIONS
    # TOKEN COUNTS
    retrieval_function_name_to_token_count = {f['name']:count_tokens(json.dumps(f)) for f in system_retrieval_caller.NON_TEMPLATE_FUNCTIONS}
    template_token_count = count_tokens(json.dumps(system_retrieval_caller.TEMPLATE_TOPIC_HANDLER))
    for function_name, file_name in function_name_to_file_name.items():
        parsed_doc = file_name_to_parsed_doc[file_name]
        retrieval_function_name_to_token_count[function_name] = template_token_count + parsed_doc.summary_token_count
    return retrieval_function_name_to_token_count