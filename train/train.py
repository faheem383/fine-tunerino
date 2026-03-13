import os
from azure.storage.blob import BlobServiceClient
from transformers import (
    AutoTokenizer,
    GPT2LMHeadModel,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset
import torch

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")
COMBINED_BLOB_NAME = "combined_documents.txt"  # The blob name to upload


blob_service_client = BlobServiceClient.from_connection_string(
    AZURE_STORAGE_CONNECTION_STRING
)

container_client = blob_service_client.get_container_client(CONTAINER_NAME)

def download_training_data():
    blob = container_client.download_blob(COMBINED_BLOB_NAME)

    with open(COMBINED_BLOB_NAME, "wb") as f:
        f.write(blob.readall())

download_training_data()

dataset = load_dataset("text", data_files={"train": COMBINED_BLOB_NAME})

tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token

def tokenize_function(examples):
    return tokenizer(examples["text"])

tokenized = dataset.map(tokenize_function, batched=True)

model = GPT2LMHeadModel.from_pretrained("gpt2")

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

training_args = TrainingArguments(
    output_dir="model",
    num_train_epochs=10,
    per_device_train_batch_size=4,
    save_strategy="epoch",
    logging_steps=50
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized["train"],
    data_collator=data_collator,
)

trainer.train()

trainer.save_model("model")

def upload_model():
    for root, dirs, files in os.walk("model"):
        for file in files:
            path = os.path.join(root, file)

            with open(path, "rb") as data:
                container_client.upload_blob(
                    name=f"model/{file}",
                    data=data,
                    overwrite=True
                )

upload_model()

print("Model uploaded to Azure Blob Storage")