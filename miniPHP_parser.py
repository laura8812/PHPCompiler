import ply.yacc as yacc
from miniPHP_lexer_v2 import tokens

parse_error_reported = False

precedence = (
    ('right', 'ELSE'),
    ('left', 'EQUAL'),
    ('left', 'OR', 'AND'),
    ('left', 'ISEQUAL', 'NOTISEQUAL', 'GREATERTHAN', 'LESSTHAN', 'GREATERTHANEQUAL', 'LESSEQUAL'),
    ('left', 'DOT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULE'),
    ('right', 'UMINUS', 'INCREMENT', 'DECREMENT'),
)

def p_program(p):
    '''program : segment_list'''
    p[0] = ('program', p[1])

def p_segment_list(p):
    '''segment_list : segment_list segment
                    | segment'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_segment(p):
    '''segment : PHP_OPEN statement_list PHP_CLOSE'''
    p[0] = ('segment', p[1:])

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : expression SEMICOLON
                 | if_statement
                 | for_statement
                 | while_statement
                 | foreach_statement
                 | function_declaration
                 | echo_statement
                 | print_statement
                 | block
                 | RETURN expression SEMICOLON'''
    if len(p) == 4 and p[1] == 'return':
        p[0] = ('return', p[2])
    else:
        p[0] = p[1]

def p_block(p):
    'block : LBLOCK statement_list RBLOCK'
    p[0] = ('block', p[2])

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN statement %prec ELSE
                    | IF LPAREN expression RPAREN statement ELSE statement'''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5], None)
    else:
        p[0] = ('if', p[3], p[5], p[7])

def p_for_statement(p):
    'for_statement : FOR LPAREN for_expr SEMICOLON for_expr SEMICOLON for_expr RPAREN statement'
    p[0] = ('for', p[3], p[5], p[7], p[9])
    
def p_for_expr(p):
    '''for_expr : expression
                | empty'''
    p[0] = p[1]

def p_while_statement(p):
    'while_statement : WHILE LPAREN expression RPAREN statement'
    p[0] = ('while', p[3], p[5])

def p_foreach_statement(p):
    'foreach_statement : FOREACH LPAREN expression AS VARIABLE RPAREN statement'
    p[0] = ('foreach', p[3], p[5], p[7])

def p_echo_statement(p):
    'echo_statement : ECHO expression SEMICOLON'
    p[0] = ('echo', p[2])

def p_print_statement(p):
    'print_statement : PRINT expression SEMICOLON'
    p[0] = ('print', p[2])

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

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
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

def p_expression_array(p):
    'expression : ARRAY LPAREN array_elements RPAREN'
    p[0] = ('array', p[3])

def p_expression_short_array(p):
    'expression : LBRACKET array_elements RBRACKET'
    p[0] = ('array', p[2])

def p_expression_empty_array(p):
    'expression : LBRACKET RBRACKET'
    p[0] = ('array', [])

def p_array_elements(p):
    '''array_elements : array_elements COMMA expression
                      | expression
                      | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_expression_array_access(p):
    'expression : VARIABLE LBRACKET expression RBRACKET'
    p[0] = ('array_access', p[1], p[3])

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = ('uminus', p[2])

def p_expression_postfix_update(p):
    '''expression : VARIABLE INCREMENT
                  | VARIABLE DECREMENT'''
    p[0] = ('postupdate', p[2], p[1])

def p_expression_prefix_update(p):
    '''expression : INCREMENT VARIABLE
                  | DECREMENT VARIABLE'''
    p[0] = ('preupdate', p[1], p[2])

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

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    global parse_error_reported
    if parse_error_reported:
        return

    parse_error_reported = True

    if not p:
        print("Error sintáctico: fin de archivo inesperado. Falta cerrar un bloque, paréntesis o llave.")
        return

    value = getattr(p, "value", "?")
    lineno = getattr(p, "lineno", "?")

    if value == "{":
        print(f"Error sintáctico en la línea {lineno}: falta cerrar paréntesis antes de '{{'.")
    elif value == "}":
        print(f"Error sintáctico en la línea {lineno}: llave '}}' sin apertura.")
    elif value == "(":
        print(f"Error sintáctico en la línea {lineno}: paréntesis sin cierre.")
    elif isinstance(value, str) and value.lower() == "function":
        print(f"Error sintáctico en la línea {lineno}: declaración de función incompleta o sin nombre.")
    elif value == "?>":
        print(f"Error sintáctico en la línea {lineno}: cierre de PHP prematuro.")
    elif value in ["+", "*", "&&", "||", "/", "*"]:
        print(f"Error sintáctico en la línea {lineno}: operador '{value}' mal ubicado.")
    else:
        print(f"Error sintáctico en la línea {lineno}: token inesperado '{value}'.")

    raise Exception("Error sintáctico")

parser = yacc.yacc()

if __name__ == '__main__':

    import sys

    if len(sys.argv) > 1:
        fin = sys.argv[1]
    else:
        fin = 'basic.php'  # Archivo por defecto

    with open(fin, 'r', encoding='utf-8') as f:
        data = f.read()

    parse_error_reported = False

    try:
        parser.parse(data, tracking=True)
        print("Amiguito, tengo el placer de informar que Tu parser reconocio correctamente todo el código PHP")
    except Exception as e:
        print("Error sintáctico:", str(e))