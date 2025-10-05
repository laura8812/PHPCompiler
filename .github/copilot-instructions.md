# Guía para agentes de IA en este repositorio

Este documento proporciona instrucciones específicas para agentes de IA que colaboran en el desarrollo de este proyecto. Aquí se resumen los patrones, convenciones y flujos de trabajo clave detectados en el código base.

## Arquitectura general
- El proyecto contiene ejemplos de analizadores léxicos y sintácticos para lenguajes de programación simples (miniPHP y minic).
- Los componentes principales están en Python (`miniPHP_lexer.py`, `miniPHP_lexer_v2.py`, `Ejemplo/minic_lexer.py`, `Ejemplo/minic_parser.py`) y C (`Ejemplo/evaluacion.c`).
- El flujo típico es: el archivo léxico procesa el código fuente y genera tokens, que luego son procesados por el parser.

## Estructura y convenciones
- Los analizadores léxicos (`*_lexer.py`) definen tokens y reglas usando la librería `ply` (Python Lex-Yacc).
- Los analizadores sintácticos (`*_parser.py`) definen la gramática y acciones semánticas, también usando `ply`.
- Los archivos generados por `ply` (`parsetab.py`, `parser.out`) se deben ignorar en cambios manuales.
- El código C (`evaluacion.c`) parece ser un ejemplo independiente y no está integrado directamente con los analizadores Python.

## Flujos de trabajo
- Para probar los analizadores, ejecuta los scripts Python directamente:
  ```bash
  python Ejemplo/minic_lexer.py
  python Ejemplo/minic_parser.py
  python miniPHP_lexer.py
  ```
- No hay scripts de build ni tests automatizados detectados; las pruebas se realizan ejecutando los scripts y revisando la salida.
- Los archivos `__pycache__` y generados por `ply` pueden eliminarse para limpiar el entorno.

## Patrones y convenciones específicas
- Los tokens y reglas léxicas siguen el patrón de definición de funciones con prefijo `t_` para tokens y expresiones regulares.
- Las reglas sintácticas se definen como funciones con docstrings que describen la producción.
- Los errores léxicos y sintácticos se manejan con funciones `t_error` y `p_error`.
- No se detectan dependencias externas más allá de `ply`.

## Ejemplo de integración
- Para agregar un nuevo lenguaje, crea un nuevo archivo `*_lexer.py` y `*_parser.py` siguiendo los patrones existentes.
- Para depuración, agrega prints en las funciones de error o en las acciones semánticas.

## Archivos clave
- `miniPHP_lexer.py`, `miniPHP_lexer_v2.py`: Ejemplo de analizador léxico para PHP reducido.
- `Ejemplo/minic_lexer.py`, `Ejemplo/minic_parser.py`: Ejemplo de analizador léxico y sintáctico para C reducido.
- `Ejemplo/evaluacion.c`: Ejemplo de código C independiente.

---

Si alguna sección requiere mayor detalle o hay flujos de trabajo no documentados, por favor indícalo para mejorar esta guía.