from dataclasses import dataclass, field
from typing import Optional, Set


@dataclass
class RetrievalOutput:
    picked_doc_file_names: Optional[Set[str]]   = field(default=None)
    response_text: str                          = field(default=None)