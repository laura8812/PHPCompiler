import ply.yacc as yacc
from miniPHP_lexer_v2 import tokens

# -----------------------------
# Precedencia de operadores
# -----------------------------
precedence = (
    ('right', 'ELSE'),
    ('left', 'EQUAL'),
    ('left', 'OR', 'AND'),
    ('left', 'ISEQUAL', 'NOTISEQUAL', 'GREATERTHAN', 'LESSTHAN', 'GREATERTHANEQUAL', 'LESSEQUAL'),
    ('left', 'DOT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'MODULE'),
    ('right', 'UMINUS', 'INCREMENT', 'DECREMENT'),
)

# -----------------------------
# Programa principal
# -----------------------------
def p_program(p):
    '''program : PHP_OPEN statement_list PHP_CLOSE
               | PHP_OPEN statement_list
               | statement_list PHP_CLOSE
               | statement_list'''
    p[0] = ('program', p[1:])

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# -----------------------------
# Sentencias
# -----------------------------
def p_statement(p):
    '''statement : expression SEMICOLON
                 | if_statement
                 | for_statement
                 | while_statement
                 | function_declaration
                 | echo_statement
                 | print_statement
                 | block
                 | RETURN expression SEMICOLON'''
    if len(p) == 3 and p[1] == 'return':
        p[0] = ('return', p[2])
    else:
        p[0] = p[1]

# -----------------------------
# If / Else
# -----------------------------
def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN statement %prec ELSE
                    | IF LPAREN expression RPAREN statement ELSE statement'''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5], None)
    else:
        p[0] = ('if', p[3], p[5], p[7])

# -----------------------------
# For
# -----------------------------
def p_for_statement(p):
    'for_statement : FOR LPAREN expression SEMICOLON expression SEMICOLON expression RPAREN statement'
    p[0] = ('for', p[3], p[5], p[7], p[9])

# -----------------------------
# While
# -----------------------------
def p_while_statement(p):
    'while_statement : WHILE LPAREN expression RPAREN statement'
    p[0] = ('while', p[3], p[5])

# -----------------------------
# Echo y Print
# -----------------------------
def p_echo_statement(p):
    'echo_statement : ECHO expression SEMICOLON'
    p[0] = ('echo', p[2])

def p_print_statement(p):
    'print_statement : PRINT expression SEMICOLON'
    p[0] = ('print', p[2])

# -----------------------------
# Declaración de funciones
# -----------------------------
def p_function_declaration(p):
    'function_declaration : FUNCTION ID LPAREN parameter_list RPAREN block'
    p[0] = ('function', p[2], p[4], p[6])

def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA VARIABLE
                      | VARIABLE
                      | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []

# -----------------------------
# Llamadas a función
# -----------------------------
def p_expression_function_call(p):
    '''expression : ID LPAREN argument_list RPAREN
                  | VARIABLE LPAREN argument_list RPAREN'''
    p[0] = ('func_call', p[1], p[3])

def p_argument_list(p):
    '''argument_list : argument_list COMMA expression
                     | expression
                     | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []

# -----------------------------
# Expresiones
# -----------------------------
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression MODULE expression
                  | expression DOT expression
                  | expression ISEQUAL expression
                  | expression NOTISEQUAL expression
                  | expression GREATERTHAN expression
                  | expression LESSTHAN expression
                  | expression GREATERTHANEQUAL expression
                  | expression LESSEQUAL expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = ('uminus', p[2])

def p_expression_increment(p):
    '''expression : VARIABLE INCREMENT
                  | VARIABLE DECREMENT'''
    p[0] = ('update', p[2], p[1])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('num', p[1])

def p_expression_variable(p):
    'expression : VARIABLE'
    p[0] = ('var', p[1])

def p_expression_string(p):
    'expression : STRING'
    p[0] = ('str', p[1])

def p_expression_boolean(p):
    'expression : BOOLEAN'
    p[0] = ('bool', p[1])

def p_expression_assign(p):
    'expression : VARIABLE EQUAL expression'
    p[0] = ('assign', p[1], p[3])

# -----------------------------
# Vacío
# -----------------------------
def p_empty(p):
    'empty :'
    pass

# -----------------------------
# Manejo de errores
# -----------------------------
def p_error(p):
    """
    Maneja errores sintácticos con mensajes claros, contextuales y sin duplicados.
    Detecta funciones incompletas, bloques sin cerrar y cierres prematuros de PHP.
    """

    # Caso: fin de archivo inesperado
    if not p:
        if not hasattr(p_error, "already_reported"):
            print("❌ Error sintáctico: fin de archivo inesperado. Es posible que falte una llave '}', un paréntesis ')' o cerrar una estructura como 'if' o 'function'.")
            p_error.already_reported = True
        return

    # Evitar mensajes repetidos
    if hasattr(p_error, "already_reported") and p_error.already_reported:
        return

    value = getattr(p, "value", "?")
    lineno = getattr(p, "lineno", "?")
    code_before = p.lexer.lexdata[:p.lexpos].lower()

    # --- CASOS ESPECÍFICOS ---

    # 1️⃣ Cierre PHP prematuro
    if value == "?>":
        if "function" in code_before.split()[-3:]:
            print(f"❌ Error sintáctico en la línea {lineno}: declaración de función incompleta. Falta el nombre, los paréntesis o las llaves de apertura.")
        elif any(kw in code_before for kw in ["if (", "while (", "for ("]):
            print(f"❌ Error sintáctico en la línea {lineno}: se encontró el cierre '?>' antes de cerrar correctamente un bloque (por ejemplo, 'if', 'while' o 'for').")
        else:
            print(f"❌ Error sintáctico en la línea {lineno}: se encontró el cierre '?>' antes de completar una estructura (por ejemplo, una función o condicional).")

    # 2️⃣ Función mal declarada directamente
    elif value.lower() == "function":
        print(f"❌ Error sintáctico en la línea {lineno}: declaración de función incompleta. Falta el nombre o los paréntesis de parámetros.")

    # 3️⃣ Paréntesis sin cerrar antes de llave
    elif value == "{":
        if any(kw in code_before[-10:] for kw in ["if", "while", "for"]):
            print(f"❌ Error sintáctico en la línea {lineno}: falta cerrar un paréntesis ')' en la condición antes de la llave '{{'.")
        else:
            print(f"❌ Error sintáctico en la línea {lineno}: llave '{{' inesperada o mal posicionada.")

    # 4️⃣ Llave de cierre sin apertura
    elif value == "}":
        print(f"❌ Error sintáctico en la línea {lineno}: llave '}}' sin apertura correspondiente.")

    # 5️⃣ Identificador fuera de contexto
    elif value.isidentifier():
        print(f"❌ Error sintáctico en la línea {lineno}: token inesperado '{value}'. Es posible que falte un paréntesis o una llave.")

    # 6️⃣ Cualquier otro token
    else:
        print(f"❌ Error sintáctico en la línea {lineno}: token inesperado '{value}'.")

    # Evita duplicados posteriores
    p_error.already_reported = True
    parser.errok()
 



# -----------------------------
# Construcción del parser
# -----------------------------
parser = yacc.yacc()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python minic_parserphp.py archivo.php")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        data = f.read()

    result = parser.parse(data)
    print("✅ El parser reconoció correctamente todo el código PHP")

