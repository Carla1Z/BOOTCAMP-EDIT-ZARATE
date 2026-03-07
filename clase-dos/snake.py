"""
🐍 La Víborita del Jardín Encantado 🌿
Snake game con estética retro cottage core
Requiere: pip install pygame
"""

import pygame
import random
import sys
import math

# ──────────────────────────────────────────────
#  CONFIGURACIÓN
# ──────────────────────────────────────────────
TILE       = 24          # tamaño de cada celda en pixels
COLS       = 24
ROWS       = 22
WIDTH      = COLS * TILE
HEIGHT     = ROWS * TILE
HUD_HEIGHT = 80
WIN_W      = WIDTH
WIN_H      = HEIGHT + HUD_HEIGHT

FPS        = 60

# Velocidades (milisegundos entre pasos)
SPEEDS = {"Lento": 200, "Normal": 130, "Rápido": 75}

# ──────────────────────────────────────────────
#  PALETA COTTAGE CORE
# ──────────────────────────────────────────────
CREAM      = (245, 237, 214)
PARCHMENT  = (232, 217, 181)
GRID_LINE  = (210, 196, 162)
MOSS       = ( 90, 122,  58)
SAGE       = (138, 171, 106)
FERN       = ( 61,  92,  40)
BARK       = (107,  66,  38)
MUSHROOM   = (176, 125,  84)
LAVENDER   = (155, 123, 184)
GOLDEN     = (200, 151,  58)
DUSTY_ROSE = (196, 135, 138)
BERRY      = (139,  34,  82)
DARK_BG    = ( 45,  58,  30)
SHADOW     = ( 45,  74,  30)
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)

# ──────────────────────────────────────────────
#  TIPOS DE COMIDA
# ──────────────────────────────────────────────
FOODS = [
    {"label": "Seta",       "char": "🍄", "color": MUSHROOM,   "glow": (212, 160, 106), "pts": 10},
    {"label": "Arándano",   "char": "●",  "color": ( 74,  42, 122), "glow": LAVENDER,    "pts": 20},
    {"label": "Flor",       "char": "✿",  "color": DUSTY_ROSE,  "glow": (224, 168, 171), "pts": 15},
    {"label": "Estrella",   "char": "★",  "color": GOLDEN,      "glow": (240, 192,  96), "pts": 30},
    {"label": "Fresa",      "char": "♥",  "color": BERRY,       "glow": (192,  64, 112), "pts": 25},
]

# ──────────────────────────────────────────────
#  PARTÍCULA
# ──────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, color):
        angle  = random.uniform(0, math.pi * 2)
        speed  = random.uniform(1.5, 4.0)
        self.x = float(x)
        self.y = float(y)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 1.0
        self.decay = random.uniform(0.035, 0.07)
        self.size = random.uniform(2, 5)
        self.color = color

    def update(self):
        self.x  += self.vx
        self.y  += self.vy
        self.vy += 0.12
        self.vx *= 0.94
        self.life -= self.decay

    def draw(self, surface):
        if self.life <= 0:
            return
        alpha = int(self.life * 255)
        r, g, b = self.color
        radius = max(1, int(self.size * self.life))
        tmp = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(tmp, (r, g, b, alpha), (radius, radius), radius)
        surface.blit(tmp, (int(self.x) - radius, int(self.y) - radius))

    @property
    def alive(self):
        return self.life > 0

