class InvalidExpr(Exception):
    """
    Exception raised when an expression is invalid.
    """

    def __init__(self, type: str, expr: str, ctx=None):
        super().__init__()
        self.type = type
        self.expr = expr
        self.ctx = ctx or {}

class InvalidNormFileError(Exception):
    """
    Exception raised when the number of normalisation impact 
    categories is not equal to impact model impact categories.
    """

    def __init__(self, file: str, nimpact_cat_norm: int, nimpact_cat_mod: int):
        super().__init__()
        self.file = file
        self.nimpact_cat_norm = nimpact_cat_norm
        self.nimpact_cat_mod = nimpact_cat_mod
    
    def __str__(self):
        return f'Impact categories from {self.file} = {self.nimpact_cat_norm} while model has {self.nimpact_cat_mod}'


