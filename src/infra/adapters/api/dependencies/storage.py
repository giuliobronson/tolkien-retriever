from functools import lru_cache
from config import MINIO_BUCKET_DOCUMENTS, MINIO_ENDPOINT_URL, MINIO_ROOT_PASSWORD, MINIO_ROOT_USER, PROVIDER
from infra.adapters.storage.minio_storage import MinIOStorage

    
@lru_cache
def get_file_storage():
    if PROVIDER == "ON_PREMISE":
        return MinIOStorage(
        endpoint=MINIO_ENDPOINT_URL, 
        access_key=MINIO_ROOT_USER,
        secret_key=MINIO_ROOT_PASSWORD,
        bucket_name=MINIO_BUCKET_DOCUMENTS,
        secure=False
    )
    raise ValueError("Invalid provider")