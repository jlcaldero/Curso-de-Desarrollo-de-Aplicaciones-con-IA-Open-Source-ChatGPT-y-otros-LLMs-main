import json
import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap
from langchain.schema.output_parser import StrOutputParser
from app.models.chatbot import ChatRequest, ChatResponse, Furtinure
from app.services.agents.frecuent_questions.frecuent_question_agent import FrecuentQuestionAgent
from app.services.agents.furniture_questions.furniture_agent import FurnitureAgent
import openai
load_dotenv(find_dotenv())

class ChatbotServiceV2:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.openai_api_key

        self.agents_dict = {
            "furniture-questions": FurnitureAgent(),
            "frecuenta-questions": FrecuentQuestionAgent(),
        }   

    async def get_response(self, request:ChatRequest, layer:str) -> str:
        response = await self.agents_dict.get(layer,None).generateResponse(request.message)
        
        return ChatResponse(chat_id=request.chat_id, response=response)
        
    
    def uploadDatabase(self, layer:str) -> str:
        file_path = "./app/services/data/furniture_data.json"
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Imprime el contenido del JSON en la terminal
        # print("Contenido del JSON:")
        # for item in data:
        #     print(f"Nombre del Producto: {item['productName']}")
        #     print(f"Precio: {item['price']}")
        #     print(f"Descripción: {item['description']}")
        #     print("-" * 40)  # Separador entre productos
        return self.agents_dict.get(layer,None).uploadDatabaseWithoutChunks(data)
    

        

