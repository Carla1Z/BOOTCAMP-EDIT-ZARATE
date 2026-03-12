import tkinter as tk
from tkinter import ttk, messagebox
import random

# ── Paleta Cottagecore ──────────────────────────────────────────────────────
BG        = "#f5ede0"          # crema cálido
PANEL     = "#e8d8c4"          # beige suave
ACCENT    = "#8b6f5e"          # marrón tierra
GREEN     = "#6b8f5e"          # verde musgo
ROSE      = "#c47e8a"          # rosa silvestre
TEXT      = "#3d2b1f"          # café oscuro
LIGHT_TXT = "#7a5c4e"          # texto secundario
BORDER    = "#c4a882"          # borde arena
ENTRY_BG  = "#fdf6ee"          # fondo inputs

FONT_TITLE  = ("Georgia", 22, "bold")
FONT_HEADER = ("Georgia", 14, "bold")
FONT_BODY   = ("Georgia", 11)
FONT_SMALL  = ("Georgia", 9, "italic")
FONT_BTN    = ("Georgia", 11, "bold")

# ── Decoraciones ────────────────────────────────────────────────────────────
FLOWERS   = ["🌸", "🌿", "🍄", "🌼", "🌾", "🍃", "🌻", "🪴"]
QUOTES    = [
    "La vida es más dulce junto a la naturaleza. 🌿",
    "Cada día es un regalo del jardín. 🌸",
    "Encuentra paz en las cosas simples. 🍃",
    "El hogar es donde florece el corazón. 🌼",
    "Un té caliente arregla casi todo. ☕",
]

def random_flower():
    return random.choice(FLOWERS)

