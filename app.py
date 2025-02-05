import os
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import openai

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

# Testing
@app.get("/")
def read_root():
    return {"message": "FastAPI is working!"}


#@app.get("/predict/health")
#async def health_check():
 #   return {"status": "ok"}


@app.get("/predict/health")
async def health_check(credentials: HTTPBasicCredentials = Depends(authenticate)):
    return {"status":"ok"}
       
@app.post("/predict")
async def predict(request: Request, credentials: HTTPBasicCredentials = Depends(authenticate)):
    data = await request.json()
    text = data.get("text", "")

    if not text:
        raise HTTPException(status_code=400, detail="Missing 'text' field in request body")

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": f"please classify the following texts into person, date, organization, location: {text}"}],
        max_tokens=100
    )

    result = response.choices[0].message.content.strip()
    return {"predictions": [{"label": result}]}

