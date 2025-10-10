import os
import subprocess

# ------------------------------
# ARCHIVO DE PRUEBAS PARA PARSER PHP
# ------------------------------
# Ejecuta cada fragmento de código PHP en tu parser y verifica si el resultado
# coincide con lo esperado. Diseñado para minic_parserphp.py
# ------------------------------

parser_command = ["python", "minic_parserphp.py"]

tests = [
    # ----- ESTRUCTURAS CORRECTAS -----
    {
        "name": "if correcto",
        "code": "<?php\nif (true) { echo 'ok'; }\n?>",
        "expect_error": False
    },
    {
        "name": "for correcto",
        "code": "<?php\nfor ($i=0; $i<3; $i++) { echo $i; }\n?>",
        "expect_error": False
    },
    {
        "name": "while correcto",
        "code": "<?php\n$x=0;\nwhile ($x<3) { $x++; }\n?>",
        "expect_error": False
    },
    {
        "name": "función correcta",
        "code": "<?php\nfunction sumar($a,$b){return $a+$b;}\n?>",
        "expect_error": False
    },
    {
        "name": "concatenación",
        "code": "<?php\n$nombre='Laura';echo 'Hola '.$nombre;\n?>",
        "expect_error": False
    },
    # ----- ERRORES CONTROLADOS -----
    {
        "name": "if sin paréntesis de cierre",
        "code": "<?php\nif (true {\n?>",
        "expect_error": True
    },
    {
        "name": "for sin cierre",
        "code": "<?php\nfor ($i=0; $i<3; $i++ {\n?>",
        "expect_error": True
    },
    {
        "name": "while sin cierre",
        "code": "<?php\nwhile ($x<3 {\n?>",
        "expect_error": True
    },
    {
        "name": "función sin llaves",
        "code": "<?php\nfunction sumar($a,$b)\n?>",
        "expect_error": True
    },
    {
        "name": "función sin paréntesis",
        "code": "<?php\nfunction sumar $a,$b) {return $a+$b;}\n?>",
        "expect_error": True
    },
    {
        "name": "función sin nombre",
        "code": "<?php\nfunction ($a,$b) {return $a+$b;}\n?>",
        "expect_error": True
    },
    {
        "name": "bloque if no cerrado",
        "code": "<?php\nif (true) {\n?>",
        "expect_error": True
    },
    {
        "name": "doble cierre PHP",
        "code": "<?php\necho 'Hola';?><?php\necho 'Mundo';?>",
        "expect_error": False
    },
    {
        "name": "llave sin apertura",
        "code": "<?php\n}\n?>",
        "expect_error": True
    },
    {
        "name": "paréntesis sin cierre",
        "code": "<?php\n$x = (5 + 3;\n?>",
        "expect_error": True
    },
    {
        "name": "incremento y decremento",
        "code": "<?php\n$i=0;$i++;--$i;\n?>",
        "expect_error": False
    },
    {
        "name": "bloques anidados correctos",
        "code": "<?php\nif (true){while($x<3){$x++;}}\n?>",
        "expect_error": False
    },
    {
        "name": "bloque incompleto",
        "code": "<?php\nif (true){while($x<3){$x++;}\n?>",
        "expect_error": True
    },
    {
        "name": "expresiones válidas",
        "code": "<?php\n$x=5+3*(2-1);$y=$x/2;\n?>",
        "expect_error": False
    },
    {
        "name": "expresión inválida",
        "code": "<?php\n$x=5+*3;\n?>",
        "expect_error": True
    }
]

def run_test(name, code, expect_error):
    # Guardar código en archivo temporal
    tmp_file = "tmp_test.php"
    with open(tmp_file, "w", encoding="utf-8") as f:
        f.write(code)

    # Ejecutar parser
    result = subprocess.run(parser_command + [tmp_file], capture_output=True, text=True)
    output = result.stdout.strip()

    has_error = "❌" in output

    if expect_error and has_error:
        print(f"✔ {name} → error detectado correctamente")
    elif not expect_error and not has_error:
        print(f"✔ {name} → código válido reconocido correctamente")
    else:
        print(f"✘ {name} → resultado inesperado")
        print(f"--- Salida ---\n{output}\n")

    os.remove(tmp_file)


if __name__ == "__main__":
    print("\n🧪 INICIANDO PRUEBAS DEL PARSER PHP...\n")
    for t in tests:
        run_test(t["name"], t["code"], t["expect_error"])
    print("\n✅ Pruebas completadas.\n")
