import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class for operating bullets that was released from the ship"""
    def __init__(self, ai_settings, screen, ship):
        """Creating a bullet object in the current ship's position"""
        super().__init__()
        self.screen = screen
        # Creating the bullet in position (0,0) and appointment the right position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # The bullet position stores in real format
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Moves the bullet up on the screen"""
        # Refreshing the bullet position in real format
        self.y -= self.speed_factor
        # Refreshing the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Showing the bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)