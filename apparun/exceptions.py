class InvalidExpr(Exception):
    """
    Exception raised when an expression is invalid.
    """

    def __init__(self, type: str, expr: str, ctx=None):
        super().__init__()
        self.type = type
        self.expr = expr
        self.ctx = ctx or {}

class InvalidFileError(Exception):
    """
    Exception raised when the number of normalisation impact
    categories is not equal to impact model impact categories.
    """

    def __init__(self, file: str):
        super().__init__()
        self.file = file

    def __str__(self):
        return f'Impact categories from {self.file} different with impact model categories. Check correspondances.'


