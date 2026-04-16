"""
Módulo de validaciones para clases de dominio.
Extrae validaciones para promover reutilización y adherir a SRP.
Permite que múltiples clases usen las mismas reglas de validación sin duplicar código.
"""

class AlumnoValidator:
    """
    Validador para la clase Alumno.
    Contiene métodos estáticos para validar atributos, centralizando lógica de validación.
    Facilita reutilización en otras clases si es necesario (ej. Profesor con validaciones similares).
    """

    @staticmethod
    def validar_id(id: int):
        """Valida que el id sea un entero positivo."""
        if not isinstance(id, int) or id <= 0:
            raise ValueError("El id debe ser un entero positivo.")

    @staticmethod
    def validar_nombre(nombre: str):
        """Valida que el nombre sea una cadena no vacía."""
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre debe ser una cadena no vacía.")

    @staticmethod
    def validar_apellido(apellido: str):
        """Valida que el apellido sea una cadena no vacía."""
        if not isinstance(apellido, str) or not apellido.strip():
            raise ValueError("El apellido debe ser una cadena no vacía.")

    @staticmethod
    def validar_cantidad_cursos(cantidad_cursos: int):
        """Valida que la cantidad de cursos sea un entero no negativo."""
        if not isinstance(cantidad_cursos, int) or cantidad_cursos < 0:
            raise ValueError("La cantidad de cursos debe ser un entero no negativo.")