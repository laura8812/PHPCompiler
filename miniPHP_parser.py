import ply.yacc as yacc
from miniPHP_lexer_v2 import tokens
from miniPHP_semantic import analyze, print_semantic_errors, clear_semantic_data

# Lista para almacenar todos los errores encontrados
parse_errors = []

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
    '''segment : PHP_OPEN statement_list PHP_CLOSE
                | PHP_OPEN statement_list'''
    p[0] = ('segment', p[1:])

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement_list class_member
                      | statement
                      | class_member'''
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
                 | class_declaration
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
    '''function_declaration : FUNCTION ID LPAREN parameter_list RPAREN block
                            | visibility FUNCTION ID LPAREN parameter_list RPAREN block'''
    if len(p) == 7:
        p[0] = ('function', p[2], p[4], p[6], 'public')
    else:
        p[0] = ('function', p[3], p[5], p[7], p[1])

def p_visibility(p):
    '''visibility : PUBLIC
                 | PRIVATE
                 | PROTECTED'''
    p[0] = p[1].lower()

def p_class_declaration(p):
    '''class_declaration : CLASS ID LBLOCK class_member_list RBLOCK
                         | CLASS ID EXTENDS ID LBLOCK class_member_list RBLOCK'''
    if len(p) == 6:
        p[0] = ('class', p[2], None, p[4])
    else:
        p[0] = ('class', p[2], p[4], p[6])

def p_class_member_list(p):
    '''class_member_list : class_member_list class_member
                         | class_member
                         | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_class_member(p):
    '''class_member : visibility VARIABLE SEMICOLON
                    | visibility FUNCTION ID LPAREN parameter_list RPAREN block
                    | FUNCTION ID LPAREN parameter_list RPAREN block
                    | VARIABLE SEMICOLON'''
    if len(p) == 4:
        # Puede ser visibility VARIABLE SEMICOLON o VARIABLE SEMICOLON (sin visibilidad)
        if isinstance(p[1], str) and p[1] in ['public', 'private', 'protected']:
            p[0] = ('property', p[2], p[1])
        else:
            # VARIABLE SEMICOLON sin visibilidad
            p[0] = ('property', p[1], 'public')
    elif len(p) == 8:
        p[0] = ('method', p[3], p[5], p[7], p[1])
    elif len(p) == 7:
        p[0] = ('method', p[2], p[4], p[6], 'public')
    else:
        p[0] = ('method', p[2], p[4], p[6], 'public')

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

def p_expression_method_call(p):
    '''expression : expression ARROW ID LPAREN argument_list RPAREN
                  | expression ARROW VARIABLE LPAREN argument_list RPAREN'''
    method_name = p[3]
    if isinstance(method_name, str) and method_name.startswith('$'):
        method_name = method_name[1:]  # Remover $ si es variable
    p[0] = ('method_call', p[1], method_name, p[5])

def p_expression_new(p):
    'expression : NEW ID LPAREN argument_list RPAREN'
    p[0] = ('new', p[2], p[4])

def p_expression_property_access(p):
    '''expression : expression ARROW ID
                  | expression ARROW VARIABLE'''
    p[0] = ('property_access', p[1], p[3])

def p_expression_this(p):
    'expression : THIS'
    p[0] = ('this',)

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
    global parse_errors
    
    if not p:
        error_msg = "Error sintáctico: fin de archivo inesperado. Falta cerrar un bloque, paréntesis o llave."
        parse_errors.append(("EOF", error_msg))
        return

    value = getattr(p, "value", "?")
    lineno = getattr(p, "lineno", "?")
    error_type = "SINTAXIS"
    error_msg = ""

    if value == "{":
        error_msg = f"Error sintáctico en la línea {lineno}: falta cerrar paréntesis antes de '{{'."
    elif value == "}":
        error_msg = f"Error sintáctico en la línea {lineno}: llave '}}' sin apertura."
    elif value == "(":
        error_msg = f"Error sintáctico en la línea {lineno}: paréntesis sin cierre."
    elif isinstance(value, str) and value.lower() == "function":
        error_msg = f"Error sintáctico en la línea {lineno}: declaración de función incompleta o sin nombre."
    elif value == "?>":
        error_msg = f"Error sintáctico en la línea {lineno}: cierre de PHP prematuro."
    elif value in ["+", "*", "&&", "||", "/", "-"]:
        error_msg = f"Error sintáctico en la línea {lineno}: operador '{value}' mal ubicado."
    elif value == ";":
        error_msg = f"Error sintáctico en la línea {lineno}: punto y coma inesperado."
    elif value == ")":
        error_msg = f"Error sintáctico en la línea {lineno}: paréntesis de cierre sin apertura."
    else:
        error_msg = f"Error sintáctico en la línea {lineno}: token inesperado '{value}'."

    parse_errors.append((error_type, error_msg, lineno, value))
    
    # Continuar el parsing para encontrar más errores
    # Intentar recuperación: saltar el token problemático
    parser.errok()

parser = yacc.yacc()

def get_parse_errors():
    """Retorna la lista de errores encontrados durante el parsing"""
    return parse_errors

def clear_parse_errors():
    """Limpia la lista de errores"""
    global parse_errors
    parse_errors = []

def print_parse_errors():
    """Imprime todos los errores encontrados de forma organizada"""
    global parse_errors
    if not parse_errors:
        return
    
    print("\n" + "="*60)
    print(f"REPORTE DE ERRORES SINTÁCTICOS ({len(parse_errors)} error(es) encontrado(s))")
    print("="*60)
    
    for i, error in enumerate(parse_errors, 1):
        if len(error) == 4:
            error_type, error_msg, lineno, value = error
            print(f"\n[{i}] Línea {lineno}: {error_msg}")
            print(f"    Token: '{value}' | Tipo: {error_type}")
        elif len(error) == 2:
            error_type, error_msg = error
            print(f"\n[{i}] {error_msg}")
            print(f"    Tipo: {error_type}")
        else:
            print(f"\n[{i}] {error}")
    
    print("\n" + "="*60)
    print(f"Total de errores: {len(parse_errors)}")
    print("="*60 + "\n")

if __name__ == '__main__':

    import sys

    if len(sys.argv) > 1:
        fin = sys.argv[1]
    else:
        fin = 'basic.php'  # Archivo por defecto

    with open(fin, 'r', encoding='utf-8') as f:
        data = f.read()

    clear_parse_errors()

    try:
        result = parser.parse(data, tracking=True)
        if parse_errors:
            print_parse_errors()
            sys.exit(1)
        else:
            print("Parser: El código PHP fue reconocido correctamente sin errores sintácticos.")
            print(f"Árbol de sintaxis generado exitosamente.")
            clear_semantic_data()
            analyze(result)
            print_semantic_errors()
    except Exception as e:
        if parse_errors:
            print_parse_errors()
        print(f"\nError durante el parsing: {str(e)}")
        sys.exit(1)