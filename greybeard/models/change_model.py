from dataclasses import dataclass, field
from typing import List
from datetime import datetime

@dataclass
class DiffBlock:
    start_line: int
    end_line: int
    original: List[str]
    replacement: List[str]

@dataclass
class ChangeBlock:
    label: str
    reason: str
    diff: DiffBlock
    status: str = "saved"
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

@dataclass
class Suggestion:
    path: str
    change_blocks: List[ChangeBlock]
