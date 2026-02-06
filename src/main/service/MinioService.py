from minio import Minio
from minio.error import S3Error
import hashlib
import io
import os
from typing import Optional


class MinioService:
    def __init__(self):
        self.endpoint = os.getenv('MINIO_ENDPOINT', 'minio:9000')
        self.access_key = os.getenv('MINIO_ROOT_USER', 'minioadmin')
        self.secret_key = os.getenv('MINIO_ROOT_PASSWORD', 'minioadmin123')
        self.use_ssl = os.getenv('MINIO_USE_SSL', 'False').lower() == 'true'
        self.bucket_name = os.getenv('MINIO_BUCKET_NAME', 'cs2-images')

        self.client = Minio(
            endpoint=self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.use_ssl
        )

        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error as e:
            print(f"Erro ao criar bucket: {e}")

    def calculate_file_hash(self, file_data: bytes) -> str:
        return hashlib.sha256(file_data).hexdigest()

    def upload_file(
        self,
        file_data: bytes,
        original_filename: str,
        content_type: str,
        object_name: Optional[str] = None
    ) -> dict:
        file_hash = self.calculate_file_hash(file_data)

        if not object_name:
            extension = os.path.splitext(original_filename)[1]
            object_name = f"games/{file_hash}{extension}"

        try:
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=io.BytesIO(file_data),
                length=len(file_data),
                content_type=content_type
            )
        except S3Error as e:
            raise Exception(f"Erro no upload para MinIO: {e}")

        protocol = "https" if self.use_ssl else "http"
        full_url = f"{protocol}://{self.endpoint}/{self.bucket_name}/{object_name}"

        return {
            'file_hash': file_hash,
            'actual_name': object_name.split('/')[-1],
            'relative_path': object_name,
            'full_path': full_url,
            'file_size': len(file_data),
            'mime_type': content_type,
            'bucket_name': self.bucket_name
        }

    def download_file(self, object_name: str) -> bytes:
        try:
            response = self.client.get_object(self.bucket_name, object_name)
            data = response.read()
            response.close()
            response.release_conn()
            return data
        except S3Error as e:
            raise Exception(f"Erro ao baixar arquivo: {e}")

    def delete_file(self, object_name: str):
        try:
            self.client.remove_object(self.bucket_name, object_name)
        except S3Error as e:
            raise Exception(f"Erro ao deletar arquivo: {e}")

    def file_exists(self, object_name: str) -> bool:
        try:
            self.client.stat_object(self.bucket_name, object_name)
            return True
        except S3Error:
            return False
