try: 
    import pygame
except ImportError:
    print("pygame-ce is missing")
    exit()
import math
import copy

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True
dt = 0

objects = []
points = []

GRAVITY = 0.000667

center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

class Object:
    def __init__(self, position, mass, density, velocity, colour, gravity = True):
        self.velocity = velocity 
        self.colour = colour
        self.position = position
        self.mass = mass
        self.density = density #unit mass / unit length ^2
        self.radius = math.sqrt(mass / density)
        self.gravity = gravity
        objects.append(self)

    def draw(self):
        pygame.draw.circle(screen, self.colour, self.position, self.radius)
        pygame.draw.line(screen, self.colour, self.position+self.velocity, self.position+self.velocity * 200)

    def move(self, step_size):
        points.append([copy.deepcopy(self.position), copy.deepcopy(self.colour)])
        self.draw()
        if self.gravity:
            for item in objects:
                if item is not self:
                    pos_difference = item.position - self.position
                    distance = self.position.distance_to(item.position)
                    if distance == 0:
                        continue

                    gravity_acceleration = (GRAVITY * item.mass) / (distance ** 2)

                    acceleration_vector = gravity_acceleration * (pos_difference / distance)
                    self.velocity += acceleration_vector * step_size * dt

                self.position += self.velocity * step_size * dt
        else:
            pass

if __name__ == "__main__":
    Object(center, 1000000, 1000, pygame.Vector2(0,0), "red", False)
    Object(center+pygame.Vector2(640, 0), 10, 0.5, pygame.Vector2(0,0.2), "white")
    Object(center+pygame.Vector2(600, 0), 15000, 50, pygame.Vector2(0,0.5), "yellow")
    

    while running:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        for item in objects:
            item.move(5)
        for point in points:
            pygame.draw.circle(screen, point[1], point[0], 2)

        pygame.display.flip()

        dt = clock.tick(60) / 10

    pygame.quit()