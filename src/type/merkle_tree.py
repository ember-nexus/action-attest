import json
from dataclasses import dataclass

from dataclasses_json import dataclass_json
from typing_extensions import Self
from .file_hash import FileHash


@dataclass_json
@dataclass
class MerkleTree:
    hash: str
    left_node: Self | FileHash
    right_node: Self | FileHash

    def to_pretty_json(self) -> str:
        return json.dumps(json.loads(self.to_json()), indent=2)
