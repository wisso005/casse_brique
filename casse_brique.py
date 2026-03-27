import json
import os
import pygame
import random
import sys


WINDOW_SIZE: pygame.Vector2 = pygame.Vector2(480, 360)
WINDOW_TITLE: str = str(os.path.basename(__file__)).replace(".py", "")
WINDOW_BORDER_LINE_OFFSET: int = int(WINDOW_SIZE.x // 96)
WINDOW_BORDERS_NAME: list[str] = ["left", "right", "top"]
WINDOW_BORDERS_COLOR: dict[str, str] = {"left" : "red", "right" : "blue", "top" : "yellow", "bottom" : "grey"}
GAME_COLOR: pygame.Color = pygame.Color(pygame.color.THECOLORS["black"])
TEXT_SIZE: int = int(WINDOW_SIZE.x // 12)
FPS: int = 24
NULL_PYGAME_VECTOR2: pygame.Vector2 = pygame.Vector2(0, 0)
RAQUETTE = {
             "size":  WINDOW_SIZE // 8,
             "speed": pygame.Vector2(WINDOW_SIZE.x // 72, 0)
            }
BRIQUES = {
             "min_diameter": int(WINDOW_SIZE.x // 48),
             "max_diameter": 5 * int(WINDOW_SIZE.x // 48),
            }

class Raquette(Actor):
    __size: pygame.Vector2

    def __init__(self, position: pygame.Vector2, size: pygame.Vector2, speed: pygame.Vector2) -> None:
        super().__init__(position, speed)
        self.__size = size

    @property
    def size(self) -> pygame.Vector2:
        return self.__size

    @property
    def position(self) -> pygame.Vector2:
        return self._position

    @position.setter
    def position(self, position: pygame.Vector2) -> None:
        offset_x = self.__size.x // 2
        if offset_x + WINDOW_BORDER_LINE_OFFSET <= position.x <= WINDOW_SIZE.x - offset_x - WINDOW_BORDER_LINE_OFFSET:
            self._position.x = position.x - offset_x
        else:
            if position.x < offset_x:
                self._position.x = WINDOW_BORDER_LINE_OFFSET
            if position.x > WINDOW_SIZE.x - offset_x:
                self._position.x = WINDOW_SIZE.x - 2 * offset_x - WINDOW_BORDER_LINE_OFFSET

class Game:
    __screen: pygame.Surface
    __screen_rect: pygame.Rect
    __screen_borders_lines: dict[str, pygame.Rect]
    __is_running: bool
    __clock: pygame.time.Clock
    __level_clock_ticks: int
    __frame_counter: int
    __game_state: str
    __level: int
    __spaceship_sprite: pygame.sprite.GroupSingle
    __asteroids_sprites: pygame.sprite.Group
    __borders_collision_sprites: pygame.sprite.Group
    __fires_sprite: pygame.sprite.Group
    __shoot_fire: bool
    __start_buttons: pygame.sprite.Group
    __end_buttons: pygame.sprite.Group
    __player: Player
    __scores: Scoreboard

    def __init__(self) -> None:
        # Initialiser tous les éléments de Pygame
        # https://www.pygame.org/docs/ref/pygame.html#pygame.init
        pygame.init()
        # Créer la fenêtre de l'application
        self.__screen = pygame.display.set_mode(WINDOW_SIZE)
        # Initialiser la variable de contrôle d'activité de l'application
        self.__is_running = False
        
    
    # Méthode fondamentale utilisée pour exécuter une application Pygame
    def run(self) -> None:
        # Mettre la variable de contrôle d'activité de l'application à `True`
        self.__is_running = True
        '''
            Le principe essentiel à comprendre est que Pygame doit actulaliser
            en permanence l'état de l'application.
        '''
        # Boucle infinie jusqu'à ce que `self.__is_running` soit définie à `False`
        while self.__is_running:
            # Boucle sur tous les événements gérés par Pygame
            for event in pygame.event.get():
                # Test de l'état du type d'événement de Pygame
                if event.type == pygame.QUIT:
                    # Mettre la variable de contrôle d'activité de l'application à `False`
                    self.__is_running = False
                    # Arrêter tous les éléments de Pygame
                    pygame.quit()


# Instancier le jeu
game = Game()
# Démarrer le jeu
game.run()
