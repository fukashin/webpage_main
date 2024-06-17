import pygame

font = pygame.font.SysFont(None, 55)

def display_score(screen, score):
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

def display_game_over(screen):
    screen.fill((255, 255, 255))
    game_over_text = font.render('Game Over', True, (255, 0, 0))
    screen.blit(game_over_text, (300, 250))
    pygame.display.flip()
