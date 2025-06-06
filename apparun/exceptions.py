class NotAnExpressionError(Exception):
    """
    Raised when a value of an element of an impact model is
    not an expression.
    """

    def __init__(self, expr):
        super().__init__(f"Invalid expression: {expr}")
        self.expr = expr
