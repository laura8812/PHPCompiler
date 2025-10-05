import ply.lex as lex

# ==================================================
# LISTA DE TOKENS
# ==================================================
tokens = [
    # Tipos de datos y valores
    'NUMBER', 'STRING', 'BOOLEAN',

    # Identificadores y variables
    'VARIABLE', 'ID',

    # Operadores aritméticos y lógicos
    'PLUS', 'MINUS', 'TIMES', 'MODULE',
    'EQUAL',
    'ISEQUAL', 'NOTISEQUAL',
    'LESSTHAN', 'GREATERTHAN', 'LESSEQUAL', 'GREATERTHANEQUAL',
    'AND', 'OR',

    # Incrementos / Decrementos
    'INCREMENT', 'DECREMENT',

    # Concatenación
    'DOT',

    # Delimitadores
    'LPAREN', 'RPAREN',
    'LBLOCK', 'RBLOCK',
    'SEMICOLON', 'COMMA',

    # Apertura y cierre de PHP
    'PHP_OPEN', 'PHP_CLOSE',

    # Palabras clave
    'IF', 'ELSE', 'FOR', 'WHILE',
    'FUNCTION', 'RETURN',
    'ECHO', 'PRINT'
]

# ==================================================
# PALABRAS RESERVADAS
# ==================================================
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'echo': 'ECHO',
    'print': 'PRINT',
    'true': 'BOOLEAN',
    'false': 'BOOLEAN'
}

# ==================================================
# REGLAS DE TOKENS
# ==================================================

# Operadores
t_PLUS              = r'\+'
t_MINUS             = r'-'
t_TIMES             = r'\*'
t_MODULE            = r'%'
t_EQUAL             = r'='
t_ISEQUAL           = r'=='
t_NOTISEQUAL        = r'!='
t_LESSTHAN          = r'<'
t_GREATERTHAN       = r'>'
t_LESSEQUAL         = r'<='
t_GREATERTHANEQUAL  = r'>='
t_AND               = r'&&'
t_OR                = r'\|\|'
t_INCREMENT         = r'\+\+'
t_DECREMENT         = r'--'
t_DOT               = r'\.'  # 👈 operador de concatenación en PHP

# Delimitadores
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBLOCK    = r'\{'
t_RBLOCK    = r'\}'
t_SEMICOLON = r';'
t_COMMA     = r','

# Apertura y cierre PHP
t_PHP_OPEN  = r'<\?php'
t_PHP_CLOSE = r'\?>'

# ==================================================
# TOKENS CON FUNCIONES
# ==================================================

# Variables PHP ($variable)
def t_VARIABLE(t):
    r'\$[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Identificadores (funciones, nombres sin $)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Números
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Cadenas de texto
def t_STRING(t):
    r'(\"([^\\\"]|\\.)*\")|(\'([^\\\']|\\.)*\')'
    t.value = t.value[1:-1]
    return t

# Comentarios (se ignoran)
def t_COMMENT(t):
    r'(\#.*|//.*|/\*(.|\n)*?\*/)'
    pass

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Contador de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores léxicos
def t_error(t):
    print(f"❌ Caracter ilegal '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

# ==================================================
# CONSTRUCCIÓN DEL LÉXICO
# ==================================================
lexer = lex.lex()
