import pygame
import pickle 

def load(filename):
    infile = open(filename,'rb')
    new_dict = pickle.load(infile)
    infile.close()

    painting = {}
    for x in new_dict:
        painting[x] = Cube(x, (0,0), (255,255,255)) 
    return painting

class Cube():
    def __init__(self, pos, dirn, color):
        self.pos = pos
        self.dirn = dirn
        self.color = color

    def draw(self, game): 
        pygame.draw.rect(game.window, self.color, (self.pos[0]*game.box_size+1,self.pos[1]*game.box_size+1, game.box_size-1, game.box_size-1))
    
class Brush():
    def __init__(self):
        self.painting = load("basic")
        
    def draw(self, game):
        for cube in self.painting:
            self.painting[cube].draw(game)

    def paint(self, game):
        if pygame.mouse.get_pressed()[0]:

            x, y = pygame.mouse.get_pos()
            col = x // game.box_size
            row = y // game.box_size

            print(col, row)
            if not (col, row) in self.painting:
                self.painting[(col, row)] = Cube((col, row), (0,0), (255,255,255))
        elif pygame.mouse.get_pressed()[2]:
            
            x, y = pygame.mouse.get_pos()
            col = x // game.box_size
            row = y // game.box_size

            if (col, row) in self.painting:
                self.painting.pop((col, row))

class Game():
    def __init__(self):
        self.width = 1000
        self.height = 500
        self.box_size = 20
        self.cols = self.width // self.box_size
        self.rows = self.height // self.box_size
        self.window = pygame.display.set_mode((self.width, self.height)) 

        self.brush = Brush()

        self.loop = True
        self.main_loop()
    
    def draw_window(self):
        self.window.fill((0,0,0))
        self.brush.draw(self)
        pygame.display.update()
    
    def quit(self):
        painting = list(map(lambda cube: self.brush.painting[cube].pos, self.brush.painting))

        outfile = open("basic",'wb')
        pickle.dump(painting, outfile)
        outfile.close()

    def main_loop(self):
        clock = pygame.time.Clock()

        while self.loop:
            pygame.time.delay(50)
            clock.tick(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_e]:
                    self.quit()
            

            self.brush.paint(self)
            self.draw_window()

if __name__ == "__main__":
    game = Game()    