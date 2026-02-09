from src.main.service.MinioService import MinioService
from src.main.model.ImageModel import ImageModel
from src.main.base.Image import Image
from src.shared.database.MySqlDriver import MySqlDriver
from src.shared.database.MySqlConnection import MySqlConnection
from typing import Optional


class ImageService:
    def __init__(self):
        self.minio_service = MinioService()
        driver = MySqlDriver(MySqlConnection())
        self.image_model = ImageModel(driver)

    def upload_image(
        self,
        file_data: bytes,
        original_filename: str,
        content_type: str
    ) -> Image:
        file_hash = self.minio_service.calculate_file_hash(file_data)

        existing_image = self.image_model.find_by_hash(file_hash)
        if existing_image:
            return existing_image

        upload_result = self.minio_service.upload_file(
            file_data=file_data,
            original_filename=original_filename,
            content_type=content_type
        )

        image = Image(
            file_hash=upload_result['file_hash'],
            actual_name=upload_result['actual_name'],
            original_name=original_filename,
            relative_path=upload_result['relative_path'],
            full_path=upload_result['full_path'],
            file_size=upload_result['file_size'],
            mime_type=upload_result['mime_type'],
            bucket_name=upload_result['bucket_name']
        )

        image_id = self.image_model.create(image)
        image.set_id(image_id)

        return image

    def get_image_by_id(self, image_id: int) -> Optional[Image]:
        return self.image_model.find_by_id(image_id)

    def download_image(self, image_id: int) -> Optional[bytes]:
        image = self.image_model.find_by_id(image_id)
        if not image:
            return None
        return self.minio_service.download_file(image.relative_path)

    def delete_image(self, image_id: int) -> bool:
        image = self.image_model.find_by_id(image_id)
        if not image:
            return False

        try:
            self.minio_service.delete_file(image.relative_path)
        except Exception as e:
            print(f"Erro ao deletar do MinIO: {e}")

        self.image_model.delete(image_id)
        return True
