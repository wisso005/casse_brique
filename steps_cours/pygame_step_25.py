import pygame
import random
import sys


WINDOW_SIZE: tuple[int, int]  = (480, 360)
WINDOW_TITLE: str = "pygame_step_25"
WINDOW_BORDER_LINE_OFFSET: int = 10
WINDOW_BORDERS_NAME: list[str] = ["left", "right"]
WINDOW_BORDERS_COLOR: dict[str, str] = {"left" : "red", "right" : "blue", "top" : "yellow", "bottom" : "grey"}
FPS: int = 24


class Actor:
    _position: pygame.Vector2
    _speed: pygame.Vector2

    def __init__(self, position: pygame.Vector2, speed: pygame.Vector2) -> None:
        self._position = position
        self._speed = speed

    @property
    def position(self) -> pygame.Vector2:
        return self._position

    @property
    def speed(self) -> pygame.Vector2:
        return self._speed

    @speed.setter
    def speed(self, speed: pygame.Vector2) -> None:
        self._speed = speed

    def _move(self) -> None:
        self._position += self._speed

    def update(self) -> None:
        self._move()


class Spaceship(Actor):
    __size: pygame.Vector2

    def __init__(self, position: pygame.Vector2, size: pygame.Vector2, speed: pygame.Vector2) -> None:
        super().__init__(position, speed)
        self.__size = size

    @property
    def size(self) -> pygame.Vector2:
        return self.__size


class Asteroid(Actor):
    __diameter: int

    def __init__(self, position: pygame.Vector2, diameter: int, speed: pygame.Vector2) -> None:
        super().__init__(position, speed)
        self.__diameter = diameter

    @property
    def diameter(self) -> int:
        return self.__diameter

    @property
    def radius(self) -> int:
        return self.__diameter // 2


class Fire(Actor):
    __side: int

    def __init__(self, position: pygame.Vector2, side: int, speed: pygame.Vector2) -> None:
        super().__init__(position, speed)
        self.__side = side

    @property
    def side(self) -> int:
        return self.__side


class ActorSprite(pygame.sprite.Sprite):
    _actor: Actor
    _color: pygame.Color
    _image: pygame.Surface
    _rect: pygame.Rect

    def __init__(self, actor: Actor, color: pygame.Color, *groups: pygame.sprite.Group) -> None:
        super().__init__(*groups)
        self._actor = actor
        self._color = color
        self._init_image()
        self._init_rect()

    @property
    def actor(self) -> Actor:
        return self._actor

    @property
    def color(self) -> pygame.Color:
        return self._color

    @color.setter
    def color(self, color: pygame.Color) -> None:
        self._color = color

    @property
    def image(self) -> pygame.Surface:
        return self._image

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    def _init_image(self) -> None:
        raise NotImplementedError("Les sous-classes doivent implémenter _init_image()")

    def _paint_image(self) -> None:
        self._image.fill(pygame.color.THECOLORS["black"])

    def _init_rect(self) -> None:
        self._rect = self._image.get_rect()
        self._rect.update(self._actor.position, self._rect.size)

    def update(self) -> None:
        raise NotImplementedError("Les sous-classes doivent implémenter update()")


class SpaceshipSprite(ActorSprite):
    _actor: Spaceship

    def __init__(self, spaceship: Spaceship, color: pygame.Color) -> None:
        super().__init__(spaceship, color)

    def _init_image(self) -> None:
        self._image = pygame.Surface(self._actor.size)
        self.paint_image()

    def paint_image(self) -> None:
        super()._paint_image()
        pygame.draw.ellipse(self._image, self._color, ((0, 0), self._actor.size))

    def update(self) -> None:
        self._actor.update()
        self._rect.update(self._actor.position, self._actor.size)


class AsteroidSprite(ActorSprite):
    _actor: Asteroid

    def __init__(self, asteroid: Asteroid, color: pygame.Color, *groups: pygame.sprite.Group) -> None:
        super().__init__(asteroid, color, *groups)

    def _init_image(self) -> None:
        self._image = pygame.Surface((self._actor.diameter, self._actor.diameter))
        self.paint_image()

    def paint_image(self) -> None:
        super()._paint_image()
        pygame.draw.circle(self._image, self._color, (self._actor.radius, self._actor.radius), self._actor.radius, width = 1)

    def update(self) -> None:
        self._actor.update()
        self._rect.update(self._actor.position, (self._actor.diameter, self._actor.diameter))


class FireSprite(ActorSprite):
    _actor: Fire

    def __init__(self, fire: Fire, color: pygame.Color, *groups: pygame.sprite.Group) -> None:
        super().__init__(fire, color, *groups)

    def _init_image(self) -> None:
        self._image = pygame.Surface((self._actor.side, self._actor.side))
        self.paint_image()

    def paint_image(self) -> None:
        super()._paint_image()
        self._image.fill(self._color)

    def update(self) -> None:
        self._actor.update()
        self._rect.update(self._actor.position, (self._actor.side, self._actor.side))


