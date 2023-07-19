from venture.logic.retrieval_logic.objects.retrieval_output import RetrievalOutput
from venture.logic.retrieval_logic.objects.package_output import PackageOutput
from venture.logic.retrieval_logic.objects.package_input import PackageInput
import venture.prompts.system_retrieval_verdict as system_retrieval_verdict
import venture.prompts.system_retrieval_caller as system_retrieval_caller
import venture.logic.model_selector_logic as model_selector_logic
import venture.logic.openai_logic as openai_logic
from venture.metadata import Metadata
from venture.config import Config
from typing import Set, List
import json

def packager(metadata:Metadata, 
             function_name_to_file_name:dict[str,str],
             picked_doc_file_names:Set[str]) -> List[PackageInput]:
    '''
    Responsible for gathering and organizing information as packaged inputs
    '''
    retrieval_doc_functions = metadata.retrieval_doc_functions
    retrieval_function_name_to_count = metadata.token_counts.retrieval_function_name_to_count

    if Config.AUTO_PILOT_NAME not in picked_doc_file_names:
        # AUTO PILOT IS OFF
        return []
    
    # AUTO PILOT IS ON
    picked_doc_file_names = picked_doc_file_names - {Config.AUTO_PILOT_NAME}
    
    # REMOVE HAND PICKED DOCS FROM OPTIONS TO CHOOSE
    file_name_to_function_name = {v:k for k,v in function_name_to_file_name.items()}
    picked_doc_function_names = {file_name_to_function_name[picked_doc_file_name] for picked_doc_file_name in picked_doc_file_names}
    doc_functions_to_use = [f for f in retrieval_doc_functions if f['name'] not in picked_doc_function_names]

    # NO FANCY 'BIN PACKAGING' ALGORITHM (FOR NOW), SHOULD BE NO ISSUE AS THE NUMBER OF POSSIBILITIES IS VERY SMALL
    max_allowed_tokens_in_single_call = max(Config.MODEL_NAME_TO_MAX_TOKENS.values()) - Config.RESERVED_RETRIEVAL_TOKEN_COUNT
    packages = []
    num_inputs = 1
    while True:
        # GENERATE INPUTS 
        num_function_tokens = sum(retrieval_function_name_to_count[function_name]for function_name in system_retrieval_caller.NON_TEMPLATE_HANDLER_NAMES)
        packages = [PackageInput(num_tokens=metadata.token_counts.retrieval_caller_system_count + num_function_tokens, 
                                 initial_functions=system_retrieval_caller.NON_TEMPLATE_FUNCTIONS[:])
                    for _ in range(num_inputs)]

        # DISTRIBUTE DOC FUNCTIONS TO PACKAGES
        doc_functions_to_use = [f for f in retrieval_doc_functions if f['name'] not in picked_doc_function_names]
        while len(doc_functions_to_use) > 0:
            # TAKE INPUT WITH LOWEST AMOUNT OF TOKENS AND ADD THIS FUNCTION TO IT
            next_function = doc_functions_to_use.pop()
            smallest_package = min(packages, key=lambda x: x.num_tokens)
            smallest_package.functions.append(next_function)
            smallest_package.function_names.add(next_function['name'])
            smallest_package.num_tokens += retrieval_function_name_to_count[next_function['name']]

        # VERIFY
        verified = True # UNLESS SAID OTHERWISE
        for package in packages:
            if package.num_tokens > max_allowed_tokens_in_single_call:
                verified = False
                num_inputs += 1
                break

        if verified:
            break

    return packages

def caller(metadata:Metadata, 
           user_query:str, 
           packages:List[PackageInput]) -> List[PackageOutput]:
    '''
    Computes possible outcomes for each package
    '''
    if len(packages) == 0:
        return []
    
    outputs = []
    for package in packages:
        model_name = model_selector_logic.get_model_name_for_retrieval_caller(metadata, user_query, package.functions)
        system_message = system_retrieval_caller.SYSTEM_MESSAGE.format(Config.EXTRA_ROLE)
        user_message = system_retrieval_caller.USER_MESSAGE.format(user_query)
        output = openai_logic.openai_chat_completion(metadata=metadata,
                                                model_name=model_name, 
                                                system=system_message,
                                                user=user_message,
                                                functions=package.functions, 
                                                function_call='auto')

        if not output.is_success:
            return None
        
        if not output.has_function_arguments:
            outputs.append(PackageOutput(function_name=system_retrieval_verdict.RESPONSE_WITHOUT_FUNCTION_NAME_HANDLER['name'],
                                         function_description=system_retrieval_verdict.RESPONSE_WITHOUT_FUNCTION_NAME_HANDLER['description'],
                                         response_text=output.assistant_message_content))
            continue

        # HANDLE FUNCTIONS
        function_name = output.assistant_function_name
        if function_name in system_retrieval_caller.NON_TEMPLATE_HANDLER_NAMES:
            outputs.append(PackageOutput(function_name=function_name,
                                 function_description=[f['description'] for f in system_retrieval_caller.NON_TEMPLATE_FUNCTIONS if function_name == f['name']][0],
                                 response_text=output.assistant_function_parsed_arguments['response']))
        elif function_name in package.function_names:
            outputs.append(PackageOutput(function_name=function_name, 
                                         function_description=[f['description'] for f in package.functions if function_name == f['name']][0],
                                         response_text=output.assistant_function_parsed_arguments['reasoning']))
        else:
            # FALL BACK TO "NO NAME" WITH THE GIVEN ARGUMENTS AS IS
            outputs.append(PackageOutput(function_name=system_retrieval_verdict.RESPONSE_WITHOUT_FUNCTION_NAME_HANDLER['name'],
                                         function_description=system_retrieval_verdict.RESPONSE_WITHOUT_FUNCTION_NAME_HANDLER['description'],
                                         response_text=output.assistant_function_arguments))

    return outputs

