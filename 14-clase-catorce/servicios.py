from alumno import Alumno


class ServicioAlumnos:
    def __init__(self) -> None:
        self._db: list[Alumno] = [Alumno("Esteban", "Calabria", 3)]

    def listar_alumnos(self) -> list[Alumno]:
        return self._db.copy()

    def agregar_alumno(self, nombre: str, apellido: str, cantidad_cursos: int) -> Alumno:
        alumno = Alumno(nombre, apellido, cantidad_cursos)
        self._db.append(alumno)
        return alumno

    def eliminar_alumno(self, index: int) -> None:
        if index < 0 or index >= len(self._db):
            raise IndexError("Índice de alumno inválido.")
        self._db.pop(index)

    def obtener_alumno(self, index: int) -> Alumno:
        if index < 0 or index >= len(self._db):
            raise IndexError("Índice de alumno inválido.")
        return self._db[index]

    def actualizar_alumno(self, index: int, nombre: str, apellido: str, cantidad_cursos: int) -> Alumno:
        alumno = self.obtener_alumno(index)
        alumno.actualizar_datos(nombre, apellido, cantidad_cursos)
        return alumno
