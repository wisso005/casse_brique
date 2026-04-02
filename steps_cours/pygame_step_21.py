import pygame
import sys
import random


WINDOW_SIZE: tuple[int, int]  = (480, 360)
WINDOW_TITLE: str = "pygame_step_21" # Titre de la fenêtre du jeu
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

    @speed.setter
    def speed(self, speed: pygame.Vector2) -> None:
        self.__speed = speed

    def __move(self) -> None:
        self.__position += self.__speed

    def update(self) -> None:
        self.__move()


class Spaceship(Actor):

    def __init__(self, position: pygame.Vector2, size: pygame.Vector2, speed: pygame.Vector2) -> None:
        super().__init__(position, size, speed)


class Asteroid(Actor):

    def __init__(self, position: pygame.Vector2, size: pygame.Vector2, speed: pygame.Vector2) -> None:
        super().__init__(position, size, speed)


# Définir la classe des sprites des acteurs
# class ActorPseudoSprite():
class ActorSprite(pygame.sprite.Sprite):
    _actor: Actor
    _color: pygame.Color
    _image: pygame.Surface # Image de l'acteur
    _rect: pygame.Rect     # Rectangle de déplacement de l'image

    # Python autorise des paramètres dont le nombre varie
    # entre 0 et une valeur arbitraire, dans ce cas, ils sont
    # précédés d'une étoile (*args est souvent utilisé)

    # Un pygame.sprite.Sprite peut appartenir à aucun, un ou
    # plusieurs pygame.sprite.Group
    def __init__(self, actor: Actor, color: pygame.Color, *groups: pygame.sprite.Group) -> None:
        super().__init__(*groups)
        self._actor = actor
        self._color = color
        self.init_image()
        self._init_rect()

    # Getter nécessaire pour la classe Game
    @property
    def actor(self) -> Actor:
        return self._actor

    @property
    def color(self) -> pygame.Color:
        return self._color

    @color.setter
    def color(self, color: pygame.Color) -> None:
        self._color = color

    # Getter nécessaire pour la classe pygame.sprite.Group
    @property
    def image(self) -> pygame.Surface:
        return self._image

    # Getter nécessaire pour gérer les collisions
    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    # Définir l'image affichée pour l'acteur
    def init_image(self) -> None:
        # Créer une surface pour déposer l'image de l'acteur
        self._image = pygame.Surface(self._actor.size)

    # Définir le rectangle qui recevra l'image de l'acteur
    def _init_rect(self) -> None:
        # Créer un rectangle à partir de l'image
        self._rect = self._image.get_rect()
        # Déplacer le rectangle à la position de l'acteur
        self._rect.update(self._actor.position, self._actor.size)

    # La méthode update() est utilisée par pygame.Sprite.Group
    def update(self) -> None:
        self._actor.update()
        self._rect.update(self._actor.position, self._actor.size)


class SpaceshipSprite(ActorSprite):

    def __init__(self, spaceship: Spaceship, color: pygame.Color, *groups: pygame.sprite.Group) -> None:
        super().__init__(spaceship, color, *groups)

    def init_image(self) -> None:
        super().init_image()
        # Dessiner sur l'image une ellipse de la couleur choisie à la création de l'image
        pygame.draw.ellipse(self._image, self._color, ((0, 0), self._actor.size))


class AsteroidSprite(ActorSprite):

    def __init__(self, asteroid: Asteroid, color: pygame.Color, *groups: pygame.sprite.Group) -> None:
        super().__init__(asteroid, color, *groups)

    def init_image(self) -> None:
        super().init_image()
        # Dessiner sur l'image un cercle avec bordure de la couleur choisie à la création de l'image
        radius = min(self._actor.size.x, self._actor.size.y) / 2
        pygame.draw.circle(self._image, self._color, (radius, radius), radius, width=1)


class Game:
    __screen: pygame.Surface
    __screen_borders_lines: dict[str, pygame.Rect]
    __is_running: bool
    __clock: pygame.time.Clock
    __spaceships_sprites: pygame.sprite.Group
    __asteroid_sprites: pygame.sprite.Group

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
        self.__spaceships_sprites = pygame.sprite.Group()
        spaceship = Spaceship(
                       pygame.Vector2(180 - 60 / 2, 360 - 45),
                       pygame.Vector2(60, 45),
                       pygame.Vector2(-5, 0)
                     )
        SpaceshipSprite(spaceship, pygame.Color(pygame.color.THECOLORS["magenta"]), self.__spaceships_sprites)
        self.__asteroids_sprites = pygame.sprite.Group()
        for i in range(16):
            radius = random.randint(1, 3)
            asteroid = Asteroid(
                pygame.Vector2(10 + 25 * i + radius, radius),
                radius * pygame.Vector2(10, 10),
                pygame.Vector2(random.randint(-2, 2), 2)
            )
            AsteroidSprite(asteroid, pygame.Color(pygame.color.THECOLORS["cyan"]), self.__asteroids_sprites)

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
    def __handle_borders_collisions(self, actors_sprites: pygame.sprite.Group) -> None:
        for actor_sprite in actors_sprites:
            for screen_border_name, screen_border_line in self.__screen_borders_lines.items():
                if actor_sprite.rect.colliderect(screen_border_line):
                    if screen_border_name == "left" and actor_sprite.actor.speed.x < 0:
                        actor_sprite.actor.speed.x = -actor_sprite.actor.speed.x
                    if screen_border_name == "right" and actor_sprite.actor.speed.x > 0:
                        actor_sprite.actor.speed.x = -actor_sprite.actor.speed.x
                    if screen_border_name == "top" and actor_sprite.actor.speed.x < 0:
                        actor_sprite.actor.speed.y = -actor_sprite.actor.speed.y
                    if screen_border_name == "bottom" and actor_sprite.actor.speed.x > 0:
                        actor_sprite.actor.speed.y = -actor_sprite.actor.speed.y

    # Détecter les collisions entre le spaceship et les asteroids
    def __handle_spaceship_collisions_with_asteroids(self):
        hinted_asteroids_sprites = pygame.sprite.groupcollide(self.__asteroids_sprites, self.__spaceships_sprites, False, False)
        for hinted_asteroid_sprite in hinted_asteroids_sprites:
            hinted_asteroid_sprite.color = pygame.color.THECOLORS["yellow"]
            hinted_asteroid_sprite.init_image()

    # Mettre à jour les sprites des acteurs
    def __update_actors(self) -> None:
        self.__asteroids_sprites.update()
        self.__spaceships_sprites.update()

    # Dessiner les sprites des acteurs
    def __draw_actors(self) -> None:
        self.__asteroids_sprites.draw(self.__screen)
        self.__spaceships_sprites.draw(self.__screen)

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
            self.__handle_borders_collisions(self.__asteroids_sprites)
            self.__handle_borders_collisions(self.__spaceships_sprites)
            self. __handle_spaceship_collisions_with_asteroids()
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
