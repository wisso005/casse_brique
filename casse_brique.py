import pygame
import sys

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

    # Getter nécessaire pour la classe ActorPseudoSprite
    @property
    def position(self) -> pygame.Vector2:
        return self.__position

    # Getter nécessaire pour la classe ActorPseudoSprite
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

    # Modifier l'acteur
    def update(self) -> None:
        self.__move()

# Définir la représenttaion graphique des acteurs sur l'écran
class ActorPseudoSprite(pygame.sprite.Sprite):
    _actor: Actor
    _color: pygame.Color
    _image: pygame.Surface
    _rect: pygame.Rect

    def __init__(
            self,
            actor : Actor,
            color : pygame.Color, 
            *groups : pygame.sprite.Group
    )-> None : 
        super().__init__(*groups)
        self._actor = actor
        self._color = color 
        self._init_image() 
        self._init_rect()

    # Définir l'image affichée pour l'acteur
    def _init_image(self) -> None:
        # Créer une surface pour déposer l'image de l'acteur
        self._image = pygame.Surface(self._actor.size)
        # Dessin de la raquette
        pygame.draw.rect(self._image, self._color, ((0, 0), self._actor.size))

    # Définir le rectangle qui recevra l'image de l'acteur
    def _init_rect(self) -> None:
        # Créer un rectangle à partir de l'image
        self._rect = self._image.get_rect()

        # Déplacer le rectangle à la position de l'acteur
        self._rect.update(
            self._actor.position.x,
            self._actor.position.y,
            self._actor.size.x,
            self._actor.size.y
        )
    
    # Dessiner l'image de l'acteur sur la surface indiquée
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._image, self._rect.topleft)

    @property
    def image(self) -> pygame.Surface:
        return self._image

    @property
    def rect(self) -> pygame.Rect:
        return self._rect
    
    @property
    def actor(self) -> Actor:
        return self._actor
   
    def update(self) -> None:
        self._actor.update()

        self._rect.update(
            self._actor.position.x,
            self._actor.position.y,
            self._actor.size.x,
            self._actor.size.y
        )

class Ball(Actor):
    def bounce_x(self) -> None:
        self.speed.x = -self.speed.x

    def bounce_y(self) -> None:
        self.speed.y = -self.speed.y

class Paddle(Actor):
    pass

class BallSprite(ActorPseudoSprite):

    def __init__(
            self,
            actor: Actor,
            color: pygame.Color,
            *groups: pygame.sprite.Group 
    ) -> None:
        super().__init__(actor, color, *groups)

    def _init_image(self) -> None:
        self._image = pygame.Surface(
            self._actor.size,
            pygame.SRCALPHA
        )

        center = self._actor.size / 2
        radius = min(self._actor.size.x, self._actor.size.y) / 2

        pygame.draw.circle(
            self._image,
            pygame.Color("green"),
            (int(center.x), int(center.y)),
            int(radius)
        )

class Brick(Actor):

    __health: int

    def __init__(
        self,
        position: pygame.Vector2,
        size: pygame.Vector2,
        speed: pygame.Vector2,
        health: int
    ) -> None:
        super().__init__(position, size, speed)
        self.__health = health

    @property
    def health(self) -> int:
        return self.__health

    def hit(self) -> None:
        self.__health -= 1

class BrickSprite(ActorPseudoSprite):
    pass

class Game:
    __screen: pygame.Surface
    __screen_borders_lines: dict[str, pygame.Rect]
    __is_running: bool
    __clock: pygame.time.Clock
    __paddles_sprites: pygame.sprite.GroupSingle #une seule raquette 
    __balls_sprites: pygame.sprite.Group
    __bricks_sprites: pygame.sprite.Group

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
        self.__paddles_sprites = pygame.sprite.GroupSingle()
        self.__balls_sprites = pygame.sprite.Group()
        self.__bricks_sprites = pygame.sprite.Group()

        # Création de la raquette
        actor = Paddle(
            pygame.Vector2(590, 700),  # position de la raquette
            pygame.Vector2(100, 10),   # taille de la raquette
            pygame.Vector2(0, 0)       # vitesse nulle pour l'instant
        )

        # Création de l'affichage de la raquette
        ActorPseudoSprite(
            actor,
            pygame.Color("white"),
            self.__paddles_sprites
            )

        # Création de la balle
        ball = Ball(
            pygame.Vector2(640, 680),
            pygame.Vector2(10, 10),
            pygame.Vector2(10, -10)
        )
        # Affichage de la balle
        BallSprite(
            ball,
            pygame.Color("green"),
            self.__balls_sprites
            )
        
        for row in range(4):
            for col in range(10):
                brick = Brick(
                    pygame.Vector2(100 + col * 90, 50 + row * 25),
                    pygame.Vector2(80, 15),
                    pygame.Vector2(0, 0),
                    3
                )

                BrickSprite(
                    brick,
                    pygame.Color("red"),
                    self.__bricks_sprites
                )

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
            offset_vector = pygame.Vector2(*screen_borders[border_name]["offset"])
            offset = offset_vector * (WINDOW_BORDER_LINE_OFFSET // 2)

            start = pygame.Vector2(*screen_borders[border_name]["start"])
            end = pygame.Vector2(*screen_borders[border_name]["end"])

            border_line = pygame.draw.line(
                self.__screen,
                pygame.color.THECOLORS[WINDOW_BORDERS_COLOR[border_name]],
                start + offset,
                end + offset,
                width=WINDOW_BORDER_LINE_OFFSET
            )

            self.__screen_borders_lines[border_name] = border_line

    # Détecter les collisions avec les bords
    def __handle_borders_collisions(self) -> None:
        for actor_pseudo_sprite in self.__balls_sprites:
            for border_name, border_line in self.__screen_borders_lines.items():
                if actor_pseudo_sprite.rect.colliderect(border_line):
                    if isinstance(actor_pseudo_sprite.actor, Ball):
                        ball = actor_pseudo_sprite.actor
                        
                        if border_name == "left" or border_name == "right":
                            
                            ball.bounce_x()

                        elif border_name == "top":
                            ball.bounce_y()

                        elif border_name == "bottom":
                            print("Balle perdue")
                            actor_pseudo_sprite.kill()

    def __handle_balls_bricks_collisions(self) -> None:
        collisions = pygame.sprite.groupcollide(
            self.__balls_sprites,
            self.__bricks_sprites,
            False,
            False
        )
        
        for ball_sprite, bricks_sprites in collisions.items():
            if isinstance(ball_sprite.actor, Ball):
                ball = ball_sprite.actor
                ball.bounce_y()
            
            for brick_sprite in bricks_sprites:
                if isinstance(brick_sprite.actor, Brick):
                    brick = brick_sprite.actor
                    brick.hit()
                    
                    if brick.health <= 0:
                        brick_sprite.kill()

    # Mettre à jour les acteurs
    def __update_actors(self) -> None:
        self.__paddles_sprites.update()
        self.__balls_sprites.update()
        self.__bricks_sprites.update()

    # Dessiner les acteurs
    def __draw_actors(self) -> None:
        self.__paddles_sprites.draw(self.__screen)
        self.__balls_sprites.draw(self.__screen)
        self.__bricks_sprites.draw(self.__screen)

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

            # Vérifier les collisions entre les balles et les briques
            self.__handle_balls_bricks_collisions()

            # Rafraîchir l'affichage
            pygame.display.flip()
        
# Instancier le jeu (Singleton)
game = Game()
# Démarrer le jeu
game.run()
