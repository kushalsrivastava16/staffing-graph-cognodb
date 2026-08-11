class DatabaseUnavailableError(Exception):
    """Raised when the graph database cannot be reached or authenticated against."""


class NotFoundError(Exception):
    """Raised when a requested entity does not exist in the graph."""

    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(message)
