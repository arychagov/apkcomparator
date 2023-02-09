class BadEnvironmentError(Exception):
    def __init__(self, message: str):
        super(BadEnvironmentError, self).__init__(message)
