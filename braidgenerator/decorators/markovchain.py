from braidgenerator import BraidWord

def _check_braidword(braidword: BraidWord) -> BraidWord:
    # Checks if input is BraidWord object
    if isinstance(braidword, BraidWord):
        return True
    else:
        return False

# Decorator to check params of MarkovChain
def checkparams_markovchain(func: 'func') -> 'func':
    # Wrapper function to wrap around MarkovChain init
    def wrapper(*args, **kwargs) -> 'None':
        # Check that between 1 and 3 arguments are given
        if len(args) == 1 and not kwargs:
            msg = ('MarjovChain.__init__ should take between 1 and 3 arguments '
                   'and requires at least BraidWord in initialization.')
            raise Exception(msg)
        elif len(args) > 1:
            if not isinstance(args[1], BraidWord):
                if not isinstance(args[1], list):
                    msg = "First argument must be BraidWord or list."
                    raise ValueError(msg)
                else:
                    # It is a list, then convert to BraidWord
                    # Required to convert to list due to immutability
                    # of tuples
                    args = list(args)
                    args[1] = BraidWord(args[1])
                    args = tuple(args)
            # Dealing with args..
            # Check number of arguments
            if len(args) > 4:
                msg = "MarjovChain.__init__ should take between 1 and 3 arguments."
                raise Exception(msg)
            if len(args) >= 3:
                # Check if maxgen is negative
                if args[2] < 0:
                    msg = "maxgen (args[1]) parameter must be nonnegative."
                    raise ValueError(msg)
            if len(args) == 4:
                # Check if maxlen is negative
                if args[3] < 0:
                    msg = "maxlen (args[2]) parameter must be nonnegative."
                    raise ValueError(msg)
            return func(*args, **kwargs)
        else:
            # Dealing with kwargs..
            # Check number of arguments
            if len(list(kwargs.keys())) > 4:
                msg = "MarjovChain.__init__ should take between 1 and 3 arguments."
                raise Exception(msg)
            for k, v in kwargs.items():
                if k == 'braidword':
                    # Check if v is empty or not list or not BraidWord
                    if not _check_braidword(v):
                        # If v is not list then raise exception
                        # Else wrap it in Braid
                        if not isinstance(v, list):
                            msg = ('MarjovChain.__init__ should take between 1 and 3 arguments '
                                   'and requires at least BraidWord in initialization.')
                            raise Exception(msg)
                        else:
                            kwargs[k] = BraidWord(v)
                elif k == 'maxgen':
                    # Check if maxgen < 0
                    if v < 0:
                        msg = "maxgen parameter must be nonnegative."
                        raise ValueError(msg)
                elif k == 'maxlen':
                    # Check if maxlen < 0
                    if v < 0:
                        msg = "maxlen parameter must be nonnegative."
                        raise ValueError(msg)
            return func(*args, **kwargs)
    return wrapper
