import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """Initialize the ship and make his starting position"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # Loading ship image and getting the rectangle
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Every new ship appears at the lowest screen edge
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # Saving the real coordinate of ship's center
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Refreshing the ship's position in case of flag movement"""
        # Refreshing only the center attribute, not rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor
        # Refreshing the rect attribute depending on self.center
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def blitime(self):
        """Drawing ship in current position"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Placing the ship into the center bottom"""
        self.centerx = self.screen_rect.centerx
        self.centery = self.screen_rect.bottom
