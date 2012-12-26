from validator import Validator


class BooleanValidator(Validator):

    def __init__(self, value):
        Validator.__init__(self)
        self.value = value

    def is_valid(self, value):
        return self.value
