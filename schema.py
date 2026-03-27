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
BRIQUE = {
             "min_diameter": int(WINDOW_SIZE.x // 48),
             "max_diameter": 5 * int(WINDOW_SIZE.x // 48),
            }

FIRES     = {
             "side":  int(WINDOW_SIZE.y // 90),
             "speed": pygame.Vector2(0, -WINDOW_SIZE.y // 90)
            }
PLAYER_NAMES: list[str] = ["Alice", "Bob", "Carla", "Debian", "Eve", "Fred", "Gaston", "Hermione"]
MAX_LEVEL: int = 2
ONE_SHOOT_LEVEL = 2


class Player:
    __name: str
    __score: int

    def __init__(self, name: str, score: int) -> None:
        self.__name = name
        self.__score = score

    @property
    def name(self) -> str:
        return self.__name

    @property
    def score(self) -> int:
        return self.__score

    @score.setter
    def score(self, score: int) -> None:
        self.__score = score

class Scoreboard:
    __players: list[Player]

    def __init__(self) -> None:
        self.__players = []

    @property
    def players(self) -> list[Player]:
        return self.__players

    def add_score(self, name: str, score: int) -> None:
        self.__players.append(Player(name, score))
        self.__players.sort(key=lambda player: player.score, reverse=True)
        self.__players = self.__players[:5]

    def save_score(self) -> None:
        data = []
        for player in self.__players:
            data.append({"name": player.name, "score": player.score})
        score_file = open("scores.json", "w")
        score_json = json.dumps(data, indent = 4)
        score_file.write(score_json)
        score_file.close()

    def load_score(self) -> None:
        if os.path.isfile("scores.json"):
            score_file = open("scores.json", "r")
            data = json.load(score_file)
            for line in data:
                self.__players.append(Player(line["name"], line["score"]))
            score_file.close()
        else:
            self.save_score()


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


class Brique(Actor):
    __diameter: int

    def __init__(self, position: pygame.Vector2, diameter: int, speed: pygame.Vector2 = (0,0)) -> None:
        super().__init__(position, speed)
        self.__diameter = diameter

    @property
    def diameter(self) -> int:
        return self.__diameter

    @diameter.setter
    def diameter(self, diameter: int) -> None:
        if diameter < 0:
            self.__diameter = BRIQUE["min_diameter"]
        elif diameter > BRIQUE["max_diameter"]:
            self.__diameter = BRIQUE["max_diameter"]
        else:
            self.__diameter = diameter

    @property
    def radius(self) -> int:
        return self.__diameter // 2

    def resize_on_center(self, delta_diameter: int) -> None:
        delta_radius = delta_diameter // 2
        self.diameter = self.__diameter + delta_diameter
        self._position += pygame.Vector2(-delta_radius, -delta_radius)


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
        # raise NotImplementedError("Les sous-classes doivent implémenter paint_image()")
        self._image.fill(GAME_COLOR)
        self._image.set_colorkey(GAME_COLOR)

    def _init_rect(self) -> None:
        self._rect = self._image.get_rect()
        self._rect.update(self._actor.position, self._rect.size)

    def update(self) -> None:
        raise NotImplementedError("Les sous-classes doivent implémenter update()")


class RaquetteSprite(ActorSprite):
    _actor: Raquette
    __sprite_image_filename: str
    __sprite_image: pygame.Surface | None

    def __init__(self, spaceship: Raquette, color: pygame.Color, **kwargs) -> None:
        self.__sprite_image_filename = kwargs.get('sprite_image_filename')
        super().__init__(spaceship, color)

    def _init_image(self) -> None:
        self.__sprite_image = None
        self._image = pygame.Surface(self._actor.size)
        if self.__sprite_image_filename is not None:
            if os.path.isfile(self.__sprite_image_filename):
                loaded_sprite_image = pygame.image.load(self.__sprite_image_filename).convert_alpha()
                self.__sprite_image = pygame.transform.scale(loaded_sprite_image, self._actor.size)
        self._paint_image()

    def _paint_image(self) -> None:
        super()._paint_image()
        if self.__sprite_image is None:
            pygame.draw.ellipse(self._image, self._color, ((0, 0), self._actor.size))
        else:
            self._image.set_alpha(255)
            self._image.blit(self.__sprite_image, (0, 0))

    def update(self) -> None:
        self._actor.update()
        self._rect.update(self._actor.position, self._actor.size)

class BriqueSprite(ActorSprite):
    _actor: Brique
    __hinted: bool
    __hintable_time: int
    __unhintable_time: int
    __unhintable: bool
    __clock_ticks: int

    def __init__(self, asteroid: Brique, *groups: pygame.sprite.Group) -> None:
        self.__hinted = False
        self.__unhintable = False
        self.__clock_ticks = 0
        super().__init__(asteroid, pygame.Color(pygame.color.THECOLORS["cyan"]), *groups)

    @property
    def hinted(self) -> bool:
        return self.__hinted

    @hinted.setter
    def hinted(self, hinted: bool) -> None:
        self.__hinted = hinted

    @property
    def unhintable(self) -> bool:
        return self.__unhintable

    def _init_image(self) -> None:
        self._image = pygame.Surface((self._actor.diameter, self._actor.diameter))
        self._paint_image()

    def _paint_image(self) -> None:
        super()._paint_image()
        pygame.draw.circle(self._image, self._color, (self._actor.radius, self._actor.radius), self._actor.radius, width = 1)
        if self.__unhintable:
            pygame.draw.rect(self._image, self._color, self._image.get_rect(), width = 1)

    def _refresh_image(self) -> None:
        self._init_image()
        self._init_rect()

    def update(self) -> None:
        self.__clock_ticks += 1
        if self.__unhintable:
            if self.__clock_ticks == 1:
                self._color = pygame.color.THECOLORS["grey"]
                self.__unhintable_time = random.randint(1, 2) * FPS
            if self.__clock_ticks > self.__unhintable_time:
                self.__unhintable = False
                self.__clock_ticks = 0
        else:
            if self.__clock_ticks == 1:
                self._color = pygame.color.THECOLORS["cyan"]
                self.__hintable_time = int(1.5 * FPS)
            if self.__clock_ticks > self.__hintable_time:
                self.__clock_ticks = 0
                self.__unhintable = True
        if self.__hinted or self.__clock_ticks == 1:
            self._refresh_image()
            self.__hinted = False
        self._actor.update()
        self._rect.update(self._actor.position, (self._actor.diameter, self._actor.diameter))


class FireSprite(ActorSprite):
    _actor: Fire

    def __init__(self, fire: Fire, color: pygame.Color, *groups: pygame.sprite.Group) -> None:
        super().__init__(fire, color, *groups)

    def _init_image(self) -> None:
        self._image = pygame.Surface((self._actor.side, self._actor.side))
        self._paint_image()

    def _paint_image(self) -> None:
        super()._paint_image()
        self._image.fill(self._color)

    def update(self) -> None:
        self._actor.update()
        self._rect.update(self._actor.position, (self._actor.side, self._actor.side))


class Button(pygame.sprite.Sprite):
    __position: pygame.Vector2
    __size: pygame.Vector2
    __color: pygame.Color
    __text_color: pygame.Color
    __text: str
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, position: pygame.Vector2, text_color: pygame.Color, color: pygame.Color, text: str, *groups: pygame.sprite.Group) -> None:
        super().__init__(*groups)
        self.__position = position
        self.__size = pygame.Vector2(len(text) * TEXT_SIZE // 2, TEXT_SIZE * 1)
        self.__color = color
        self.__text_color = text_color
        self.__text = text
        self.__init_button()

    def __init_button(self) -> None:
        self.image = pygame.Surface(self.__size)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, self.__color, ((0,0), self.__size), width = 2, border_radius = 5)
        font = pygame.font.SysFont(None, TEXT_SIZE)
        text_render = font.render(self.__text, True, self.__text_color)
        self.image.blit(text_render, (self.rect.centerx - text_render.get_rect().width // 2, self.rect.centery - text_render.get_rect().height // 2))
        self.update()

    def center_at_width(self) -> None:
        self.__position = pygame.Vector2(self.rect.left - self.rect.width // 2, self.rect.top)
        self.update()

    def center_at_height(self) -> None:
        self.__position = pygame.Vector2(self.rect.left, self.rect.top - self.rect.height // 2)
        self.update()

    def update(self) -> None:
        self.rect.update(self.__position, self.__size)

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
        pygame.init()
        self.__clock = pygame.time.Clock()
        self.__level = 0
        self.__frame_counter = 0
        self.__is_running = False
        self.__init_screen()
        self.__game_state = "start"

    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(WINDOW_TITLE)
        self.__screen_rect = self.__screen.get_rect()

    def __init_start(self) -> None:
        self.__init_start_buttons()
        self.__player = Player(random.choice(PLAYER_NAMES), 0)
        self.__scores = Scoreboard()
        self.__scores.load_score()

    def __init_start_buttons(self) -> None:
        self.__start_buttons = pygame.sprite.Group()
        Button(
               pygame.Vector2(self.__screen_rect.center),
               pygame.Color(pygame.color.THECOLORS["green"]),
               pygame.Color(pygame.color.THECOLORS["white"]),
               "Play",
               self.__start_buttons
              )
        self.__start_buttons.sprites()[0].center_at_width()
        self.__start_buttons.sprites()[0].center_at_height()

    def __handle_start_events(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if self.__start_buttons.sprites()[0].rect.collidepoint(event.pos):
                    self.__game_state = "level"
                    self.__init_level()
            case pygame.QUIT:
                self.__is_running = False
                pygame.quit()
                sys.exit()

    def __draw_greetings(self) -> None:
        text = "Hello " + self.__player.name
        font = pygame.font.SysFont(None, TEXT_SIZE)
        text_render = font.render(text, True, pygame.Color(pygame.color.THECOLORS["white"]))
        self.__screen.blit(text_render, (self.__screen_rect.centerx - text_render.get_rect().width // 2, TEXT_SIZE))

    def __draw_start_buttons(self) -> None:
        self.__draw_greetings()
        self.__start_buttons.draw(self.__screen)

    def __inside_start_loop(self) -> None:
        for event in pygame.event.get():
            self.__handle_start_events(event)
        self.__draw_start_buttons()

    def __init_level(self) -> None:
        self.__level += 1
        self.__level_clock_ticks = self.__frame_counter

    def __inside_level_loop(self) -> None:
        if self.__frame_counter - self.__level_clock_ticks < 2 * FPS:
            self.__screen.fill(GAME_COLOR)
            text = "Level " + str(self.__level)
            font = pygame.font.SysFont(None, TEXT_SIZE)
            text_render = font.render(text, True, pygame.Color(255, 0, int(255 // MAX_LEVEL * self.__level) % 255))
            self.__screen.blit(text_render, (self.__screen_rect.centerx - text_render.get_rect().width // 2,
                                             self.__screen_rect.centery - text_render.get_rect().height // 2))
        else:
            self.__game_state = "play"
            self.__init_game()
            self.__frame_counter = 0
            self.__shoot_fire = False

    def __init_game(self) -> None:
        self.__init_actors()

    def __init_spaceship(self) -> None:
        spaceship = Raquette(
                       pygame.Vector2(WINDOW_SIZE.x / 2, WINDOW_SIZE.y - RAQUETTE["size"].y),
                       RAQUETTE["size"],
                       NULL_PYGAME_VECTOR2.copy()
                     )
        spaceship_sprite = RaquetteSprite(spaceship, pygame.Color(pygame.color.THECOLORS["magenta"]), sprite_image_filename ="spaceship.png")
        self.__spaceship_sprite = pygame.sprite.GroupSingle(spaceship_sprite)
        #self.__borders_collision_sprites.add(self.__spaceship_sprite)

    def __init_asteroids(self) -> None:
        self.__asteroids_sprites = pygame.sprite.Group()
        initial_vertical_offset = 0
        for i in range(1 + self.__level):
            diameter = (4 - i) * BRIQUE["min_diameter"]
            j_max = int((WINDOW_SIZE. x - 2 * WINDOW_BORDER_LINE_OFFSET) // diameter // 2) + 1
            for j in range(j_max):
                offset = WINDOW_BORDER_LINE_OFFSET * (1 + 4 * (i % 2))
                asteroid = Brique(
                                    pygame.Vector2(
                                                   offset + 2 * j * diameter,
                                                   initial_vertical_offset + WINDOW_BORDER_LINE_OFFSET + 1
                                                  ),
                                    diameter 
                                   )
                BriqueSprite(asteroid, self.__asteroids_sprites, self.__borders_collision_sprites)
            initial_vertical_offset += diameter

            
    def __init_actors(self) -> None:
        self.__fires_sprites = pygame.sprite.Group()
        self.__borders_collision_sprites = pygame.sprite.Group()
        self.__init_spaceship()
        self.__init_asteroids()

    def __handle_game_events(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if self.__level < ONE_SHOOT_LEVEL:
                    self.__shoot_fire = True
                else:
                    self.__shoot_fire = False
                    self.__init_fire()
            case pygame.MOUSEBUTTONUP:
                self.__shoot_fire = False
            case pygame.MOUSEMOTION:
                if self.__spaceship_sprite.sprite is not None:
                    if pygame.mouse.get_focused():
                        self.__spaceship_sprite.sprite.actor.position = pygame.Vector2(pygame.mouse.get_pos())
                        if self.__level >= ONE_SHOOT_LEVEL:
                            for asteroid_sprite in self.__asteroids_sprites:
                                if pygame.mouse.get_rel()[0] > RAQUETTE["speed"].x:
                                    asteroid_sprite.actor.speed.y += 1
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_LEFT:
                        if self.__spaceship_sprite.sprite is not None:
                            self.__spaceship_sprite.sprite.actor.speed = -RAQUETTE["speed"].copy()
                    case pygame.K_RIGHT:
                        if self.__spaceship_sprite.sprite is not None:
                            self.__spaceship_sprite.sprite.actor.speed = RAQUETTE["speed"].copy()
                    case pygame.K_SPACE:
                        if self.__level < ONE_SHOOT_LEVEL:
                            self.__shoot_fire = True
                        else:
                            self.__shoot_fire = False
                            if self.__spaceship_sprite.sprite is not None:
                                self.__init_fire()
            case pygame.KEYUP:
                match event.key:
                    case pygame.K_LEFT:
                        if self.__spaceship_sprite.sprite is not None:
                            self.__spaceship_sprite.sprite.actor.speed = NULL_PYGAME_VECTOR2.copy()
                    case pygame.K_RIGHT:
                        if self.__spaceship_sprite.sprite is not None:
                            self.__spaceship_sprite.sprite.actor.speed = NULL_PYGAME_VECTOR2.copy()
                    case pygame.K_SPACE:
                        self.__shoot_fire = False
            case pygame.QUIT:
                self.__is_running = False
                pygame.quit()
                sys.exit()

    def __detect_borders_collisions(self) -> None:
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

    def __detect_fires_collisions_with_asteroids(self):
        # hinted_asteroids_sprites = pygame.sprite.groupcollide(self.__asteroids_sprites, self.__fires_sprites, True, True)
        hinted_asteroids_sprites = pygame.sprite.groupcollide(self.__asteroids_sprites, self.__fires_sprites, False, True)
        for hinted_asteroid_sprite in hinted_asteroids_sprites:
            if hinted_asteroid_sprite.actor.diameter <= 10:
                hinted_asteroid_sprite.kill()
            else:
                hinted_asteroid_sprite.color = pygame.color.THECOLORS["yellow"]
                hinted_asteroid_sprite.actor.resize_on_center(-10)

    def __detect_fire_collisions_with_asteroids(self):
        if len(self.__fires_sprites) != 0:
            for fire_sprite in self.__fires_sprites:
                hinted_asteroids_sprites = pygame.sprite.spritecollide(fire_sprite, self.__asteroids_sprites,False)
                if len(hinted_asteroids_sprites) != 0:
                    for hinted_asteroid_sprite in hinted_asteroids_sprites:
                        if not hinted_asteroid_sprite.unhintable:
                            if  fire_sprite.rect.top - hinted_asteroid_sprite.rect.bottom <= fire_sprite.rect.height and fire_sprite.actor.speed.y < 0 :
                                if hinted_asteroid_sprite.actor.diameter <= BRIQUE["min_diameter"]:
                                    self.__player.score += 1
                                    hinted_asteroid_sprite.kill()
                                else:
                                    hinted_asteroid_sprite.actor.resize_on_center(-BRIQUE["min_diameter"])
                                    hinted_asteroid_sprite.color = pygame.color.THECOLORS["green"]
                                    hinted_asteroid_sprite.hinted = True
                            elif fire_sprite.rect.top - hinted_asteroid_sprite.rect.bottom <= fire_sprite.rect.height and fire_sprite.actor.speed.y > 0:
                                hinted_asteroid_sprite.actor.resize_on_center(BRIQUE["min_diameter"])
                                hinted_asteroid_sprite.color = pygame.color.THECOLORS["red"]
                                hinted_asteroid_sprite.hinted = True
                            fire_sprite.kill()

    def __detect_spaceship_collisions_with_asteroids(self):
        killed_spaceship_sprite = pygame.sprite.groupcollide(self.__spaceship_sprite, self.__asteroids_sprites, True, True)
        if len(killed_spaceship_sprite) > 0:
            self.__to_next_level_or_end()

    def __detect_asteroid_out_of_game(self):
        for asteroid_sprite in self.__asteroids_sprites:
            if not self.__screen_rect.contains(asteroid_sprite.rect):
                asteroid_sprite.kill()
        if len(self.__asteroids_sprites) == 0:
            self.__to_next_level_or_end()

    def __detect_game_collisions(self):
        self.__detect_borders_collisions()
        # self.__handle_fires_collisions_with_asteroids()
        self.__detect_fire_collisions_with_asteroids()
        self.__detect_spaceship_collisions_with_asteroids()
        self.__detect_asteroid_out_of_game()

    def __to_next_level_or_end(self):
        if self.__level < MAX_LEVEL:
            self.__game_state = "level"
            self.__init_level()
        else:
            self.__scores.add_score(self.__player.name, self.__player.score)
            self.__scores.save_score()
            self.__game_state = "end"
            self.__init_end()

    def __update_actors(self) -> None:
        self.__spaceship_sprite.update()
        self.__asteroids_sprites.update()
        self.__fires_sprites.update()

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

    def __draw_score(self) -> None:
        font = pygame.font.SysFont(None, TEXT_SIZE)
        text_render = font.render(str(self.__player.score), True, pygame.Color(pygame.color.THECOLORS["white"]))
        self.__screen.blit(text_render,
                           (self.__screen_rect.right - TEXT_SIZE // 4 - text_render.get_rect().width, TEXT_SIZE // 4))

    def __draw_actors(self) -> None:
        self.__spaceship_sprite.draw(self.__screen)
        self.__asteroids_sprites.draw(self.__screen)
        self.__fires_sprites.draw(self.__screen)
        self.__draw_score()

    def __inside_game_loop(self) -> None:
        for event in pygame.event.get():
            self.__handle_game_events(event)
        self.__draw_screen_borders()
        if self.__shoot_fire:
            self.__init_fire()
        self.__detect_game_collisions()
        self.__update_actors()
        self.__draw_actors()

    def __init_end(self) -> None:
        self.__init_end_buttons()

    def __init_end_buttons(self) -> None:
        self.__end_buttons = pygame.sprite.Group()
        Button(
            pygame.Vector2(self.__screen_rect.width // 4, self.__screen_rect.bottom - 1.5 * TEXT_SIZE),
            pygame.Color(pygame.color.THECOLORS["orange"]),
            pygame.Color(pygame.color.THECOLORS["white"]),
            " Quit ",
            self.__end_buttons
        )
        self.__end_buttons.sprites()[0].center_at_width()
        Button(
            pygame.Vector2(3 * self.__screen_rect.width // 4, self.__screen_rect.bottom - 1.5 * TEXT_SIZE),
            pygame.Color(pygame.color.THECOLORS["green"]),
            pygame.Color(pygame.color.THECOLORS["white"]),
            "Replay",
            self.__end_buttons
        )
        self.__end_buttons.sprites()[1].center_at_width()

    def __handle_end_events(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if self.__end_buttons.sprites()[0].rect.collidepoint(event.pos):
                    self.__is_running = False
                    pygame.quit()
                    sys.exit()
                elif self.__end_buttons.sprites()[1].rect.collidepoint(event.pos):
                    self.__game_state = "level"
                    self.__level = 0
                    self.__init_level()
                    self.__player.score = 0
            case pygame.QUIT:
                self.__is_running = False
                pygame.quit()
                sys.exit()

    def __draw_top_5_scores(self) -> None:
        font = pygame.font.SysFont(None, TEXT_SIZE)
        i = 0.5
        text_render = font.render("Top 5 scores", True, pygame.Color(pygame.color.THECOLORS["white"]))
        self.__screen.blit(text_render, (self.__screen_rect.centerx - text_render.get_width() // 2, TEXT_SIZE * i))
        i += 1
        for player in self.__scores.players:
            text_render = font.render(player.name, True, pygame.Color(pygame.color.THECOLORS["white"]))
            self.__screen.blit(text_render, (TEXT_SIZE, TEXT_SIZE * i))
            text_render = font.render(str(player.score), True, pygame.Color(pygame.color.THECOLORS["white"]))
            self.__screen.blit(text_render,
                               (self.__screen_rect.right - TEXT_SIZE - text_render.get_rect().width, TEXT_SIZE * i))
            i += 1

    def __draw_end_buttons(self) -> None:
        self.__end_buttons.draw(self.__screen)
        self.__draw_top_5_scores()

    def __inside_end_loop(self) -> None:
        for event in pygame.event.get():
            self.__handle_end_events(event)
        self.__draw_end_buttons()

    def run(self) -> None:
        self.__is_running = True
        self.__frame_counter = 0
        self.__init_start()
        while self.__is_running:
            self.__clock.tick_busy_loop(FPS)
            self.__frame_counter += 1
            self.__screen.fill(GAME_COLOR)
            match self.__game_state:
                case "start":
                    self.__inside_start_loop()
                case "level":
                    self.__inside_level_loop()
                case "play":
                    self.__inside_game_loop()
                case "end":
                    self.__inside_end_loop()
            pygame.display.flip()


game = Game()
game.run()
