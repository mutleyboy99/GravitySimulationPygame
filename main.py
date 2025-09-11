try: 
    import pygame
except ImportError:
    print("pygame-ce is missing")
    exit()
import math
import copy

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.SRCALPHA)
clock = pygame.time.Clock()
running = True
dt = 0

objects = []
points = []
MAXPOINTS = 1000
stepsize = 100
offset = pygame.Vector2(0, 0)

GRAVITY = 0.000667

center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

def draw_circle_alpha(surface, colour, center, radius):
    target_rect = pygame.Rect(center, (0,0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, colour, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

class PhysicsObject:
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
        pygame.draw.circle(screen, self.colour, self.position + offset, self.radius)
        #pygame.draw.line(screen, self.colour, self.position+self.velocity, self.position+self.velocity * 200)

    def move(self, step_size):
        if step_size != 0:
            if len(points) >= MAXPOINTS:
                points.pop(0)
            points.append([copy.deepcopy(self.position), copy.deepcopy(self.colour)])
        self.draw()
        if self.gravity:
            for item in objects:
                if item is not self:
                    pos_difference = item.position - self.position
                    distance = self.position.distance_to(item.position)
                    if distance == 0:
                        continue

                    gravity_acceleration = (GRAVITY * item.mass * self.mass) / (distance ** 2)

                    acceleration_vector = gravity_acceleration * (pos_difference / distance) / self.mass
                    self.velocity += acceleration_vector * (step_size) * dt

            for item in objects:
                self.position += self.velocity * step_size * dt
        else:
            pass


if __name__ == "__main__":
    PhysicsObject(center, 1000000, 1000, pygame.Vector2(0, 0), (255, 0, 0), False)
    PhysicsObject(center+pygame.Vector2(535, 0), 10, 0.5, pygame.Vector2(0,0.3), (255, 255, 255))
    PhysicsObject(center+pygame.Vector2(500, 0), 15000, 50, pygame.Vector2(0,0.6), (255, 255, 0))
    

    keys = pygame.key.get_pressed()

    while running:
        prev_keys = keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_MINUS] and not prev_keys[pygame.K_MINUS]:
            stepsize -= 10
        if keys[pygame.K_EQUALS] and not prev_keys[pygame.K_EQUALS]:
            stepsize += 10
        if keys[pygame.K_UP]:
            offset += pygame.Vector2(0, 10)
        if keys[pygame.K_DOWN]:
            offset -= pygame.Vector2(0, 10)
        if keys[pygame.K_LEFT]:
            offset += pygame.Vector2(10, 0)
        if keys[pygame.K_RIGHT]:
            offset -= pygame.Vector2(10, 0)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        for point in points:
            radius = float(10 * (points.index(point) / (len(points) - 1))) if len(points) > 1 else 255
            opacity = int(255 * (points.index(point) / (len(points) - 1))) if len(points) > 1 else 255
            draw_circle_alpha(screen, (point[1][0], point[1][1], point[1][2], opacity), point[0] + offset, 2)
        for item in objects:
            item.move(stepsize)


        pygame.display.flip()

        dt = clock.tick(60) / 1000

    pygame.quit()