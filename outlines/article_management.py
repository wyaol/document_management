import time
from enum import Enum

outlines_ready = []
outlines_progressing = []
outlines_done = []


class OutlineStatus(Enum):
    WAIT_FOR_START = 0
    PROGRESSING = 1
    DONE = 2


class Outline:

    def __init__(self, id: int, content: str):
        self.id = id
        self.content = content


def add_one_outline(outline_content: str):
    outlines_ready.append(Outline(int(time.time()), outline_content))
    return {
        'ready': outlines_ready,
        'progressing': outlines_progressing,
        'done': outlines_done
    }


def get_outlines() -> [Outline]:
    return {
        'ready': outlines_ready,
        'progressing': outlines_progressing,
        'done': outlines_done
    }


def pop_one_outline():
    if len(outlines_ready) == 0:
        return None
    outline = outlines_ready.pop()
    outlines_progressing.append(outline)
    return outline
