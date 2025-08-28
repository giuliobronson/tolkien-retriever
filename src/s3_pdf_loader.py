import os
import tempfile
import boto3
from typing import List, Optional
from langchain.document_loaders.base import BaseLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document


class S3PDFLoader(BaseLoader):
    """Loader that loads all PDFs from a specified S3 bucket and prefix."""

    def __init__(
        self,
        bucket: str,
        prefix: str,
        endpoint_url: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
    ):
        """Initialize with S3 bucket and prefix."""
        self.bucket = bucket
        self.prefix = prefix
        self.endpoint_url = endpoint_url
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def load(self) -> List[Document]:
        """Load all PDFs from the specified S3 bucket and prefix."""
        s3_client = boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

        # List all objects in the specified bucket and prefix
        response = s3_client.list_objects_v2(Bucket=self.bucket, Prefix=self.prefix)
        documents = []

        for obj in response.get("Contents", []):
            key = obj["Key"]
            if key.endswith(".pdf"):
                # Download the PDF file
                pdf_obj = s3_client.get_object(Bucket=self.bucket, Key=key)
                pdf_content = pdf_obj["Body"].read()

                # Load the PDF content into a Document
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                    temp_pdf.write(pdf_content)
                    temp_pdf_path = temp_pdf.name

                pdf_loader = PyMuPDFLoader(temp_pdf_path)
                docs = pdf_loader.load()
                documents.extend(docs)

                # Clean up the temporary file
                os.remove(temp_pdf_path)

        return documents