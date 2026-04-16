from alumno import Alumno

alu = Alumno(1, "Juan", "Pérez", 3)
print(alu.nombre)  # Imprime: Juan

## Esto lanzará una excepción ValueError porque el nombre no puede ser una cadena vacía
alu.nombre = ""
alu.apellido = "García"

print(alu.nombre)  # No se ejecutará debido a la excepción anterior