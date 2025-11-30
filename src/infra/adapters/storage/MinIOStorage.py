import io
from minio import Minio, S3Error

from core.ports.storage.file_storage import IFileStorage


class MinIOStorage(IFileStorage):
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        secure: bool = False
    ):
        self.bucket = bucket_name
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )

        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)

    def upload(self, path: str, content: bytes, content_type: str = "application/octet-stream"):
        self.client.put_object(
            bucket_name=self.bucket,
            object_name=path,
            data=io.BytesIO(content),
            length=len(content),
            content_type=content_type
        )

    def download(self, path: str) -> bytes:
        response = None
        try:
            response = self.client.get_object(self.bucket, path)
            return response.read()
        finally:
            if response is not None:
                response.close()
                response.release_conn()

    def exists(self, path: str) -> bool:
        try:
            self.client.stat_object(self.bucket, path)
            return True
        except S3Error as e:
            if e.code == "NoSuchKey":
                return False
            raise