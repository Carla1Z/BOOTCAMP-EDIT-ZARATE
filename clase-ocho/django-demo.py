import os
import sys
import django
from django.conf import settings
from django.urls import path
from django.http import HttpResponse
from django.core.management import execute_from_command_line

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE DJANGO
# -----------------------------------------------------------------------------
settings.configure(
    DEBUG=True,
    SECRET_KEY='clave-secreta-cottagecore-123',
    ROOT_URLCONF=__name__,
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
    ],
    MIDDLEWARE=[
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [],
        },
    }],
)

django.setup()

# -----------------------------------------------------------------------------
# 2. VISTAS Y DISEÑO (LANDING PAGE COTTAGECORE)
# -----------------------------------------------------------------------------

def get_cottage_html():
    """Genera el HTML completo con estilos CSS integrados."""
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>El Rincón del Bosque | Cottagecore Demo</title>
        <!-- Fuentes de Google para el estilo -->
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Quicksand:wght@300;400;500&display=swap" rel="stylesheet">
        
        <style>
            :root {
                --bg-color: #FDFCF0;       /* Crema suave */
                --text-color: #4A4036;     /* Marrón tierra */
                --accent-green: #556B2F;   /* Verde musgo */
                --accent-sage: #8F9E8B;    /* Verde salvia */
                --accent-clay: #C19A6B;    /* Arcilla */
                --white: #FFFFFF;
            }

            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Quicksand', sans-serif;
                background-color: var(--bg-color);
                color: var(--text-color);
                line-height: 1.6;
                background-image: radial-gradient(#8F9E8B 0.5px, transparent 0.5px);
                background-size: 20px 20px; /* Patrón de puntos sutil */
            }

            h1, h2, h3 {
                font-family: 'Cormorant Garamond', serif;
                font-weight: 600;
            }

            /* Header */
            header {
                padding: 2rem 5%;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid var(--accent-sage);
            }

            .logo {
                font-size: 1.8rem;
                color: var(--accent-green);
                font-style: italic;
            }

            nav a {
                text-decoration: none;
                color: var(--text-color);
                margin-left: 20px;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 1px;
                transition: color 0.3s;
            }

            nav a:hover {
                color: var(--accent-clay);
            }

            /* Hero Section */
            .hero {
                text-align: center;
                padding: 6rem 1rem;
                background: linear-gradient(to bottom, rgba(253,252,240,0), rgba(143,158,139,0.2));
            }

            .hero h1 {
                font-size: 4rem;
                color: var(--accent-green);
                margin-bottom: 1rem;
                line-height: 1.1;
            }

            .hero p {
                font-size: 1.2rem;
                max-width: 600px;
                margin: 0 auto 2rem auto;
                font-style: italic;
            }

            .btn {
                display: inline-block;
                padding: 12px 30px;
                background-color: var(--accent-green);
                color: var(--white);
                text-decoration: none;
                border-radius: 50px;
                font-family: 'Cormorant Garamond', serif;
                font-size: 1.2rem;
                transition: background 0.3s;
                border: 1px solid var(--accent-green);
            }

            .btn:hover {
                background-color: var(--bg-color);
                color: var(--accent-green);
            }

            /* Features / Cards */
            .features {
                padding: 4rem 10%;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 2rem;
            }

            .card {
                background: var(--white);
                padding: 2rem;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.05);
                border: 1px solid #eee;
            }

            .card-icon {
                font-size: 2.5rem;
                margin-bottom: 1rem;
                display: block;
            }

            .card h3 {
                color: var(--accent-clay);
                margin-bottom: 1rem;
                font-size: 1.5rem;
            }

            /* Quote Section */
            .quote-section {
                background-color: var(--accent-sage);
                color: var(--white);
                text-align: center;
                padding: 4rem 1rem;
                margin: 2rem 0;
            }

            .quote-section blockquote {
                font-family: 'Cormorant Garamond', serif;
                font-size: 2rem;
                font-style: italic;
            }

            /* Footer */
            footer {
                text-align: center;
                padding: 2rem;
                border-top: 1px solid var(--accent-sage);
                font-size: 0.8rem;
                color: var(--accent-green);
            }

            /* Decorative elements */
            .flower-divider {
                text-align: center;
                font-size: 1.5rem;
                color: var(--accent-clay);
                margin: 2rem 0;
            }

        </style>
    </head>
    <body>

        <header>
            <div class="logo">🌿 El Rincón del Bosque</div>
            <nav>
                <a href="#inicio">Inicio</a>
                <a href="#esencia">Esencia</a>
                <a href="#contacto">Contacto</a>
            </nav>
        </header>

        <section class="hero" id="inicio">
            <h1>Vida lenta y<br>simplicidad rural</h1>
            <p>Un espacio digital dedicado a la estética del campo, la cocina casera y la conexión con la naturaleza.</p>
            <a href="#esencia" class="btn">Explorar el jardín</a>
        </section>

        <div class="flower-divider">❦ ❦ ❦</div>

        <section class="features" id="esencia">
            <div class="card">
                <span class="card-icon">🍞</span>
                <h3>Pan de Masa Madre</h3>
                <p>El arte de fermentar lentamente. Recetas tradicionales para un desayuno perfecto.</p>
            </div>
            <div class="card">
                <span class="card-icon">🧶</span>
                <h3>Tejidos a Mano</h3>
                <p>Lana suave, agujas de madera y patrones vintage para crear abrigo en invierno.</p>
            </div>
            <div class="card">
                <span class="card-icon">🍄</span>
                <h3>Forrajeo</h3>
                <p>Salidas al bosque para recolectar setas, hierbas silvestres y flores de temporada.</p>
            </div>
        </section>

        <section class="quote-section">
            <blockquote>
                "No hay nada como el silencio del campo para escuchar los propios pensamientos."
            </blockquote>
        </section>

        <footer id="contacto">
            <p>Hecho con 🤎 y Python (Django Demo)</p>
            <p>&copy; 2023 El Rincón del Bosque. Todos los derechos reservados.</p>
        </footer>

    </body>
    </html>
    """

def home(request):
    return HttpResponse(get_cottage_html())

# -----------------------------------------------------------------------------
# 3. URLS
# -----------------------------------------------------------------------------
urlpatterns = [
    path('', home, name='home'),
]

# -----------------------------------------------------------------------------
# 4. PUNTO DE ENTRADA
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    execute_from_command_line(sys.argv)