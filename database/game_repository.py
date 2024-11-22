class GameRepository:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_data"):
            self._data = {}

    def get_resource(self, key, default=None):
        return self._data.get(key, default)

    def set_resource(self, key, value):
        self._data[key] = value

