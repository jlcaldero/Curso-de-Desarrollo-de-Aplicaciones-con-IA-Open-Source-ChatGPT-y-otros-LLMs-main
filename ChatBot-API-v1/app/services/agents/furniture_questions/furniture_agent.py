import json
import random

from langchain_text_splitters import CharacterTextSplitter
from app.services.agents.base_agent import BaseAgent
from chromadb import Client
from chromadb.config import Settings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from typing import List
from app.services.langchain_service import LanchainService 
import os

class FurnitureAgent(BaseAgent):
    layer = 'furniture_questions'
    collection_name = 'furniture-collection'
    

    def __init__(self):
        self.chroma_client = Client(Settings(chroma_server_host="localhost", chroma_server_http_port="8000"))

        self.collection = self.chroma_client.get_or_create_collection(
            name=self.collection_name
        )
        self.langchain_service = LanchainService()

    
    def generateResponse(self, input_text: str) -> str:
        context = self.searchBySimilarity(input_text)
        concatenated_docs = ""
        for doc_list in context['documents']:
            for doc in doc_list:
                concatenated_docs += doc + "\n"   

        respuesta = self.langchain_service.chat(self, input_text, concatenated_docs )
        return respuesta
        
    
    def uploadDatabaseWithChunks(self, new_data: List[str]):
        text_splitter = CharacterTextSplitter(
            separator=" ",  # Separador por palabras
            chunk_size=200,  # Tamaño de cada chunk
            chunk_overlap=20  # Superposición entre chunks
        )   
        
        # Separar las descripciones en chunks
        documents = []
        for product in new_data:
            # Crear los chunks a partir de la descripción
            chunks = text_splitter.split_text(product['description'])
            
            # Crear un documento para cada chunk con su metadata
            for chunk in chunks:
                documents.append(
                    Document(
                        page_content=f"{product['productName']}\n{chunk}\nPrecio: {product['price']}",  # Usamos el chunk en lugar de toda la descripción
                        metadata={"id": str(product["id"])} 
                    )
                )
            
        print("Documentos a insertar: " + str(len(documents)))

        # Insertar los documentos en Chroma
        self.collection.add(
            ids=[doc.metadata['id']+str(random.randint(1, 1000)) for doc in documents],  # Usar los IDs únicos de cada chunk
            documents=[doc.page_content for doc in documents],  # Insertar los contenidos de cada chunk
            metadatas=[doc.metadata for doc in documents]  # Insertar los metadatos correspondientes
        )
    
        return "Base vectorial actualizada."
    
    def uploadDatabaseWithoutChunks(self, new_data: List[dict]):
        documents = [
            Document(
                page_content=f"{product['productName']}\n{product['description']}\nPrecio: {product['price']}",  # Concatenamos nombre, descripción y precio
                metadata={"id": product["id"]}  
            )
            for product in new_data
        ]

        print("Documentos a insertar: " + str(len(documents)))

        # Insertar los documentos en Chroma
        self.collection.add(
            ids=[str(i) for i in range(1, len(new_data) + 1)],
            documents=[doc.page_content for doc in documents],
            metadatas=[doc.metadata for doc in documents]
        )
        
        return "Base vectorial actualizada."


    
    def searchBySimilarity(self, query: str) -> str:
        # Buscar en la base vectorial utilizando embeddings
        results = self.collection.query(
            query_texts=[query],  # La consulta que estamos buscando
            n_results=3  # Número de resultados que queremos devolver (1 en este caso)
        )

        # if results['documents']:
        #     most_similar_doc = results['documents'][0][0]  # Primer documento del primer resultado
        #     most_similar_metadata = results['metadatas'][0][0]  # Metadatos del primer resultado
        #     print("Documento más similar encontrado:")
        #     print("Contenido:", most_similar_doc)
        #     print("Metadatos:", most_similar_metadata)
        # else:
        #     print("No se encontraron documentos similares.")

        return results
