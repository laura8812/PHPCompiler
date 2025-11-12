semantic_errors = []
symbol_table = {
    "global": {}
}
current_scope = "global"


# ---------------------- UTILIDADES ----------------------
def enter_scope(name):
    """Crea un nuevo ámbito (función o clase)."""
    global current_scope
    symbol_table[name] = {}
    current_scope = name


def exit_scope():
    """Regresa al ámbito global."""
    global current_scope
    current_scope = "global"


def declare_variable(name, var_type):
    """Declara una variable en el ámbito actual."""
    if name in symbol_table[current_scope]:
        semantic_errors.append(
            f"Variable {name} ya declarada en el ámbito '{current_scope}'."
        )
    else:
        symbol_table[current_scope][name] = var_type


def get_variable_type(name):
    """Obtiene el tipo de una variable, buscando en el ámbito actual y global."""
    if name in symbol_table[current_scope]:
        return symbol_table[current_scope][name]
    elif name in symbol_table["global"]:
        return symbol_table["global"][name]
    else:
        semantic_errors.append(f"Variable {name} usada sin declarar.")
        return "undef"


# ---------------------- ANALIZADOR ----------------------
def analyze(node):
    """Analiza recursivamente un nodo del AST."""
    if node is None:
        return None

    # Si es lista de sentencias
    if isinstance(node, list):
        for stmt in node:
            analyze(stmt)
        return

    # Cada nodo del parser es una tupla
    node_type = node[0]

    # ---------------------- PROGRAMA ----------------------
    if node_type == "program":
        analyze(node[1])

    elif node_type == "segment":
        # segment = ('segment', ['<?php', statement_list, '?>'])
        for part in node[1]:
            analyze(part)

    # ---------------------- ASIGNACIÓN ----------------------
    elif node_type == "assign":
        var_name = node[1]
        expr = node[2]
        expr_type = analyze(expr)
        declare_variable(var_name, expr_type)
        return expr_type

    # ---------------------- VARIABLE ----------------------
    elif node_type == "var":
        return get_variable_type(node[1])

    # ---------------------- LITERALES ----------------------
    elif node_type == "num":
        return "int"
    elif node_type == "str":
        return "string"
    elif node_type == "bool":
        return "bool"

    # ---------------------- OPERACIONES ----------------------
    elif node_type == "binop":
        op, left, right = node[1], node[2], node[3]
        left_type = analyze(left)
        right_type = analyze(right)

        if left_type == "undef" or right_type == "undef":
            return "undef"

        # Concatenación con '.'
        if op == ".":
            return "string"

        # Operadores aritméticos
        if op in ["+", "-", "*", "/", "%"]:
            if left_type != "int" or right_type != "int":
                semantic_errors.append(
                    f"Operación '{op}' inválida entre {left_type} y {right_type}."
                )
                return "undef"
            return "int"

        # Comparaciones lógicas
        if op in ["==", "!=", ">", "<", ">=", "<="]:
            if left_type != right_type:
                semantic_errors.append(
                    f"Comparación inválida entre {left_type} y {right_type}."
                )
            return "bool"

        # Lógicos (AND / OR)
        if op in ["and", "or", "&&", "||"]:
            if left_type != "bool" or right_type != "bool":
                semantic_errors.append(
                    f"Operador lógico '{op}' requiere valores booleanos."
                )
            return "bool"

    # ---------------------- IF ----------------------
    elif node_type == "if":
        condition = node[1]
        then_block = node[2]
        else_block = node[3]

        cond_type = analyze(condition)
        if cond_type not in ["bool", "int"]:
            semantic_errors.append("Condición del 'if' no es booleana o entera.")

        analyze(then_block)
        if else_block:
            analyze(else_block)

    # ---------------------- FUNCIONES ----------------------
    elif node_type == "function":
        func_name = node[1]
        params = node[2]
        body = node[3]
        visibility = node[4]

        if func_name in symbol_table["global"]:
            semantic_errors.append(f"Función '{func_name}' redeclarada.")
            return "undef"

        symbol_table["global"][func_name] = "function"

        # Nuevo ámbito para la función
        enter_scope(func_name)
        for param in params:
            declare_variable(param, "param")

        analyze(body)
        exit_scope()
        return "function"

    # ---------------------- LLAMADAS ----------------------
    elif node_type == "func_call":
        func_name = node[1]
        args = node[2]
        if func_name not in symbol_table["global"]:
            semantic_errors.append(f"Llamada a función no declarada: '{func_name}'.")
        for arg in args:
            analyze(arg)
        return "undef"

    elif node_type == "method_call":
        obj = analyze(node[1])
        method_name = node[2]
        args = node[3]
        # En este analizador básico, no se resuelve el tipo del objeto
        for arg in args:
            analyze(arg)
        return "undef"

    # ---------------------- CLASES ----------------------
    elif node_type == "class":
        class_name = node[1]
        base_class = node[2]
        members = node[3]

        if class_name in symbol_table["global"]:
            semantic_errors.append(f"Clase '{class_name}' redeclarada.")
        else:
            symbol_table["global"][class_name] = "class"

        enter_scope(class_name)
        analyze(members)
        exit_scope()

    # ---------------------- BLOQUES ----------------------
    elif node_type == "block":
        analyze(node[1])

    # ---------------------- ECHO / PRINT ----------------------
    elif node_type in ["echo", "print"]:
        expr = node[1]
        analyze(expr)

    # ---------------------- FOREACH / WHILE / FOR ----------------------
    elif node_type == "foreach":
        iterable = node[1]
        var = node[2]
        body = node[3]
        analyze(iterable)
        declare_variable(var, "var")
        analyze(body)

    elif node_type == "while":
        cond = node[1]
        body = node[2]
        cond_type = analyze(cond)
        if cond_type not in ["bool", "int"]:
            semantic_errors.append("Condición del 'while' no es válida.")
        analyze(body)

    elif node_type == "for":
        init = node[1]
        cond = node[2]
        step = node[3]
        body = node[4]
        analyze(init)
        cond_type = analyze(cond)
        if cond_type not in ["bool", "int"]:
            semantic_errors.append("Condición del 'for' no es válida.")
        analyze(step)
        analyze(body)

    return None


# ---------------------- REPORTE ----------------------
def print_semantic_errors():
    if not semantic_errors:
        print("✓ Análisis semántico: sin errores encontrados.")
    else:
        print("\n ERRORES SEMÁNTICOS:")
        for i, err in enumerate(semantic_errors, 1):
            print(f" [{i}] {err}")
        print(f"\nTotal: {len(semantic_errors)} error(es).")


def clear_semantic_data():
    """Limpia errores y tabla de símbolos (para nueva ejecución)."""
    global semantic_errors, symbol_table, current_scope
    semantic_errors = []
    symbol_table = {"global": {}}
    current_scope = "global"