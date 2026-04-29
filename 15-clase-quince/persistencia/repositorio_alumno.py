import sqlite3
from pathlib import Path

from alumno import Alumno


class RepositorioAlumno:
    """Persistencia de alumnos en SQLite (id autogenerado por la base)."""

    def __init__(self, ruta_bd: str | Path = "alumnos.db") -> None:
        self._ruta = Path(ruta_bd)
        self._inicializar()

    def _conexion(self) -> sqlite3.Connection:
        return sqlite3.connect(self._ruta)

    def _inicializar(self) -> None:
        with self._conexion() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS alumnos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    cantidad_cursos INTEGER NOT NULL
                )
                """
            )
            cantidad = conn.execute("SELECT COUNT(*) FROM alumnos").fetchone()[0]
            if cantidad == 0:
                inicial = Alumno("Esteban", "Calabria", 3)
                conn.execute(
                    """
                    INSERT INTO alumnos (nombre, apellido, cantidad_cursos)
                    VALUES (?, ?, ?)
                    """,
                    (inicial.nombre, inicial.apellido, inicial.cantidad_cursos),
                )

    def listar(self) -> list[Alumno]:
        with self._conexion() as conn:
            filas = conn.execute(
                """
                SELECT id, nombre, apellido, cantidad_cursos
                FROM alumnos
                ORDER BY id
                """
            ).fetchall()
        return [
            Alumno(nombre, apellido, cantidad_cursos, id=id_)
            for id_, nombre, apellido, cantidad_cursos in filas
        ]

    def obtener_por_indice(self, indice: int) -> Alumno:
        with self._conexion() as conn:
            fila = conn.execute(
                """
                SELECT id, nombre, apellido, cantidad_cursos
                FROM alumnos
                ORDER BY id
                LIMIT 1 OFFSET ?
                """,
                (indice,),
            ).fetchone()
        if fila is None:
            raise IndexError("Indice de alumno fuera de rango.")
        id_, nombre, apellido, cantidad_cursos = fila
        return Alumno(nombre, apellido, cantidad_cursos, id=id_)

    def insertar(self, alumno: Alumno) -> None:
        if alumno.id is not None:
            raise ValueError("Solo se pueden insertar alumnos sin id asignado.")
        with self._conexion() as conn:
            cur = conn.execute(
                """
                INSERT INTO alumnos (nombre, apellido, cantidad_cursos)
                VALUES (?, ?, ?)
                """,
                (alumno.nombre, alumno.apellido, alumno.cantidad_cursos),
            )
            alumno.asignar_id(int(cur.lastrowid))

    def actualizar(self, alumno: Alumno) -> None:
        if alumno.id is None:
            raise ValueError("No se puede actualizar un alumno sin id.")
        with self._conexion() as conn:
            cur = conn.execute(
                """
                UPDATE alumnos
                SET nombre = ?, apellido = ?, cantidad_cursos = ?
                WHERE id = ?
                """,
                (alumno.nombre, alumno.apellido, alumno.cantidad_cursos, alumno.id),
            )
            if cur.rowcount == 0:
                raise ValueError("No existe un alumno con ese id en la base.")

    def eliminar(self, alumno: Alumno) -> None:
        if alumno.id is None:
            raise ValueError("No se puede eliminar un alumno sin id.")
        with self._conexion() as conn:
            cur = conn.execute("DELETE FROM alumnos WHERE id = ?", (alumno.id,))
            if cur.rowcount == 0:
                raise ValueError("No existe un alumno con ese id en la base.")
