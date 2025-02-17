
---

# End to End RAG APIs

## Description
This project implements an end-to-end History Aware Retrieval-Augmented Generation (RAG) API. It integrates with FAST APIs to fetch relevant data and generate meaningful outputs. The APIs used in this project include **GROQ** and **Gemini**.

## API IMAGE

![Image Alt Text](images\api_img.PNG)


## Requirements

Before running the project, ensure you have the following API keys and dependencies:

1. **GROQ_API_KEY**
2. **GEMINI_API_KEY**

Both keys must be provided in a `.env` file.

## Setting Up the Project

### Step 1: Clone the Repository
Clone this repository to your local machine.

```bash
git clone <repository-url>
cd <repository-directory>
```

### Step 2: Install Required Dependencies

Install all the required dependencies using the `requirements.txt` file. Run the following command:

```bash
pip install -r requirements.txt
```

### Step 3: Add API Keys

Create a `.env` file in the root directory of the project and add the following lines:

```
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

Make sure to replace the placeholders with your actual API keys.

### Step 4: Running the Application

Once everything is set up, you can run the application by using the following command:

```bash
python app.py
```

This will start the API, and you can begin making requests to interact with the RAG functionality.

## Available Endpoints

### 1. **Upload Document**
- **Endpoint**: `POST /upload-document`
- **Description**: Upload a document for processing.
- **Request Body**:
  - `file`: The document file to upload (PDF, Word, HTML.)
- **Response**:
  - `status`: Success or failure of the upload.
  - `message`: Details or errors.

### 2. **Delete Document**
- **Endpoint**: `POST /delete-doc`
- **Description**: Delete an uploaded document using its `document_id` (int).
- **Request Parameter**:
  - `document_id`: The ID of the document to delete.
- **Response**:
  - `status`: Success or failure of the deletion.
  - `message`: Confirmation or error details.

### 3. **List Uploaded Documents**
- **Endpoint**: `GET /list-docs`
- **Description**: Get a list of all uploaded documents.
- **Response**:
  - `documents`: A list of document objects with details such as `document_id`, `file_name`, and `uploaded_at`.

### 4. **Chat with RAG Model**
- **Endpoint**: `POST /chat`
- **Description**: Send a chat query to the RAG model and receive a response.
- **Request Body**:
  - `query`: The question or statement you want to ask the model.
- **Response**:
  - `response`: The generated response based on the uploaded documents.

## License

Include any licensing information, if applicable.

---

This version now includes the basic details of the endpoints for uploading, deleting, listing documents, and chatting. If you have more specific details for each endpoint, feel free to add them!


# Thank You!