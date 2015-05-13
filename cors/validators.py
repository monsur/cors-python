import re
import types


def create(obj):
    obj_type = type(obj)
    if isinstance(obj, types.BooleanType):
        return BooleanValidator(obj)
    if isinstance(obj, types.ListType):
        return ListValidator(obj)
    if isinstance(obj, re._pattern_type):
        return RegexValidator(obj)

    raise Exception('Validator not found for type: %s' % str(obj_type))


class Validator(object):

    def __init__(self):
        pass

    def is_valid(self, value):
        pass


class BooleanValidator(Validator):

    def __init__(self, value):
        Validator.__init__(self)
        self.value = value

    def is_valid(self, value):
        return self.value


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


class RegexValidator(Validator):

    def __init__(self, value):
        Validator.__init__(self)
        self.value = value

    def is_valid(self, value):
        return self.value.match(value) is not None
