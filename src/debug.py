import pprint

def dump(object: object, message: str = 'Dumped'):
    print('\n[' + message + ']:')
    pprint.PrettyPrinter().pprint(object)
    print('\n')