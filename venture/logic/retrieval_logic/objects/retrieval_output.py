from dataclasses import dataclass, field
from typing import Optional, Set


@dataclass
class RetrievalOutput:
    file_names_to_use: Optional[Set[str]]   = field(default=None)
    response_text: str                      = field(default=None)
