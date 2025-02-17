from langchain_chroma import Chroma
import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("GROQ_API_KEY"))

# Initialize text splitter with specific chunk size and overlap
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)

# Initialize embedding model
embedding_model = GoogleGenerativeAIEmbeddings(model='models/text-embedding-004')

# Initialize vector store with embedding model and persistence directory
vectore_store = Chroma(persist_directory="./chroma_db", 
                      embedding_function=embedding_model)

# Function to load and split document based on file type
def load_and_split_document(file_path: str) -> List[Document]:
    # Determine the loader to use based on file extension
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.docx'):
        loader = Docx2txtLoader(file_path)
    elif file_path.endswith('.html'):
        loader = UnstructuredHTMLLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
    documents: List[Document]= loader.load()

    return text_splitter.split_documents(documents)



def index_document_to_chroma(file_path:str, file_id:int) -> bool:
    try:
        splits= load_and_split_document(file_path)

        #Add metadata to each split
        for split in splits:
            split.metadata['file_id']= file_id
        
        vectore_store.add_documents(splits)
        return True
    except Exception as e:
        print(f"Error indexing document: {e}")
        return False



def delete_documents_from_chroma(file_id:int):
    try:
        docs = vectore_store.get(where={"file_id": file_id})
        print(f"Found {len(docs['ids'])} document chunks for file_id {file_id}")

        vectore_store._collection.delete(where={"file_id": file_id})
        print(f"Deleted all documents with file_id {file_id}")
        return True
    except Exception as e:
        print(f"Error deleting document with file_id {file_id} from Chroma: {str(e)}")
        return False




