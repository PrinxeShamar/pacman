import pygame
import pickle
import random  

class Cube():
    def __init__(self, pos, dirn, color):
        self.pos = pos
        self.dirn = dirn
        self.color = color

    def draw(self, game): 
        pygame.draw.rect(game.window, self.color, (self.pos[0]*game.box_size+1,self.pos[1]*game.box_size+1, game.box_size-1, game.box_size-1))

class Food(Cube):
    def draw(self, game):
        pygame.draw.rect(game.window, self.color, (self.pos[0]*game.box_size+10,self.pos[1]*game.box_size+10, game.box_size-20, game.box_size-20))

class Level():
    def __init__(self, game):
        infile = open("basic",'rb')
        walls = pickle.load(infile)
        infile.close()

        self.walls = {}
        for pos in walls:
            self.walls[pos] = Cube(pos, (0,0), (255,255,255)) 

        self.food = {}
        for x in range(game.cols):
            for y in range(game.rows):
                if not (x,y) in self.walls:
                    self.food[(x,y)] = Food((x,y), (0,0), (255, 215, 0))

    
    def draw(self, game):
        for wall in self.walls:
            self.walls[wall].draw(game)
        for food in self.food:
            self.food[food].draw(game)

class PacMan():
    def __init__(self):
        self.character = Cube((24,22), (1,0), (255,255,0))

    def move(self, game):
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                pos = (self.character.pos[0] - 1, self.character.pos[1])
                if not pos in game.level.walls:
                    self.character.dirn = (-1, 0)
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                pos = (self.character.pos[0] + 1, self.character.pos[1])
                if not pos in game.level.walls:
                    self.character.dirn = (1, 0)
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                pos = (self.character.pos[0], self.character.pos[1] - 1)
                if not pos in game.level.walls:
                    self.character.dirn = (0, -1)
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                pos = (self.character.pos[0], self.character.pos[1] + 1)
                if not pos in game.level.walls:
                    self.character.dirn = (0, 1)
        
        pos = (self.character.pos[0] + self.character.dirn[0], self.character.pos[1] + self.character.dirn[1])
        if not pos in game.level.walls:
            self.character.pos = pos

    def eat(self, game):
        if self.character.pos in game.level.food:
            game.level.food.pop(self.character.pos)

    def draw(self, game):
        self.character.draw(game)

class Ghost():
    def __init__(self, color):
        self.character = Cube((34,6), (1,0), color)

    def move(self, game):
        routes = []

        if self.character.dirn != (1,0):
            if not (self.character.pos[0] - 1, self.character.pos[1]) in game.level.walls:
                routes.append((-1, 0))

        if self.character.dirn != (-1,0):
            if not (self.character.pos[0] + 1, self.character.pos[1]) in game.level.walls:
                routes.append((1, 0))

        if self.character.dirn != (0,1):
            if not (self.character.pos[0], self.character.pos[1] - 1) in game.level.walls:
                routes.append((0, -1))

        if self.character.dirn != (0,-1):
            if not (self.character.pos[0], self.character.pos[1] + 1) in game.level.walls:
                routes.append((0, 1))
        
        self.character.dirn = random.choice(routes)
        pos = (self.character.pos[0] + self.character.dirn[0], self.character.pos[1] + self.character.dirn[1])
        if not pos in game.level.walls:
            self.character.pos = pos

    def eat(self, game):
        if game.pacman.character.pos == self.character.pos:
            game.reset()

    def draw(self, game):
        self.character.draw(game)

class Game():
    def __init__(self):
        self.width = 1000
        self.height = 500
        self.box_size = 20
        self.cols = self.width // self.box_size
        self.rows = self.height // self.box_size
        self.window = pygame.display.set_mode((self.width, self.height)) 

        self.clock = pygame.time.Clock()

        self.level = Level(self)
        self.pacman = PacMan()
        self.ghosts = [Ghost((255,0,0)), Ghost((173,216,230)), Ghost((255,192,203)), Ghost((0,255,0))]

        self.loop = True
        self.main_loop()
    
    def draw_window(self):
        self.window.fill((0,0,0))

        self.level.draw(self)
        self.pacman.draw(self)
        for ghost in self.ghosts:
            ghost.draw(self)

        pygame.display.update()
    
    def reset(self):
        self.pacman.__init__()

    def main_loop(self):
        while self.loop:
            pygame.time.delay(50)
            self.clock.tick(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 

            self.pacman.move(self)
            self.pacman.eat(self)

            for ghost in self.ghosts:
                ghost.move(self)
                ghost.eat(self)

            self.draw_window()

if __name__ == "__main__":
    game = Game()    