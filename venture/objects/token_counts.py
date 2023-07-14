from dataclasses import dataclass
from typing import Dict

@dataclass
class TokenCounts:
    retrieval_function_name_to_count:Dict[str,int]
    retrieval_system_count:int

    explore_all_prompt_token_count:int

    cosmos_function_name_all_prompt_count:int
    cosmos_system_summary_count:int
    cosmos_system_ownership_all_prompt_count:int