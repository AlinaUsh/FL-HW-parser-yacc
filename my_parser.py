import ply.yacc as yacc
import sys
from my_lex import tokens

'''
prog       -> prog_line | prog_line prog
prog_line  -> rel .
rel        -> atom :- disj | atom
disj       -> conj ; disj | conj
conj       -> expr , conj | expr
expr       -> atom | ( disj )
atom       -> lit | lit tail
tail       -> atom | inner_atom | inner_atom tail
inner_atom -> ( atom ) | ( inner_atom )
'''


def p_prog(p):
    '''prog : prog_line prog
            | prog_line'''
    # print("p_prog")
    if len(p) == 3:
        p[0] = p[1] + "\n" + p[2]
    if len(p) == 2:
        p[0] = p[1]


def p_check_dot(p):
    'prog_line : rel DOT'
    # print("p_check_dot")
    p[0] = p[1] + ".\n"


def p_rel(p):
    '''rel : atom
           | atom OPERATOR disj'''
    # print("p_rel")
    if len(p) == 2:
        p[0] = p[1]
    if len(p) == 4:
        p[0] = ":- " + " ( " + p[1] + " ) ( " + p[3] + " )"


def p_disj(p):
    '''disj : conj DISJ disj
            | conj'''
    # print("p_disj")
    if len(p) == 2:
        p[0] = p[1]
    if len(p) == 4:
        p[0] = "; " + "( " + p[1] + " ) ( " + p[3] + " )"


def p_conj(p):
    '''conj : expr CONJ conj
            | expr'''
    # print("p_conj")
    if len(p) == 2:
        p[0] = p[1]
    if len(p) == 4:
        p[0] = ", " + " ( " + p[1] + " ) ( " + p[3] + " )"


def p_expr(p):
    '''expr : atom
            | OPENBR disj CLOSEBR'''
    # print("p_expr")
    if len(p) == 2:
        p[0] = p[1]
    if len(p) == 4:
        p[0] = "( " + p[2] + " )"


def p_atom(p):
    '''atom : LITERAL
            | LITERAL tail'''
    # print("p_atom")
    if len(p) == 2:
        p[0] = " ( " + p[1] + " ) "
    if len(p) == 3:
        p[0] = p[1] + " " + p[2]


def p_tail_atom(p):
    '''tail : atom'''
    # print("p_tail_atom")
    p[0] = " ( " + p[1] + " ) "


def p_tail_inner_atom(p):
    '''tail : inner_atom'''
    # print("p_tail_inner_atom")
    p[0] = " ( " + p[1] + " ) "


def p_tail_inner_atom_tail(p):
    '''tail : inner_atom tail'''
    # print("p_tail_inner_atom_tail")
    p[0] = " ( " + p[1] + p[2] + " ) "


def p_inner_atom_atom(p):
    '''inner_atom : OPENBR atom CLOSEBR'''
    # print("p_inner_atom_atom")
    p[0] = "( " + p[2] + " )"


def p_inner_atom_inner_atom(p):
    '''inner_atom : OPENBR inner_atom CLOSEBR'''
    # print("p_inner_atom_inner_atom")
    p[0] = "( " + p[2] + " )"


def p_error(p):
    raise Exception(syntax_error_str)


lex_error_str = "Failed to lex"
parse_error_str = "Failed to parse"
open_file_error_str = "Failed to open {0}"
syntax_error_str = "Syntax error"


if __name__ == "__main__":
    input_file_name = sys.argv[1]
    try:
        input = open(input_file_name)
    except Exception:
        print(open_file_error_str.format(input_file_name))
        sys.exit(0)
    output_file_name = input_file_name + ".out"
    output_file = open(output_file_name, "w")
    try:
        parser = yacc.yacc()
        output_file.write(parser.parse(input.read()))
    except Exception as err:
        output_file.write(str(err))
    input.close()
    output_file.close()
