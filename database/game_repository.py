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

class MessageLog:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.journal = None
        return cls._instance
    
    @classmethod
    def init_journal(cls, journal):
        cls._instance.journal = journal
        
    @classmethod
    def add_message(cls, text: str, color=(255, 255,  255)):
        if cls._instance and cls._instance.journal:
            cls._instance.journal.add_entry(text, color)
        else:
            print(f'[FALLBACK LOG]: {text}')