import pygame
import random
import math

class Bird:
    def __init__(self, image_path, screen, settings):
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(100, screen.get_height() - 100))
        self.screen = screen
        self.settings = settings
        self.position = pygame.math.Vector2(self.rect.center)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.angle = 0
        self.is_dragging = False
        self.is_launched = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_dragging = True
                self.start_pos = pygame.math.Vector2(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_dragging:
                self.is_dragging = False
                self.is_launched = True
                end_pos = pygame.math.Vector2(event.pos)
                direction_vector = self.start_pos - end_pos
                force_magnitude = direction_vector.length()

                if force_magnitude > self.settings.max_force:
                    direction_vector = direction_vector.normalize() * self.settings.max_force

                self.velocity = direction_vector * 0.3
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            current_pos = pygame.math.Vector2(event.pos)
            self.position = self.start_pos + (current_pos - self.start_pos)
            self.position.x = min(max(self.position.x, 50), 150)
            self.position.y = min(max(self.position.y, self.screen.get_height() - 150), self.screen.get_height() - 50)
            self.rect.center = (int(self.position.x), int(self.position.y))

    def apply_gravity(self, planets):
        for planet in planets:
            direction = planet.position - self.position
            distance = direction.length()
            if distance < planet.influence_radius:
                if distance == 0:
                    continue  # Evita divisão por zero
                direction = direction.normalize()
                force = direction * planet.gravity_strength / (distance ** 2)
                if planet.is_repulsive:
                    force = -force
                self.acceleration += force

    def update(self, planets):
        if self.is_launched:
            self.acceleration = pygame.math.Vector2(0, 0.5)  # Gravidade padrão
            self.apply_gravity(planets)  # Aplica a gravidade dos planetas

            self.velocity += self.acceleration
            self.velocity *= 0.99  # Resistência do ar
            self.position += self.velocity
            self.angle = (self.angle - self.velocity.x * 2) % 360

            self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))
            self.image = pygame.transform.rotate(self.original_image, self.angle)

    def draw(self):
        self.screen.blit(self.image, self.rect.topleft)

class Planet:
    def __init__(self, image_path, position, gravity_strength, is_repulsive, screen):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))  # Redimensiona o planeta
        self.position = pygame.math.Vector2(position)
        self.rect = self.image.get_rect(center=self.position)
        self.gravity_strength = gravity_strength
        self.is_repulsive = is_repulsive
        self.influence_radius = 200  # Raio de influência da gravidade
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, self.rect.topleft)

class GameScreen:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.bird = Bird('assets/bird.png', screen, settings)
        self.planets = self.create_planets()

    def create_planets(self):
        planets = []
        num_planets = random.randint(1, 3)
        for _ in range(num_planets):
            x = random.randint(self.settings.screen_width // 2, self.settings.screen_width - 100)
            y = random.randint(self.settings.screen_height // 3, self.settings.screen_height - 150)
            gravity_strength = random.uniform(1, 3)
            is_repulsive = random.choice([True, False])
            planets.append(Planet('assets/planet.png', (x, y), gravity_strength, is_repulsive, self.screen))
        return planets

    def handle_event(self, event):
        self.bird.handle_event(event)

    def update(self):
        self.bird.update(self.planets)

    def draw(self):
        self.screen.fill(self.settings.bg_color)
        for planet in self.planets:
            planet.draw()
        self.bird.draw()
