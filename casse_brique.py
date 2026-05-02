import pygame
import sys

WINDOW_SIZE: tuple[int, int]  = (1280, 720)
WINDOW_TITLE: str = "pygame_step_05" 
FPS: int = 6
WINDOW_BORDERS_NAME: list[str] = ["left", "right", "top", "bottom"]
WINDOW_BORDER_LINE_OFFSET: int = 2
WINDOW_BORDERS_COLOR: dict[str, str] = {
    "left": "red",
    "right": "red",
    "top": "red",
    "bottom": "red"
}

class Actor:
    __position: pygame.Vector2
    __size: pygame.Vector2
    __speed: pygame.Vector2

    def __init__(self, position: pygame.Vector2, size: pygame.Vector2, speed: pygame.Vector2) -> None:
        self.__position = position
        self.__size = size
        self.__speed = speed

    # Getter nécessaire pour la classe ActorPseudoSprite
    @property
    def position(self) -> pygame.Vector2:
        return self.__position

    # Getter nécessaire pour la classe ActorPseudoSprite
    @property
    def size(self) -> pygame.Vector2:
        return self.__size
    
    def __move(self) -> None:
        self.__position += self.__speed

    # Modifier l'acteur
    def update(self) -> None:
        self.__move()
    
# Définir la représenttaion graphique des acteurs sur l'écran
class ActorPseudoSprite:
    __actor: Actor
    __color: pygame.Color
    __image: pygame.Surface # Zone de dessin de l'acteur 
    __rect: pygame.Rect #Pour le déplacement de la raquette 

    def __init__(self, actor: Actor, color: pygame.Color) -> None:
        self.__actor = actor
        self.__color = color
        self.__init_image()
        self.__init_rect()

    # Définir l'image affichée pour l'acteur
    def __init_image(self) -> None:
        # Créer une surface pour déposer l'image de l'acteur
        self.__image = pygame.Surface(self.__actor.size)
        # Dessin de la raquette
        pygame.draw.rect(self.__image, self.__color, ((0, 0), self.__actor.size))

    # Définir le rectangle qui recevra l'image de l'acteur
    def __init_rect(self) -> None:
        # Créer un rectangle à partir de l'image
        self.__rect = self.__image.get_rect()

        # Déplacer le rectangle à la position de l'acteur
        self.__rect.update(
            self.__actor.position.x,
            self.__actor.position.y,
            self.__actor.size.x,
            self.__actor.size.y
        )
    def update(self) -> None:
        self.__actor.update()

        # Déplacer le rectangle à la position de l'acteur
        self.__rect.update(
            self.__actor.position.x,
            self.__actor.position.y,
            self.__actor.size.x,
            self.__actor.size.y
        )
      
    # Dessiner l'image de l'acteur sur la surface indiquée
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.__image, self.__rect.topleft)

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect

