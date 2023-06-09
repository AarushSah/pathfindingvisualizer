import pygame
from heapq import heappush, heappop

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.width = width
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.parent = None
        self.f_score = float("inf")
        self.g_score = float("inf")
        self.is_wall = False
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall: # up
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.row < len(grid) - 1 and not grid[self.row + 1][self.col].is_wall: # down
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall: # left
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.col < len(grid[0]) - 1 and not grid[self.row][self.col + 1].is_wall: # right
            self.neighbors.append(grid[self.row][self.col + 1])

    def get_pos(self):
        return self.row, self.col

    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.color = PURPLE
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = []
    heappush(open_set, (0, count, start))
    g_scores = {spot: float("inf") for row in grid for spot in row}
    g_scores[start] = 0
    f_scores = {spot: float("inf") for row in grid for spot in row}
    f_scores[start] = h(start.get_pos(), end.get_pos())
    came_from = {}

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = heappop(open_set)[2]

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.color = GREEN
            return True

        for neighbor in current.neighbors:
            tentative_g_score = g_scores[current] + 1

            if tentative_g_score < g_scores[neighbor]:
                came_from[neighbor] = current
                g_scores[neighbor] = tentative_g_score
                f_scores[neighbor] = tentative_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set:
                    count += 1
                    heappush(open_set, (f_scores[neighbor], count, neighbor))
                    neighbor.color = YELLOW

        draw()

        if current != start:
            current.color = GREY

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap)
            grid[i].append(spot)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.color = ORANGE
                elif not end and spot != start:
                    end = spot
                    end.color = RED
                elif spot != start and spot != end:
                    spot.is_wall = True
            elif pygame.mouse.get_pressed()[2]: # right mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.is_wall = False
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)
