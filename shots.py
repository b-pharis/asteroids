import pygame
from constants import *
from circleshape import CircleShape



class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
            
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, SHOT_RADIUS, width=2)

    def update(self, dt):
        self.position += self.velocity * dt

        # removes bullets after they leave screen
        if self.position.x < -self.radius:  # Off left edge
            self.kill()

        elif self.position.x > SCREEN_WIDTH + self.radius:  # Off right edge
            self.kill()

        if self.position.y < -self.radius:  # Off top edge
            self.kill()

        elif self.position.y > SCREEN_HEIGHT + self.radius:  # Off bottom edge
            self.kill()
    
