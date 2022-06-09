import pygame
from time import sleep
import sys
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets, stats, aliens, sb):
    """Reacting for pressing the button"""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_UP:
            ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            fire_bullet(ai_settings, screen, ship, bullets, stats)
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            check_button_p(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_keyup_event(event, ship):
    """Reacting for releasing the button"""
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            ship.moving_left = False
        elif event.key == pygame.K_UP:
            ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            ship.moving_down = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Monitoring actions for keyboard and mouse."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats, aliens, sb)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Runs new game when click on Play button"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset game settings
        ai_settings.initialize_dynamic_settings()
        # Mouse is hidden
        pygame.mouse.set_visible(False)
        # Reset game stats
        stats.reset_stats()
        stats.game_active = True
        # Clear images of score and level
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # Clear alien and bullet lists
        aliens.empty()
        bullets.empty()
        # Creating new alien fleet and ship's central alignment
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_button_p(ai_settings, screen, stats, sb, ship, aliens, bullets):
    ai_settings.initialize_dynamic_settings()
    stats.reset_stats()
    stats.game_active = True
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    aliens.empty()
    bullets.empty()
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, sb):
    """Refreshing images on a screen and showing a new screen"""
    # For every cycle pass, screen is redrawing
    screen.fill(ai_settings.bg_color)
    # All bullets are shown below the ship and alien images
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitime()
    aliens.draw(screen)
    # Score output
    sb.show_score()
    # Play buttons shows only when the game is not active
    if not stats.game_active:
        play_button.draw_button()
    # Showing the last traced screen.
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb):
    """Refreshing bullets position and deleting old bullets"""
    # Refreshing bullets
    bullets.update()
    # Destroying disappeared bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, sb, stats)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, sb, stats):
    """Processing colissions between bullets with aliens"""
    # Deleting bullets and aliens, that were collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)
    if len(aliens) == 0:
        # Destroying current bullets, increasing speed and creating a new fleet
        bullets.empty()
        ai_settings.increase_speed()
        # Increasing level
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets, stats):
    """Releasing a bullet if the maximum is not achieved"""
    # Creating a new bullet and including her in bullets group
    if stats.game_active:
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """Calculating the number of aliens in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Defining the number of rows, accessible in the screen"""
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Creating an alien and placing it in a row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Creating an alien fleet"""
    # Creating an alien and calculating the number of aliens in a row
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # Creating an alien fleet
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Reacting when alien reaches an edge of the screen"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Moving all fleet down and changes the movement direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Handles collision between ship and alien"""
    if stats.ships_left > 1:
        # Reducing ships_left
        stats.ships_left -= 1
        # Refreshing game info
        sb.prep_ships()
        # Clearing aliens and bullets lists
        aliens.empty()
        bullets.empty()
        # Creating new fleet and placing the ship into the center
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if aliens reach the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # It also happens while with collision with the ship
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Checking, if alien fleet reaches an edge of the screen,
    therefore refresh positions of all aliens in the fleet
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Checking colisions 'alien-ship'
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    """Check if the new record"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()