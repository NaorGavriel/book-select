import enum

class JobStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"

class Decision(str, enum.Enum):
    strong_match = "strong_match"
    consider = "consider"
    avoid = "avoid"
