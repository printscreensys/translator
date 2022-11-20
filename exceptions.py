class UnsupportedLanguageException(Exception):
    def __init__(self, language):
        self.message = f"Sorry, the program doesn't support {language}"
        super().__init__(self.message)


class ConnectionProblemException(Exception):
    def __init__(self):
        self.message = "Something wrong with your internet connection"
        super().__init__(self.message)


class UnknownWordException(Exception):
    def __init__(self, word):
        self.message = f"Sorry, unable to find {word}"
        super().__init__(self.message)
