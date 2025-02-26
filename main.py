# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame, sys, random, math, os
from asteroidfield import AsteroidField
from constants import *
from player import Player
from asteroid import Asteroid
from shots import Shot
from particles import *
from powerups import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    score = 0
    lives = 3

    # Load the background image and scale it to fit the screen
    background_path = os.path.join("sprites", "asteroid_background.png")  # Adjust filename if needed
    background = pygame.image.load(background_path).convert_alpha()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create a transparent overlay
    opacity = 175 # Set opacity (0-255, lower is more transparent)
    transparent_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)  
    transparent_surface.fill((0, 0, 0, opacity))  # White with alpha

    font = pygame.font.Font(None, 36)
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()


    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Particle.containers = (particles, updatable, drawable)
    Powerup.containers = (powerups, updatable, drawable)

    player = Player(x= SCREEN_WIDTH / 2, y= SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    def score_system(screen):
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))  # Draw at the top-left corner
        screen.blit(lives_text, (10, 40))

    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        updatable.update(dt)
        screen.fill(color="black")
        screen.blit(background, (0, 0))
        screen.blit(transparent_surface, (0, 0))  # Apply the opacity effect
        score_system(screen)
        #check if player collides with asteroid
        for ast in asteroids:
            if ast.collision(player):
                player.take_damage()
                lives -= 1
            # check if bullet collides with asteroid    
            for bullet in shots:
                if ast.collision(bullet):
                    bullet.kill()
                    ast.split()
                    score += 100
                    particles.add(Particle.spawn_particles(ast.position.x, ast.position.y))  # Add particles
                    #call spawn_powerup
                    powerup = Powerup.spawn_powerup(ast.position.x, ast.position.y)
                    if powerup:
                        powerups.add(Powerup.spawn_powerup(ast.position.x, ast.position.y))
        #checks if player collides with powerup
        for power in powerups:
            if power.collision(player):
                player.decrease_cooldown(0.01)
                power.kill()

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()