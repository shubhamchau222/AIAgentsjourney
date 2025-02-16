# This file will containt the data type restrictions classes
# certain parameters or the arguments should follow mentioned datatype
from pydantic import Field, BaseModel
from enum import Enum
from datetime import datetime

class ModelName(str, Enum):
    LLAMA_8BINSTANT= "llama-3.1-8b-instant"
    GEMMA = "gemma2-9b-it"

class QueryInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
    model: ModelName = Field(default= ModelName.LLAMA_8BINSTANT)

class QueryResponse(BaseModel):
    answer : str
    session_id:str 
    model: ModelName

class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime

class DeleteFileRequest(BaseModel):
    file_id:int