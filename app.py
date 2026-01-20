import pygame as pg
import random

class Player(pg.sprite.Sprite):
    def __init__(self, x,):
        super().__init__()
        self.x = x
        self.radius = 50
        self.rect = pg.Rect(self.x - self.radius, 600 - self.radius, self.radius * 2, self.radius * 2)

    def move(self, dx, rad):
        self.radius = rad
        self.x += dx
        self.x = max(rad, min(self.x, 1200 - rad))
        self.rect = pg.Rect(self.x - rad, 600 - rad, rad * 2, rad * 2)
        self.rect.center = (int(self.x), 600)
        return self.x
    
    def draw(self, screen, rad):
        pg.draw.circle(screen, (255, 0, 0), (int(self.x), 600), rad)

class fallingObject(pg.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.x = random.randint(20, 1180)
        self.colour = ((random.randint(0, 255)), (random.randint(0, 255)), (random.randint(0, 255)))
        self.speed = 420
        self.y = y
        self.radius = 20
        self.rect = pg.Rect(self.x - 20, self.y - 20, 40, 40)
    
    def update(self, dt):
        self.y += self.speed * dt
        self.y = max(0, min(self.y, 800))
        self.rect.center = (int(self.x), int(self.y))
        if self.y >= 800:
            self.kill()
    
    def draw(self, screen):
        pg.draw.circle(screen, (self.colour), (int(self.x), int(self.y)), 20)

def printScore(score, screen):
    font = pg.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

def main():   
    pg.init()
    screen = pg.display.set_mode((1200, 800))
    clock = pg.time.Clock()
    spawn_interval = 1000
    last_spawn_time = pg.time.get_ticks()
    max_objects = 15
    size = 50
    score = 0
    speed = 350          
    modify_size = True
    ball = Player(600)   
    fallingBoi = fallingObject(0)
    falling_group = pg.sprite.Group()
    falling_group.add(fallingBoi)
    running = True
    while running:
        dt = clock.tick(60) / 1000

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        keys = pg.key.get_pressed()
        direction = keys[pg.K_d] - keys[pg.K_a]
        ball.move(direction * speed * dt, size)
        
        current_time = pg.time.get_ticks()
        if current_time - last_spawn_time > spawn_interval and len(falling_group) < max_objects:
            falling_group.add(fallingObject(0))
            last_spawn_time = current_time

        collided_objects = pg.sprite.spritecollide(ball, falling_group, dokill=True)
        for obj in collided_objects:
            obj.kill()
            if size < 170 and modify_size == True:
                size += 10
            else:
                if size >= 80:
                    size -= 10
                speed += 10
                modify_size = False
            if speed > 800:
                ball.kill()
            
            score += 1
            print(f"Score: {score}")

        falling_group.update(dt)

        screen.fill((0, 0, 0))
        ball.draw(screen, size)
        for i in falling_group:
            i.draw(screen)

        printScore(score, screen)
        pg.display.flip()
main()