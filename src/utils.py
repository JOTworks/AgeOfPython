from enums import Structure

def isReservedInitFunc(name):
    if isinstance(name, Structure):
        return True
    return False

def isReservedInitFunc_str(name):
    if name in ['Int', 'Point', 'State', 'Const']: return True
    return False

def get_type_length(type):
    length_map = {
        Structure.INT: 1,
        Structure.POINT: 2,
        Structure.STATE: 4,
    }
    return length_map[type]