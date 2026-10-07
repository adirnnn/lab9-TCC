# laboratorio 9 - teoria de la computacion

simulador sencillo de maquinas de turing en python que use para comprobar las
respuestas del laboratorio 9 (descripciones instantaneas, salidas y el
lenguaje del problema 3).

## archivos

- `maquina_turing.py`: la clase de la maquina de turing (cinta infinita a los dos lados, blanco = `⊔`)
- `problema1.py`: maquina que pasa las mayusculas a minusculas
- `problema2.py`: maquina que le suma 1 a un numero binario, imprime las trazas de `100`, `10011` y `11`
- `problema3.py`: maquina que reconoce `a^n b^n` (n >= 1), traza de `aabb`, prueba de `aba` y el diagrama en dot
- `diagrama_problema3.py`: genera `diagrama_problema3.svg` con q1..q5 en pentagono
- `test_laboratorio.py`: pruebas

## como correrlo

solo necesita python 3, no usa librerias externas.

```
python problema1.py
python problema2.py
python problema3.py
python diagrama_problema3.py
python -m unittest -v
```
