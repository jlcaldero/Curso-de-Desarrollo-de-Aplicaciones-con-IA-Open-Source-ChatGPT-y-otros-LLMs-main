from fastapi import APIRouter, HTTPException
from app.models.chatbot import ChatRequest, ChatResponse
from app.services.chatbot_service import ChatbotService
from app.services.chatbot_serviceV2 import ChatbotServiceV2

router = APIRouter()

chatbot_serviceV2 = ChatbotServiceV2()

@router.post("/chatt")
async def chat(request: ChatRequest):
    
    print('chatV2')
    response = await chatbot_serviceV2.get_response(request, "furniture-questions")
    return response

@router.post("/upload-data")
def chat(layer: str):
    print('upload-data')
    response = chatbot_serviceV2.uploadDatabase(layer)
    return response
    
