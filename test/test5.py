from enum import Enum

class PendingStatus(Enum):
    """
    交易状态
    """
    Waiting = 1
    Success = 2
    Reject  = 3
    Redraw  = 4

print(PendingStatus(1))
print(PendingStatus.Waiting.value)