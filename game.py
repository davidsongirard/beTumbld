import pygame
import sys
import random
import constants
import gridimage
import api
import queue

tag_set = ["horse", "cat", "apple", "dog"]

image_link_set = {}
image_inc = {}
img_queue = queue.Queue()

for i in range(constants.THREAD_POOL_SIZE):
  t = api.ImageDownloader(img_queue)
  t.setDaemon(True)
  t.start()

for tag in tag_set:
  image_link_set[tag] = api.get_by_tag(tag)
  image_inc[tag] = 1

image_bytes = {}
for tag in tag_set:
  image_list = []
  for y in image_link_set[tag]:
    img_queue.put((y, image_list))
  image_bytes[tag] = image_list

img_queue.join()

image_set = {}
for tag, img_bytes in image_bytes.items():
  image_list = []
  for y in image_bytes[tag]:
    image = pygame.image.load(y[0], y[1])
    image_list.append(image)
  image_set[tag] = image_list

def draw_at_grid(surface, grid, image):

  box_size = min(image.get_width(), image.get_height())
  new_image = pygame.Surface((box_size, box_size))
  new_image.blit(image, (0, 0))

  new_image = pygame.transform.scale(new_image, (constants.IMAGE_SIZE,constants.IMAGE_SIZE))

  screen.blit(new_image, (grid[0]*constants.IMAGE_SIZE,grid[1]*constants.IMAGE_SIZE))


def draw_squares(surface, squares):
    screen.fill(constants.BLACK)
    for col_num, col in enumerate(squares):
        for row_num, gi in enumerate(col):
          draw_at_grid(screen, (row_num, col_num), gi.surface)
    pygame.display.flip()

def new_random_square(pos):
    tag = random.sample(tag_set,1)[0]
    if len(image_set[tag]) < 10:
      image_inc[tag] += 1
      new_images = api.get_flickr_by_tag(tag,image_inc[tag])
      for x in new_images:
        image = pygame.image.load(api.get_image(x), x)
        image_set[tag].append(image)
    return gridimage.GridImage(pos,image_set[tag].pop(),tag)

def init_squares():
    sqs = []
    for col in range(constants.IMAGES_WIDE):
        col_list = []
        for row in range(constants.IMAGES_HIGH):
            value = new_random_square((row, col))
            col_list.append(value)
        sqs.append(col_list)

    return sqs

def check_clicks(squares, pos):
    for col in squares:
        for square in col:
            if square is None:
                continue
            if square.check_click(pos):
                return square

def all_same(grids):
    prev = grids[0]
    for grid in grids:
        if grid.value != prev.value:
            return False
        prev = grid
    return True

def move(squares):
    new_cols = []
    for col_num, col in enumerate(squares):
        new_col = [x for x in col if x is not None]
        new_squares = [new_random_square((x, col_num)) for x in range(constants.IMAGES_HIGH - len(new_col))]

        new_cols.append(new_squares + new_col)
    squares[:] = new_cols

def update_positions(squares):
    for col_num, col in enumerate(squares):
        for row_num, square in enumerate(col):
            square.pos = row_num, col_num


pygame.init()
width = constants.IMAGE_SIZE * constants.IMAGES_WIDE
height = constants.IMAGE_SIZE * constants.IMAGES_HIGH
size = width, height

screen = pygame.display.set_mode(size)

screen.fill(constants.BLACK)

squares = init_squares()
clock = pygame.time.Clock()

selected_grids = []

while 1:
    clock.tick(60)
    draw_squares(screen, squares)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                selected_grids.append(check_clicks(squares, event.pos))
                print(check_clicks(squares, event.pos))
                if len(selected_grids) == 3:
                    if all_same(selected_grids):
                        for grid in selected_grids:
                            squares[grid.pos[1]][grid.pos[0]] = None
                    selected_grids = []
                    move(squares)
                    update_positions(squares)
            elif event.button == 3:
                selected_grids = []
