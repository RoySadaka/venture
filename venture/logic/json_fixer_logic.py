import string
from venture.objects.chat_gpt_output import ChatGPTOutput 


def endswith_json_eligible(input_str):
    return input_str.endswith('true') or input_str.endswith('false') or input_str.endswith('null')

def should_add_missing_braces_at_the_end(input_str, canonical):
    if canonical == '{"1":"2"':
        return True
    
    if canonical == '{"1":2' and endswith_json_eligible(input_str):
        return True
    
    return False

def should_add_missing_braces_at_the_start(input_str, canonical):
    if canonical == '"1":"2"}':
        return True
    
    return False

def should_add_missing_quotes_and_braces_at_the_end(input_str, canonical):
    if canonical in { '{"1":"2', '{"1":"2"3' }:
        return True
    return False

def should_add_missing_quotes_and_braces_at_the_start(input_str, canonical):
    if canonical == '1":"2"}':
        return True
    return False

def should_remove_single_excessive_braces_at_the_end(input_str, canonical):
    if canonical == '''{"1":"2"}}''':
        return True
    return False

def should_remove_2_excessive_braces_at_the_end(input_str, canonical):
    if canonical == '''{"1":"2"}}}''':
        return True
    return False

def should_remove_single_excessive_braces_at_the_start(input_str, canonical):
    if canonical == '''{{"1":"2"}''':
        return True
    return False

def should_remove_2_excessive_braces_at_the_start(input_str, canonical):
    if canonical == '''{{{"1":"2"}''':
        return True
    return False

def should_merge_value_strings(input_str, canonical):
    if canonical == '{"1":"2"3"4"}':
        return True
    return False


def common_json_repair_shop(input_str: str, verbose:bool=False) -> str:
    """
    We will transform the faulty json into a canonical 
    representation, and then compare it against the most common cases that are practical for production use.

    This approach give us the ability to support more cases as they popup
    """

    def str_to_canonical(input_str):
        canonical = ""
        counter = 1
        valid_symbols = set(string.printable) - {':','"','{','}'}
        for char in input_str:
            if char.isspace():
                continue
            if char in valid_symbols:
                if len(canonical) == 0 or not canonical[-1].isdigit():
                    canonical += str(counter)
                    counter += 1
            else:
                canonical += char
        return canonical

    canonical = str_to_canonical(input_str)

    if should_add_missing_braces_at_the_end(input_str, canonical):
        if verbose: print("add missing braces at the end")
        return input_str + '}'

    if should_add_missing_braces_at_the_start(input_str, canonical):
        if verbose: print("add missing braces at the start")
        return "{" + input_str

    if should_add_missing_quotes_and_braces_at_the_end(input_str, canonical):
        if verbose: print("add missing quotes and braces at the end")
        return input_str + '"}'
    
    if should_add_missing_quotes_and_braces_at_the_start(input_str, canonical):
        if verbose: print("add missing quotes and braces at the start")
        return '{"' + input_str

    if should_remove_single_excessive_braces_at_the_end(input_str, canonical):
        if verbose: print("remove single excessive braces at the end")
        return input_str[:-1]

    if should_remove_2_excessive_braces_at_the_end(input_str, canonical):
        if verbose: print("remove 2 excessive braces at the end")
        return input_str[:-2]

    if should_remove_single_excessive_braces_at_the_start(input_str, canonical):
        if verbose: print("remove single excessive braces at the start")
        return input_str[1:]

    if should_remove_2_excessive_braces_at_the_start(input_str, canonical):
        if verbose: print("remove 2 excessive braces at the start")
        return input_str[2:]

    if should_merge_value_strings(input_str, canonical):
        if verbose: print("merge value strings")
        split_input = input_str.split('"')
        return '"'.join([split_input[0],split_input[1],split_input[2],split_input[3]+split_input[4]+split_input[5],split_input[6]])

    return input_str

def fix_predict_output(chat_gpt_output:ChatGPTOutput) -> ChatGPTOutput:
    fixed_response = common_json_repair_shop(chat_gpt_output.assistant_function_arguments, verbose=True)
    fixed_response = fixed_response.replace('\n','')
    chat_gpt_output.output['choices'][0]['message']['function_call']['arguments'] = fixed_response
    fixed = ChatGPTOutput(chat_gpt_output.output)
    return fixed

# TESTS
# faulty_jsons = [
#     '{\n  "response": "Try2.this.',
#     '{\n  "response": null',
#     '{\n  "r": "To \\"epochs.',
#     '''{"response":"this is a response"''',
#     '''"response":"this is a response"}''',
#     '''{"response":"this is a response''',
#     '''response":"this is a response"}''',
#     '''{"response":"this is a response"}}''',
#     '''{"response":"this is a response"}}}''',
#     '''{{"response":"this is a response"}''',
#     '''{{{"response":"this is a response"}''',
#     '''{"response":"this is a response"}''',
#     ]

# import json
# for faulty_json in faulty_jsons:
#     fixed_json = common_json_repair_shop(faulty_json, verbose=True)
#     json.loads(fixed_json)
#     print(f'{faulty_json} -> {fixed_json}')