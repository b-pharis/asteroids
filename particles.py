import pygame
import random
import math

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color, lifetime=1.0, speed=2):
        super().__init__()
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.x = x
        self.y = y
        self.radius = random.randint(2, 4)  # Randomize particle size
        self.color = color
        self.lifetime = lifetime  # In seconds
        self.age = 0
        self.vel_x = random.uniform(-speed, speed)
        self.vel_y = random.uniform(-speed, speed)
        self.alpha = 255  # Start fully opaque

    def update(self, dt):
        """Update particle position and fade out over time."""
        self.x += self.vel_x
        self.y += self.vel_y
        self.age += dt

        # Reduce opacity over time
        if self.age < self.lifetime:
            self.alpha = max(255 * (1 - self.age / self.lifetime), 0)
        else:
            self.kill()  # Remove particle from sprite group when time is up

    def draw(self, surface):
        """Draw the particle as a circle with fading effect."""
        if self.alpha > 0:
            particle_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (self.color[0], self.color[1], self.color[2], int(self.alpha)), 
                               (self.radius, self.radius), self.radius)
            surface.blit(particle_surface, (self.x - self.radius, self.y - self.radius))

    #@staticmethod
    def spawn_particles(x, y, color=(255, 255, 255), count=10):
        """Static method to generate a list of particles at a given position."""
        return [Particle(x, y, color) for _ in range(count)]

    