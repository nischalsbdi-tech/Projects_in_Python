import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
FPS = 60

# Colors
BLACK = (10, 10, 18)
WHITE = (255, 255, 255)
CYAN = (0, 255, 240)
ORANGE = (255, 120, 0)
RED = (255, 50, 50)

# Setup Screen and Clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Vector Space Shooter")
clock = pygame.time.Clock()


class Particle:
    """Manages a single glowing exhaust or explosion particle using basic physics."""

    def __init__(self, x, y, dx, dy, color):
        self.x = x
        self.y = y
        self.dx = dx + random.uniform(-1, 1)
        self.dy = dy + random.uniform(-1, 1)
        self.life = random.randint(20, 40)
        self.max_life = self.life
        self.color = color

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

    def draw(self, surface):
        alpha = int((self.life / self.max_life) * 255)
        # Create a tiny surface for alpha blending (transparency fade)
        size = max(2, int(self.life / 8))
        p_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(p_surf, (*self.color, alpha), (size, size), size)
        surface.blit(p_surf, (int(self.x - size), int(self.y - size)))


class Ship:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.radius = 15
        self.angle = 0  # In degrees
        self.dx = 0  # Velocity X
        self.dy = 0  # Velocity Y
        self.acceleration = 0.15
        self.friction = 0.985
        self.rotation_speed = 4.5

    def update(self, keys, particles):
        # Rotate Ship
        if keys[pygame.K_LEFT]:
            self.angle -= self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.angle += self.rotation_speed

        # Thrust (Math: Using Trigonometry to find heading vector)
        rad = math.radians(self.angle)
        if keys[pygame.K_UP]:
            self.dx += math.cos(rad) * self.acceleration
            self.dy += math.sin(rad) * self.acceleration

            # Emit engine thrust particles backwards
            back_x = self.x - math.cos(rad) * self.radius
            back_y = self.y - math.sin(rad) * self.radius
            particles.append(Particle(back_x, back_y, -math.cos(rad) * 3, -math.sin(rad) * 3, ORANGE))

        # Apply Momentum and Friction
        self.x += self.dx
        self.y += self.dy
        self.dx *= self.friction
        self.dy *= self.friction

        # Screen Wrap-around
        self.x %= SCREEN_WIDTH
        self.y %= SCREEN_HEIGHT

    def draw(self, surface):
        rad = math.radians(self.angle)
        # Calculate the 3 vertices of the triangle ship using polar coordinates
        tip = (self.x + math.cos(rad) * self.radius * 1.5, self.y + math.sin(rad) * self.radius * 1.5)
        left = (self.x + math.cos(rad + 2.5) * self.radius, self.y + math.sin(rad + 2.5) * self.radius)
        right = (self.x + math.cos(rad - 2.5) * self.radius, self.y + math.sin(rad - 2.5) * self.radius)

        pygame.draw.polygon(surface, CYAN, [tip, left, right], 2)


class Laser:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        rad = math.radians(angle)
        self.speed = 10       
        self.dx = math.cos(rad) * self.speed
        self.dy = math.sin(rad) * self.speed
        self.life = 60  # Disappears after 60 frames

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

    def draw(self, surface):
        pygame.draw.line(surface, RED, (self.x, self.y), (self.x - self.dx * 0.5, self.y - self.dy * 0.5), 3)


class Asteroid:
    def __init__(self, x=None, y=None, radius=40):
        self.x = x if x is not None else random.choice([0, SCREEN_WIDTH])
        self.y = y if y is not None else random.randint(0, SCREEN_HEIGHT)
        self.radius = radius
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1, 3.5)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

        # Generate custom rigid bumpy vector shape for asteroid geometry
        self.points = []
        num_points = 12
        for i in range(num_points):
            a = (i / num_points) * math.pi * 2
            r = self.radius * random.uniform(0.75, 1.25)
            self.points.append((math.cos(a) * r, math.sin(a) * r))

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.x %= SCREEN_WIDTH
        self.y %= SCREEN_HEIGHT

    def draw(self, surface):
        transformed_points = [(self.x + px, self.y + py) for px, py in self.points]
        pygame.draw.polygon(surface, WHITE, transformed_points, 1)


# Game entities initialization
ship = Ship()
lasers = []
asteroids = [Asteroid() for _ in range(5)]
particles = []
score = 0
font = pygame.font.SysFont("Courier New", 24, bold=True)

# Main Loop
running = True
while running:
    # 1. Input Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Spawn laser at ship's nose tip
                rad = math.radians(ship.angle)
                tip_x = ship.x + math.cos(rad) * ship.radius * 1.5
                tip_y = ship.y + math.sin(rad) * ship.radius * 1.5
                lasers.append(Laser(tip_x, tip_y, ship.angle))

    keys = pygame.key.get_pressed()

    # 2. Physics & Engine Updates
    ship.update(keys, particles)

    for laser in lasers[:]:
        laser.update()
        if laser.life <= 0:
            lasers.remove(laser)

    for asteroid in asteroids:
        asteroid.update()

    for particle in particles[:]:
        particle.update()
        if particle.life <= 0:
            particles.remove(particle)

    # 3. Trigonometric Distance Collisions
    for laser in lasers[:]:
        for asteroid in asteroids[:]:
            # Math: Euclidean distance formula d = sqrt((x2-x1)^2 + (y2-y1)^2)
            distance = math.hypot(laser.x - asteroid.x, laser.y - asteroid.y)
            if distance < asteroid.radius:
                # Trigger Explosion Particles
                for _ in range(15):
                    particles.append(
                        Particle(asteroid.x, asteroid.y, random.uniform(-3, 3), random.uniform(-3, 3), WHITE))

                # Split large asteroids into smaller fragments
                if asteroid.radius > 20:
                    asteroids.append(Asteroid(asteroid.x, asteroid.y, asteroid.radius // 2))
                    asteroids.append(Asteroid(asteroid.x, asteroid.y, asteroid.radius // 2))

                lasers.remove(laser)
                asteroids.remove(asteroid)
                score += 100
                break

    # Ship collision check
    for asteroid in asteroids:
        distance = math.hypot(ship.x - asteroid.x, ship.y - asteroid.y)
        if distance < ship.radius + asteroid.radius:
            print(f"Hull Destroyed! Final Score: {score}")
            running = False

    # Replenish asteroids if cleared
    if not asteroids:
        asteroids = [Asteroid() for _ in range(6)]

    # 4. Rendering Graphics Layer
    screen.fill(BLACK)

    # Draw Background ambient stars
    for _ in range(3):
        rx, ry = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
        pygame.draw.circle(screen, (50, 50, 80), (rx, ry), 1)

    for particle in particles:
        particle.draw(screen)
    for laser in lasers:
        laser.draw(screen)
    for asteroid in asteroids:
        asteroid.draw(screen)
    ship.draw(screen)

    # UI Graphics Overlay
    ui_text = font.render(f"SCORE: {score:05d}", True, CYAN)
    screen.blit(ui_text, (20, 20))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()