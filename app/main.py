from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .schemas import ChatMessage, DocumentInput
from .openai_service import RAGService

app = FastAPI()

# Khởi tạo RAG service
rag_service = RAGService()

# Mount static files và templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(message: ChatMessage):
    response = await rag_service.get_openai_response(message.message)
    return {"response": response}

@app.post("/add-documents")
async def add_documents(documents: DocumentInput):
    """API endpoint để thêm documents vào knowledge base"""
    rag_service.add_documents(documents.texts)
    return {"message": "Documents added successfully"}