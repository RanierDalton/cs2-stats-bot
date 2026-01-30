class Map:
    def __init__(self, id: int, name: str, is_active: bool = True):
        self._id = id
        self._name = name
        self._is_active = is_active

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def is_active(self):
        return self._is_active

    def set_name(self, name):
        self._name = name

    def set_is_active(self, is_active):
        self._is_active = is_active
