from enum import Enum


class ProcessingStatus(Enum):
    PENDING = "pending"
    DONE = "done"
    ERROR = "error"
