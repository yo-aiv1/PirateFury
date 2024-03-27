class InvalidFileName(Exception):
    def __str__(self) -> str:
        return "the file name must have the json extention."
