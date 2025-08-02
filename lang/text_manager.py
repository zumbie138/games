from lang.en_text import EnText

class LanguageManager:
    _current_language = EnText

    @classmethod
    def set_language(cls, language_class):
        cls._current_language = language_class

    @classmethod
    def get_text(cls, key, **kwargs):
        """
        :param key: Chave do texto no idioma ativo.
        :param kwargs: Variáveis para substituir no texto.
        """
        template = getattr(cls._current_language, key, f"Text '{key}' not found")
        return template.format(**kwargs)
    
    def print_text(self, key, **kwargs):
        print(self.get_text(key, **kwargs))