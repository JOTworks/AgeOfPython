from enums import Structure

def isReservedInitFunc(name):
    if isinstance(name, Structure):
        return True
    return False

def isReservedInitFunc_str(name):
    if name in ['Int', 'Point', 'State', 'Const']: return True
    return False
