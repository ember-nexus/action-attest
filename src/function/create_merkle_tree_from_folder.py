import hashlib
import math
import os

from ..type.file_hash import FileHash
from ..type.merkle_tree import MerkleTree


def create_merkle_tree_from_folder(folder) -> MerkleTree:
    files = get_files_and_hash_for_folder(folder)
    return create_merkle_tree(files)


def create_merkle_tree(files: list[FileHash]) -> MerkleTree:
    available_elements: list[FileHash | MerkleTree] = files
    temporary_elements: list[FileHash | MerkleTree] = []
    while len(available_elements) > 1:
        for i in range(0, math.floor(len(available_elements) / 2)):
            left_element = available_elements.pop(0)
            right_element = available_elements.pop(0)
            hash = hashlib.new("sha256")
            hash.update(bytearray(left_element.hash.encode()))
            hash.update(bytearray(right_element.hash.encode()))
            new_merkle_tree = MerkleTree(hash.hexdigest(), left_element, right_element)
            temporary_elements.append(new_merkle_tree)
        if len(available_elements) > 0:
            temporary_elements.append(available_elements.pop(0))
        available_elements = temporary_elements
        temporary_elements = []
    return available_elements[0]


def get_files_and_hash_for_folder(folder: str) -> list[FileHash]:
    files: list[FileHash] = []
    for file_path in os.listdir(folder):
        if os.path.isfile(f"{folder}/{file_path}"):
            with open(f"{folder}/{file_path}", "rb") as f:
                digest = hashlib.file_digest(f, "sha256").hexdigest()
                files.append(FileHash(digest, file_path))
    files.sort(key=lambda file: file.file_name)
    return files
