class Person:
    """Generic person with a name and a hobby."""

    def __init__(self, name: str, hobby: str) -> None:
        self.name = name
        self.hobby = hobby

    def hobby(self):  # Error on this line
        return "Working!"
