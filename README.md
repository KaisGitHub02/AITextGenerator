# API de Generación de Texto con FastAPI y GPT-2

Esta API permite generar texto de manera dinámica utilizando el modelo **GPT-2**. La API está construida con **FastAPI** y expuesta a través de **ngrok** para ser accesible de manera pública. Puedes interactuar con la API para generar texto a partir de un `prompt` y configurar varios parámetros como la longitud y la temperatura del texto generado.

## Características

- Generación de texto con **GPT-2**.
- Autenticación mediante un **token básico**.
- Histórico de solicitudes guardado en un archivo JSON.
- Acceso público a la API mediante **ngrok**.
- Uso de **FastAPI** para crear y gestionar los endpoints.

## Requisitos

Antes de ejecutar la API, asegúrate de tener instalado Python y las siguientes dependencias:

- **Python 3.7 o superior**
- **pip** (gestor de paquetes de Python)

### **Notas importantes:**
1. **Token de ngrok**: Como se menciona en el archivo, asegúrate de obtener tu token de autenticación de ngrok y configurarlo correctamente en las variables de entorno.
2. **Autenticación**: La API está protegida con un token básico configurado en el código. Asegúrate de cambiar el valor de `API_TOKEN` antes de usarla en producción.
![image](https://github.com/user-attachments/assets/fa9c0449-a8a2-4063-8e9b-aa6a16a49a4d)

### Descripción de los Endpoints:

1. **`/generate`** (POST): 
   - Recibe un prompt de texto junto con parámetros como `max_length`, `temperature`, y `top_p`. Utiliza el modelo GPT-2 para generar texto y devolverlo como respuesta. También guarda el resultado en un historial y lo registra en los logs.
![Imagen de WhatsApp 2025-01-23 a las 11 03 16_c07f3a98](https://github.com/user-attachments/assets/24dab9ea-aa2d-47d1-a9a7-74d960bec2a6)

2. **`/history`** (GET): 
   - Devuelve el historial de todas las solicitudes previas y sus respuestas generadas, permitiendo ver los textos generados previamente.
![image](https://github.com/user-attachments/assets/cdc60507-e748-43ca-96c1-703731c8e80c)

Con este `README.md` tendrás la documentación completa de tu API, incluyendo la descripción detallada de los endpoints.

## Guía de Ejecución

### 1. **Clonar el Repositorio o Descargar el Proyecto**

Si no tienes el proyecto aún, clónalo o descárgalo:

```bash
git clone <URL_DEL_REPOSITORIO>
```

### 2. **Instalación de dependencias**

Puedes instalar las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
```

### 3. **Modificación del código**

Cambiar la variable "" por su token de autenticación ngrok

### 4. **Ejecución del código**

```bash
python app.py
```

### 5. **Salida esperada y pruebas**

Cargando modelo GPT2...
Device set to use cpu
La API está disponible públicamente en: NgrokTunnel: "https://947a-34-148-67-83.ngrok-free.app" -> "http://localhost:8000"

A continuación se cogerá el NgrokTunnel y se añadirá a Postman en método POST para probar los métodos generate e history.

La salida quedará recogida en "history.json"
![image](https://github.com/user-attachments/assets/e5d4f956-dec7-46df-8f26-3886510d329e)

Y el registro de logs será visible en el terminal de ejecución
![Imagen de WhatsApp 2025-01-23 a las 11 09 05_6eef0b3f](https://github.com/user-attachments/assets/7dbf386e-7b4f-4866-9153-b96b353116b9)





