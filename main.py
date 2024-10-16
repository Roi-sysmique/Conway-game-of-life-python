import pygame

pygame.init()

game_env = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

SCREEN_HEIGHT = 400
SCREEN_WIDTH = 400

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()
setup_mode = True
game_mode = False
click_pos = None


class Cell(pygame.sprite.Sprite):
    def __init__(self, row, col):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.status = False
        self.width = len(game_env)
        self.image = pygame.surface.Surface((self.width, self.width))
        self.rect = self.image.get_rect()
        self.rect.x = self.col * self.width
        self.rect.y = self.row * self.width
        self.image.fill('green')
        self.last_click_pos = None

    def update(self, last_click_pos):
        global game_env

        if setup_mode and type(last_click_pos) == tuple and last_click_pos != self.last_click_pos:
            self.last_click_pos = last_click_pos
            if self.rect.collidepoint(last_click_pos) and not self.status:
                self.status = True
                game_env[self.row][self.col] = 1
                self.image.fill('red')
            elif self.rect.collidepoint(last_click_pos) and self.status:
                self.status = False
                game_env[self.row][self.col] = 0
                self.image.fill('green')
        else:
            pass


def lines(surface_width, game_environment):
    width_square = len(game_environment)
    for i in range(width_square, surface_width + 1, width_square):
        pygame.draw.line(SCREEN, 'white', (i, 0), (i, surface_width))
        pygame.draw.line(SCREEN, 'white', (0, i), (surface_width, i))


cells = pygame.sprite.Group()
row_num = 0
for row in range(0, len(game_env) + 1):
    for col in range(0, len(game_env) + 1):
        cell = Cell(row=row, col=col)
        print(f"{cell.rect.x} | {cell.rect.y}")
        cells.add(cell)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_pos = event.pos
            print(click_pos)

    cells.draw(SCREEN)
    cells.update(click_pos)
    lines(SCREEN_WIDTH, game_env)
    pygame.display.update()
    CLOCK.tick(300)