# ──────────────────────────────────────────────
#  JUEGO PRINCIPAL
# ──────────────────────────────────────────────
class ViboritaGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("🐍 La Víborita del Jardín Encantado 🌿")
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        self.clock  = pygame.time.Clock()

        self._load_fonts()

        self.high_score  = 0
        self.speed_name  = "Lento"
        self.state       = "menu"   # menu | playing | paused | gameover

        self.game_surface = pygame.Surface((WIDTH, HEIGHT))

        # Decoraciones de pasto estáticas (posiciones fijas)
        self.grass_spots = [(random.randint(0, COLS-1), random.randint(0, ROWS-1))
                            for _ in range(18)]

        self._init_round()

    # ── Fuentes ────────────────────────────────
    def _load_fonts(self):
        """Carga fuentes del sistema con fallbacks."""
        candidates_mono = ["Courier New", "Courier", "monospace"]
        candidates_serif = ["Georgia", "Times New Roman", "serif"]

        self.font_title  = pygame.font.SysFont("Georgia", 38, bold=True)
        self.font_hud    = pygame.font.SysFont("Courier New", 22, bold=True)
        self.font_small  = pygame.font.SysFont("Georgia", 16, italic=True)
        self.font_big    = pygame.font.SysFont("Courier New", 48, bold=True)
        self.font_food   = pygame.font.SysFont("Segoe UI Emoji", 18)
        self.font_tiny   = pygame.font.SysFont("Georgia", 13, italic=True)

    # ── Inicializar ronda ──────────────────────
    def _init_round(self):
        cx, cy = COLS // 2, ROWS // 2
        self.snake    = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.dir      = (1, 0)
        self.next_dir = (1, 0)
        self.score    = 0
        self.particles = []
        self.frame    = 0
        self._move_timer  = 0
        self._place_food()

    # ── Colocar comida ─────────────────────────
    def _place_food(self):
        snake_set = set(self.snake)
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in snake_set:
                break
        self.food     = pos
        weights = [35, 25, 20, 8, 12]
        self.food_type = random.choices(FOODS, weights=weights, k=1)[0]

    # ── Level / velocidad dinámica ─────────────
    def _get_level(self):
        return self.score // 100 + 1

    def _get_step_ms(self):
        base = SPEEDS[self.speed_name]
        reduction = min(60, (self._get_level() - 1) * 5)
        return max(60, base - reduction)

    # ──────────────────────────────────────────
    #  LÓGICA DE ACTUALIZACIÓN
    # ──────────────────────────────────────────
    def update(self, dt):
        if self.state != "playing":
            return

        self._move_timer += dt
        if self._move_timer < self._get_step_ms():
            return
        self._move_timer = 0
        self.frame += 1

        # Aplicar dirección
        self.dir = self.next_dir
        dx, dy   = self.dir
        hx, hy   = self.snake[0]
        nx, ny   = hx + dx, hy + dy

        # Colisión con paredes
        if not (0 <= nx < COLS and 0 <= ny < ROWS):
            self.state = "gameover"
            return

        # Colisión consigo misma
        if (nx, ny) in set(self.snake):
            self.state = "gameover"
            return

        self.snake.insert(0, (nx, ny))

        # ¿Comió?
        if (nx, ny) == self.food:
            self.score     += self.food_type["pts"] * self._get_level()
            self.high_score = max(self.high_score, self.score)
            px = nx * TILE + TILE // 2
            py = ny * TILE + TILE // 2 + HUD_HEIGHT
            self._spawn_particles(px, py, self.food_type["glow"])
            self._place_food()
        else:
            self.snake.pop()

        # Actualizar partículas
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.alive]

    def _spawn_particles(self, x, y, color):
        for _ in range(12):
            self.particles.append(Particle(x, y, color))

    # ──────────────────────────────────────────
    #  DIBUJO
    # ──────────────────────────────────────────
    def draw(self):
        self.screen.fill(DARK_BG)
        self._draw_hud()

        gs = self.game_surface
        gs.fill(PARCHMENT)
        self._draw_grid(gs)
        self._draw_grass(gs)
        self._draw_food(gs)
        self._draw_snake(gs)

        self.screen.blit(gs, (0, HUD_HEIGHT))

        # Partículas encima del game surface
        for p in self.particles:
            p.draw(self.screen)

        # Overlays según estado
        if self.state == "menu":
            self._draw_menu()
        elif self.state == "paused":
            self._draw_pause()
        elif self.state == "gameover":
            self._draw_gameover()

        pygame.display.flip()

    # ── HUD ────────────────────────────────────
    def _draw_hud(self):
        pygame.draw.rect(self.screen, FERN,   (0, 0, WIN_W, HUD_HEIGHT))
        pygame.draw.rect(self.screen, BARK,   (0, 0, WIN_W, HUD_HEIGHT), 3)
        pygame.draw.line(self.screen, SAGE,   (0, HUD_HEIGHT - 2), (WIN_W, HUD_HEIGHT - 2), 2)

        # Score
        lbl = self.font_tiny.render("✿ PUNTOS", True, SAGE)
        val = self.font_hud.render(f"{self.score:05d}", True, CREAM)
        self.screen.blit(lbl, (20, 10))
        self.screen.blit(val, (20, 28))

        # Nivel
        lvl = self._get_level()
        flowers = "❀" * min(lvl, 8)
        lbl2 = self.font_tiny.render("❧ NIVEL", True, SAGE)
        flw  = self.font_small.render(flowers, True, DUSTY_ROSE)
        num  = self.font_hud.render(str(lvl), True, GOLDEN)
        self.screen.blit(lbl2, (WIN_W // 2 - 30, 10))
        self.screen.blit(flw,  (WIN_W // 2 - 30, 30))

        # High score
        lbl3 = self.font_tiny.render("✿ RÉCORD", True, SAGE)
        val3 = self.font_hud.render(f"{self.high_score:05d}", True, CREAM)
        self.screen.blit(lbl3, (WIN_W - 130, 10))
        self.screen.blit(val3, (WIN_W - 130, 28))

        # Velocidad actual
        spd_txt = self.font_tiny.render(f"[ {self.speed_name} ]", True, MUSHROOM)
        self.screen.blit(spd_txt, (WIN_W // 2 - 28, 58))

    # ── Cuadrícula ─────────────────────────────
    def _draw_grid(self, surf):
        for x in range(0, WIDTH + 1, TILE):
            pygame.draw.line(surf, GRID_LINE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT + 1, TILE):
            pygame.draw.line(surf, GRID_LINE, (0, y), (WIDTH, y))

    # ── Decoración de pasto ────────────────────
    def _draw_grass(self, surf):
        snake_set = set(self.snake)
        for (gx, gy) in self.grass_spots:
            if (gx, gy) in snake_set or (gx, gy) == self.food:
                continue
            px = gx * TILE + TILE // 2
            py = gy * TILE + TILE - 2
            for i in (-4, 0, 4):
                start = (px + i, py)
                ctrl  = (px + i * 2, py - 8)
                end   = (px + i + (2 if i == 0 else 0), py - 13)
                # Dibujar blade como línea curva aproximada
                steps = 5
                pts = []
                for t_i in range(steps + 1):
                    t = t_i / steps
                    bx = (1-t)**2 * start[0] + 2*(1-t)*t*ctrl[0] + t**2*end[0]
                    by = (1-t)**2 * start[1] + 2*(1-t)*t*ctrl[1] + t**2*end[1]
                    pts.append((int(bx), int(by)))
                if len(pts) >= 2:
                    pygame.draw.lines(surf, SAGE, False, pts, 1)

    # ── Comida ─────────────────────────────────
    def _draw_food(self, surf):
        fx = self.food[0] * TILE
        fy = self.food[1] * TILE
        cx = fx + TILE // 2
        cy = fy + TILE // 2
        pulse = math.sin(pygame.time.get_ticks() * 0.005) * 2

        # Brillo de fondo
        glow_r = int(TILE // 2 + 2 + pulse)
        glow_surf = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
        gr, gg, gb = self.food_type["glow"]
        pygame.draw.circle(glow_surf, (gr, gg, gb, 70), (glow_r, glow_r), glow_r)
        surf.blit(glow_surf, (cx - glow_r, cy - glow_r))

        # Símbolo de la comida
        color = self.food_type["color"]
        char  = self.food_type["char"]

        size = int(TILE - 4 + pulse)
        size = max(8, size)

        if char in ("●", "✿", "★", "♥"):
            font = pygame.font.SysFont("Segoe UI Symbol", size + 4, bold=True)
        else:
            font = pygame.font.SysFont("Segoe UI Emoji", size)

        txt_surf = font.render(char, True, color)
        txt_rect = txt_surf.get_rect(center=(cx, cy))
        surf.blit(txt_surf, txt_rect)

    # ── Serpiente ──────────────────────────────
    def _draw_snake(self, surf):
        for i, (sx, sy) in enumerate(reversed(self.snake)):
            idx = len(self.snake) - 1 - i
            x = sx * TILE
            y = sy * TILE
            is_head = (idx == 0)

            if is_head:
                color = FERN
            elif idx % 2 == 0:
                color = MOSS
            else:
                color = (78, 110, 48)

            # Cuerpo
            rect = pygame.Rect(x + 2, y + 2, TILE - 4, TILE - 4)
            pygame.draw.rect(surf, color, rect, border_radius=4)

            # Highlight
            h_surf = pygame.Surface((TILE - 10, TILE - 10), pygame.SRCALPHA)
            h_surf.fill((255, 255, 255, 25))
            surf.blit(h_surf, (x + 3, y + 3))

            # Sombra
            pygame.draw.rect(surf, SHADOW,
                             pygame.Rect(x + TILE - 5, y + 4, 2, TILE - 6))
            pygame.draw.rect(surf, SHADOW,
                             pygame.Rect(x + 4, y + TILE - 5, TILE - 6, 2))

            if is_head:
                self._draw_eyes(surf, x, y)

    def _draw_eyes(self, surf, x, y):
        dx, dy = self.dir
        if dx == 1:
            eyes = [(x + TILE - 5, y + 5), (x + TILE - 5, y + TILE - 8)]
        elif dx == -1:
            eyes = [(x + 3, y + 5), (x + 3, y + TILE - 8)]
        elif dy == -1:
            eyes = [(x + 5, y + 3), (x + TILE - 8, y + 3)]
        else:
            eyes = [(x + 5, y + TILE - 5), (x + TILE - 8, y + TILE - 5)]

        for ex, ey in eyes:
            pygame.draw.circle(surf, CREAM, (ex, ey), 3)
            pygame.draw.circle(surf, BLACK, (ex + 1, ey + 1), 1)

    # ──────────────────────────────────────────
    #  OVERLAYS
    # ──────────────────────────────────────────
    def _draw_overlay_bg(self, alpha=210):
        overlay = pygame.Surface((WIN_W, WIN_H), pygame.SRCALPHA)
        overlay.fill((*DARK_BG, alpha))
        self.screen.blit(overlay, (0, 0))

        # Marco decorativo
        border = pygame.Rect(WIN_W // 6, WIN_H // 8, WIN_W * 2 // 3, WIN_H * 3 // 4)
        pygame.draw.rect(self.screen, BARK, border, border_radius=6)
        pygame.draw.rect(self.screen, PARCHMENT, border.inflate(-6, -6), border_radius=5)
        pygame.draw.rect(self.screen, MOSS, border.inflate(-6, -6), 2, border_radius=5)
        pygame.draw.rect(self.screen, BARK, border.inflate(-10, -10), 1, border_radius=4)
        return border

    def _center_text(self, text, font, color, y):
        surf = font.render(text, True, color)
        rect = surf.get_rect(centerx=WIN_W // 2, y=y)
        self.screen.blit(surf, rect)

    def _draw_menu(self):
        border = self._draw_overlay_bg()
        by = border.top

        self._center_text("~ La Víborita ~", self.font_title, FERN, by + 30)
        self._center_text("del Jardín Encantado", self.font_small, MUSHROOM, by + 74)
        self._center_text("✿ ❧ ✿", self.font_small, SAGE, by + 96)

        self._center_text("Elige el ritmo:", self.font_small, BARK, by + 126)

        # Botones de velocidad
        speeds = list(SPEEDS.keys())
        bw, bh = 100, 32
        total_w = len(speeds) * bw + (len(speeds) - 1) * 10
        start_x = WIN_W // 2 - total_w // 2
        for i, name in enumerate(speeds):
            bx = start_x + i * (bw + 10)
            rect = pygame.Rect(bx, by + 150, bw, bh)
            active = (name == self.speed_name)
            pygame.draw.rect(self.screen, MOSS if active else PARCHMENT, rect, border_radius=4)
            pygame.draw.rect(self.screen, BARK, rect, 2, border_radius=4)
            color = CREAM if active else BARK
            lbl = self.font_small.render(name, True, color)
            self.screen.blit(lbl, lbl.get_rect(center=rect.center))

        self._center_text("[ ESPACIO ] para comenzar", self.font_hud, FERN, by + 202)

        self._center_text("Flechas / WASD  ·  P = pausa", self.font_tiny, MUSHROOM, by + 238)
        self._center_text("1/2/3 = cambiar velocidad", self.font_tiny, MUSHROOM, by + 255)

    def _draw_pause(self):
        border = self._draw_overlay_bg(180)
        by = border.top
        self._center_text("✿  Pausa  ✿", self.font_title, FERN, by + 60)
        self._center_text("El jardín espera en silencio...", self.font_small, MUSHROOM, by + 110)
        self._center_text("[ P ] para continuar", self.font_hud, MOSS, by + 150)
        self._center_text("[ ESC ] para volver al menú", self.font_tiny, MUSHROOM, by + 185)

    def _draw_gameover(self):
        border = self._draw_overlay_bg()
        by = border.top
        self._center_text("Oh, pobrecita...", self.font_title, BERRY, by + 30)
        self._center_text("La víborita chocó con algo.", self.font_small, MUSHROOM, by + 76)
        self._center_text("El jardín aguarda su regreso.", self.font_small, MUSHROOM, by + 96)

        score_txt = self.font_big.render(str(self.score), True, GOLDEN)
        self.screen.blit(score_txt, score_txt.get_rect(centerx=WIN_W // 2, y=by + 126))
        self._center_text("puntos cosechados", self.font_small, MUSHROOM, by + 182)

        if self.score >= self.high_score and self.score > 0:
            self._center_text("✨ ¡Nuevo récord! ✨", self.font_small, GOLDEN, by + 202)

        self._center_text("[ ESPACIO ] Volver al jardín", self.font_hud, FERN, by + 228)
        self._center_text("[ ESC ] Menú principal", self.font_tiny, MUSHROOM, by + 260)

    # ──────────────────────────────────────────
    #  EVENTOS
    # ──────────────────────────────────────────
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                self._handle_key(event.key)

    def _handle_key(self, key):
        # Cambio de velocidad global
        if key == pygame.K_1:
            self.speed_name = "Lento"
        elif key == pygame.K_2:
            self.speed_name = "Normal"
        elif key == pygame.K_3:
            self.speed_name = "Rápido"

        if self.state == "menu":
            # Ciclar velocidad con flechas izq/der en el menú
            speeds = list(SPEEDS.keys())
            if key in (pygame.K_LEFT, pygame.K_a):
                idx = (speeds.index(self.speed_name) - 1) % len(speeds)
                self.speed_name = speeds[idx]
            elif key in (pygame.K_RIGHT, pygame.K_d):
                idx = (speeds.index(self.speed_name) + 1) % len(speeds)
                self.speed_name = speeds[idx]
            elif key == pygame.K_SPACE or key == pygame.K_RETURN:
                self._init_round()
                self.state = "playing"

        elif self.state == "playing":
            dx, dy = self.dir
            if key in (pygame.K_UP, pygame.K_w) and dy == 0:
                self.next_dir = (0, -1)
            elif key in (pygame.K_DOWN, pygame.K_s) and dy == 0:
                self.next_dir = (0, 1)
            elif key in (pygame.K_LEFT, pygame.K_a) and dx == 0:
                self.next_dir = (-1, 0)
            elif key in (pygame.K_RIGHT, pygame.K_d) and dx == 0:
                self.next_dir = (1, 0)
            elif key == pygame.K_p:
                self.state = "paused"
            elif key == pygame.K_ESCAPE:
                self.state = "menu"

        elif self.state == "paused":
            if key == pygame.K_p:
                self.state = "playing"
            elif key == pygame.K_ESCAPE:
                self.state = "menu"

        elif self.state == "gameover":
            if key == pygame.K_SPACE or key == pygame.K_RETURN:
                self._init_round()
                self.state = "playing"
            elif key == pygame.K_ESCAPE:
                self.state = "menu"

    # ──────────────────────────────────────────
    #  BUCLE PRINCIPAL
    # ──────────────────────────────────────────
    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            self.handle_events()
            self.update(dt)
            self.draw()


# ──────────────────────────────────────────────
if __name__ == "__main__":
    game = ViboritaGame()
    game.run()