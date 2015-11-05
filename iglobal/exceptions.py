class iGlobalException(Exception):
    """Base class for iGlobal errors"""

    @property
    def message(self):
        '''Returns the message (first argument) used to create the exception.'''
        return self.args[0]


class iGlobalUnauthorizedException(iGlobalException):
    pass
