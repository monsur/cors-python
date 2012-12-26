import types
from boolean_validator import BooleanValidator
from list_validator import ListValidator


def create(obj):
    obj_type = type(obj)
    if obj_type == types.BooleanType:
        return BooleanValidator(obj)
    if obj_type == types.ListType:
        return ListValidator(obj)
    raise Exception('Validator not found for type: %s' % str(obj_type))