# ── Widgets personalizados ───────────────────────────────────────────────────
def make_btn(parent, text, cmd, color=GREEN, fg="white", padx=18, pady=8):
    btn = tk.Button(
        parent, text=text, command=cmd,
        bg=color, fg=fg, activebackground=ACCENT, activeforeground="white",
        font=FONT_BTN, relief="flat", cursor="hand2",
        padx=padx, pady=pady, bd=0
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn

def make_label(parent, text, font=FONT_BODY, fg=TEXT, **kw):
    return tk.Label(parent, text=text, font=font, fg=fg, bg=kw.pop("bg", BG), **kw)

def make_entry(parent, width=28, **kw):
    e = tk.Entry(
        parent, width=width, font=FONT_BODY,
        bg=ENTRY_BG, fg=TEXT, insertbackground=ACCENT,
        relief="flat", bd=0, highlightthickness=2,
        highlightbackground=BORDER, highlightcolor=ROSE,
        **kw
    )
    return e

def separator(parent, pad=8):
    tk.Label(parent, text="✦ ─────────────────── ✦",
             font=("Georgia", 9), fg=BORDER, bg=BG).pack(pady=pad)

# ── Ventana principal ────────────────────────────────────────────────────────
class CottageCoreApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🌿 Cabaña Digital")
        self.geometry("780x620")
        self.resizable(False, False)
        self.configure(bg=BG)

        self._build_header()
        self._build_tabs()
        self._build_footer()

    # ── Encabezado ──────────────────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self, bg=PANEL, pady=14)
        hdr.pack(fill="x")

        make_label(hdr, f"{random_flower()}  Cabaña Digital  {random_flower()}",
                   font=FONT_TITLE, fg=ACCENT, bg=PANEL).pack()
        make_label(hdr, "Un rincón tranquilo y natural ✿",
                   font=FONT_SMALL, fg=LIGHT_TXT, bg=PANEL).pack()

    # ── Pestañas ────────────────────────────────────────────────────────────
    def _build_tabs(self):
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("TNotebook", background=BG, borderwidth=0, tabmargins=[6, 6, 0, 0])
        style.configure("TNotebook.Tab",
                        background=PANEL, foreground=TEXT,
                        font=FONT_BODY, padding=[14, 6],
                        borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", BG)],
                  foreground=[("selected", ACCENT)])

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=16, pady=10)

        tabs = [
            ("🌿  Bienvenida",   self._tab_welcome),
            ("📖  Diario",        self._tab_diary),
            ("🌸  Recetas",       self._tab_recipes),
            ("🍄  Galería",       self._tab_gallery),
        ]
        for name, builder in tabs:
            frame = tk.Frame(nb, bg=BG)
            nb.add(frame, text=name)
            builder(frame)

    # ── Pestaña 1 — Bienvenida ───────────────────────────────────────────────
    def _tab_welcome(self, f):
        tk.Label(f, text="", bg=BG).pack(pady=10)
        make_label(f, "✿  Bienvenida a tu rincón  ✿",
                   font=FONT_HEADER, fg=ROSE).pack()
        separator(f)

        quote_var = tk.StringVar(value=random.choice(QUOTES))
        qlbl = make_label(f, quote_var.get(), font=("Georgia", 12, "italic"),
                          fg=GREEN, wraplength=500, justify="center")
        qlbl.pack(pady=8)

        def new_quote():
            quote_var.set(random.choice(QUOTES))
            qlbl.config(text=quote_var.get())

        make_btn(f, f"{random_flower()} Nueva inspiración", new_quote,
                 color=ROSE).pack(pady=6)

        separator(f)

        # Mini clima ficticio
        weather = tk.Frame(f, bg=PANEL, padx=20, pady=14, relief="flat")
        weather.pack(padx=60, pady=4, fill="x")
        make_label(weather, "🌤  El campo hoy…", font=FONT_HEADER,
                   fg=ACCENT, bg=PANEL).pack()
        datos = [("Temperatura", "18 °C  ·  Brisa suave"),
                 ("Flores abiertas", "Rosas, Margaritas, Amapolas"),
                 ("Momento ideal", "Tarde con té y libro 📚")]
        for k, v in datos:
            row = tk.Frame(weather, bg=PANEL)
            row.pack(fill="x", pady=2)
            make_label(row, f"{k}:", font=("Georgia", 10, "bold"),
                       fg=LIGHT_TXT, bg=PANEL).pack(side="left")
            make_label(row, f"  {v}", font=("Georgia", 10),
                       fg=TEXT, bg=PANEL).pack(side="left")

    # ── Pestaña 2 — Diario ──────────────────────────────────────────────────
    def _tab_diary(self, f):
        self.diary_entries = []

        tk.Label(f, text="", bg=BG).pack(pady=6)
        make_label(f, "📖  Mi Diario del Jardín", font=FONT_HEADER, fg=ACCENT).pack()
        separator(f)

        form = tk.Frame(f, bg=BG)
        form.pack(padx=30)

        make_label(form, "¿Cómo se llama tu entrada?").grid(
            row=0, column=0, sticky="w", pady=4)
        self.diary_title = make_entry(form, width=36)
        self.diary_title.grid(row=0, column=1, padx=8)

        make_label(form, "Escribe tus pensamientos:").grid(
            row=1, column=0, sticky="nw", pady=4)
        self.diary_text = tk.Text(
            form, width=36, height=5, font=FONT_BODY,
            bg=ENTRY_BG, fg=TEXT, relief="flat", bd=0,
            highlightthickness=2, highlightbackground=BORDER,
            highlightcolor=ROSE, wrap="word"
        )
        self.diary_text.grid(row=1, column=1, padx=8)

        make_btn(form, f"🌸 Guardar entrada", self._save_diary,
                 color=ROSE).grid(row=2, column=1, sticky="e", pady=8)

        separator(f)
        make_label(f, "Entradas guardadas:", fg=LIGHT_TXT,
                   font=FONT_SMALL).pack(anchor="w", padx=30)

        self.diary_list = tk.Listbox(
            f, font=FONT_BODY, bg=ENTRY_BG, fg=TEXT,
            selectbackground=ROSE, selectforeground="white",
            relief="flat", bd=0, highlightthickness=1,
            highlightbackground=BORDER, height=5
        )
        self.diary_list.pack(padx=30, pady=4, fill="x")

    def _save_diary(self):
        title = self.diary_title.get().strip()
        body  = self.diary_text.get("1.0", "end").strip()
        if not title:
            messagebox.showwarning("🌿 Atención", "Por favor escribe un título.")
            return
        entry = f"{random_flower()}  {title}"
        self.diary_entries.append((title, body))
        self.diary_list.insert("end", entry)
        self.diary_title.delete(0, "end")
        self.diary_text.delete("1.0", "end")
        messagebox.showinfo("✿ Guardado", f"Tu entrada «{title}» fue guardada. 🌸")

    # ── Pestaña 3 — Recetas ─────────────────────────────────────────────────
    def _tab_recipes(self, f):
        RECIPES = {
            "🫖 Té de manzanilla y miel": [
                "1 taza de agua caliente",
                "1 bolsita de manzanilla",
                "1 cdta de miel silvestre",
                "1 rodaja de limón 🍋",
            ],
            "🍞 Pan de lavanda": [
                "2 tazas de harina integral",
                "1 cdta de levadura",
                "1 pizca de flores de lavanda",
                "Sal de mar y agua tibia",
            ],
            "🫙 Mermelada de fresas silvestres": [
                "500 g de fresas",
                "250 g de azúcar morena",
                "Jugo de ½ limón",
                "1 ramita de romero 🌿",
            ],
        }

        tk.Label(f, text="", bg=BG).pack(pady=6)
        make_label(f, "🌸  Recetas de la Cabaña", font=FONT_HEADER, fg=ACCENT).pack()
        separator(f)

        sel = tk.StringVar(value=list(RECIPES.keys())[0])

        opt_frame = tk.Frame(f, bg=BG)
        opt_frame.pack()

        ingredients_var = tk.StringVar()

        def show_recipe(*_):
            r = sel.get()
            ingredients_var.set("\n".join(f"  {random_flower()}  {i}"
                                         for i in RECIPES[r]))

        for name in RECIPES:
            tk.Radiobutton(
                opt_frame, text=name, variable=sel, value=name,
                command=show_recipe, bg=BG, fg=TEXT, activebackground=BG,
                selectcolor=ENTRY_BG, font=FONT_BODY
            ).pack(anchor="w", pady=2)

        separator(f, pad=4)
        make_label(f, "Ingredientes:", font=("Georgia", 11, "bold"),
                   fg=ACCENT).pack(anchor="w", padx=40)

        ing_lbl = make_label(f, "", font=FONT_BODY, fg=TEXT,
                             justify="left", wraplength=500)
        ing_lbl.pack(anchor="w", padx=40, pady=4)
        ingredients_var.trace_add("write",
                                   lambda *_: ing_lbl.config(text=ingredients_var.get()))
        show_recipe()

    # ── Pestaña 4 — Galería ─────────────────────────────────────────────────
    def _tab_gallery(self, f):
        items = [
            ("🌸", "Rosa silvestre",    "Florece en primavera"),
            ("🍄", "Champiñón del bosque", "Crece bajo los robles"),
            ("🌿", "Helecho esmeralda", "Ama la sombra húmeda"),
            ("🌼", "Margarita campestre","Símbolo de alegría"),
            ("🫙", "Tarro de mermelada", "Fresa con lavanda"),
            ("🕯️", "Vela de cera de abeja","Aroma suave y cálido"),
        ]
        tk.Label(f, text="", bg=BG).pack(pady=6)
        make_label(f, "🍃  Galería del Campo", font=FONT_HEADER, fg=ACCENT).pack()
        separator(f)

        grid = tk.Frame(f, bg=BG)
        grid.pack(padx=20)

        for idx, (emoji, name, desc) in enumerate(items):
            card = tk.Frame(grid, bg=PANEL, padx=12, pady=10,
                            relief="flat", bd=0,
                            highlightthickness=1, highlightbackground=BORDER)
            card.grid(row=idx//3, column=idx%3, padx=8, pady=8, sticky="nsew")

            make_label(card, emoji, font=("Georgia", 28), bg=PANEL).pack()
            make_label(card, name, font=("Georgia", 10, "bold"),
                       fg=ACCENT, bg=PANEL).pack()
            make_label(card, desc, font=("Georgia", 9, "italic"),
                       fg=LIGHT_TXT, bg=PANEL, wraplength=130).pack()

    # ── Pie de página ────────────────────────────────────────────────────────
    def _build_footer(self):
        footer = tk.Frame(self, bg=PANEL, pady=6)
        footer.pack(fill="x", side="bottom")
        make_label(footer,
                   "🌿  Hecho con amor y una taza de té  ·  Cabaña Digital  🌸",
                   font=FONT_SMALL, fg=LIGHT_TXT, bg=PANEL).pack()


# ── Arranque ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = CottageCoreApp()
    app.mainloop()