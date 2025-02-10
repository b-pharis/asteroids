import pygame, random

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, color=(255,255,255), lifetime=8.0):
        super().__init__()
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(x, y)
        self.x = x
        self.y = y
        self.color = color
        self.radius = 15
        self.lifetime = lifetime
        self.age = 0
        self.alpha = 255  # Start fully opaque

    def update(self, dt):
        self.x
        self.y
        self.age += dt

        if self.age < self.lifetime:
            self.alpha = max(255 * (1 - self.age / self.lifetime), 0)
        else:
            self.kill()
    
    def draw(self, surface):
        powerup_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(powerup_surface, (self.color[0], self.color[1], self.color[2], int(self.alpha)), (self.radius, self.radius), self.radius)
        surface.blit(powerup_surface, (self.x - self.radius, self.y - self.radius))

    def spawn_powerup(x, y, color=(255, 0, 0), count=10):
        """Static method to generate a list of particles at a given position."""
        powerup_chance = random.randint(0, 100)
        if powerup_chance < 60:
            return [Powerup(x, y, color) for _ in range(count)]
        return []
    
    def collision(self, other):
        return self.position.distance_to(other.position) <= self.radius + other.radius
        