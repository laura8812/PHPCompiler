<?php
// calculadora.php
// Calculadora básica para probar el parser PHP

function evaluar($expresion) {
    // Solo permitir números, operadores y paréntesis
    if (preg_match('/^[0-9+\-*/(). ]+$/', $expresion)) {
        // Evaluar la expresión usando eval
        eval("$resultado = $expresion;");
        return $resultado;
    } else {
        return "Expresión inválida";
    }
}

// Ejemplo de uso
$expresion = "3 + 5 * (2 - 1)";
echo "Expresión: $expresion\n";
echo "Resultado: " . evaluar($expresion) . "\n";
?>
