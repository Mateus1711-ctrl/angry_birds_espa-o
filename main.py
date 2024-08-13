import pygame
from settings import Settings
from game_screen import GameScreen
from menu_screen import MenuScreen

def main():
    pygame.init()
    
    settings = Settings()
    
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Angry Birds Clone")
    
    menu_screen = MenuScreen(screen, settings)
    game_screen = GameScreen(screen, settings)
    
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if menu_screen.active:
                menu_screen.handle_event(event)
            else:
                game_screen.handle_event(event)
        
        if menu_screen.active:
            menu_screen.update()
            menu_screen.draw()
        else:
            game_screen.update()
            game_screen.draw()
        
        pygame.display.flip()
        clock.tick(60)  # Limita o jogo a 60 FPS
    
    pygame.quit()

if __name__ == "__main__":
    main()