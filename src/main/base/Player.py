class Player:
    def __init__(self, id, name, nick):
        self._id = id
        self._name = name
        self._nick = nick

    def set_id(self, id):
        self._id = id

    def set_name(self, name):
        self._name = name

    def set_nick(self, nick):
        self._nick = nick

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def nick(self):
        return self._nick
