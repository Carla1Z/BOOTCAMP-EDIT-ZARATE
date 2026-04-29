import tkinter as tk
from tkinter import messagebox
from servicios import ServicioAlumnos


class AlumnoApp:
    def __init__(self) -> None:
        self.servicio = ServicioAlumnos()
        self.seleccion_actual: int | None = None

        self.ventana = tk.Tk()
        self.ventana.title("Gestión de Alumnos")
        self.ventana.geometry("500x400")

        self.entry_nombre: tk.Entry
        self.entry_apellido: tk.Entry
        self.entry_cursos: tk.Entry
        self.lista: tk.Listbox

        self._crear_widgets()

    def _crear_widgets(self) -> None:
        tk.Label(self.ventana, text="Nombre").pack()
        self.entry_nombre = tk.Entry(self.ventana)
        self.entry_nombre.pack()

        tk.Label(self.ventana, text="Apellido").pack()
        self.entry_apellido = tk.Entry(self.ventana)
        self.entry_apellido.pack()

        tk.Label(self.ventana, text="Cursos").pack()
        self.entry_cursos = tk.Entry(self.ventana)
        self.entry_cursos.pack()

        tk.Button(self.ventana, text="Agregar", command=self.agregar_alumno).pack(pady=5)
        tk.Button(self.ventana, text="Modificar", command=self.modificar_alumno).pack(pady=5)
        tk.Button(self.ventana, text="Eliminar", command=self.eliminar_alumno).pack(pady=5)

        self.lista = tk.Listbox(self.ventana)
        self.lista.pack(fill=tk.BOTH, expand=True)
        self.lista.bind("<<ListboxSelect>>", self.cargar_seleccion)

        self.actualizar_lista()

    def actualizar_lista(self) -> None:
        seleccionado = self.obtener_indice_seleccionado()
        self.lista.delete(0, tk.END)

        for alumno in self.servicio.listar_alumnos():
            self.lista.insert(tk.END, str(alumno))

        if seleccionado is not None and seleccionado < self.lista.size():
            self.lista.selection_set(seleccionado)

    def agregar_alumno(self) -> None:
        try:
            nombre, apellido, cursos = self._leer_campos()
            self.servicio.agregar_alumno(nombre, apellido, cursos)
            self.actualizar_lista()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos\\n{e}")

    def eliminar_alumno(self) -> None:
        index = self.obtener_indice_seleccionado()
        if index is None:
            messagebox.showwarning("Atención", "Debe seleccionar un alumno antes de eliminar.")
            return

        self.servicio.eliminar_alumno(index)
        self.seleccion_actual = None
        self.actualizar_lista()

    def cargar_seleccion(self, event: tk.Event | None = None) -> None:
        index = self.obtener_indice_seleccionado()
        if index is None:
            return

        self.seleccion_actual = index
        alumno = self.servicio.obtener_alumno(index)

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, alumno.nombre)

        self.entry_apellido.delete(0, tk.END)
        self.entry_apellido.insert(0, alumno.apellido)

        self.entry_cursos.delete(0, tk.END)
        self.entry_cursos.insert(0, str(alumno.cantidad_cursos))

    def obtener_indice_seleccionado(self) -> int | None:
        seleccionado = self.lista.curselection()
        return seleccionado[0] if seleccionado else self.seleccion_actual

    def modificar_alumno(self) -> None:
        index = self.obtener_indice_seleccionado()
        if index is None:
            messagebox.showwarning("Atención", "Debe seleccionar un alumno antes de modificar.")
            return

        try:
            nombre, apellido, cursos = self._leer_campos()
            self.servicio.actualizar_alumno(index, nombre, apellido, cursos)

            self.actualizar_lista()
            self.lista.selection_clear(0, tk.END)
            self.lista.selection_set(index)
            self.lista.activate(index)
            self.seleccion_actual = index

            messagebox.showinfo("Éxito", "Alumno modificado correctamente.")
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos\\n{e}")

    def limpiar_campos(self) -> None:
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_cursos.delete(0, tk.END)

    def _leer_campos(self) -> tuple[str, str, int]:
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        cursos = int(self.entry_cursos.get())
        return nombre, apellido, cursos

    def ejecutar(self) -> None:
        self.ventana.mainloop()


if __name__ == "__main__":
    AlumnoApp().ejecutar()
