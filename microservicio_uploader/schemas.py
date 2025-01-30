from pydantic import BaseModel
from typing import Optional

class UploadResponse(BaseModel):
    message: str
    rows_processed: Optional[int] = None
