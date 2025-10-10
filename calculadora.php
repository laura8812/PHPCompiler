<?php

function evaluar($expresion) {
 
    if (preg_match('/^[0-9+\-*/(). ]+$/', $expresion)) {
      
        eval("$resultado = $expresion;");
        return $resultado;
    } else {
        return "Expresión inválida";
    }
}

$expresion = "3 + 5 * (2 - 1)";
echo "Expresión: $expresion\n";
echo "Resultado: " . evaluar($expresion) . "\n";
?>
