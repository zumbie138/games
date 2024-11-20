class GameRepository():
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GameRepository, cls).__new__(cls, *args, **kwargs)
            cls._instance._data = {}
    
    def set_resource(self, key: str, value):
        self._data[key] = value

    def get_resource(self, key: str):
        return self._data.get(key)

