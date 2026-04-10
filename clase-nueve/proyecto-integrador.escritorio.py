import tkinter as tk
from tkinter import messagebox, ttk

# Base de datos en memoria
db = [
    {"id": 1, "nombre": "Juan", "apellido": "Perez", "cantidad_cursos": 3}
]

# ---------------- FUNCIONES ---------------- #

def actualizar_lista():
    lista.delete(*lista.get_children())
    for alumno in db:
        lista.insert("", "end", values=(
            alumno["id"],
            alumno["nombre"],
            alumno["apellido"],
            alumno["cantidad_cursos"]
        ))

def agregar_alumno():
    try:
        nombre = entry_nombre.get().strip()
        apellido = entry_apellido.get().strip()
        cursos = int(entry_cursos.get())

        if not nombre or not apellido:
            raise ValueError

        nuevo_id = max([a["id"] for a in db], default=0) + 1

        db.append({
            "id": nuevo_id,
            "nombre": nombre,
            "apellido": apellido,
            "cantidad_cursos": cursos
        })

        limpiar_campos()
        actualizar_lista()

    except:
        messagebox.showerror("Error", "Datos inválidos")

def eliminar_alumno():
    seleccionado = lista.selection()
    if not seleccionado:
        return

    item = lista.item(seleccionado)
    id_alumno = item["values"][0]

    for alumno in db:
        if alumno["id"] == id_alumno:
            db.remove(alumno)
            break

    actualizar_lista()

def cargar_seleccion():
    seleccionado = lista.selection()
    if not seleccionado:
        return

    item = lista.item(seleccionado)
    valores = item["values"]

    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_cursos.delete(0, tk.END)

    entry_nombre.insert(0, valores[1])
    entry_apellido.insert(0, valores[2])
    entry_cursos.insert(0, valores[3])

def modificar_alumno():
    seleccionado = lista.selection()
    if not seleccionado:
        return

    item = lista.item(seleccionado)
    id_alumno = item["values"][0]

    try:
        nombre = entry_nombre.get().strip()
        apellido = entry_apellido.get().strip()
        cursos = int(entry_cursos.get())

        for alumno in db:
            if alumno["id"] == id_alumno:
                alumno["nombre"] = nombre
                alumno["apellido"] = apellido
                alumno["cantidad_cursos"] = cursos
                break

        limpiar_campos()
        actualizar_lista()

    except:
        messagebox.showerror("Error", "Datos inválidos")

def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_cursos.delete(0, tk.END)

# ---------------- UI ---------------- #

root = tk.Tk()
root.title("Gestión de Alumnos")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Nombre").grid(row=0, column=0)
entry_nombre = tk.Entry(frame)
entry_nombre.grid(row=0, column=1)

tk.Label(frame, text="Apellido").grid(row=1, column=0)
entry_apellido = tk.Entry(frame)
entry_apellido.grid(row=1, column=1)

tk.Label(frame, text="Cursos").grid(row=2, column=0)
entry_cursos = tk.Entry(frame)
entry_cursos.grid(row=2, column=1)

# Botones
tk.Button(frame, text="Agregar", command=agregar_alumno).grid(row=3, column=0, pady=5)
tk.Button(frame, text="Modificar", command=modificar_alumno).grid(row=3, column=1)
tk.Button(frame, text="Eliminar", command=eliminar_alumno).grid(row=3, column=2)

# Tabla
lista = ttk.Treeview(root, columns=("ID", "Nombre", "Apellido", "Cursos"), show="headings")
lista.heading("ID", text="ID")
lista.heading("Nombre", text="Nombre")
lista.heading("Apellido", text="Apellido")
lista.heading("Cursos", text="Cursos")

lista.pack(fill="both", expand=True)
lista.bind("<<TreeviewSelect>>", lambda e: cargar_seleccion())

actualizar_lista()

root.mainloop()