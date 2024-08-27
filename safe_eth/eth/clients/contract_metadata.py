from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ContractMetadata:
    name: Optional[str]
    abi: List[Dict[str, Any]]
    partial_match: bool
