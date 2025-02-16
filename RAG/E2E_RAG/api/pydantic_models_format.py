# This file will contain the data type restriction classes
# Certain parameters or arguments should follow the mentioned datatype

from pydantic import Field, BaseModel
from enum import Enum
from datetime import datetime

# Enum class for model names
class ModelName(str, Enum):
    LLAMA_8BINSTANT = "llama-3.1-8b-instant"
    GEMMA = "gemma2-9b-it"

# Pydantic model for query input
class QueryInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
    model: ModelName = Field(default=ModelName.LLAMA_8BINSTANT)

# Pydantic model for query response
class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName

# Pydantic model for document information
class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime

# Pydantic model for delete file request
class DeleteFileRequest(BaseModel):
    file_id: int