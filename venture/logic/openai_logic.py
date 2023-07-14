from venture.config import Config
from venture.metadata import Metadata
from venture.objects.chat_gpt_output import ChatGPTOutput
from typing import Dict, List, Optional, Union
import openai
import time

def openai_chat_completion(metadata:Metadata,
                           model_name: str, 
                           system:str,
                           user:str,
                           functions: Optional[List[object]] = None,
                           function_call: Union[str, Dict[str, str]] = "auto") -> ChatGPTOutput:
    time.sleep(1) # NAIVE BACKOFF
    messages = [{"role": "system", "content": system},
                {"role": "user", "content": user}]
    if functions is not None:
        result = openai.ChatCompletion.create(model=model_name,
                                                messages=messages,
                                                functions=functions,
                                                function_call=function_call,
                                                temperature=0.0)
    else:
        result = openai.ChatCompletion.create(model=model_name,
                                                messages=messages,
                                                temperature=0.0)
    chat_gpt_output = ChatGPTOutput(output=result)
    metadata.sum_cost_in_since_start_session += chat_gpt_output.input_tokens_count * Config.MODEL_NAME_TO_COST_PER_TOKEN[model_name]['in']
    metadata.sum_cost_out_since_start_session += chat_gpt_output.output_tokens_count * Config.MODEL_NAME_TO_COST_PER_TOKEN[model_name]['out']
    return chat_gpt_output