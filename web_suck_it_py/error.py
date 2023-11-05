class InitializationError(Exception):
    """Raised whenever a particular optional variable was not set"""

    def __init__(self, variable: str):
        self.message = f"{variable} not initialized"
        super().__init__(self.message)
