import pygame

class GameScreen:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
    
    def handle_event(self, event):
        pass
    
    def update(self):
        pass
    
    def draw(self):
        self.screen.fill(self.settings.bg_color)