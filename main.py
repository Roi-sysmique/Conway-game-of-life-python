import pygame

pygame.init()

SCREEN_LENGTH = 750
square_length = 15
cell_length = (SCREEN_LENGTH + 200)/square_length
game_env = [[0 for _ in range(int(cell_length))] for _ in range(int(cell_length))]
SCREEN = pygame.display.set_mode((SCREEN_LENGTH, SCREEN_LENGTH))
CLOCK = pygame.time.Clock()
FPS = 300
setup_mode = True
setup_mode_fps = 300
game_mode = False
game_mode_fps = 10
click_pos = None


class Cell(pygame.sprite.Sprite):
    def __init__(self, row, col):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.status = False
        self.width = square_length
        self.image = pygame.surface.Surface((self.width, self.width))
        self.rect = self.image.get_rect()
        self.rect.x = (self.col * self.width) - 100
        self.rect.y = (self.row * self.width) - 100
        self.last_click_pos = None
        self.neighbor_positions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                                   (-1, -1), (-1, 1), (1, -1), (1, 1)]

        if self.row == 0:
            self.neighbor_positions.remove((-1, 0))
            self.neighbor_positions.remove((-1, -1))
            self.neighbor_positions.remove((-1, 1))
            if self.col == 0:
                self.neighbor_positions.remove((0, -1))
                self.neighbor_positions.remove((1, -1))
            elif self.col == len(game_env) - 1:
                self.neighbor_positions.remove((0, 1))
                self.neighbor_positions.remove((1, 1))
        elif self.row == len(game_env) - 1:
            self.neighbor_positions.remove((1, 0))
            self.neighbor_positions.remove((1, -1))
            self.neighbor_positions.remove((1, 1))
            if self.col == 0:
                self.neighbor_positions.remove((0, -1))
                self.neighbor_positions.remove((-1, -1))
            if self.col == len(game_env) - 1:
                self.neighbor_positions.remove((-1, 1))
                self.neighbor_positions.remove((0, 1))
        elif self.col == 0 and (self.row != 0 and self.row != len(game_env) - 1):
            self.neighbor_positions.remove((1, 1))
            self.neighbor_positions.remove((0, 1))
            self.neighbor_positions.remove((-1, -1))
        elif self.col == len(game_env) - 1 and (self.row != 0 and self.row != len(game_env) - 1):
            self.neighbor_positions.remove((1, 1))
            self.neighbor_positions.remove((0, 1))
            self.neighbor_positions.remove((-1, 1))

        self.cells_to_check = None

    def update(self, last_click_pos):
        global game_env, FPS

        self.cells_to_check = []
        for _ in self.neighbor_positions:
            new_row = self.row + _[0]
            new_col = self.col + _[1]
            self.cells_to_check.append(game_env[new_row][new_col])
        if self.status:
            self.image.fill((50, 50, 50))
        else:
            self.image.fill((200, 200, 200))

        if setup_mode and type(last_click_pos) == tuple and last_click_pos != self.last_click_pos:
            FPS = setup_mode_fps
            self.last_click_pos = last_click_pos
            if self.rect.collidepoint(last_click_pos) and not self.status:
                self.status = True
                game_env[self.row][self.col] = 1
            elif self.rect.collidepoint(last_click_pos) and self.status:
                self.status = False
                game_env[self.row][self.col] = 0

        elif game_mode:
            FPS = game_mode_fps
            if not self.status and self.cells_to_check.count(1) == 3:
                self.status = True
                self.image.fill((10, 200, 100))
            elif self.status and self.cells_to_check.count(1) < 2 or self.cells_to_check.count(1) > 3:
                self.status = False
                self.image.fill((200, 100, 10))

            elif self.status and self.cells_to_check.count(1) >= 2 and self.cells_to_check.count(1) <= 3:
                self.status = True
                self.image.fill((10, 100, 200))


cells = pygame.sprite.Group()

for row in range(0, len(game_env)):
    for col in range(0, len(game_env)):
        cell = Cell(row=row, col=col)
        cells.add(cell)
while True:
    mouse_keys = pygame.mouse.get_pressed(3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if mouse_keys[0] and setup_mode:
            click_pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                setup_mode = False
                game_mode = True
            elif event.key == pygame.K_ESCAPE:
                setup_mode = True
                game_mode = False

    cells.draw(SCREEN)
    cells.update(click_pos)
    if game_mode:
        for i in cells:
            if i.status:
                game_env[i.row][i.col] = 1
            elif not i.status:
                game_env[i.row][i.col] = 0
    pygame.display.update()
    CLOCK.tick(FPS)
