""" This will parse the data from the windows command 'tasklist /FO csv > "file_path here"'

"""
tokens = ('HEADER', 'EXE', 'SYSTEM', 'Q', 'BETWEEN', 'INTEGER', 'K', 'COMMA', 'SESSION')
literals = [","]

# Tokens
t_HEADER = r'^(?i)\"Image.*$'
t_EXE = r'([a-zA-Z\_0-9]+\.exe)'
t_Q = r'\"'
t_BETWEEN = r'\",\"'
t_K = r'K'
t_COMMA = r','
t_SYSTEM = r'(?i)System[a-zA-Z\s]*'
t_SESSION = r'(Services)|(Console)'

def t_INTEGER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \r"

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
             | exenc
             | system
             | systemnc
    '''

def p_header(t):
    'header : HEADER'
    print ('\nBegin analyzing memory usage on current host:\n')

def p_exe(t):
    'exe : Q EXE BETWEEN INTEGER BETWEEN SESSION BETWEEN INTEGER BETWEEN INTEGER COMMA INTEGER K Q'
    print "Image name, " + str(t[2]) + ", is currently taking up " + str(t[10])+ str(t[11]) + str(t[12]) + str(t[13]) + " worth of memory."

def p_exenc(t):
    'exenc : Q EXE BETWEEN INTEGER BETWEEN SESSION BETWEEN INTEGER BETWEEN INTEGER K Q'
    print "Image name, " + str(t[2]) + ", is currently taking up " + str(t[10])+ str(t[11]) + " worth of memory."

def p_system(t):
    'system : Q SYSTEM BETWEEN INTEGER BETWEEN SESSION BETWEEN INTEGER BETWEEN INTEGER COMMA INTEGER K Q'
    print "Image name, " + str(t[2]) + ", is currently taking up " + str(t[10])+ str(t[11]) + str(t[12]) + str(t[13]) + " worth of memory."

def p_systemnc(t):
    'systemnc : Q SYSTEM BETWEEN INTEGER BETWEEN SESSION BETWEEN INTEGER BETWEEN INTEGER K Q'
    print "Image name, " + str(t[2]) + ", is currently taking up " + str(t[10])+ str(t[11]) + " worth of memory."

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

