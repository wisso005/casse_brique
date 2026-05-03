# Message au prof: Vous pouvez ignorer les notes informatives, je (Wissam) les ai faites générer
# par IA pour faciliter la relecture lors de la reprise du travail.
# Il me semble que ce soit une utilisation apropriée et tolérée de l'IA mais elles seront tout de même
# effacées en fin de projet.

# 03.05:j'ai fait une class ball avec la class ballsprite et j'ai mis les 
#  fonctions d'iversions de la vitesse. pour l'instant y a le rebond avec le sol aussi 
#  mais on remplacera ça par un game over plus tard. 
#  Pour info, la fonction isinstance permet de verifier si qqch appartient à une classe 
#  elle rend True ou false ce qui dans notre cas est une condition pour que ça rebondisse
#  sans ça je pense que la raquette rebondira aussi.

import pygame
import sys

# Configuration de la fenêtre et des bords du jeu

WINDOW_SIZE: tuple[int, int]  = (1280, 720)
WINDOW_TITLE: str = "pygame_step_05" 
FPS: int = 60
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

    @property
    def position(self) -> pygame.Vector2:
        return self.__position

    @property
    def size(self) -> pygame.Vector2:
        return self.__size
    
    def __move(self) -> None:
        self.__position += self.__speed

    def update(self) -> None:
        self.__move()
    
# Représentation graphique d'un acteur dans le jeu
class ActorPseudoSprite:
    __actor: Actor
    __color: pygame.Color
    __image: pygame.Surface
    __rect: pygame.Rect

    def __init__(self, actor: Actor, color: pygame.Color) -> None:
        self.__actor = actor
        self.__color = color
        self._init_image()
        self._init_rect()

    def _init_image(self) -> None:
        # Créer l'image du sprite et dessiner un rectangle blanc pour la raquette
        self.__image = pygame.Surface(self.__actor.size)
        pygame.draw.rect(self.__image, self.__color, ((0, 0), self.__actor.size))

    def _init_rect(self) -> None:
        # Configurer le rectangle de collision et de dessin à la bonne position
        self.__rect = self.__image.get_rect()
        self.__rect.update(
            self.__actor.position.x,
            self.__actor.position.y,
            self.__actor.size.x,
            self.__actor.size.y
        )

    def update(self) -> None:
        self.__actor.update()
        self.__rect.update(
            self.__actor.position.x,
            self.__actor.position.y,
            self.__actor.size.x,
            self.__actor.size.y
        )
      
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.__image, self.__rect.topleft)

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect

class Ball(Actor):
    # Comportement spécifique de la balle : inversion de la vitesse sur un rebond
    def bounce_x(self) -> None:
        self._Actor__speed.x = -self._Actor__speed.x
    
    def bounce_y(self) -> None:
        self._Actor__speed.y = -self._Actor__speed.y

class BallSprite(ActorPseudoSprite):
    def _init_image(self) -> None:
        # Créer une surface transparente pour la balle et dessiner un cercle jaune
        self._ActorPseudoSprite__image = pygame.Surface(self._ActorPseudoSprite__actor.size, pygame.SRCALPHA)
        self._ActorPseudoSprite__image.fill((0, 0, 0, 0))

        center = pygame.Vector2(self._ActorPseudoSprite__actor.size) / 2
        radius = min(self._ActorPseudoSprite__actor.size.x, self._ActorPseudoSprite__actor.size.y) / 2
        pygame.draw.circle(
            self._ActorPseudoSprite__image,
            self._ActorPseudoSprite__color,
            (int(center.x), int(center.y)),
            int(radius)
        )

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

        # Créer la raquette et son sprite blanc
        actor = Actor(
            pygame.Vector2(590, 700),
            pygame.Vector2(100, 10),
            pygame.Vector2(0, 0)
        )
        actor_sprite = ActorPseudoSprite(actor, pygame.Color("white"))
        self.__actors_pseudo_sprites.append(actor_sprite)

        # Créer la balle et son sprite circulaire
        ball = Ball(
            pygame.Vector2(640, 360),
            pygame.Vector2(20, 20),
            pygame.Vector2(5, -5)
        )
        ball_sprite = BallSprite(ball, pygame.Color("yellow"))
        self.__actors_pseudo_sprites.append(ball_sprite)

    def __handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.__is_running = False
            pygame.quit()
            sys.exit()

    # Créer les bords de l'écran
    def __draw_screen_borders(self) -> None:
        # Préparer les lignes de bordures affichées à l'écran
        self.__screen_borders_lines = {}

        screen_rect = self.__screen.get_rect()

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

    # Détecter les collisions avec les bords et faire rebondir la balle
    def __handle_borders_collisions(self) -> None:
        screen_rect = self.__screen.get_rect()

        for actor_pseudo_sprite in self.__actors_pseudo_sprites:
            if "left" in WINDOW_BORDERS_NAME and actor_pseudo_sprite.rect.left < screen_rect.left + WINDOW_BORDER_LINE_OFFSET:
                if isinstance(actor_pseudo_sprite, BallSprite):
                    actor_pseudo_sprite._ActorPseudoSprite__actor.bounce_x()
                else:
                    print("Collision at left !")

            if "right" in WINDOW_BORDERS_NAME and actor_pseudo_sprite.rect.right > screen_rect.right - WINDOW_BORDER_LINE_OFFSET:
                if isinstance(actor_pseudo_sprite, BallSprite):
                    actor_pseudo_sprite._ActorPseudoSprite__actor.bounce_x()
                else:
                    print("Collision at right !")

            if "top" in WINDOW_BORDERS_NAME and actor_pseudo_sprite.rect.top < screen_rect.top + WINDOW_BORDER_LINE_OFFSET:
                if isinstance(actor_pseudo_sprite, BallSprite):
                    actor_pseudo_sprite._ActorPseudoSprite__actor.bounce_y()
                else:
                    print("Collision at top !")

            if "bottom" in WINDOW_BORDERS_NAME and actor_pseudo_sprite.rect.bottom > screen_rect.bottom - WINDOW_BORDER_LINE_OFFSET:
                if isinstance(actor_pseudo_sprite, BallSprite):
                    actor_pseudo_sprite._ActorPseudoSprite__actor.bounce_y()
                else:
                    print("Collision at bottom !")

    # Mettre à jour les acteurs
    def __update_actors(self) -> None:
        for actor_pseudo_sprite in self.__actors_pseudo_sprites:
            actor_pseudo_sprite.update()

    # Dessiner les acteurs
    def __draw_actors(self) -> None:
        for actor_pseudo_sprite in self.__actors_pseudo_sprites:
            actor_pseudo_sprite.draw(self.__screen)

    # Boucle principale du jeu : événements, mise à jour, dessin
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
