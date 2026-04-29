<div align="center">

# 🌿 Cabaña Digital

### *Una aplicación de escritorio con estética cottagecore hecha en Python + Tkinter*

![Python](https://img.shields.io/badge/Python-3.8%2B-c47e8a?style=flat-square&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-built--in-6b8f5e?style=flat-square)
![License](https://img.shields.io/badge/licencia-MIT-8b6f5e?style=flat-square)
![Sin dependencias](https://img.shields.io/badge/dependencias-ninguna-c4a882?style=flat-square)

> *"La vida es más dulce junto a la naturaleza."* 🌸

</div>

---

## ✦ ¿Qué es esto?

**Cabaña Digital** es una aplicación de ventanas construida con `tkinter` que adopta la estética **cottagecore**: colores cálidos en tonos crema, beige y verde musgo, tipografía Georgia, y decoraciones inspiradas en la naturaleza.

Es un proyecto de ejemplo ideal para aprender cómo personalizar interfaces gráficas en Python más allá del estilo por defecto de Tkinter.

---

## 🍄 Características

| Pestaña | Descripción |
|---|---|
| 🌿 **Bienvenida** | Tarjeta de clima campestre y citas inspiradoras aleatorias |
| 📖 **Diario del Jardín** | Formulario para escribir y guardar entradas personales |
| 🌸 **Recetas** | Selección de recetas con lista de ingredientes |
| 🍄 **Galería** | Cuadrícula de tarjetas con elementos del campo |

**Aspectos de diseño destacados:**
- Paleta de colores completamente personalizada (crema · beige · verde musgo · rosa silvestre)
- Tipografía Georgia en todos los elementos
- Botones con efecto hover suave
- Bordes y separadores ornamentales
- Emojis decorativos integrados en la UI

---

## 🌾 Requisitos

- **Python 3.8 o superior**
- `tkinter` — viene incluido por defecto en la mayoría de instalaciones de Python

> No se necesita instalar ninguna librería externa. ✿

### Verificar que tkinter está disponible

```bash
python -m tkinter
```

Si se abre una ventana de prueba, estás listo/a.

---

## 🌼 Instalación y uso

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/cabana-digital.git
cd cabana-digital

# 2. Ejecutar la aplicación
python cottagecore_app.py
```

No hay pasos adicionales. Sin `pip install`, sin entornos virtuales, sin configuración. 🍃

---

## 📁 Estructura del proyecto

```
cabana-digital/
│
├── cottagecore_app.py   # Aplicación principal (todo en un solo archivo)
└── README.md            # Este archivo
```

---

## 🎨 Paleta de colores

| Nombre | Hex | Uso |
|---|---|---|
| Crema cálido | `#f5ede0` | Fondo principal |
| Beige suave | `#e8d8c4` | Paneles y encabezado |
| Marrón tierra | `#8b6f5e` | Acento y títulos |
| Verde musgo | `#6b8f5e` | Botones principales |
| Rosa silvestre | `#c47e8a` | Botones secundarios y foco |
| Café oscuro | `#3d2b1f` | Texto principal |
| Arena | `#c4a882` | Bordes |

---

## 🪴 Personalización

El archivo está organizado con constantes al inicio para que sea fácil modificar el estilo:

```python
# Cambiá la paleta de colores
BG     = "#f5ede0"   # fondo
ACCENT = "#8b6f5e"   # acento

# Cambiá la tipografía
FONT_TITLE = ("Georgia", 22, "bold")
FONT_BODY  = ("Georgia", 11)
```

Podés reemplazar cualquier valor y la app adoptará el nuevo estilo de forma automática.

---

## 🌻 Ideas para extender el proyecto

- [ ] Persistencia del diario con `json` o `sqlite3`
- [ ] Exportar entradas del diario a `.txt`
- [ ] Agregar más recetas desde un archivo externo
- [ ] Música de fondo con `pygame`
- [ ] Modo oscuro (estética "dark cottagecore")
- [ ] Reloj analógico decorativo en la pestaña de bienvenida

---

## 📜 Licencia

Distribuido bajo la licencia **MIT**. Podés usar, modificar y compartir este código libremente.

---

<div align="center">

*Hecho con amor y una taza de té* ☕🌿

</div>
