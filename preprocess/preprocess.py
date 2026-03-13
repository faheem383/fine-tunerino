import os
import io
from azure.storage.blob import BlobServiceClient
from pypdf import PdfReader

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")
COMBINED_BLOB_NAME = "combined_documents.txt"  # The blob name to upload

def extract_text_from_pdfs():
    """Extracts text from PDFs stored in Azure Blob Storage and uploads combined text back to blob."""
    
    # Connect to Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(
        AZURE_STORAGE_CONNECTION_STRING
    )
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    all_text = ""

    # Read PDFs from blob
    for blob in container_client.list_blobs():
        if blob.name.endswith(".pdf"):
            print(f"Reading {blob.name}")
            blob_client = container_client.get_blob_client(blob.name)
            pdf_bytes = blob_client.download_blob().readall()

            try:
                reader = PdfReader(io.BytesIO(pdf_bytes))
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        all_text += text + "\n"
            except Exception as e:
                print(f"Could not read {blob.name}: {e}")

    # Upload combined text back to blob storage
    combined_blob_client = container_client.get_blob_client(COMBINED_BLOB_NAME)
    combined_blob_client.upload_blob(all_text, overwrite=True)
    print(f"Combined text uploaded to blob: {COMBINED_BLOB_NAME}")

    return COMBINED_BLOB_NAME

# Run extraction and upload
blob_path = extract_text_from_pdfs()
print(f"Processing complete. File available on blob: {blob_path}")
