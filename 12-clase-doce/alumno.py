"""
Clase Alumno con encapsulamiento, validaciones y principios SOLID aplicados.
"""

from validators import AlumnoValidator


class Alumno:
    """
    Clase que representa a un alumno con encapsulamiento y validaciones.
    """

    def __init__(self, id: int, nombre: str, apellido: str, cantidad_cursos: int):
        """
        Constructor que valida y crea un objeto Alumno consistente.

        Args:
            id (int): Identificador único del alumno, debe ser un entero positivo.
            nombre (str): Nombre del alumno, cadena no vacía.
            apellido (str): Apellido del alumno, cadena no vacía.
            cantidad_cursos (int): Cantidad de cursos inscritos, entero no negativo.

        Raises:
            ValueError: Si algún parámetro no cumple las reglas de validación.
        """
        AlumnoValidator.validar_id(id)
        AlumnoValidator.validar_nombre(nombre)
        AlumnoValidator.validar_apellido(apellido)
        AlumnoValidator.validar_cantidad_cursos(cantidad_cursos)

        self._id = id
        self._nombre = nombre.strip()
        self._apellido = apellido.strip()
        self._cantidad_cursos = cantidad_cursos

    @property
    def id(self) -> int:
        """Getter para el id del alumno."""
        return self._id

    @property
    def nombre(self) -> str:
        """Getter para el nombre del alumno."""
        return self._nombre

    @nombre.setter
    def nombre(self, value: str):
        """Setter para el nombre del alumno, con validación."""
        AlumnoValidator.validar_nombre(value)
        self._nombre = value.strip()

    @property
    def apellido(self) -> str:
        """Getter para el apellido del alumno."""
        return self._apellido

    @apellido.setter
    def apellido(self, value: str):
        """Setter para el apellido del alumno, con validación."""
        AlumnoValidator.validar_apellido(value)
        self._apellido = value.strip()

    @property
    def cantidad_cursos(self) -> int:
        """Getter para la cantidad de cursos del alumno."""
        return self._cantidad_cursos

    @cantidad_cursos.setter
    def cantidad_cursos(self, value: int):
        """Setter para la cantidad de cursos del alumno, con validación."""
        AlumnoValidator.validar_cantidad_cursos(value)
        self._cantidad_cursos = value

    def __str__(self) -> str:
        """Representación legible del alumno para el usuario."""
        return (
            f"Alumno(id={self._id}, nombre='{self._nombre}', "
            f"apellido='{self._apellido}', cantidad_cursos={self._cantidad_cursos})"
        )

    def __repr__(self) -> str:
        """Representación oficial del alumno para debugging y recreación."""
        return (
            f"Alumno(id={self._id}, nombre='{self._nombre}', "
            f"apellido='{self._apellido}', cantidad_cursos={self._cantidad_cursos})"
        )