class Game:
    __screen: pygame.Surface # attribut de l'écran Pygame de l'application
    __is_running: bool # attribut de contrôle de l'activation de l'application
    __clock: pygame.time.Clock #horloge du jeu
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

    def __init_actors(self) -> None:
        self.__actors = []
        self.__actors_pseudo_sprites = []
        actor = Actor(
            pygame.Vector2(590, 450),   # position de la raquette
            pygame.Vector2(100, 10),    # taille de la raquette
            pygame.Vector2(0, 0)        # vitesse nulle pour l'instant
        )

        self.__actors.append(actor)
        actor_pseudo_sprite = ActorPseudoSprite(
                actor,
                pygame.Color(255, 255, 255)
        )
        self.__actors_pseudo_sprites.append(actor_pseudo_sprite)
        
    # Méthode fondamentale utilisée pour exécuter une application Pygame
    def __handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.__is_running = False
            pygame.quit()
            exit()

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

    # Initialiser les acteurs du jeu
    def __init_actors(self) -> None:
        self.__actors_pseudo_sprites = []

        # Création de la raquette
        actor = Actor(
            pygame.Vector2(590, 700),  # position de la raquette
            pygame.Vector2(100, 10),   # taille de la raquette
            pygame.Vector2(0, 0)       # vitesse nulle pour l'instant
        )

        # Création de l'affichage de la raquette
        actor_sprite = ActorPseudoSprite(
            actor,
            pygame.Color("white")
        )

        self.__actors_pseudo_sprites.append(actor_sprite)

    def __handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.__is_running = False
            pygame.quit()
            sys.exit()

    # Créer les bords de l'écran
    def __draw_screen_borders(self) -> None:
        # Initialiser le dictionnaire des lignes des bords
        self.__screen_borders_lines = {}

        # Récupérer le rectangle de l'écran
        screen_rect = self.__screen.get_rect()

        # Définir les caractéristiques des bords
        screen_borders = {
            "left": {
                "offset": pygame.Vector2(+1, 0),
                "start": screen_rect.topleft,
                "end": screen_rect.bottomleft
            },
            "right": {
                "offset": pygame.Vector2(-1, 0),
                "start": screen_rect.topright,
                "end": screen_rect.bottomright
            },
            "top": {
                "offset": pygame.Vector2(0, +1),
                "start": screen_rect.topleft,
                "end": screen_rect.topright
            },
            "bottom": {
                "offset": pygame.Vector2(0, -1),
                "start": screen_rect.bottomleft,
                "end": screen_rect.bottomright
            }
        }

        # Dessiner chaque bord demandé
        for border_name in WINDOW_BORDERS_NAME:
            offset = WINDOW_BORDER_LINE_OFFSET * screen_borders[border_name]["offset"] // 2

            border_line = pygame.draw.line(
                self.__screen,
                pygame.color.THECOLORS[WINDOW_BORDERS_COLOR[border_name]],
                pygame.Vector2(screen_borders[border_name]["start"]) + offset,
                pygame.Vector2(screen_borders[border_name]["end"]) + offset,
                width=WINDOW_BORDER_LINE_OFFSET
            )

            self.__screen_borders_lines[border_name] = border_line

    # Détecter les collisions avec les bords
    def __handle_borders_collisions(self) -> None:
        screen_rect = self.__screen.get_rect()

        for actor_pseudo_sprite in self.__actors_pseudo_sprites:
            if "left" in WINDOW_BORDERS_NAME and actor_pseudo_sprite.rect.left < screen_rect.left + WINDOW_BORDER_LINE_OFFSET:
                print("Collision at left !")

            if "right" in WINDOW_BORDERS_NAME and actor_pseudo_sprite.rect.right > screen_rect.right - WINDOW_BORDER_LINE_OFFSET:
                print("Collision at right !")

            if "top" in WINDOW_BORDERS_NAME and actor_pseudo_sprite.rect.top < screen_rect.top + WINDOW_BORDER_LINE_OFFSET:
                print("Collision at top !")

            if "bottom" in WINDOW_BORDERS_NAME and actor_pseudo_sprite.rect.bottom > screen_rect.bottom - WINDOW_BORDER_LINE_OFFSET:
                print("Collision at bottom !")

    # Mettre à jour les acteurs
    def __update_actors(self) -> None:
        for actor_pseudo_sprite in self.__actors_pseudo_sprites:
            actor_pseudo_sprite.update()

    # Dessiner les acteurs
    def __draw_actors(self) -> None:
        for actor_pseudo_sprite in self.__actors_pseudo_sprites:
            actor_pseudo_sprite.draw(self.__screen)

    def run(self) -> None:
        self.__is_running = True

        while self.__is_running:
            self.__clock.tick_busy_loop(FPS)

            for event in pygame.event.get():
                self.__handle_events(event)

            # Effacer l'écran
            self.__screen.fill(pygame.color.THECOLORS["black"])

            # Dessiner les bords
            self.__draw_screen_borders()

            # Mettre à jour les acteurs
            self.__update_actors()

            # Vérifier les collisions avec les bords
            self.__handle_borders_collisions()

            # Dessiner les acteurs
            self.__draw_actors()

            # Rafraîchir l'affichage
            pygame.display.flip()
        
# Instancier le jeu (Singleton)
game = Game()
# Démarrer le jeu
game.run()
