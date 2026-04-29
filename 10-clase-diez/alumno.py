class Alumno:
    def __init__(self, id, nombre, apellido, cantidad_cursos):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.cantidad_cursos = cantidad_cursos

    def __str__(self):
        return f"Alumno({self.id}): {self.nombre} {self.apellido}, Cursos: {self.cantidad_cursos}