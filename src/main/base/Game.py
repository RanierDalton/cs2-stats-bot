from datetime import datetime


class Game:
    def __init__(self, id=None, date=None, allies_rounds=None, adversary_rounds=None, map_id: int = 1, status='win'):
        self._id = id
        self.status = status
        self._date = date if date else datetime.now()
        self._allies_rounds = allies_rounds
        self._adversary_rounds = adversary_rounds
        self._map_id = map_id

    def set_id(self, id):

        self._id = id

    def set_genre(self, genre):
        self._genre = genre

    def set_date(self, date):
        self._date = date

    def set_allies_rounds(self, allies_rounds):
        self._allies_rounds = allies_rounds

    def set_adversary_rounds(self, adversary_rounds):
        self._adversary_rounds = adversary_rounds

    def set_map(self, map_id: int):
        self._map_id = map_id

    @property
    def id(self):
        return self._id

    @property
    def genre(self):
        return self._genre

    @property
    def date(self):
        return self._date

    @property
    def allies_rounds(self):
        return self._allies_rounds

    @property
    def adversary_rounds(self):
        return self._adversary_rounds

    @property
    def map_id(self):
        return self._map_id
