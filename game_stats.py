class GameStats:
    """Monitoring stats for the game"""

    def __init__(self, ai_settings):
        """Initialize stats"""
        self.ai_settings = ai_settings
        self.reset_stats()
        # Game runs in inactive condition
        self.game_active = False
        # Record should not been resetted
        self.high_score = 0

    def reset_stats(self):
        """Initialize stats, that changing while the game is on"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
