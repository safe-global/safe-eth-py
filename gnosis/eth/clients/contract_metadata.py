from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class ContractMetadata:
    name: Optional[str]
    abi: List[Dict[str, Any]]
    partial_match: bool
