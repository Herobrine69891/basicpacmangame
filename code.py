import pygame
import math
import random
import os

# --- Constants ---
TILE_SIZE = 20 
FPS = 60
BLACK, WHITE, YELLOW = (0, 0, 0), (255, 255, 255), (255, 255, 0)
BLUE, RED, PINK = (0, 0, 255), (255, 0, 0), (255, 182, 193)
CYAN, ORANGE, GREEN = (0, 255, 255), (255, 165, 0), (0, 255, 0)

# --- High Score Logic (Universal Formatting) ---
def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            try:
                line = f.read().split(",")
                return line[0], int(line[1]) 
            except:
                return "None", 0
    return "None", 0

def save_high_score(name, score):
    with open("highscore.txt", "w") as f:
        # Using .format() to avoid SyntaxErrors on older Python versions
        f.write("{},{}".format(name, score))

# --- MAP 1 ---
MAP_1 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
    [1,2,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,2,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,0,1,1,1,1,1,3,3,3,3,1,1,1,1,1,0,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,1,1,3,3,3,3,3,3,3,3,3,3,1,1,0,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,1,1,3,1,1,1,3,3,1,1,1,3,1,1,0,1,1,1,1,1,1],
    [3,0,0,0,0,0,0,3,3,3,1,3,3,3,3,3,3,1,3,3,3,0,0,0,0,0,0,3], # Portal Row
    [1,1,1,1,1,1,0,1,1,3,1,1,1,1,1,1,1,1,3,1,1,0,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,1,1,3,1,1,1,1,1,1,1,1,3,1,1,0,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
    [1,2,0,0,1,1,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,1,1,0,0,2,1],
    [1,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,1],
    [1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

ALL_MAZES = [MAP_1]

class GameState:
    def __init__(self):
        self.player_name = ""
        self.hi_name, self.hi_score = load_high_score()
        self.score = 0
        self.lives = 3
        self.level = 1
        self.maze = [row[:] for row in ALL_MAZES[0]]
        self.screen_offset = 60
        self.state = "NAME_ENTRY"
        self.dots_eaten = 0
        self.fruit_active = False
        self.fruit_timer = 0
        self.fruit_pos = (13 * TILE_SIZE, 12 * TILE_SIZE)

class Pacman:
    def __init__(self, x, y):
        self.start_pos = (x * TILE_SIZE, y * TILE_SIZE)
        self.x, self.y = self.start_pos
        self.vel_x, self.vel_y = 0, 0
        self.req_x, self.req_y = 0, 0
        self.speed = 2
        self.anim = 0

    def update(self, maze):
        if self.x < -TILE_SIZE//2: self.x = (len(maze[0]) - 1) * TILE_SIZE
        elif self.x > (len(maze[0]) - 1) * TILE_SIZE + TILE_SIZE//2: self.x = 0
        if self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0:
            grid_x, grid_y = int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)
            if 0 <= grid_x < len(maze[0]):
                nx, ny = grid_x + self.req_x, grid_y + self.req_y
                if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]) and maze[ny][nx] != 1:
                    self.vel_x, self.vel_y = self.req_x, self.req_y
                cx, cy = grid_x + self.vel_x, grid_y + self.vel_y
                if 0 <= cy < len(maze) and 0 <= cx < len(maze[0]) and maze[cy][cx] == 1:
                    self.vel_x, self.vel_y = 0, 0
        self.x += self.vel_x * self.speed
        self.y += self.vel_y * self.speed
        if self.vel_x != 0 or self.vel_y != 0: self.anim = (self.anim + 1) % 10

    def draw(self, screen, offset):
        center = (int(self.x + TILE_SIZE//2), int(self.y + TILE_SIZE//2 + offset))
        pygame.draw.circle(screen, YELLOW, center, TILE_SIZE//2 - 2)
        if self.anim < 5: pygame.draw.circle(screen, BLACK, center, 4)

class Ghost:
    def __init__(self, x, y, color):
        self.start_pos = (x * TILE_SIZE, y * TILE_SIZE)
        self.x, self.y = self.start_pos
        self.color = color
        self.speed = 1
        self.dir = (0, -1)
        self.frightened = False

    def move(self, maze, target_x, target_y):
        if self.x < -TILE_SIZE//2: self.x = (len(maze[0]) - 1) * TILE_SIZE
        elif self.x > (len(maze[0]) - 1) * TILE_SIZE + TILE_SIZE//2: self.x = 0
        if self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0:
            grid_x, grid_y = int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)
            if 0 <= grid_x < len(maze[0]):
                dirs = [(0,1), (0,-1), (1,0), (-1,0)]
                valid = [d for d in dirs if not (d[0]==-self.dir[0] and d[1]==-self.dir[1])]
                valid = [d for d in valid if 0<=grid_y+d[1]<len(maze) and 0<=grid_x+d[0]<len(maze[0]) and maze[grid_y+d[1]][grid_x+d[0]] != 1]
                if valid:
                    if self.frightened: self.dir = random.choice(valid)
                    else: self.dir = min(valid, key=lambda d: math.hypot((self.x+d[0]*TILE_SIZE)-target_x, (self.y+d[1]*TILE_SIZE)-target_y))
                else: self.dir = (-self.dir[0], -self.dir[1])
        self.x += self.dir[0] * self.speed
        self.y += self.dir[1] * self.speed

    def draw(self, screen, offset):
        c = (50, 50, 255) if self.frightened else self.color
        pygame.draw.ellipse(screen, c, (int(self.x), int(self.y + offset), TILE_SIZE, TILE_SIZE))

def main():
    pygame.init()
    game = GameState()
    screen = pygame.display.set_mode((28*TILE_SIZE, 22*TILE_SIZE + game.screen_offset))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 18, bold=True)
    big_font = pygame.font.SysFont("monospace", 40, bold=True)

    def spawn():
        return Pacman(13, 16), [Ghost(13, 10, RED), Ghost(14, 10, PINK), Ghost(12, 10, CYAN), Ghost(15, 10, ORANGE)]

    pacman, ghosts = spawn()
    power_timer = 0
    running = True

    while running:
        screen.fill(BLACK)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: running = False
            
            if game.state == "NAME_ENTRY":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(game.player_name) > 0:
                        game.state = "START"
                    elif event.key == pygame.K_BACKSPACE:
                        game.player_name = game.player_name[:-1]
                    else:
                        if len(game.player_name) < 10 and event.unicode.isalnum():
                            game.player_name += event.unicode.upper()

            elif event.type == pygame.KEYDOWN:
                if game.state == "START": game.state = "PLAY"
                if game.state == "GAMEOVER" and event.key == pygame.K_r:
                    old_name = game.player_name
                    game = GameState()
                    game.player_name = old_name
                    pacman, ghosts = spawn()
                    game.state = "PLAY"
                if game.state == "WIN" and event.key == pygame.K_c:
                    game.level += 1
                    game.maze = [row[:] for row in ALL_MAZES[(game.level-1)%len(ALL_MAZES)]]
                    game.dots_eaten = 0; game.fruit_active = False
                    pacman.x, pacman.y = pacman.start_pos
                    for g in ghosts: g.x, g.y = g.start_pos
                    game.state = "PLAY"
                
                if game.state == "PLAY":
                    if event.key == pygame.K_UP: pacman.req_x, pacman.req_y = 0, -1
                    elif event.key == pygame.K_DOWN: pacman.req_x, pacman.req_y = 0, 1
                    elif event.key == pygame.K_LEFT: pacman.req_x, pacman.req_y = -1, 0
                    elif event.key == pygame.K_RIGHT: pacman.req_x, pacman.req_y = 1, 0

        if game.state == "PLAY":
            pacman.update(game.maze)
            px, py = int(pacman.x//TILE_SIZE), int(pacman.y//TILE_SIZE)
            
            if 0 <= py < len(game.maze) and 0 <= px < len(game.maze[0]):
                if game.maze[py][px] in [0, 2]:
                    val = game.maze[py][px]
                    game.maze[py][px] = 3
                    game.score += 10 if val == 0 else 50
                    game.dots_eaten += 1
                    if val == 2:
                        power_timer = 400
                        for g in ghosts: g.frightened = True
                    if game.dots_eaten == 50:
                        game.fruit_active = True
                        game.fruit_timer = 600

            if game.fruit_active:
                game.fruit_timer -= 1
                if math.hypot(pacman.x - game.fruit_pos[0], pacman.y - game.fruit_pos[1]) < TILE_SIZE:
                    game.score += 500; game.fruit_active = False
                if game.fruit_timer <= 0: game.fruit_active = False

            if power_timer > 0:
                power_timer -= 1
                if power_timer == 0:
                    for g in ghosts: g.frightened = False

            for g in ghosts:
                g.move(game.maze, pacman.x, pacman.y)
                if math.hypot(pacman.x - g.x, pacman.y - g.y) < TILE_SIZE:
                    if g.frightened:
                        game.score += 200; g.x, g.y = g.start_pos; g.frightened = False
                    else:
                        game.lives -= 1
                        if game.lives <= 0:
                            if game.score > game.hi_score: 
                                save_high_score(game.player_name, game.score)
                            game.state = "GAMEOVER"
                        else:
                            pacman.x, pacman.y = pacman.start_pos
                            for ghost in ghosts: ghost.x, ghost.y = ghost.start_pos

            if not any(0 in r or 2 in r for r in game.maze): game.state = "WIN"

        # --- DRAWING ---
        if game.state == "NAME_ENTRY":
            screen.blit(big_font.render("ENTER YOUR NAME", True, YELLOW), (100, 200))
            screen.blit(big_font.render(game.player_name + "_", True, WHITE), (200, 260))
            screen.blit(font.render("PRESS ENTER TO START", True, GREEN), (180, 350))

        elif game.state in ["START", "PLAY"]:
            for r, row in enumerate(game.maze):
                for c, val in enumerate(row):
                    pos = (c*TILE_SIZE + TILE_SIZE//2, r*TILE_SIZE + game.screen_offset + TILE_SIZE//2)
                    if val == 1: pygame.draw.rect(screen, BLUE, (c*TILE_SIZE, r*TILE_SIZE+game.screen_offset, TILE_SIZE, TILE_SIZE), 1)
                    elif val == 0: pygame.draw.circle(screen, WHITE, pos, 2)
                    elif val == 2: pygame.draw.circle(screen, WHITE, pos, 6)
            
            if game.fruit_active:
                f_pos = (int(game.fruit_pos[0] + TILE_SIZE//2), int(game.fruit_pos[1] + game.screen_offset + TILE_SIZE//2))
                pygame.draw.circle(screen, GREEN, f_pos, 8)
            
            pacman.draw(screen, game.screen_offset)
            for g in ghosts: g.draw(screen, game.screen_offset)
            
            # Universal formatting for the HUD
            score_txt = "{}: {} | BEST: {} ({})".format(game.player_name, game.score, game.hi_name, game.hi_score)
            screen.blit(font.render(score_txt, True, WHITE), (10, 10))
            life_txt = "LIVES: {} | FRUIT IN: {}".format(game.lives, max(0, 50-game.dots_eaten) if game.dots_eaten < 50 else 'ACTIVE!')
            screen.blit(font.render(life_txt, True, WHITE), (10, 30))

            if game.state == "START": screen.blit(font.render("READY! PRESS ANY KEY", True, YELLOW), (180, 300))
        
        elif game.state == "WIN":
            screen.fill(BLACK)
            screen.blit(big_font.render("YOU WIN!", True, YELLOW), (180, 200))
            screen.blit(font.render("PRESS 'C' FOR NEXT MAP", True, YELLOW), (150, 350))
        
        elif game.state == "GAMEOVER":
            screen.fill(BLACK)
            screen.blit(big_font.render("GAME OVER", True, RED), (160, 200))
            if game.score >= game.hi_score:
                msg = "NEW RECORD {}!".format(game.player_name)
                screen.blit(font.render(msg, True, YELLOW), (170, 280))
            screen.blit(font.render("PRESS 'R' TO RESTART", True, YELLOW), (170, 370))

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()

