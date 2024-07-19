from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class FileHash:
    hash: str
    file_name: str
