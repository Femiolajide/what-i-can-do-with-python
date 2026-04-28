from lark import Lark, Transformer, v_args, UnexpectedInput


grammar = r"""
?start: expr

?expr: expr "+" term   -> add
     | expr "-" term   -> sub
     | term

?term: term "*" factor -> mul
     | term "/" factor -> div
     | factor

?factor: "+" factor    -> pos
       | "-" factor    -> neg
       | power

?power: atom "^" factor -> pow
      | atom

?atom: NUMBER           -> number
     | "(" expr ")"     -> grouped

%import common.NUMBER
%import common.WS
%ignore WS
"""


@v_args(inline=True)
class ToLatex(Transformer):
    def number(self, token):
        return str(token)

    def add(self, left, right):
        return f"{left} + {right}"

    def sub(self, left, right):
        return f"{left} - {right}"

    def mul(self, left, right):
        return f"{left} \\times {right}"

    def div(self, left, right):
        return f"\\frac{{{left}}}{{{right}}}"

    def pow(self, base, exponent):
        return f"{base}^{{{exponent}}}"

    def pos(self, value):
        return f"+{value}"

    def neg(self, value):
        return f"-{value}"

    def grouped(self, value):
        return f"\\left({value}\\right)"


parser = Lark(grammar, parser="lalr", transformer=ToLatex())


def exp_to_latex(expression: str) -> str:
    """
    Convert a valid arithmetic expression into LaTeX.

    Supports:
    +, -, *, /, ^, parentheses, negative numbers, decimals.

    Example:
    arithmetic_to_latex("(2+3)*4")
    -> "\\left(2 + 3\\right) \\cdot 4"
    """
    try:
        return parser.parse(expression)
    except UnexpectedInput as e:
        raise ValueError(f"Invalid arithmetic expression: {expression}") from e

