import pygame
import sys


WINDOW_SIZE: tuple[int, int]  = (480, 360)
WINDOW_TITLE: str = "pygame_step_10" # Titre de la fenêtre du jeu
# Définir le demi-décalage et l'épaisseur des bords de la fenêtre de jeu
WINDOW_BORDER_LINE_OFFSET = 10
# Liste des bords où le rebond est possible
WINDOW_BORDERS_NAME: list[str] = ["left", "right", "top", "bottom"]
# Couleur des bords
WINDOW_BORDERS_COLOR: dict[str, str] = {"left" : "red", "right" : "blue", "top" : "yellow", "bottom" : "grey"}
FPS: int = 24 # Frame Per Second = taux de rafraîchissement de l'affichage par seconde


# Définir la classe des acteurs
class Actor:
    __position: pygame.Vector2
    __size: pygame.Vector2
    __speed: pygame.Vector2
    
    def __init__(self, position: pygame.Vector2, size: pygame.Vector2, speed: pygame.Vector2) -> None:
        self.__position = position
        self.__size = size
        self.__speed = speed

    @property
    def position(self) -> pygame.Vector2:
        return self.__position

    @property
    def size(self) -> pygame.Vector2:
        return self.__size

    @property
    def speed(self) -> pygame.Vector2:
        return self.__speed

    def __move(self) -> None:
        self.__position += self.__speed

    def update(self) -> None:
        self.__move()


# Définir la classe de la représentation graphique des acteurs
class ActorPseudoSprite:
    __actor: Actor
    __color: pygame.Color
    __image: pygame.Surface # Image de l'acteur
    __rect: pygame.Rect     # Rectangle de déplacement de l'image

    def __init__(self, actor: Actor, color: pygame.Color) -> None:
        self.__actor = actor
        self.__color = color
        self.__init_image()
        self.__init_rect()

    # Définir l'image affichée pour l'acteur
    def __init_image(self) -> None:
        # Créer une surface pour déposer l'image de l'acteur
        self.__image = pygame.Surface(self.__actor.size)
        # Dessiner sur l'image une ellipse de la couleur choisie à la création de l'image
        pygame.draw.ellipse(self.__image, self.__color, ((0, 0), self.__actor.size))

    # Définir le rectangle qui recevra l'image de l'acteur
    def __init_rect(self) -> None:
        # Créer un rectangle à partir de l'image
        self.__rect = self.__image.get_rect()
        # Déplacer le rectangle à la position de l'acteur
        self.__rect.update(self.__actor.position, self.__actor.size)

    def update(self) -> None:
        self.__actor.update()
        self.__rect.update(self.__actor.position, self.__actor.size)

    # Dessiner l'image de l'acteur sur la surface indiquée
    # Les coordonnées sont celles de la position du coin
    # supérieur gauche du rectangle mis à jour par update()
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.__image, self.__rect.topleft)


class Game:
    __screen: pygame.Surface
    __screen_borders_lines: dict[str, pygame.Rect]
    __is_running: bool
    __clock: pygame.time.Clock
    __actors_pseudo_sprites: list[ActorPseudoSprite]

    def __init__(self) -> None:
        pygame.init()
        self.__clock = pygame.time.Clock()
        self.__is_running = False
        self.__init_screen()
        self.__init_actors()
     
    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(WINDOW_TITLE)

    # Initialiser les acteurs et leurs sprites
    def __init_actors(self) -> None:
        self.__actors_pseudo_sprites = []
        actor = Actor(
                       pygame.Vector2(120, 90),
                       pygame.Vector2(60, 45),
                       pygame.Vector2(5, 3.75)
                     )
        actor_sprite = ActorPseudoSprite(actor, pygame.Color(pygame.color.THECOLORS["magenta"]))
        self.__actors_pseudo_sprites.append(actor_sprite)
    
    def __handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.__is_running = False
            pygame.quit()
            # Terminer le processus Python
            sys.exit()

    # Créer les bords de l'écran
    def __draw_screen_borders(self) -> None:
        # Initialiser le dictionnaire des lignes des bords
        self.__screen_borders_lines = {}
        # Récupérer le rectangle de l'écran
        screen_rect = self.__screen.get_rect()
        # Définir les caractéristiques des bords
        screen_borders = {
                          "left":   {"offset": pygame.Vector2(+1, 0), "start": screen_rect.topleft,    "end": screen_rect.bottomleft},
                          "right":  {"offset": pygame.Vector2(-1, 0), "start": screen_rect.topright,   "end": screen_rect.bottomright},
                          "top":    {"offset": pygame.Vector2(0, +1), "start": screen_rect.topleft,    "end": screen_rect.topright },
                          "bottom": {"offset": pygame.Vector2(0, -1), "start": screen_rect.bottomleft, "end": screen_rect.bottomright}
        }
        # Boucle de création des bords
        for border_name in WINDOW_BORDERS_NAME:
            # Calcul du décalage intérieur
            offset = WINDOW_BORDER_LINE_OFFSET * screen_borders[border_name]["offset"] // 2
            # Dessin de la ligne concerné avec ajour direct dans le dictionnaire des bords
            border_line = pygame.draw.line(
                self.__screen,
                pygame.color.THECOLORS[WINDOW_BORDERS_COLOR[border_name]],
                pygame.Vector2(screen_borders[border_name]["start"]) + offset,
                pygame.Vector2(screen_borders[border_name]["end"]) + offset,
                width = WINDOW_BORDER_LINE_OFFSET
            )
            self.__screen_borders_lines[border_name] = border_line


    # Mettre à jour les sprites des acteurs
    def __update_actors(self) -> None:
        for actor_pseudo_sprite in self.__actors_pseudo_sprites:
            actor_pseudo_sprite.update()

    # Dessiner les sprites des acteurs
    def __draw_actors(self) -> None:
        for actor_pseudo_sprite in self.__actors_pseudo_sprites:
            actor_pseudo_sprite.draw(self.__screen)

    def run(self) -> None:
        self.__is_running = True
        while self.__is_running:
            # Maintenir le taux de rafraîchissement
            self.__clock.tick_busy_loop(FPS)
            for event in pygame.event.get():
                self.__handle_events(event)
            # Remplir le fonds de l'écran
            self.__screen.fill(pygame.color.THECOLORS["black"])
            # Dessiner les bords
            self.__draw_screen_borders()
            # Mettre à jour les acteurs
            self.__update_actors()
            # Dessiner les acteurs
            self.__draw_actors()
            # Rafraîchir l'affichage de tout l'écran
            pygame.display.flip()


# Instancier le jeu (Singleton)
game = Game()
# Démarrer le jeu
game.run()