def verdict(metadata:Metadata,
            outputs:List[PackageOutput],
            user_query:str) -> PackageOutput:
    if len(outputs) is None:
        # THERE WAS AN ERROR
        return None

    if len(outputs) == 0:
        return None
    
    if len(outputs) == 1:
        return outputs[0]


    # MORE THAN 1 POSSIBLE OUTPUT, NEED TO FIND THE BEST DOC, OR RESPONSE

    system_message = system_retrieval_verdict.SYSTEM_MESSAGE.format(Config.EXTRA_ROLE)
    ai_responses = []
    for idx, output in enumerate(outputs):
        ai_responses.append(json.dumps({
                    "AI identifier": idx,
                    "function_name" : output.function_name,
                    "description" : output.function_description,
                    "response" : output.response_text
                    }))

    ai_responses = "```\n" +'\n```\n\n```\n'.join(ai_responses) + "\n```"
    user_message = system_retrieval_verdict.USER_MESSAGE.format(user_query, ai_responses)
    model_name = model_selector_logic.get_model_name_for_retrieval_verdict(metadata, user_message)
    output = openai_logic.openai_chat_completion(metadata=metadata,
                                            model_name=model_name, 
                                            system=system_message,
                                            user=user_message,
                                            functions=[system_retrieval_verdict.VERDICT_HANDLER], 
                                            function_call={'name':system_retrieval_verdict.VERDICT_HANDLER['name']})

    chosen_function_name = output.assistant_function_parsed_arguments['chosen_function_name']
    chosen_package_output = [o for o in outputs if o.function_name == chosen_function_name][0]

    return chosen_package_output

def parse_output(metadata:Metadata, chosen_output:PackageOutput, picked_doc_file_names:Set[str]) -> RetrievalOutput:
    if chosen_output is None:
        return RetrievalOutput(file_names_to_use=picked_doc_file_names, response_text='')

    file_names_to_use = picked_doc_file_names - {Config.AUTO_PILOT_NAME}
    if chosen_output.function_name in metadata.function_name_to_file_name:
        file_names_to_use.add(metadata.function_name_to_file_name[chosen_output.function_name])
    return RetrievalOutput(file_names_to_use=file_names_to_use,
                           response_text=chosen_output.response_text)

def fixer(metadata:Metadata, packages:List[PackageInput], retrieval_output:RetrievalOutput) -> RetrievalOutput:
    all_function_names = set()
    for p in packages:
        for fn in p.function_names:
            all_function_names.add(fn)
    if not retrieval_output.file_names_to_use:
        if retrieval_output.response_text in all_function_names:
            # SOMETIMES CHATGPT PUTS THE FUNCTION NAME IN THE SYSTEM MESSAGE
            return RetrievalOutput(file_names_to_use={metadata.function_name_to_file_name[retrieval_output.response_text]}, 
                                    response_text='')

        # IN CASE NO FILE WAS FOUND, VENTURE WILL ADD A DISCLAIMER FOR THE RAW OUTPUT
        disclaimer = """⚠️ Venture was unable to identify a specific document related to your query.\nThe following text is the unprocessed output:\n\n"""
        return RetrievalOutput(file_names_to_use={}, 
                                    response_text=f'{disclaimer}{retrieval_output.response_text}')

    return retrieval_output

def retrieve(metadata:Metadata, 
             function_name_to_file_name:dict[str,str], 
             picked_doc_file_names:Set[str], 
             user_query:str) -> RetrievalOutput:

    packages = packager(metadata, function_name_to_file_name, picked_doc_file_names)
    # print(f'-----num packages {len(packages)}')
    outputs = caller(metadata, user_query, packages)
    # print(f'-----outputs\n{outputs}')
    chosen_output = verdict(metadata, outputs, user_query)
    # print(f'-----chosen_output\n{chosen_output}')
    retrieval_output = parse_output(metadata, chosen_output, picked_doc_file_names)
    # print(f'-----retrieval_output\n{retrieval_output}')
    fixed_retrieval_output = fixer(metadata, packages, retrieval_output)
    # print(f'-----fixed_retrieval_output\n{fixed_retrieval_output}')
    return fixed_retrieval_output

