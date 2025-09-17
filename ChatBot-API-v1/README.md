# Chatbot de UTN Muebles

Este es un proyecto de un chatbot de ventas para UTN Muebles, implementado con FastAPI. El chatbot utiliza la integración de OpenAI y LangChain para responder preguntas sobre productos de muebles y ayudar a los usuarios a encontrar el producto adecuado para sus necesidades.

## Requisitos previos

Asegúrate de tener instaladas las siguientes herramientas:

- **Python 3.10 o superior**
- **pip** (el gestor de paquetes de Python)
- **uvicorn** para correr el servidor ASGI

## Instalación

Sigue los siguientes pasos para clonar el proyecto, instalar las dependencias y correr el servidor:

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu-repositorio/chatbot-utn-muebles.git
   cd chatbot-utn-muebles
   ```

2. Crea y activa un entorno virtual (opcional pero recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```

3. Instala las dependencias del proyecto:

   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno. Crea un archivo `.env` en la raíz del proyecto con tu clave API de OpenAI:

   ```bash
   OPENAI_API_KEY=tu_clave_api_aqui
   ```

## Ejecutar el proyecto

Una vez instaladas las dependencias, puedes iniciar el servidor de la aplicación utilizando Uvicorn:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Esto iniciará el servidor en `http://127.0.0.1:8000/`.

## Funcionalidades

1. **Chatbot para Ventas de Muebles**:
   El chatbot está entrenado para responder preguntas sobre productos de muebles utilizando una base de datos de productos. Se puede interactuar con el chatbot a través de una interfaz web simple o mediante una API.

2. **Interfaz Web**:
   El chatbot tiene una interfaz de usuario simple disponible en `http://127.0.0.1:8000/`, donde los usuarios pueden interactuar con el chatbot en una ventana de chat.

3. **Endpoints API**:
   - `POST /chat`: Este endpoint acepta un `chat_id` y un `message` como cuerpo de la solicitud y devuelve una respuesta del chatbot.

### Ejemplo de solicitud a la API:

```bash
POST http://127.0.0.1:8000/chat
Content-Type: application/json

{
  "chat_id": "12345",
  "message": "¿Cuánto cuesta el sofá minimalista?"
}
```

### Respuesta esperada:

```json
{
  "chat_id": "12345",
  "response": "El sofá minimalista cuesta 500 USD."
}
```

## Estructura del proyecto

```plaintext
├── app/
│   ├── __init__.py
│   ├── main.py            # Punto de entrada principal de la aplicación FastAPI
│   ├── routes/
│   │   ├── __init__.py
│   │   └── chatbot.py     # Rutas del chatbot
│   ├── services/
│   │   ├── __init__.py
│   │   └── chatbot_service.py  # Lógica del chatbot con LangChain y OpenAI
│   ├── models/
│   │   ├── __init__.py
│   │   └── chatbot.py     # Modelos de entrada y salida para la API
│   ├── static/
│   │   └── index.html     # Interfaz de usuario simple para el chatbot
├── .env                   # Archivo para variables de entorno (agregar tu clave API aquí)
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Este archivo
```

## Dependencias

Las principales dependencias de este proyecto son:

- **FastAPI**: Para construir la API web.
- **Uvicorn**: Para correr el servidor ASGI.
- **LangChain**: Para la lógica del chatbot y generación de respuestas.
- **OpenAI**: Para integrar el modelo GPT de OpenAI.
- **pydantic**: Para la validación de datos.
