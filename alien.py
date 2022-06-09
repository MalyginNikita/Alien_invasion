import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Class, describing one aline"""

    def __init__(self, ai_settings, screen):
        """Initialize an alien and gives him a starting position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # Loading an alien image and define the rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        # Every new alien appears in the left top edge of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Saving the exact alien position
        self.x = float(self.rect.x)

    def blitme(self):
        """Show an alien in current position"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Returns True, if an alien is on the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Moving an alien to the right"""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x
