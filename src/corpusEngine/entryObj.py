from pathlib import Path
import numpy as np


class entry:
    path: Path
    start_line: int
    end_line: int
    time: str
    raw_text: str
    embedding: np.ndarray

    def __init__(
        self,
        path: Path,
        start_line: int,
        end_line: int,
        time: str,
        raw_text: str,
    ):
        self.path = path
        self.start_line = start_line
        self.end_line = end_line
        self.time = time
        self.raw_text = raw_text

    def set_embed(self, embed: np.ndarray):
        self.embedding = embed
        return
