from pathlib import Path
import numpy as np


class entry:
    path: Path
    start_line: int
    end_line: int
    time: str
    chunk_num: int
    embedding: np.ndarray

    def __init__(
        self,
        path: Path,
        start_line: int,
        end_line: int,
        time: str,
        chunk_num: int,
    ):
        self.path = path
        self.start_line = start_line
        self.end_line = end_line
        self.time = time
        self.chunk_num = chunk_num
        self.embedding = None

    def set_embed(self, embed: np.ndarray):
        self.embedding = embed
        return

    def printAll(self):
        print(
            f"Path: {self.path} Start: {self.start_line} End: {self.end_line} Time {self.time} Raw: {self.chunk_num}"
        )
