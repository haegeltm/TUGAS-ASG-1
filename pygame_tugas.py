import pygame
import random
import time

pygame.init()

# ----- WINDOW SETTINGS -----
WIDTH, HEIGHT = 720, 540
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Card – Pastel Edition")

FONT = pygame.font.SysFont("centurygothic", 22)
BIG_FONT = pygame.font.SysFont("centurygothic", 50)

# ----- COLORS (Pastel aesthetic) -----
CREAM = (255, 246, 230)
SOFT_PINK = (255, 204, 213)
SOFT_BLUE = (186, 210, 255)
SOFT_PURPLE = (214, 201, 255)
SOFT_GREEN = (204, 255, 234)
DARK_TEXT = (60, 60, 60)

# ----- DATA PAIRS -----
pairs = {
    "Indonesia": "Jakarta",
    "Jepang": "Tokyo",
    "Italia": "Roma",
    "Brazil": "Brasília",
    "Australia": "Canberra",
    "Mesir": "Kairo",
    "Thailand": "Bangkok",
    "Turki": "Ankara"
}

# Flatten card list
cards = list(pairs.keys()) + list(pairs.values())
random.shuffle(cards)

# ----- CARD SETTINGS -----
ROWS, COLS = 4, 4
CARD_W = WIDTH // COLS
CARD_H = HEIGHT // ROWS

revealed = [False] * len(cards)
selected = []

# ----- Pretty Card Colors -----
CARD_COLORS = [SOFT_PINK, SOFT_PURPLE, SOFT_BLUE, SOFT_GREEN]


def draw_rounded_rect(surface, color, rect, radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def draw_board():
    WIN.fill(CREAM)

    for idx, text in enumerate(cards):
        row = idx // COLS
        col = idx % COLS
        x = col * CARD_W + 5
        y = row * CARD_H + 5
        rect = (x, y, CARD_W - 10, CARD_H - 10)

        # Choose pastel color per column so visual harmonis
        card_color = CARD_COLORS[col % len(CARD_COLORS)]

        if revealed[idx]:
            draw_rounded_rect(WIN, card_color, rect, 20)
            txt = FONT.render(text, True, DARK_TEXT)
            WIN.blit(txt, (x + 12, y + CARD_H // 2 - 10))
        else:
            draw_rounded_rect(WIN, (255, 228, 230), rect, 20)  # soft very light pink
            q_txt = FONT.render("?", True, DARK_TEXT)
            WIN.blit(q_txt, (x + CARD_W // 2 - 10, y + CARD_H // 2 - 12))

    pygame.display.update()


def check_match(i1, i2):
    v1, v2 = cards[i1], cards[i2]
    if (v1 in pairs and pairs[v1] == v2) or (v2 in pairs and pairs[v2] == v1):
        return True
    return False


def win_screen():
    WIN.fill(CREAM)
    msg = BIG_FONT.render("You Win!", True, SOFT_PURPLE)
    WIN.blit(msg, (WIDTH // 2 - msg.get_width() // 2,
                   HEIGHT // 2 - 40))

    pygame.display.update()
    time.sleep(3)


# ----- GAME LOOP -----
running = True
while running:
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            col = mx // CARD_W
            row = my // CARD_H
            idx = row * COLS + col

            if not revealed[idx] and len(selected) < 2:
                revealed[idx] = True
                selected.append(idx)

            if len(selected) == 2:
                draw_board()
                pygame.time.delay(700)

                i1, i2 = selected
                if not check_match(i1, i2):
                    revealed[i1] = False
                    revealed[i2] = False

                selected = []

                if all(revealed):
                    win_screen()
                    running = False

pygame.quit()