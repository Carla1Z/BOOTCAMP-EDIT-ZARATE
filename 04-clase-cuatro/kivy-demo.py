"""
🌿 Cottage Notes — una app multi-plataforma con Kivy
Estética cottage core: colores terrosos, flores, calidez.
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.core.window import Window

# Paleta cottage core
Window.clearcolor = (0.96, 0.93, 0.87, 1)  # crema cálida

KV = """
#: import Window kivy.core.window.Window

<HomeScreen>:
    canvas.before:
        Color:
            rgba: 0.96, 0.93, 0.87, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: "vertical"
        padding: dp(30)
        spacing: dp(16)

        # ── Cabecera ─────────────────────────────
        Label:
            text: "🌸 Cottage Notes 🌿"
            font_size: dp(32)
            bold: True
            color: 0.40, 0.28, 0.18, 1
            size_hint_y: None
            height: dp(60)

        Label:
            text: "un rinconcito para tus pensamientos"
            font_size: dp(14)
            italic: True
            color: 0.60, 0.45, 0.30, 1
            size_hint_y: None
            height: dp(28)

        # ── Separador floral ──────────────────────
        Label:
            text: "❁ ── ── ── ── ── ── ❁"
            font_size: dp(13)
            color: 0.72, 0.55, 0.38, 1
            size_hint_y: None
            height: dp(28)

        # ── Campo de texto ────────────────────────
        Label:
            text: "escribe tu nota de hoy…"
            font_size: dp(13)
            color: 0.50, 0.38, 0.25, 1
            size_hint_y: None
            height: dp(22)
            halign: "left"
            text_size: self.width, None

        TextInput:
            id: note_input
            hint_text: "El jardín huele a lavanda esta mañana…"
            hint_text_color: 0.75, 0.65, 0.52, 1
            foreground_color: 0.35, 0.23, 0.13, 1
            background_color: 0.99, 0.97, 0.92, 1
            cursor_color: 0.60, 0.40, 0.20, 1
            font_size: dp(15)
            padding: dp(14), dp(12)
            size_hint_y: None
            height: dp(130)
            multiline: True

        # ── Botones ───────────────────────────────
        BoxLayout:
            orientation: "horizontal"
            spacing: dp(12)
            size_hint_y: None
            height: dp(48)

            Button:
                id: save_btn
                text: "🍃  Guardar"
                font_size: dp(15)
                background_color: 0.55, 0.72, 0.48, 1
                color: 1, 1, 1, 1
                background_normal: ""
                on_press: root.save_note(self)

            Button:
                text: "🌾  Ver notas"
                font_size: dp(15)
                background_color: 0.72, 0.55, 0.38, 1
                color: 1, 1, 1, 1
                background_normal: ""
                on_press: app.root.current = "list"

        # ── Mensaje de confirmación ───────────────
        Label:
            id: msg_label
            text: ""
            font_size: dp(13)
            italic: True
            color: 0.45, 0.62, 0.38, 1
            size_hint_y: None
            height: dp(28)

        # ── Decoración inferior ───────────────────
        Label:
            text: "🌼  🍄  🌿  🐝  🌺"
            font_size: dp(22)
            size_hint_y: None
            height: dp(40)

        Widget:  # espacio vacío flexible


<ListScreen>:
    canvas.before:
        Color:
            rgba: 0.96, 0.93, 0.87, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: "vertical"
        padding: dp(30)
        spacing: dp(14)

        Label:
            text: "📖  Mis notas"
            font_size: dp(28)
            bold: True
            color: 0.40, 0.28, 0.18, 1
            size_hint_y: None
            height: dp(52)

        ScrollView:
            GridLayout:
                id: notes_grid
                cols: 1
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height
                padding: 0, dp(4)

        Button:
            text: "🌸  volver al jardín"
            font_size: dp(15)
            background_color: 0.72, 0.55, 0.38, 1
            color: 1, 1, 1, 1
            background_normal: ""
            size_hint_y: None
            height: dp(48)
            on_press: app.root.current = "home"
"""


class HomeScreen(Screen):
    notes = []  # lista compartida en memoria

    def save_note(self, btn):
        text = self.ids.note_input.text.strip()
        if not text:
            self.ids.msg_label.text = "✦ escribe algo primero…"
            return

        HomeScreen.notes.append(text)
        self.ids.note_input.text = ""
        self.ids.msg_label.text = "✦ nota guardada con cariño ✦"

        # animación suave en el botón
        anim = Animation(background_color=(0.45, 0.62, 0.35, 1), duration=0.15)
        anim += Animation(background_color=(0.55, 0.72, 0.48, 1), duration=0.3)
        anim.start(btn)


class ListScreen(Screen):
    def on_enter(self):
        """Refresca la lista cada vez que entramos a esta pantalla."""
        from kivy.uix.label import Label
        grid = self.ids.notes_grid
        grid.clear_widgets()

        if not HomeScreen.notes:
            grid.add_widget(Label(
                text="🌱 aún no hay notas…",
                font_size="15sp",
                italic=True,
                color=(0.60, 0.45, 0.30, 1),
                size_hint_y=None,
                height="40dp",
            ))
            return

        for i, note in enumerate(reversed(HomeScreen.notes), 1):
            preview = note[:60] + ("…" if len(note) > 60 else "")
            grid.add_widget(Label(
                text=f"🌿  {preview}",
                font_size="14sp",
                color=(0.38, 0.25, 0.13, 1),
                size_hint_y=None,
                height="38dp",
                halign="left",
                text_size=(Window.width - 60, None),
            ))


class CottageApp(App):
    title = "Cottage Notes 🌸"

    def build(self):
        Builder.load_string(KV)
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(ListScreen(name="list"))
        return sm


if __name__ == "__main__":
    CottageApp().run()