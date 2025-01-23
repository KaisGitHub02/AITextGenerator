from pyngrok import ngrok
import nest_asyncio
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from transformers import pipeline
import logging
import json

# Configuración de ngrok
ngrok.set_auth_token("2rzhtVRe2wJ8jrWBu9Jat3RNe2F_519Kxi9Uu91CqNzk99awZ")

# Permitir la ejecución asincrónica
nest_asyncio.apply()

# Inicializar el sistema de logs
logging.basicConfig(
    filename="api_requests.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Inicializar el modelo DeepSeek-R1-Distill-Qwen-1.5B
print("Cargando modelo GPT2...")
text_generator = pipeline("text-generation", model="gpt2")
# Crear la app de FastAPI
app = FastAPI(
    title="API de Generación de Texto",
    description="Usa GPT2 para generar texto a partir de un prompt.",
)

# Esquema para validar entradas con Pydantic
class TextGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Texto inicial para generar contenido.")
    max_length: int = Field(50, ge=10, le=512, description="Longitud máxima del texto generado.")
    temperature: float = Field(1.0, ge=0.0, le=1.0, description="Nivel de creatividad del modelo (0 a 1).")
    top_p: float = Field(1.0, ge=0.0, le=1.0, description="Proporción acumulativa de probabilidades.")

# Sistema de autenticación básica con token
API_TOKEN = "2rzhtVRe2wJ8jrWBu9Jat3RNe2F_519Kxi9Uu91CqNzk99awZ"
security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.password != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token de autenticación inválido.")

# Histórico con persistencia
HISTORY_FILE = "history.json"

def load_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_to_history(entry):
    history = load_history()
    history.append(entry)
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)
        file.write("\n")
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Generación de Texto"}

# Endpoint para generar texto
@app.post("/generate")
async def generate_text(request: TextGenerationRequest, credentials: HTTPBasicCredentials = Depends(authenticate)):
    try:
        response = text_generator(
            request.prompt,
            max_length=request.max_length,
            temperature=request.temperature,
            top_p=request.top_p,
            repetition_penalty=1.2,  # Penaliza repeticiones
            truncation=True
        )
        generated_text = response[0]["generated_text"]
        
        # Guardar en histórico
        entry = {"prompt": request.prompt, "generated_text": generated_text}
        save_to_history(entry)

        # Registrar en logs
        logging.info(f"Prompt: {request.prompt} | Respuesta: {generated_text}")
        
        return {"prompt": request.prompt, "generated_text": generated_text}
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener histórico
@app.get("/history")
async def get_history(credentials: HTTPBasicCredentials = Depends(authenticate)):
    return load_history()

# Iniciar ngrok y exponer la API
public_url = ngrok.connect(8000)
print(f"La API está disponible públicamente en: {public_url}")

# Iniciar el servidor FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
