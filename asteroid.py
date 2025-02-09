import pygame, random
from constants import *
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, width=2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return ("this was a small asteroid")
        else:
            angle = random.uniform(20.0, 50.0)
            first_vel = self.velocity.rotate(angle)
            second_vel = self.velocity.rotate(-angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            first_split = Asteroid(self.position, self.position, new_radius)
            second_split = Asteroid(self.position, self.position, new_radius)
            first_split.velocity = (first_vel * 1.5)
            second_split.velocity = (second_vel)
            
            
            
            