import os
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import openai
from pydantic import BaseModel

app = FastAPI()

# Set Basic Auth
security = HTTPBasic()

API_path = r"C:\Users\4019-tjyen\Desktop\API.txt"
with open(API_path,"r") as file:
    openapi_key = file.read().strip()

os.environ['OPENAI_API_KEY'] = openapi_key
openai.api_key = openapi_key

USERNAME = "jaslene"
PASSWORD = "password"

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != USERNAME or credentials.password != PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials


@app.get("/health")
async def root_health():
    return {"status": "ok"}

@app.get("/predict/health")
async def health_check():
    return {"status": "ok"}

@app.post("/predict/setup")
async def setup():
    return {"status": "ok"}


class TextRequest(BaseModel):
    data: dict

@app.post("/predict")
async def predict(request: TextRequest):
    text = request.data.get("text", "")

    if not text:
        raise HTTPException(status_code=400, detail="No text provided")
       
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": f"Please classfy the following text as Person, Date, Organization, Location: {text}"}],
    )

    label = response["choices"][0]["message"]["content"].strip()


    return [{

        "result": [
                {
                    "value": {
                        "text": text,
                        "labels": [label]},
                    "from_name": "label",
                    "to_name": "text",
                    "type": "labels"
                }
            ]
        }]
    
    