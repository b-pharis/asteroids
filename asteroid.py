import pygame, random, math
from constants import *
from circleshape import CircleShape
            
class Asteroid(CircleShape):
    def __init__(self, x, y, radius, num_points=6, irregularity=0.3):
        """
        Create an asteroid with a lumpy shape.

        :param x: X position
        :param y: Y position
        :param radius: Base radius of the asteroid
        :param num_points: Number of points in the polygon (more = smoother, less = chunkier)
        :param irregularity: How lumpy the asteroid is (0 = smooth, 1 = very jagged)
        """
        super().__init__(x, y, radius)
        self.num_points = num_points
        self.irregularity = irregularity
        self.points = self.generate_lumpy_shape()

    def generate_lumpy_shape(self):
        """Generate a lumpy polygon shape for the asteroid."""
        points = []
        for i in range(self.num_points):
            angle = (i / self.num_points) * 360  # Evenly spaced around the circle
            offset = random.uniform(1 - self.irregularity, 1 + self.irregularity)  # Vary radius
            point_radius = self.radius * offset
            point = pygame.Vector2(
                self.position.x + point_radius * math.cos(math.radians(angle)),
                self.position.y + point_radius * math.sin(math.radians(angle)),
            )
            points.append(point)
        return points
    
    def collision(self, other):
        """Check if another object collides with this asteroid using polygon detection."""
        if isinstance(other, CircleShape):  # If other object is circular (like Player or Bullets)
            return self.point_inside_polygon(other.position, self.points)
        
        return False  # Default to no collision

    def point_inside_polygon(self, point, polygon):
        """Uses the Ray-Casting algorithm to determine if a point is inside the asteroid polygon."""
        x, y = point
        inside = False
        n = len(polygon)
        px, py = polygon[0]

        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(py, p2y):
                if y <= max(py, p2y):
                    if x <= max(px, p2x):
                        if py != p2y:
                            x_intersect = (y - py) * (p2x - px) / (p2y - py) + px
                        if px == p2x or x <= x_intersect:
                            inside = not inside
            px, py = p2x, p2y

        return inside


    def draw(self, screen):
        """Draw the asteroid as a jagged polygon."""
        pygame.draw.polygon(screen, "white", self.points, width=2)

    def update(self, dt):
        """Move the asteroid and update shape position."""
        self.position += self.velocity * dt
        self.points = [p + self.velocity * dt for p in self.points]  # Move shape points

        # Wrap around the screen edges
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius

        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

    def split(self):
        """Break asteroid into two smaller lumpy asteroids when hit."""
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return  # No smaller asteroids

        angle = random.uniform(20.0, 50.0)
        first_vel = self.velocity.rotate(angle)
        second_vel = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        first_split = Asteroid(self.position.x, self.position.y, new_radius)
        second_split = Asteroid(self.position.x, self.position.y, new_radius)

        first_split.velocity = first_vel * 1.5
        second_split.velocity = second_vel * 1.5          
            