class Game:
    __screen: pygame.Surface
    __screen_borders_lines: dict[str, pygame.Rect]
    __is_running: bool
    __clock: pygame.time.Clock
    __frame_counter: int
    __spaceship_sprite: pygame.sprite.GroupSingle
    __asteroids_sprites: pygame.sprite.Group
    __borders_collision_sprites: pygame.sprite.Group
    __fires_sprites: pygame.sprite.Group

    def __init__(self) -> None:
        pygame.init()
        self.__clock = pygame.time.Clock()
        self.__is_running = False
        self.__init_screen()
        self.__init_actors()
     
    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(WINDOW_TITLE)

    def __init_spaceship(self) -> None:
        spaceship = Spaceship(
                       pygame.Vector2(180 - 60 / 2, 360 - 45),
                       pygame.Vector2(60, 45),
                       pygame.Vector2(-5, 0)
                     )
        spaceship_sprite = SpaceshipSprite(spaceship, pygame.Color(pygame.color.THECOLORS["magenta"]))
        self.__spaceship_sprite = pygame.sprite.GroupSingle(spaceship_sprite)
        self.__borders_collision_sprites.add(self.__spaceship_sprite)

    def __init_asteroids(self) -> None:
        self.__asteroids_sprites = pygame.sprite.Group()
        for i in range(16):
            radius = random.randint(1, 3)
            asteroid = Asteroid(
                pygame.Vector2(10 + 25 * i + radius, radius),
                10 * radius,
                pygame.Vector2(random.randint(-2, 2), random.randint(1, 2))
            )
            AsteroidSprite(asteroid, pygame.Color(pygame.color.THECOLORS["cyan"]), self.__asteroids_sprites, self.__borders_collision_sprites)

    def __init_actors(self) -> None:
        self.__fires_sprites = pygame.sprite.Group()
        self.__borders_collision_sprites = pygame.sprite.Group()
        self.__init_spaceship()
        self.__init_asteroids()

    def __handle_events(self, event: pygame.event.Event) -> None:
        match event.type:
            # Analyser la pression d'une touche du clavier
            case pygame.KEYDOWN:
                # Identifier la touche pressée
                match event.key:
                    # Cas où il s'agit de la touche ESPACE
                    case pygame.K_SPACE:
                        print("Fire !")
                        # self.__init_fire()
            case pygame.QUIT:
                self.__is_running = False
                pygame.quit()
                sys.exit()
            # case _:
            #    print(event)

    def __draw_screen_borders(self) -> None:
        self.__screen_borders_lines = {}
        screen_rect = self.__screen.get_rect()
        screen_borders = {
                          "left":   {"offset": pygame.Vector2(+1, 0), "start": screen_rect.topleft,    "end": screen_rect.bottomleft},
                          "right":  {"offset": pygame.Vector2(-1, 0), "start": screen_rect.topright,   "end": screen_rect.bottomright},
                          "top":    {"offset": pygame.Vector2(0, +1), "start": screen_rect.topleft,    "end": screen_rect.topright },
                          "bottom": {"offset": pygame.Vector2(0, -1), "start": screen_rect.bottomleft, "end": screen_rect.bottomright}
        }
        for border_name in WINDOW_BORDERS_NAME:
            offset = WINDOW_BORDER_LINE_OFFSET * screen_borders[border_name]["offset"] // 2
            border_line = pygame.draw.line(
                self.__screen,
                pygame.color.THECOLORS[WINDOW_BORDERS_COLOR[border_name]],
                pygame.Vector2(screen_borders[border_name]["start"]) + offset,
                pygame.Vector2(screen_borders[border_name]["end"]) + offset,
                width = WINDOW_BORDER_LINE_OFFSET
            )
            self.__screen_borders_lines[border_name] = border_line

    def __handle_borders_collisions(self) -> None:
        for actor_sprite in self.__borders_collision_sprites:
            for screen_border_name, screen_border_line in self.__screen_borders_lines.items():
                if actor_sprite.rect.colliderect(screen_border_line):
                    if screen_border_name == "left" and actor_sprite.actor.speed.x < 0:
                        actor_sprite.actor.speed.x = -actor_sprite.actor.speed.x
                    if screen_border_name == "right" and actor_sprite.actor.speed.x > 0:
                        actor_sprite.actor.speed.x = -actor_sprite.actor.speed.x
                    if screen_border_name == "top" and actor_sprite.actor.speed.y < 0:
                        actor_sprite.actor.speed.y = -actor_sprite.actor.speed.y
                    if screen_border_name == "bottom" and actor_sprite.actor.speed.y > 0:
                        actor_sprite.actor.speed.y = -actor_sprite.actor.speed.y

    def __handle_spaceship_collisions_with_asteroids(self):
        pygame.sprite.groupcollide(self.__asteroids_sprites, self.__spaceship_sprite, True, True)

    def __handle_collisions(self):
        self.__handle_borders_collisions()
        self.__handle_spaceship_collisions_with_asteroids()

    def __update_actors(self) -> None:
        self.__spaceship_sprite.update()
        self.__asteroids_sprites.update()
        self.__fires_sprites.update()

    def __draw_actors(self) -> None:
        self.__spaceship_sprite.draw(self.__screen)
        self.__asteroids_sprites.draw(self.__screen)
        self.__fires_sprites.draw(self.__screen)

    def run(self) -> None:
        self.__is_running = True
        self.__frame_counter = 0
        while self.__is_running:
            self.__clock.tick_busy_loop(FPS)
            self.__frame_counter += 1
            for event in pygame.event.get():
                self.__handle_events(event)
            self.__screen.fill(pygame.color.THECOLORS["black"])
            self.__draw_screen_borders()
            self.__handle_collisions()
            self.__update_actors()
            self.__draw_actors()
            pygame.display.flip()


game = Game()
game.run()
