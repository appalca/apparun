class InvalidExpr(Exception):
    """
    Exception raised when an expression is invalid.
    """

    def __init__(self, type: str, expr: str, ctx=None):
        super().__init__()
        self.type = type
        self.expr = expr
        self.ctx = ctx or {}
