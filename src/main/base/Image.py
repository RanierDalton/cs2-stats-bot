from datetime import datetime


class Image:
    def __init__(
        self,
        id=None,
        file_hash=None,
        actual_name=None,
        original_name=None,
        relative_path=None,
        full_path=None,
        file_size=None,
        mime_type=None,
        bucket_name='cs2-images',
        uploaded_at=None
    ):
        self._id = id
        self._file_hash = file_hash
        self._actual_name = actual_name
        self._original_name = original_name
        self._relative_path = relative_path
        self._full_path = full_path
        self._file_size = file_size
        self._mime_type = mime_type
        self._bucket_name = bucket_name
        self._uploaded_at = uploaded_at if uploaded_at else datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def file_hash(self):
        return self._file_hash

    @property
    def actual_name(self):
        return self._actual_name

    @property
    def original_name(self):
        return self._original_name

    @property
    def relative_path(self):
        return self._relative_path

    @property
    def full_path(self):
        return self._full_path

    @property
    def file_size(self):
        return self._file_size

    @property
    def mime_type(self):
        return self._mime_type

    @property
    def bucket_name(self):
        return self._bucket_name

    @property
    def uploaded_at(self):
        return self._uploaded_at

    def set_id(self, id):
        self._id = id
