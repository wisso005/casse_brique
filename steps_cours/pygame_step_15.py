import pygame
import sys


WINDOW_SIZE: tuple[int, int]  = (480, 360)
WINDOW_TITLE: str = "pygame_step_15" # Titre de la fenêtre du jeu
# Définir le demi-décalage et l'épaisseur des bords de la fenêtre de jeu
WINDOW_BORDER_LINE_OFFSET = 10
# Liste des bords où le rebond est possible
WINDOW_BORDERS_NAME: list[str] = ["left", "right"]
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


# Définir la classe des sprites des acteurs
# class ActorPseudoSprite():
class ActorSprite(pygame.sprite.Sprite):
    __actor: Actor
    __color: pygame.Color
    __image: pygame.Surface # Image de l'acteur
    __rect: pygame.Rect     # Rectangle de déplacement de l'image

    # Python autorise des paramètres dont le nombre varie
    # entre 0 et une valeur arbitraire, dans ce cas, ils sont
    # précédés d'une étoile (*args est souvent utilisé)

    # Un pygame.sprite.Sprite peut appartenir à aucun, un ou
    # plusieurs pygame.sprite.Group
    def __init__(self, actor: Actor, color: pygame.Color, *groups: pygame.sprite.Group) -> None:
        super().__init__(*groups)
        self.__actor = actor
        self.__color = color
        self.__init_image()
        self.__init_rect()

    # Getter nécessaire pour la classe pygame.sprite.Group
    @property
    def image(self) -> pygame.Surface:
        return self.__image

    # Getter nécessaire pour gérer les collisions
    @property
    def rect(self) -> pygame.Rect:
        return self.__rect

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

    # La méthode update() est utilisée par pygame.Sprite.Group
    def update(self) -> None:
        self.__actor.update()
        self.__rect.update(self.__actor.position, self.__actor.size)

    # La méthode draw() est gérée par pygame.sprite.Group
    # def draw(self, surface: pygame.Surface) -> None:
    #     surface.blit(self.__image, self.__rect.topleft)


class Game:
    __screen: pygame.Surface
    __screen_borders_lines: dict[str, pygame.Rect]
    __is_running: bool
    __clock: pygame.time.Clock
    __actors_sprites: pygame.sprite.Group

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
        # self.__actors_sprites = []
        self.__actors_sprites = pygame.sprite.Group()
        actor = Actor(
                       pygame.Vector2(120, 90),
                       pygame.Vector2(60, 45),
                       pygame.Vector2(5, 3.75)
                     )
        ActorSprite(actor, pygame.Color(pygame.color.THECOLORS["magenta"]), self.__actors_sprites)
        # self.__actors_sprites.add(actor_sprite)
    
    def __handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.__is_running = False
            pygame.quit()
            # Terminer le processus Python
            sys.exit()

    # Créer les lignes des bords de l'écran
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

    # Détecter la collision avec la bordure droite
    # en utilisant la détection de collision entre rectangles
    def __handle_borders_collisions(self) -> None:
        for actor_sprite in self.__actors_sprites:
            for screen_border_name, screen_border_line in self.__screen_borders_lines.items():
                if actor_sprite.rect.colliderect(screen_border_line):
                    print(f"Collision at {screen_border_name} !")


    # Mettre à jour les sprites des acteurs
    def __update_actors(self) -> None:
        self.__actors_sprites.update()

    # Dessiner les sprites des acteurs
    def __draw_actors(self) -> None:
        self.__actors_sprites.draw(self.__screen)

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
            # Détecter les collisions avec les bords
            self.__handle_borders_collisions()
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
