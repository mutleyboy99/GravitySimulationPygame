try: 
    import pygame
except ImportError:
    print("pygame-ce is missing")
    exit()
import math
import copy
import random

# initiating pygame
pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.SRCALPHA)
clock = pygame.time.Clock()
running = True
dt = 0

# Initialising required variables
objects = []
points = []
stepsize = 100
offset = pygame.Vector2(0, 0)
previous_stepsize = 0

# Initialising required constants
MAXPOINTS = 1000
GRAVITY = 0.000667

center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Drawing circles for the trails with alpha channel
def draw_circle_alpha(surface, colour, center, radius):
    target_rect = pygame.Rect(center, (0,0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, colour, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

# Physics object object 
class PhysicsObject:
    def __init__(self, position, mass, density, velocity, colour, gravity = True):
        self.velocity = velocity 
        self.colour = colour
        self.position = position
        self.mass = mass
        self.density = density #unit mass / unit length ^2
        self.acceleration_vector = pygame.Vector2(0,0)
        self.radius = math.sqrt(mass / density)
        self.gravity = gravity
        objects.append(self)

    def draw(self):
        # Drawing the physics objects onto the screen
        pygame.draw.circle(screen, self.colour, self.position + offset, self.radius)
        # Velocity Visualisation for debug:
        pygame.draw.aaline(screen, self.colour, self.position + self.velocity + offset, (self.position+self.velocity * 200) + offset)
        #pygame.draw.aaline(screen, self.colour, self.position, self.position + self.acceleration_vector * 1000)


    # Calculates the gravity and the previous positions of objects for the trail
    def move(self, step_size):
        if step_size != 0:
            if len(points) >= MAXPOINTS:
                points.pop(0)
            points.append([copy.deepcopy(self.position), copy.deepcopy(self.colour), self.radius])
        self.draw()
        # Ability to make it so certain objects do not simulate their gravity or movement
        if self.gravity:
            for item in objects:
                if item is not self:
                    pos_difference = item.position - self.position
                    distance = self.position.distance_to(item.position)
                    if distance == 0:
                        continue

                    # Self.mass not truely necessary for accurate calculation
                    gravity_acceleration = (GRAVITY * item.mass * self.mass) / (distance ** 2)
                    self.acceleration_vector = gravity_acceleration * (pos_difference / distance) / self.mass
                    self.velocity += self.acceleration_vector * (step_size) * dt

            for item in objects:
                self.position += self.velocity * step_size * dt
        else:
            pass


if __name__ == "__main__":
    # Place physics objects here:
    PhysicsObject(center, 1000000, 1000, pygame.Vector2(0, 0), (255, 0, 0), False)
    PhysicsObject(center+pygame.Vector2(535, 0), 10, 0.5, pygame.Vector2(0,0.3), (255, 255, 255))
    PhysicsObject(center+pygame.Vector2(500, 0), 15000, 50, pygame.Vector2(0,0.6), (255, 255, 0))
    # EndBlock

    keys = pygame.key.get_pressed()
    
    while running:
        prev_keys = keys
        keys = pygame.key.get_pressed()
        # Exit keybind
        if keys[pygame.K_ESCAPE] and not prev_keys[pygame.K_ESCAPE]:
            running = False
        # Time step increase and decrease
        if keys[pygame.K_MINUS] and not prev_keys[pygame.K_MINUS]:
            stepsize -= 10
        if keys[pygame.K_EQUALS] and not prev_keys[pygame.K_EQUALS]:
            stepsize += 10
        # Movement keybinds
        if keys[pygame.K_UP]:
            offset += pygame.Vector2(0, 10)
        if keys[pygame.K_DOWN]:
            offset -= pygame.Vector2(0, 10)
        if keys[pygame.K_LEFT]:
            offset += pygame.Vector2(10, 0)
        if keys[pygame.K_RIGHT]:
            offset -= pygame.Vector2(10, 0)
        # Reset camera to origin
        if keys[pygame.K_BACKSPACE] and not prev_keys[pygame.K_BACKSPACE]:
            offset = pygame.Vector2(0, 0)
        # Pause / Play
        if keys[pygame.K_SPACE] and not prev_keys[pygame.K_SPACE]:
            if stepsize != 0:
                previous_stepsize = stepsize
                stepsize = 0
            else:
                stepsize = previous_stepsize

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear screen
        screen.fill("black")

        # Draw trails behind objects
        for point in points:
            radius = float(random.uniform(0.9, 1) * point[2] / 1.5 * (points.index(point) / (len(points) - 1))) if len(points) > 1 else 255
            opacity = float(random.uniform(0.9, 1) * 255 * (points.index(point) / (len(points) - 1))) if len(points) > 1 else 255
            draw_circle_alpha(screen, (point[1][0], point[1][1], point[1][2], opacity), point[0] + offset, radius)
        # Move objects
        for item in objects:
            item.move(stepsize)

        # Update frame
        pygame.display.flip()
        dt = clock.tick(60) / 1000

    pygame.quit()