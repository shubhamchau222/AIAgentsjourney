from fastapi import FastAPI, File, UploadFile, HTTPException
import shutil
from pydantic_models_format import QueryInput, QueryResponse, DocumentInfo, DeleteFileRequest
from langchain_utils import get_rag_chain
from db_utils import  insert_application_logs, get_chat_history, get_all_documents, insert_document_record, delete_document_record
from chroma_utils import index_document_to_chroma, delete_documents_from_chroma
import os
import uuid
import logging
import uvicorn
from dotenv import load_dotenv

#loading the envs
load_dotenv()
print(os.getenv("GROQ_API_KEY"))

logging.basicConfig(filename='application.log', level=logging.INFO)
app = FastAPI()

@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    session_id= query_input.session_id
    logging.info(f"Session ID: {session_id}, User Query: {query_input.question}, Model: {query_input.model.value}")
    if not session_id:
        session_id= str(uuid.uuid4())

    chat_history= get_chat_history(session_id)
    rag_chain= get_rag_chain(query_input.model.value)
    answer= rag_chain.invoke({
        "input": query_input.question,
        "chat_history":chat_history})['answer']
    
    insert_application_logs(session_id, query_input.question, answer, query_input.model.value)
    logging.info(f"Session ID: {session_id}, AI Response: {answer}")
    return QueryResponse(answer=answer, session_id=session_id, model=query_input.model)


@app.post("/upload-document")
def upload_document(file: UploadFile=File(...)):
    allowed_extensions = ['.pdf', '.docx', '.html']
    file_extension= os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file type{file_extension}")
    temp_file_path= f"temp_{file.filename}"

    try:
        #save the uploaded file to temp files
        with open(temp_file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        file_id= insert_document_record(file.filename)
        sucusses= index_document_to_chroma(temp_file_path, file_id)

        if sucusses:
            return {"message": f"File {file.filename} has been added successfully"}
        else:
            delete_document_record(file_id)
            raise HTTPException(status_code=500, detail=f"Failed to index {file.filename}")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/list-docs",  response_model=list[DocumentInfo])
def list_documents():
    return get_all_documents()

@app.post("/delete-doc")
def delete_document(request: DeleteFileRequest):
    #delete from chroma
    chroma_delete_success= delete_documents_from_chroma(request.file_id)

    if chroma_delete_success:
        db_delete_success= delete_document_record(request.file_id)
        if db_delete_success:
            return {"message": f"Successfully deleted document with file id{request.file_id}"}
        else:
            return {"error": f"Deleted from chroma but failed to delete document from {request.file_id} database"}
    else:
        return {"error": f"Failed to delete document with file_id {request.file_id} from Chroma"}
    
if __name__ == "__main__":
    uvicorn.run( app, host="127.0.0.1", port=8000)