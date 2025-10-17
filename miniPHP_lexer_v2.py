import ply.lex as lex
import sys

#Tokens list
tokens = (
    "PHP_OPEN",
    "PHP_CLOSE",
    "IF",
    "ELSE",
    "ELSEIF",
    "ENDIF",
    "SWITCH",
    "CASE",
    "BRAKE",
    "DEFAULT",
    "FOREACH",
    "AS",
    "FOR",
    "ENDFOR",
    "ENDFOREACH",
    "WHILE",
    "ENDWHILE",
    "DO",
    "FUNCTION",
    "RETURN",
    "GLOBAL",
    "STATIC",
    "TRY",
    "CATCH",
    "FINALLY",
    "THROW",
    "ECHO",
    "PRINT",
    "EMPTY",
    "ARRAY",
    "LIST",
    "BOOLEAN",

    "CLASS",
    "NAMESPACE",
    "USE",
    "PUBLIC",
    "PRIVATE",
    "PROTECTED",
    "EXTENDS",
    "IMPLEMENTS",
    "YIELD",
    "MATCH",
    "ENUM",
    "DIR_CONST",
    "FILE_CONST",
    "LINE_CONST",
    "FUNCTION_CONST",
    "METHOD_CONST",
    "NAMESPACE_CONST",

    "PLUSEQUAL",          # +=
    "MINUSEQUAL",         # -=
    "INCREMENT",          # ++
    "DECREMENT",          # --
    "ARROW",              # ->
    "DOUBLECOLON",        # ::
    "DOUBLEARROW",        # =>
    "SEMICOLON",          # ;
    "LBRACKET",           # [
    "RBRACKET",           # ]
    "LBLOCK",             # {
    "RBLOCK",             # }
    "LPAREN",             # (
    "RPAREN",             # )
    "COMMA",              # ,
    "PLUS",               # +
    "MINUS",              # -
    "TIMES",              # *
    "DIVIDE",             # /
    "MODULE",             # %
    "EQUAL",              # =
    "LESSTHAN",           # <
    "GREATERTHAN",        # >
    "LESSEQUAL",          # <=
    "GREATERTHANEQUAL",   # >=
    "ISEQUAL",            # ==
    "NOTISEQUAL",         # !=
    "AND",                # &&
    "OR",                 # ||
    "DOT",                # .

    "VARIABLE",
    "VARVAR",
    "STRING",
    "NUMBER",
    "ID",
)
def t_CLASS(t):
    r'class'
    return t

def t_NAMESPACE(t):
    r'namespace'
    return t

def t_USE(t):
    r'use'
    return t

def t_PUBLIC(t):
    r'public'
    return t

def t_PRIVATE(t):
    r'private'
    return t

def t_PROTECTED(t):
    r'protected'
    return t

def t_EXTENDS(t):
    r'extends'
    return t

def t_IMPLEMENTS(t):
    r'implements'
    return t

def t_YIELD(t):
    r'yield'
    return t

def t_MATCH(t):
    r'match'
    return t

def t_ENUM(t):
    r'enum'
    return t

def t_DIR_CONST(t):
    r'__DIR__'
    return t

def t_FILE_CONST(t):
    r'__FILE__'
    return t

def t_LINE_CONST(t):
    r'__LINE__'
    return t

def t_FUNCTION_CONST(t):
    r'__FUNCTION__'
    return t

def t_METHOD_CONST(t):
    r'__METHOD__'
    return t

def t_NAMESPACE_CONST(t):
    r'__NAMESPACE__'
    return t

t_PLUSEQUAL = r'\+='  # +=
t_MINUSEQUAL = r'-='   # -=
t_INCREMENT = r'\+\+' # ++
t_DECREMENT = r'--'    # --
t_ARROW = r'->'        # ->
t_DOUBLECOLON = r'::'  # ::
t_DOUBLEARROW = r'=>'  # =>

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

def t_ELSEIF(t):
    r'elseif'
    return t

def t_ENDIF(t):
    r'endif'
    return t

def t_FUNCTION(t):
    r'function'
    return t

def t_SWITCH(t):
    r'switch'
    return t

def t_CASE(t):
    r'case'
    return t

def t_VARIABLE(t):
    r'\$[a-zA-Z_][\w]*' 
    return t

def t_VARVAR(t):
    r'\${2}[a-zA-Z_][\w]*'
    return t

# Regla para cualquier uso inválido de $ (incluye $ suelto, $ con espacio, $ con número, etc.)
def t_INVALID_VARIABLE(t):
    r'\$[^a-zA-Z_]\S*'
    print(f"Lexical error: Invalid variable usage '{t.value}' at line {t.lineno}")
    t.lexer.skip(len(t.value))

def t_FOREACH(t):
    r'foreach'
    return t

def t_AS(t):
    r'as'
    return t

def t_ENDFOREACH(t):
    r'endforeach'
    return t

def t_WHILE(t): 
    r'while'
    return t

def t_ENDWHILE(t):
    r'endwhile'
    return t

def t_DO(t):
    r'do'
    return t

def t_RETURN(t):
    r'return'
    return t

def t_GLOBAL(t):
    r'global'
    return t

def t_STATIC(t):
    r'static'
    return t    

def t_TRY(t):
    r'try'
    return t

def t_CATCH(t):
    r'catch'
    return t

def t_FINALLY(t):
    r'finally'
    return t

def t_THROW(t):
    r'throw'
    return t

def t_ECHO(t):
    r'echo'
    return t

def t_PRINT(t):
    r'print'
    return t

def t_EMPTY(t):
    r'empty'
    return t

def t_ARRAY(t):
    r'array'
    return t

def t_LIST(t):
    r'list'
    return t

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