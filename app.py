import os
from fastapi import FastAPI, Request
import openai

app = FastAPI()


API_path = r"C:\Users\4019-tjyen\Desktop\API.txt"
with open(API_path,"r") as file:
    openapi_key = file.read().strip()

os.environ['OPENAI_API_KEY'] = openapi_key
openai.api_key = openapi_key

# Testing
@app.get("/")
def read_root():
    return {"message": "FastAPI is working!"}
            
@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    text = data.get("text", "")
       

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            prompt= f"please classify the following texts:{text}",
            max_tokens=100
        )

        return {"predictions": [{"label": response['choices'][0]['text'].strip()}]}
    
    except Exception as e:
        return {"error":str(e)}