import ply.lex as lex
import sys

#Tokens list - Solo los esenciales
tokens = (
    "PHP_OPEN",
    "PHP_CLOSE",
    "IF",
    "ELSE",
    "FOREACH",
    "FOR",
    "WHILE",
    "AS",
    "FUNCTION",
    "RETURN",
    "ECHO",
    "PRINT",
    "ARRAY",
    "BOOLEAN",

    # Operadores y símbolos
    "INCREMENT",
    "DECREMENT",
    "SEMICOLON",
    "LBRACKET",
    "RBRACKET",
    "LBLOCK",
    "RBLOCK",
    "LPAREN",
    "RPAREN",
    "COMMA",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MODULE",
    "EQUAL",
    "LESSTHAN",
    "GREATERTHAN",
    "LESSEQUAL",
    "GREATERTHANEQUAL",
    "ISEQUAL",
    "NOTISEQUAL",
    "AND",
    "OR",
    "DOT",

    # Elementos básicos
    "VARIABLE",
    "STRING",
    "NUMBER",
    "ID",
)

# Símbolos simples
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_SEMICOLON = r';'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBLOCK = r'{'
t_RBLOCK = r'}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_MODULE = r'\%'
t_EQUAL = r'='
t_LESSTHAN = r'<'
t_GREATERTHAN = r'>'
t_LESSEQUAL = r'<='
t_GREATERTHANEQUAL = r'>='
t_ISEQUAL = r'=='
t_NOTISEQUAL = r'!='
t_AND = r'&&'
t_OR = r'\|\|'
t_DOT = r'\.'

def t_STRING(t):
    r'("([^\\\n]|(\\.))*?"|\'([^\\\n]|(\\.))*?\')'
    return t

t_ignore = ' \t'

def t_PHP_OPEN(t):
    r'\<\?php'
    return t

def t_PHP_CLOSE(t):
    r'\?>'
    return t

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_FOREACH(t):
    r'foreach'
    return t

def t_FOR(t):
    r'for'
    return t

def t_WHILE(t): 
    r'while'
    return t

def t_AS(t):
    r'as'
    return t

def t_FUNCTION(t):
    r'function'
    return t

def t_RETURN(t):
    r'return'
    return t

def t_ECHO(t):
    r'echo'
    return t

def t_PRINT(t):
    r'print'
    return t

def t_ARRAY(t):
    r'array'
    return t

def t_VARIABLE(t):
    r'\$[a-zA-Z_][\w]*' 
    return t

# Regla para cualquier uso inválido de $ (incluye $ suelto, $ con espacio, $ con número, etc.)
def t_INVALID_VARIABLE(t):
    r'\$[^a-zA-Z_]\S*'
    print(f"Lexical error: Invalid variable usage '{t.value}' at line {t.lineno}")
    t.lexer.skip(len(t.value))

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comments(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

def t_comments_C99(t):
    r'//(.)*?\n'
    t.lexer.lineno += 1

def t_comments_hashtag(t):
    r'\#(.)*?\n'
    t.lexer.lineno += 1

def t_BOOLEAN(t):
    r'true|false'
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?((E|e)(\-)?\d+(\.\d+)?)?'
    return t

def t_ID(t):
     r'(_|[a-z]|[A-Z])(\w)*'
     return t

def t_error(t):
    print ("Lexical error: " + str(t.value[0]))
    t.lexer.skip(1)

def test(data, lexer):
	lexer.input(data)
	while True:
		tok = lexer.token()
		if not tok:
			break
		print (tok)

lexer = lex.lex()

if __name__ == '__main__':
	if (len(sys.argv) > 1):
		fin = sys.argv[1]
	else:
		fin = 'basic.php'
	f = open(fin, 'r')
	data = f.read()
	print (data)
	lexer.input(data)
	test(data, lexer)