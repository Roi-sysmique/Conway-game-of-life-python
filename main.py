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
FPS = 300
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
        self.neighbor_positions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                                   (-1, -1), (-1, 1), (1, -1), (1, 1)]

        if self.row == 0:
            self.safe_remove((-1, 0))
            self.safe_remove((-1, -1))
            self.safe_remove((-1, 1))
            if self.col == 0:
                self.safe_remove((0, -1))
                self.safe_remove((1, -1))
            elif self.col == len(game_env) - 1:
                self.safe_remove((0, -1))
                self.safe_remove((1, -1))
        elif self.row == len(game_env) - 1:
            self.safe_remove((1, 0))
            self.safe_remove((1, -1))
            self.safe_remove((1, 1))
            if self.col == 0:
                self.safe_remove((0, -1))
                self.safe_remove((-1, -1))
            if self.col == len(game_env) - 1:
                self.safe_remove((-1, 1))
                self.safe_remove((0, 1))
        elif self.col == 0 and (self.row != 0 and self.row != len(game_env) - 1):
            self.safe_remove((1, -1))
            self.safe_remove((0, -1))
            self.safe_remove((-1, -1))
        elif self.col == len(game_env) - 1 and (self.row != 0 and self.row != len(game_env) - 1):
            self.safe_remove((1, -1))
            self.safe_remove((0, -1))
            self.safe_remove((-1, -1))

        self.cells_to_check = []
        for i in self.neighbor_positions:
            new_row = self.row + i[0]
            new_col = self.col + i[1]
            if 0 <= new_row < len(game_env) and 0 <= new_col < len(game_env[0]):
                self.cells_to_check.append(game_env[new_row][new_col])

    def safe_remove(self, pos):
        if pos in self.neighbor_positions:
            self.neighbor_positions.remove(pos)

    def update(self, last_click_pos):
        global game_env, FPS
        self.cells_to_check = []
        for i in self.neighbor_positions:
            new_row = self.row + i[0]
            new_col = self.col + i[1]
            if 0 <= new_row < len(game_env) and 0 <= new_col < len(game_env[0]):
                self.cells_to_check.append(game_env[new_row][new_col])
        if self.status:
            self.image.fill('white')
        else:
            self.image.fill('black')
        if setup_mode and type(last_click_pos) == tuple and last_click_pos != self.last_click_pos:
            FPS = 300
            self.last_click_pos = last_click_pos
            if self.rect.collidepoint(last_click_pos) and not self.status:
                self.status = True
                game_env[self.row][self.col] = 1
            elif self.rect.collidepoint(last_click_pos) and self.status:
                self.status = False
                game_env[self.row][self.col] = 0

        elif game_mode:
            FPS = 10
            if not self.status and self.cells_to_check.count(1) == 3:
                self.status = True
                game_env[self.row][self.col] = 1
                print(f"live:{self.cells_to_check.count(1)}")
            elif self.status and self.cells_to_check.count(1) < 2 or self.cells_to_check.count(1) > 3:
                self.status = False
                game_env[self.row][self.col] = 0
                print(f"Die:{self.cells_to_check.count(1)}")
            elif self.status and self.cells_to_check.count(1) == 2 or self.cells_to_check.count(1) == 3:
                self.status = True
                game_env[self.row][self.col] = 1
                print(f"Die:{self.cells_to_check.count(1)}")


def lines(surface_width, game_environment):
    width_square = len(game_environment)
    for i in range(width_square, surface_width + 1, width_square):
        pygame.draw.line(SCREEN, 'grey', (i, 0), (i, surface_width))
        pygame.draw.line(SCREEN, 'grey', (0, i), (surface_width, i))


cells = pygame.sprite.Group()
row_num = 0

for row in range(0, len(game_env)):
    for col in range(0, len(game_env)):
        cell = Cell(row=row, col=col)
        cells.add(cell)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and setup_mode:
            click_pos = event.pos
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                setup_mode = False
                game_mode = True
            elif event.key == pygame.K_ESCAPE:
                setup_mode = True
                game_mode = False

    cells.draw(SCREEN)
    cells.update(click_pos)
    lines(SCREEN_WIDTH, game_env)
    pygame.display.update()
    CLOCK.tick(FPS)
