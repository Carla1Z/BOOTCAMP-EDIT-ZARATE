from alumno import Alumno
from persistencia import RepositorioAlumno


class ServicioAlumnos:
    def __init__(self, repositorio: RepositorioAlumno | None = None) -> None:
        self._repositorio = repositorio or RepositorioAlumno()

    def listar(self) -> list[Alumno]:
        return self._repositorio.listar()

    def obtener_por_indice(self, indice: int) -> Alumno:
        return self._repositorio.obtener_por_indice(indice)

    def agregar(self, nombre: str, apellido: str, cursos: int) -> Alumno:
        nuevo = Alumno(nombre, apellido, cursos)
        self._repositorio.insertar(nuevo)
        return nuevo

    def eliminar_por_indice(self, indice: int) -> Alumno:
        alumno = self._repositorio.obtener_por_indice(indice)
        self._repositorio.eliminar(alumno)
        return alumno

    def modificar_por_indice(self, indice: int, nombre: str, apellido: str, cursos: int) -> Alumno:
        alumno = self._repositorio.obtener_por_indice(indice)
        alumno.actualizar_datos(nombre, apellido, cursos)
        self._repositorio.actualizar(alumno)
        return alumno
