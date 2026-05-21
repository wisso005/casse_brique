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

NULL_PYGAME_VECTOR2: pygame.Vector2 = pygame.Vector2()
PADDLE: dict[str, pygame.Vector2] = {
    "speed": pygame.Vector2(10, 0)
}

class Actor:
    def __init__(self, position: pygame.Vector2, size: pygame.Vector2, speed: pygame.Vector2) -> None:
        self._position = position
        self._size = size
        self._speed = speed
        self._alive = True

    # Accesseurs public, protégés par l'encapsulation
    @property
    def position(self) -> pygame.Vector2:
        return self._position

    @property
    def size(self) -> pygame.Vector2:
        return self._size

    @property
    def speed(self) -> pygame.Vector2:
        return self._speed

    @speed.setter
    def speed(self, speed: pygame.Vector2) -> None:
        self._speed = speed

    def set_size(self, size: pygame.Vector2) -> None:
        self._size = size

    def set_speed(self, speed: pygame.Vector2) -> None:
        self._speed = speed

    def move(self) -> None:
        self._position += self._speed

    def update(self) -> None:
        self.move()
        self.on_update()

    # Hooks que les sous-classes peuvent implémenter
    def on_update(self) -> None:
        pass

    def on_collide_border(self, border_name: str) -> None:
        pass

    def on_collide_actor(self, other: "Actor") -> None:
        pass

    def destroy(self) -> None:
        self._alive = False

    def is_alive(self) -> bool:
        return self._alive

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
        size = (int(self._actor.size.x), int(self._actor.size.y))
        # Utiliser SRCALPHA pour permettre la transparence si nécessaire
        # SRCALPHA rend la sprite plus polyvalente pour les formes non rectangulaires
        self._image = pygame.Surface(size, pygame.SRCALPHA)
        # Dessin de la raquette (adapté à la taille entière)
        pygame.draw.rect(self._image, self._color, ((0, 0), size))

    # Définir le rectangle qui recevra l'image de l'acteur
    def _init_rect(self) -> None:
        # Créer un rectangle à partir de l'image
        self._rect = self._image.get_rect()
        # Déplacer le rectangle à la position de l'acteur (entiers)
        self._rect.update(
            int(self._actor.position.x),
            int(self._actor.position.y),
            int(self._actor.size.x),
            int(self._actor.size.y)
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
        # Mettre à jour le modèle
        prev_size = (int(self._rect.w), int(self._rect.h)) if hasattr(self, "_rect") else None
        self._actor.update()

        new_size = (int(self._actor.size.x), int(self._actor.size.y))
        # Si la taille a changé, régénérer l'image et le rect
        if prev_size is None or new_size != prev_size:
            self._init_image()
            self._init_rect()
        # Mettre à jour la position du rect
        self._rect.topleft = (int(self._actor.position.x), int(self._actor.position.y))

class Ball(Actor):
    def bounce_x(self) -> None:
        self.speed.x = -self.speed.x

    def bounce_y(self) -> None:
        self.speed.y = -self.speed.y
    
    def on_collide_border(self, border_name: str) -> None:
        if border_name in ("left", "right"):
            self.bounce_x()
        elif border_name == "top":
            self.bounce_y()
        elif border_name == "bottom":
            # La balle est perdue
            self.destroy()

    def on_collide_actor(self, other: "Actor", collision_axis: str | None = None) -> None:
        # Si c'est une raquette, rebondir avec angle selon position de contact
        if isinstance(other, Paddle):
            paddle_left = other.position.x
            paddle_right = other.position.x + other.size.x
            paddle_center_x = (paddle_left + paddle_right) / 2
            ball_center_x = self.position.x + self.size.x / 2
            paddle_width = other.size.x / 2
            position_ratio = (ball_center_x - paddle_center_x) / paddle_width
            position_ratio = max(-1, min(1, position_ratio))

            self.bounce_y()
            max_horizontal_speed = abs(self.speed.y)
            self.speed.x = position_ratio * max_horizontal_speed
        else:
            if collision_axis == "horizontal":
                self.bounce_x()
            else:
                self.bounce_y()

class Paddle(Actor):
    @property
    def position(self) -> pygame.Vector2:
        return self._position

    @position.setter
    def position(self, position: pygame.Vector2) -> None:
        half_width = self.size.x / 2
        if half_width + WINDOW_BORDER_LINE_OFFSET <= position.x <= WINDOW_SIZE[0] - half_width - WINDOW_BORDER_LINE_OFFSET:
            self._position.x = position.x - half_width
        elif position.x < half_width + WINDOW_BORDER_LINE_OFFSET:
            self._position.x = WINDOW_BORDER_LINE_OFFSET
        else:
            self._position.x = WINDOW_SIZE[0] - self.size.x - WINDOW_BORDER_LINE_OFFSET

    def apply_size_modifier(self, factor: float) -> None:
        new_size = pygame.Vector2(self.size.x * factor, self.size.y)
        self.set_size(new_size)

    def on_update(self) -> None:
        min_x = WINDOW_BORDER_LINE_OFFSET
        max_x = WINDOW_SIZE[0] - self.size.x - WINDOW_BORDER_LINE_OFFSET
        if self._position.x < min_x:
            self._position.x = min_x
        elif self._position.x > max_x:
            self._position.x = max_x

class BallSprite(ActorPseudoSprite):

    def __init__(
            self,
            actor: Actor,
            color: pygame.Color,
            *groups: pygame.sprite.Group 
    ) -> None:
        super().__init__(actor, color, *groups)

    def _init_image(self) -> None:
        size = (int(self._actor.size.x), int(self._actor.size.y))
        self._image = pygame.Surface(size, pygame.SRCALPHA)

        center = (size[0] // 2, size[1] // 2)
        radius = min(size[0], size[1]) // 2

        pygame.draw.circle(
            self._image,
            pygame.Color("green"),
            center,
            radius
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
        
        for row in range(3):
            for col in range(14):
                brick = Brick(
                    pygame.Vector2(45 + col * 85, 100 + row * 20),
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
        match event.type:
            case pygame.QUIT:
                self.__is_running = False
                pygame.quit()
                sys.exit()
            case pygame.MOUSEMOTION:
                if self.__paddles_sprites.sprite is not None:
                    if pygame.mouse.get_focused():
                        self.__paddles_sprites.sprite.actor.position = pygame.Vector2(pygame.mouse.get_pos())
            case pygame.KEYDOWN: # IL FAUT REGLER LE PROBLEME DES FLECHES LORS DU TRANSFER KEYUP KEYDOWN
                match event.key:
                    case pygame.K_LEFT:
                        if self.__paddles_sprites.sprite is not None:
                            self.__paddles_sprites.sprite.actor.speed = -PADDLE["speed"].copy()
                    case pygame.K_RIGHT:
                        if self.__paddles_sprites.sprite is not None:
                            self.__paddles_sprites.sprite.actor.speed = PADDLE["speed"].copy()
            case pygame.KEYUP:
                match event.key:
                    case pygame.K_LEFT | pygame.K_RIGHT:
                        if self.__paddles_sprites.sprite is not None:
                            self.__paddles_sprites.sprite.actor.speed = NULL_PYGAME_VECTOR2.copy()

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
                    # Déléguer la réaction de collision à l'acteur
                    actor = actor_pseudo_sprite.actor
                    actor.on_collide_border(border_name)
                    # Si l'acteur s'est auto-détruit, supprimer le sprite
                    if not actor.is_alive():
                        actor_pseudo_sprite.kill()

    def __handle_balls_paddle_collisions(self) -> None:
        collisions = pygame.sprite.groupcollide(
            self.__balls_sprites,
            self.__paddles_sprites,
            False,
            False
        )

        for ball_sprite, paddle_sprites in collisions.items():
            ball = ball_sprite.actor
            for paddle_sprite in paddle_sprites:
                ball.on_collide_actor(paddle_sprite.actor, collision_axis="vertical")

    def __handle_balls_bricks_collisions(self) -> None:
        collisions = pygame.sprite.groupcollide(
            self.__balls_sprites,
            self.__bricks_sprites,
            False,
            False
        )
        
        for ball_sprite, bricks_sprites in collisions.items():
            ball = ball_sprite.actor

            for brick_sprite in bricks_sprites:
                brick = brick_sprite.actor
                # Calculer l'axe principal de collision avec la brique
                ball_rect = ball_sprite.rect
                brick_rect = brick_sprite.rect
                overlap_x = min(ball_rect.right, brick_rect.right) - max(ball_rect.left, brick_rect.left)
                overlap_y = min(ball_rect.bottom, brick_rect.bottom) - max(ball_rect.top, brick_rect.top)
                collision_axis = "horizontal" if overlap_x < overlap_y else "vertical"
                ball.on_collide_actor(brick, collision_axis=collision_axis)

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

            # Vérifier les collisions entre les balles et la raquette
            self.__handle_balls_paddle_collisions()

            # Vérifier les collisions entre les balles et les briques
            self.__handle_balls_bricks_collisions()

            # Rafraîchir l'affichage
            pygame.display.flip()
        
# Instancier le jeu (Singleton)
game = Game()
# Démarrer le jeu
game.run()
