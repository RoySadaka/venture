from dataclasses import dataclass, field
from typing import Optional, Set


@dataclass
class LLMOutput:
    used_context_file_names: Optional[Set[str]] = field(default_factory=set)
    response_text: str = field(default_factory=str)