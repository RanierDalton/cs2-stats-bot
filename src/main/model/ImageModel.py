from src.shared.database.interfaces.DBDriver import DBDriver
from src.main.base.Image import Image
from typing import Optional


class ImageModel:
    def __init__(self, driver: DBDriver):
        self.driver = driver

    def create(self, image: Image) -> int:
        query = """
            INSERT INTO image (
                file_hash, actual_name, original_name, relative_path,
                full_path, file_size, mime_type, bucket_name
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            image.file_hash,
            image.actual_name,
            image.original_name,
            image.relative_path,
            image.full_path,
            image.file_size,
            image.mime_type,
            image.bucket_name
        )
        return self.driver.insert(query, params)

    def find_by_hash(self, file_hash: str) -> Optional[Image]:
        query = "SELECT * FROM image WHERE file_hash = %s"
        row = self.driver.select(query, (file_hash,))

        if row:
            return Image(
                id=row[0],
                file_hash=row[1],
                actual_name=row[2],
                original_name=row[3],
                relative_path=row[4],
                full_path=row[5],
                file_size=row[6],
                mime_type=row[7],
                bucket_name=row[8],
                uploaded_at=row[9]
            )
        return None

    def find_by_id(self, image_id: int) -> Optional[Image]:
        query = "SELECT * FROM image WHERE id = %s"
        row = self.driver.select(query, (image_id,))

        if row:
            return Image(
                id=row[0],
                file_hash=row[1],
                actual_name=row[2],
                original_name=row[3],
                relative_path=row[4],
                full_path=row[5],
                file_size=row[6],
                mime_type=row[7],
                bucket_name=row[8],
                uploaded_at=row[9]
            )
        return None

    def delete(self, image_id: int):
        query = "DELETE FROM image WHERE id = %s"
        return self.driver.delete(query, (image_id,))
