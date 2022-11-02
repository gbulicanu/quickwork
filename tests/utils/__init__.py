"""
Unit test utilities module.
"""


def anything(cls):
    """
    Matcher whose __eq__ method always returns True.

    Return
    @param cls: The cls of the arg in assert_called_with.
    @return: A class whose __eq__ method always returns True.
    """

    class Anything(cls):
        """ Anything
        """
        def __init__(self):
            pass

        def __eq__(self, other):
            return True

    return Anything()

def empty_stub():
    """ Empty stub function.
    """
    return None
