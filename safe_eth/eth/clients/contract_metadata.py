from dataclasses import dataclass
from typing import Any


@dataclass
class ContractMetadata:
    name: str | None
    abi: list[dict[str, Any]]
    partial_match: bool
    implementation: str | None = None
