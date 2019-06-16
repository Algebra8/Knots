# Decorator to check params of BraidWord
def checkparams_braidword(func: 'func') -> 'func':
    def wrapper(*args, **kwargs):
        if len(args) > 1:  # args will have self since for class
            initword = args[1]
            # Check if type is not list
            if not isinstance(initword, list):
                msg = "BraidWord initword argument must be a list."
                raise TypeError(msg)

            # Check if any generators are zero
            elif 0 in initword:
                msg = ('Braid generators are indexed starting at one. '
                       'No zero braid generators allowed.')
                raise ValueError(msg)
            else:
                return func(*args, **kwargs)
        else:
            initword = kwargs[list(kwargs.keys())[0]]
            # Check if type is not list
            if not isinstance(initword, list):
                msg = "initword argument must be a list."
                raise TypeError(msg)

            # Check if any generators are zero
            elif 0 in initword:
                msg = ('Braid generators are indexed starting at one. '
                       'No zero braid generators allowed.')
                raise ValueError(msg)
            else:
                return func(*args, **kwargs)
    return wrapper
