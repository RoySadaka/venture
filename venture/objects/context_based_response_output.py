from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ContextBasedResponseOutput:
    response_text: str
    selected_function: Optional[str] = field(default=None)