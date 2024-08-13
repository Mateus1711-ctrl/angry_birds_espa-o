import pygame

class MenuScreen:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.active = True
        self.font_title = pygame.font.SysFont(None, int(settings.screen_width * 0.08))
        self.font_text = pygame.font.SysFont(None, int(settings.screen_width * 0.04))
        self.font_button = pygame.font.SysFont(None, int(settings.screen_width * 0.05))
        self.text_color = (255, 255, 255)
        self.bg_color = (0, 0, 0)
        self.button_color = (0, 128, 0)
        self.button_hover_color = (0, 180, 0)
        self.play_button = self.font_button.render("Jogar", True, self.text_color)
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.center = (settings.screen_width // 2, settings.screen_height * 0.75)
        self.intro_text = [
            "Bem-vindo ao Angry Birds!",
            "Regras do jogo:",
            "1. Use o mouse para mirar.",
            "2. Lance os pássaros para derrubar os porcos.",
            "3. Complete os níveis com o menor número de lançamentos possível."
        ]
        self.title = "Angry Birds"

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.play_button_rect.collidepoint(mouse_pos):
                self.active = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button_rect.collidepoint(mouse_pos):
            self.play_button = self.font_button.render("Jogar", True, self.text_color, self.button_hover_color)
        else:
            self.play_button = self.font_button.render("Jogar", True, self.text_color, self.button_color)

    def draw(self):
        self.screen.fill(self.bg_color)
        
        title_surface = self.font_title.render(self.title, True, self.text_color)
        title_rect = title_surface.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height * 0.15))
        self.screen.blit(title_surface, title_rect)
        
        y_offset = self.settings.screen_height * 0.30
        for line in self.intro_text:
            intro_text_surface = self.font_text.render(line, True, self.text_color)
            intro_text_rect = intro_text_surface.get_rect(centerx=self.screen.get_rect().centerx, y=y_offset)
            self.screen.blit(intro_text_surface, intro_text_rect)
            y_offset += self.settings.screen_height * 0.07
        
        pygame.draw.rect(self.screen, self.button_color, self.play_button_rect.inflate(20, 10))
        self.screen.blit(self.play_button, self.play_button_rect)
