from typing import Dict, List, Set
from venture.config import Config
from venture.objects.interlink_commander_details_output import InterlinkCaptainDetailsOutput
from venture.objects.llm_output import LLMOutput
from venture.objects.parsed_doc import ParsedDoc
from venture.objects.token_counts import TokenCounts

class Metadata:
    file_name_to_parsed_doc:Dict[str,ParsedDoc] = dict()
    retrieval_functions = None
    function_name_to_file_name:Dict[str,str] = None
    token_counts: TokenCounts = None
    sum_cost_in_since_start_session:int
    sum_cost_out_since_start_session:int


    # EXPLORE
    explore_llm_output: LLMOutput = LLMOutput()
    explore_last_picked_file_names: Set[str] = set()

    # COSMOS
    cosmos_result:str = ''

    # INTERLINK
    interlink_last_text:str = ''
    interlink_captain_details:InterlinkCaptainDetailsOutput = InterlinkCaptainDetailsOutput(contact_details='',email_address=Config.CAPTAIN_EMAIL)

    @property
    def file_names(self) -> List[str]:
        return list(self.function_name_to_file_name.values())