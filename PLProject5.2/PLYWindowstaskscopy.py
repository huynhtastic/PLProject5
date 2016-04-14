""" This will parse the data from the windows command 'tasklist /FO'

"""
tokens = ('HEADER', 'EXE', 'SYSTEM')
literals = ["\"", ","]

# Tokens
t_HEADER = r'^(?i)\"Image.*$'
t_EXE = r'^\".*\.exe$'
# t_TASK   = r'^(?i).*\.exe$'
t_SYSTEM= r'^(?i)\".*System.*$'

# Ignored characters
t_ignore = " "

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex   # ply.lex comes from the ply folder in the PLY download.
lexer = lex.lex()

# Parsing rules

global time_step
time_step = 0

def p_start(t):
    '''start : header
             | exe
             | system
    '''

def p_header(t):
    'header : HEADER'
    print ('\nBegin analyzing memory usage on current host:\n')

def p_exe(t):
    'exe : EXE'
    print ('Saw', t[1])

def p_system(t):
    'system : SYSTEM'

# def p_empty(t):
#     'empty : '
#     pass

def p_error(t):
    if t == None:
        print("Syntax error at '%s'" % t)
    else:
        print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc   # ply.yacc comes from the ply folder in the PLY download.
parser = yacc.yacc()

while True:
    try:
        s = raw_input('')
    except EOFError:
        break
    parser.parse(s)

