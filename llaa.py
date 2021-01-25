import os
import sys

import pygame

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tile_width = tile_height = 50
size = []
clock = pygame.time.Clock()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    level = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    size.append(len(level[0]) * tile_width)
    size.append(len(level) * tile_height)
    return level


load_level('map.txt')


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


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


screen = pygame.display.set_mode(size)

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png')


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = load_image('fon.jpg')
    fon = pygame.transform.scale(fon, size)
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(100)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.type = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def get_wall(self):
        return self.type == 'wall'


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, x):
        if x == 8:
            if self.rect.y - tile_height >= 0:
                self.rect = self.rect.move(0, -tile_height)
            a = pygame.sprite.spritecollideany(self, tiles_group)
            if a.get_wall():
                self.rect = self.rect.move(0, tile_height)
            return
        if x == 2:
            if self.rect.y + tile_height <= size[1]:
                self.rect = self.rect.move(0, tile_height)
            a = pygame.sprite.spritecollideany(self, tiles_group)
            if a.get_wall():
                self.rect = self.rect.move(0, -tile_height)
            return
        if x == 4:
            if self.rect.x - tile_width >= 0:
                self.rect = self.rect.move(-tile_width, 0)
            a = pygame.sprite.spritecollideany(self, tiles_group)
            if a.get_wall():
                self.rect = self.rect.move(tile_width, 0)
            return
        if x == 6:
            if self.rect.x + tile_width <= size[0]:
                self.rect = self.rect.move(tile_width, 0)
            a = pygame.sprite.spritecollideany(self, tiles_group)
            if a.get_wall():
                self.rect = self.rect.move(-tile_width, 0)
            return


def main():
    pygame.init()
    start_screen()
    running = True
    player, level_x, level_y = generate_level(load_level('map.txt'))
    while running:
        for event in pygame.event.get():
            if pygame.QUIT == event.type:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player.move(6)
                if event.key == pygame.K_LEFT:
                    player.move(4)
                if event.key == pygame.K_UP:
                    player.move(8)
                if event.key == pygame.K_DOWN:
                    player.move(2)
        screen.fill((255, 255, 255))
        player.update()
        tiles_group.draw(screen)
        player_group.draw(screen)
        clock.tick(50)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
