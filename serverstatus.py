import enum

class ServerStatus(enum.Enum):
    stop = enum.auto()
    starting = enum.auto()
    waiting = enum.auto()
    playing = enum.auto()
    stopping = enum.auto()