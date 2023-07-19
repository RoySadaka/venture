from venture.objects.context_based_response_output import ContextBasedResponseOutput
import venture.logic.retrieval_logic.retrieval_logic as retrieval_logic
from venture.objects.llm_output import LLMOutput
import venture.logic.model_selector_logic as model_selector_logic
import venture.logic.token_count_logic as token_count_logic
import venture.logic.json_fixer_logic as json_fixer_logic
import venture.prompts.system_venture as system_venture
import venture.casual_utils as casual_utils 
import venture.logic.openai_logic as openai_logic
from venture.metadata import Metadata
from venture.config import Config
from typing import List, Set


def get_updated_picked_docs(metadata:Metadata):
    available_file_names = set(metadata.file_name_to_parsed_doc.keys())
    explore_last_picked_file_names = metadata.explore_last_picked_file_names

    updated_file_names = []
    for file_name in explore_last_picked_file_names:
        if file_name in available_file_names or file_name == Config.AUTO_PILOT_NAME:
            updated_file_names.append(file_name)
    
    if len(updated_file_names) == 0:
        updated_file_names = [Config.AUTO_PILOT_NAME]
    return updated_file_names

def get_doc_picker_all_choices(metadata:Metadata):
    return [Config.AUTO_PILOT_NAME]+list(metadata.file_name_to_parsed_doc.keys())

def get_context_file_names_that_fit_in_window(metadata:Metadata, user_query:str, context_file_names_to_use:List[str]) -> List[str]:
    file_name_to_parsed_doc = metadata.file_name_to_parsed_doc

    max_token_count = max(Config.MODEL_NAME_TO_MAX_TOKENS.values())

    minimal_token_count = metadata.token_counts.explore_all_prompt_token_count + \
                            token_count_logic.count_tokens(user_query)
    minimal_token_count = minimal_token_count + Config.RESERVED_RESPONSE_TOKEN_COUNT
    
    left_over_token_count = max_token_count - minimal_token_count
    result = []
    # WE CAN ASSUME AT LEAST 1 DOC WILL FIT
    for context_file_name_to_use in context_file_names_to_use:
        if left_over_token_count > file_name_to_parsed_doc[context_file_name_to_use].content_token_count:
            result.append(context_file_name_to_use)
            left_over_token_count -= file_name_to_parsed_doc[context_file_name_to_use].content_token_count

    return result

def llm_response_based_on_docs(metadata:Metadata, 
                                  context_file_names_to_use:List[str], 
                                  user_query:str) -> ContextBasedResponseOutput:
    file_name_to_parsed_doc = metadata.file_name_to_parsed_doc
    context_file_names_to_use = get_context_file_names_that_fit_in_window(metadata, user_query, context_file_names_to_use)
    contexts = [f'File name: {file_name}\n{file_name_to_parsed_doc[file_name].content}' for file_name in context_file_names_to_use]
    
    model_name = model_selector_logic.get_model_name_for_llm_response(metadata, user_query, context_file_names_to_use)

    contexts = "```\n" +'\n```\n\n```\n'.join(contexts) + "\n```"
    system_message = system_venture.SYSTEM_MESSAGE.format(Config.EXTRA_ROLE)
    user_message = system_venture.USER_MESSAGE.format(contexts, user_query) 
    functions = system_venture.ALL_FUNCTIONS
    output = openai_logic.openai_chat_completion(metadata=metadata,
                                          model_name=model_name, 
                                          system=system_message,
                                          user=user_message, 
                                          functions=functions, 
                                          function_call='auto')

    if not output.is_success and \
            output.has_function_arguments and \
            '"response":' in output.assistant_function_arguments:
        # TRY ONE LAST JSON PARSING FIX
        output = json_fixer_logic.fix_predict_output(output)

    if not output.is_success:
        return ContextBasedResponseOutput(response_text=Config.ERROR_RESPONSE)
    
    if not output.has_function_arguments:
        return ContextBasedResponseOutput(response_text=output.assistant_message_content)
    
    return ContextBasedResponseOutput(response_text=output.assistant_function_parsed_arguments['response'], selected_function=output.assistant_function_name)

def get_file_name_and_owner_by_file_name(metadata:Metadata, file_name:str) ->str:
    if file_name not in metadata.file_name_to_parsed_doc:
        return file_name
    contact_details = metadata.file_name_to_parsed_doc[file_name].contact_details
    if contact_details:
        return f'🌟 {file_name}  |  🧑‍✈️ {contact_details}'
    return f'🌟 {file_name}'


@casual_utils.suppress_errors(fallback_value=LLMOutput(response_text=Config.ERROR_RESPONSE))
def call_llm(metadata:Metadata, user_query:str,) -> LLMOutput:
    picked_doc_file_names = metadata.explore_last_picked_file_names
    function_name_to_file_name = metadata.function_name_to_file_name

    if len(user_query) == 0:
        return LLMOutput(response_text="Please provide a query")
    
    if len(picked_doc_file_names) == 0:
        return LLMOutput(response_text=f"Please select at least 1 document, or '{Config.AUTO_PILOT_NAME}'")

    if len(function_name_to_file_name) == 0:
        return LLMOutput(response_text="No docs found, go to Cosmos tab and add some wisdom")

    retrieval_output = retrieval_logic.retrieve(metadata, function_name_to_file_name, picked_doc_file_names, user_query)

    if retrieval_output is None:
        return LLMOutput(response_text=Config.ERROR_RESPONSE)

    if len(retrieval_output.file_names_to_use) == 0:
        return LLMOutput(response_text=casual_utils.prettify_response(retrieval_output.response_text))
    
    context_based_response_output = llm_response_based_on_docs(metadata, retrieval_output.file_names_to_use, user_query)
    if context_based_response_output.selected_function in {None,system_venture.MISSING_ANSWER_HANDLER['name']}:
        file_and_owner = '\n'.join([get_file_name_and_owner_by_file_name(metadata, file_name) for file_name in retrieval_output.file_names_to_use])
        response = casual_utils.prettify_response(f'Tried using the following documentations:\n{file_and_owner}\n\n{context_based_response_output.response_text}')
        return LLMOutput(used_context_file_names=retrieval_output.file_names_to_use,
                        response_text=response)
    else:
        file_and_owner = '\n'.join([get_file_name_and_owner_by_file_name(metadata, file_name) for file_name in retrieval_output.file_names_to_use])
        response = casual_utils.prettify_response(f'Based on the following documentations:\n{file_and_owner}\n\n{context_based_response_output.response_text}')
        return LLMOutput(used_context_file_names=retrieval_output.file_names_to_use, 
                         response_text=response)