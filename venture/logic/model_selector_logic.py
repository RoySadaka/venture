import venture.logic.token_count_logic as token_count_logic
from venture.metadata import Metadata
from venture.config import Config
from typing import List

def get_model_based_on_token_count(token_count:int):
    token_count = int(token_count)
    lowest_model_name = None
    lowest_model_token_count = max(Config.MODEL_NAME_TO_MAX_TOKENS.values()) * 2
    for model_name, max_tokens in Config.MODEL_NAME_TO_MAX_TOKENS.items():
        if token_count < max_tokens and max_tokens < lowest_model_token_count:
            lowest_model_name = model_name
            lowest_model_token_count = max_tokens
    return lowest_model_name

def get_model_name_for_function_name_extract(metadata:Metadata, summary_token_count:int) -> str:
    token_count = metadata.token_counts.cosmos_function_name_all_prompt_count + summary_token_count
    token_count = token_count * Config.TOKEN_COUNT_MULTIPLIER + Config.FUNCTION_NAME_RESERVED_RESPONSE_TOKEN_COUNT
    model_name = get_model_based_on_token_count(token_count)
    return model_name

def get_model_name_for_ownership_extract(metadata:Metadata, processed_doc_token_count:int) -> str:
    token_count = metadata.token_counts.cosmos_system_ownership_all_prompt_count + processed_doc_token_count
    token_count = token_count * Config.TOKEN_COUNT_MULTIPLIER + Config.OWNERSHIP_RESERVED_RESPONSE_TOKEN_COUNT
    model_name = get_model_based_on_token_count(token_count)
    return model_name

def get_model_name_for_summary_extract(metadata:Metadata, processed_doc_token_count:int) -> str:
    token_count = metadata.token_counts.cosmos_system_summary_count + processed_doc_token_count
    token_count = token_count * Config.TOKEN_COUNT_MULTIPLIER + Config.SUMMARY_RESERVED_RESPONSE_TOKEN_COUNT
    model_name = get_model_based_on_token_count(token_count)
    return model_name

def get_model_name_for_retrieval_caller(metadata:Metadata, user_query:str, functions:List[object]) -> str:
    token_count =   metadata.token_counts.retrieval_caller_system_count + \
                    token_count_logic.count_tokens(user_query) + \
                    token_count_logic.count_tokens(Config.EXTRA_ROLE) + \
                    sum(metadata.token_counts.retrieval_function_name_to_count[f['name']] for f in functions)
    token_count = token_count * Config.TOKEN_COUNT_MULTIPLIER + Config.RESERVED_RESPONSE_TOKEN_COUNT
    model_name = get_model_based_on_token_count(token_count)
    return model_name


def get_model_name_for_retrieval_verdict(metadata:Metadata, user_message:str) -> str:
    token_count =   metadata.token_counts.retrieval_verdict_system_count + \
                    token_count_logic.count_tokens(user_message) + \
                    token_count_logic.count_tokens(Config.EXTRA_ROLE)
    
    token_count = token_count * Config.TOKEN_COUNT_MULTIPLIER + Config.RESERVED_RESPONSE_TOKEN_COUNT
    model_name = get_model_based_on_token_count(token_count)
    return model_name

def get_model_name_for_llm_response(metadata:Metadata, user_query:str, context_file_names_to_use:List[str]) -> str:
    file_name_to_parsed_doc = metadata.file_name_to_parsed_doc

    token_count =   metadata.token_counts.explore_all_prompt_token_count + \
                    token_count_logic.count_tokens(Config.EXTRA_ROLE) + \
                    sum(file_name_to_parsed_doc[file_name].content_token_count for file_name in context_file_names_to_use) + \
                    token_count_logic.count_tokens(user_query)
    
    token_count = token_count * Config.TOKEN_COUNT_MULTIPLIER + Config.RESERVED_RESPONSE_TOKEN_COUNT
    model_name = get_model_based_on_token_count(token_count)
    return model_name

