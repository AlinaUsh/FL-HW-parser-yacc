import ply.lex as lex

tokens = [
    'LITERAL',
    'CONJ',
    'DISJ',
    'DOT',
    'OPERATOR',
    'OPENBR',
    'CLOSEBR'
]

t_LITERAL = r'[a-zA-Z_][a-zA-Z_0-9]*'

t_OPERATOR = r'\:\-'

t_CONJ = r'\,'

t_DOT = r'\.'

t_DISJ = r'\;'

t_OPENBR = r'\('

t_CLOSEBR = r'\)'

t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


template = 'Illegal character {0} at line {1} in position {2}'


def t_error(t):
    t.lexer.skip(1)
    raise Exception("Syntax error\n" + template.format(t.value[0], t.lineno, t.lexpos))


lexer = lex.lex()
