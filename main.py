import os
import sys
import pygame


def load_level(filename):
    try:
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        max_width = max(map(len, level_map))

        return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    except Exception:
        print('Ошибка')
        exit()


filename = input()
level = load_level(filename)

pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 50
running = True


def load_image(name, colorkey=None):
    filename = os.path.join('data', name)
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        raise SystemExit(message)
    except FileNotFoundError as message:
        raise SystemExit(message)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def up(self):
        if level[self.pos_y - 1][self.pos_x] != '#':
            self.pos_y -= 1
            self.rect = self.image.get_rect().move(tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)

    def down(self):
        if level[self.pos_y + 1][self.pos_x] != '#':
            self.pos_y += 1
            self.rect = self.image.get_rect().move(tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)

    def left(self):
        if level[self.pos_y][self.pos_x - 1] != '#':
            self.pos_x -= 1
            self.rect = self.image.get_rect().move(tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)

    def right(self):
        if level[self.pos_y][self.pos_x + 1] != '#':
            self.pos_x += 1
            self.rect = self.image.get_rect().move(tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)


player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


player, level_x, level_y = generate_level(level)

start_screen()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.up()
            elif event.key == pygame.K_DOWN:
                player.down()
            elif event.key == pygame.K_LEFT:
                player.left()
            elif event.key == pygame.K_RIGHT:
                player.right()

    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()
