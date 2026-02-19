from enum import Enum


class ProcessingStatus(Enum):
    IN_PROGRESS = "in progress"
    DONE = "done"
    ERROR = "error"
