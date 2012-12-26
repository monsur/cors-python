from validator import Validator


class ListValidator(Validator):

    def __init__(self, values=None):
        Validator.__init__(self)
        if values is None:
            values = []
        self.values = values

    def is_valid(self, value):
        for item in self.values:
            if item.lower() == value.lower():
                return True
        return False
