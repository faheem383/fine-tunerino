from fastapi import FastAPI
from transformers import pipeline, GPT2LMHeadModel, AutoTokenizer
from azure.storage.blob import BlobServiceClient
import os
import torch

app = FastAPI()

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")

blob_service_client = BlobServiceClient.from_connection_string(
    AZURE_STORAGE_CONNECTION_STRING
)

container_client = blob_service_client.get_container_client(CONTAINER_NAME)

MODEL_PATH = "model"

def download_model():
    os.makedirs(MODEL_PATH, exist_ok=True)

    blobs = container_client.list_blobs(name_starts_with="model/")


    for blob in blobs:
        filename = blob.name.split("/")[-1]
        local_path = os.path.join(MODEL_PATH, filename)

        #data = container_client.download_blob(blob.name)

        #with open(f"{MODEL_PATH}/{filename}", "wb") as f:
        #    f.write(data.readall())
        #blob_client = container_client.get_blob_client(blob.name)

        #with open(f"{MODEL_PATH}/{filename}", "wb") as f:
        #    f.write(blob_client.download_blob().readall())
        print("Downloading:", blob.name)

        blob_client = container_client.get_blob_client(blob.name)

        with open(local_path, "wb") as f:
            stream = blob_client.download_blob()
            f.write(stream.readall())

download_model()

#tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
#model = GPT2LMHeadModel.from_pretrained(MODEL_PATH)

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained(MODEL_PATH)


generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1
)

@app.post("/generate")
def generate_text(prompt: str):

    result = generator(
        prompt,
        max_new_tokens=100,
        temperature=0.7,
        top_p=0.95
    )

    return {"generated_text": result[0]["generated_text"]}