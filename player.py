import pygame, sys
from constants import *
from circleshape import CircleShape
from shots import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        self.default_cooldown = PLAYER_SHOOT_COOLDOWN
        self.powerup_timer = 0
        self.lives = 3  # Start with 3 lives
        self.invincible = False
        self.invincible_timer = 0

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2) 

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoots(self):
        if self.timer > 0:
            return True
        else:
            shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
            shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            self.timer = self.shoot_cooldown

    def decrease_cooldown(self, amount=0.1, duration=5.0):
        """Decrease shoot cooldown but ensure a minimum limit."""
        self.shoot_cooldown = max(self.shoot_cooldown - amount, 0.1)  # Prevents it from being too fast
        self.powerup_timer = duration

    def take_damage(self):
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.invincible_timer = 2  # 2 seconds of invincibility

            if self.lives <= 0:
                print("Game Over!")
                sys.exit()  # End the game if out of lives
            else:
                self.respawn()

    def respawn(self):
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.velocity = pygame.Vector2(0, 0)
            
    def update(self, dt):
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= dt:
                self.invincible = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)
        
        if keys[pygame.K_w]:
            self.move(dt)
        
        if keys[pygame.K_s]:
            self.move(-dt)

        if keys[pygame.K_SPACE]:
            self.shoots()

        
        self.timer -= dt

        #powerup effect timer
        if self.powerup_timer > 0:
            self.powerup_timer -= dt
            if self.powerup_timer <= 0:  # Reset cooldown after 5 seconds
                self.shoot_cooldown = self.default_cooldown

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

            
        