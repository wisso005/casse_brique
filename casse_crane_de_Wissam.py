import pygame
import sys
import random

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
        if hasattr(self, "_rect"):
            prev_size = (int(self._rect.w), int(self._rect.h))
        else:
            prev_size = None
        self._actor.update()

        new_size = (int(self._actor.size.x), int(self._actor.size.y))
        # Si la taille a changé, régénérer l'image et le rect
        if prev_size is None or new_size != prev_size:
            self._init_image()
            self._init_rect()
        # Mettre à jour la position du rect
        self._rect.topleft = (int(self._actor.position.x), int(self._actor.position.y))

class Button(pygame.sprite.Sprite):
    __position: pygame.Vector2
    __size: pygame.Vector2
    __color: pygame.Color
    __hover_color: pygame.Color
    __text_color: pygame.Color
    __text: str
    __hovered: bool

    def __init__(self, position: pygame.Vector2, text_color: pygame.Color, color: pygame.Color, hover_color: pygame.Color, text: str, *groups: pygame.sprite.Group, size: pygame.Vector2 = None) -> None:
        super().__init__(*groups)
        self.__position = position
        if size is None:
            self.__size = pygame.Vector2(len(text) * 18, 50)
        else:
            self.__size = size
        self.__color = color
        self.__hover_color = hover_color
        self.__text_color = text_color
        self.__text = text
        self.__hovered = False
        self.__init_button()

    def __init_button(self) -> None:
        self.image = pygame.Surface(self.__size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.__draw_button()
        self.update()

    def __draw_button(self) -> None:
        if self.__hovered:
            background = self.__hover_color
        else:
            background = self.__color
        self.image.fill(pygame.Color(0, 0, 0, 0))
        pygame.draw.rect(self.image, background, ((0, 0), self.__size), border_radius=8)
        pygame.draw.rect(self.image, pygame.Color("white"), ((0, 0), self.__size), width=2, border_radius=8)
        font = pygame.font.SysFont(None, 30)
        text_render = font.render(self.__text, True, self.__text_color)
        self.image.blit(text_render, ((self.__size.x - text_render.get_rect().width) // 2, (self.__size.y - text_render.get_rect().height) // 2))

    def center_at_width(self) -> None:
        self.__position.x = WINDOW_SIZE[0] / 2 - self.__size.x / 2
        self.update()

    def center_at_height(self) -> None:
        self.__position.y = WINDOW_SIZE[1] / 2 - self.__size.y / 2
        self.update()

    def set_position(self, position: pygame.Vector2) -> None:
        self.__position = position
        self.update()

    @property
    def text(self) -> str:
        return self.__text

    def set_hovered(self, hovered: bool) -> None:
        if self.__hovered != hovered:
            self.__hovered = hovered
            self.__draw_button()

    def update(self) -> None:
        self.rect.update(int(self.__position.x), int(self.__position.y), int(self.__size.x), int(self.__size.y))

class Ball(Actor):
    def bounce_x(self) -> None:
        self.speed.x = -self.speed.x

    def bounce_y(self) -> None:
        self.speed.y = -self.speed.y
    
    def on_collide_border(self, border_name: str) -> None:
        if border_name == "left":
            self.speed.x = abs(self.speed.x)
            self.position.x = WINDOW_BORDER_LINE_OFFSET
        elif border_name == "right":
            self.speed.x = -abs(self.speed.x)
            self.position.x = WINDOW_SIZE[0] - self.size.x - WINDOW_BORDER_LINE_OFFSET
        elif border_name == "top":
            self.speed.y = abs(self.speed.y)
            self.position.y = WINDOW_BORDER_LINE_OFFSET
        elif border_name == "bottom":
            # La balle est perdue
            self.destroy()

    def on_collide_actor(self, other: "Actor", collision_axis: str | None = None) -> None:
        if isinstance(other, Paddle):
            rel_x, rel_y = pygame.mouse.get_rel()
            self.bounce_y()
            if rel_x != 0:
                self.speed.x = max(-10, min(10, rel_x))
        else:
            if collision_axis == "horizontal":
                self.bounce_x()
            else:
                self.bounce_y()

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

class Paddle(Actor):
    def __init__(self, position: pygame.Vector2, size: pygame.Vector2, speed: pygame.Vector2) -> None:
        super().__init__(position, size, speed)
        self._previous_position = pygame.Vector2(position)
        self._actual_velocity = pygame.Vector2(0, 0)

    @property
    def actual_velocity(self) -> pygame.Vector2:
        return self._actual_velocity

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

        self._actual_velocity = self._position - self._previous_position
        self._previous_position = pygame.Vector2(self._position)

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
    def _get_color_by_health(self) -> pygame.Color:
        #Calcule la couleur en fonction des HP de la brique.
        brick = self._actor
        current_health = brick.health
        
        if current_health <= 0:
            return pygame.Color(0, 0, 0)
        elif current_health == 3:
            return pygame.Color("red")
        elif current_health == 2:
            return pygame.Color("#990000")
        else:
            return pygame.Color("#330000")
    
    def _init_image(self) -> None:
        size = (int(self._actor.size.x), int(self._actor.size.y))
        self._image = pygame.Surface(size, pygame.SRCALPHA)
        color = self._get_color_by_health()
        pygame.draw.rect(self._image, color, ((0, 0), size))
    
    def update(self) -> None:
        if hasattr(self, "_rect"):
            prev_size = (int(self._rect.w), int(self._rect.h))
        else:
            prev_size = None

        self._actor.update()
        new_size = (int(self._actor.size.x), int(self._actor.size.y))
        if prev_size is None or new_size != prev_size:
            self._init_image()
            self._init_rect()
        else:
            self._init_image()
        self._rect.topleft = (int(self._actor.position.x), int(self._actor.position.y))

class PowerUp(Actor):
    def __init__(self, position: pygame.Vector2) -> None:
        # Taille de 15x15, et vitesse vers le bas (y = 3)
        super().__init__(position, pygame.Vector2(10, 10), pygame.Vector2(0, 3))

    def on_collide_border(self, border_name: str) -> None:
        if border_name == "bottom":
            self.destroy()

class PowerUpSprite(ActorPseudoSprite):
    def _init_image(self) -> None:
        size = (int(self._actor.size.x), int(self._actor.size.y))
        self._image = pygame.Surface(size, pygame.SRCALPHA)
        # On dessine un cercle jaune pour différencier le powerup des briques
        pygame.draw.circle(
            self._image, 
            pygame.Color("yellow"), 
            (size[0] // 2, size[1] // 2), 
            min(size[0], size[1]) // 2
        )

MAIN_MENU: str = "main_menu"
PLAYING: str = "playing"
GAME_OVER: str = "game_over"

class Game:
    __screen: pygame.Surface
    __screen_borders_lines: dict[str, pygame.Rect]
    __is_running: bool
    __clock: pygame.time.Clock
    __paddles_sprites: pygame.sprite.GroupSingle #une seule raquette 
    __balls_sprites: pygame.sprite.Group
    __bricks_sprites: pygame.sprite.Group
    __game_state: str
    __menu_buttons: pygame.sprite.Group
    __powerups_sprites: pygame.sprite.Group

    def __init__(self) -> None:
        pygame.init()
        self.__clock = pygame.time.Clock()
        self.__is_running = False
        self.__game_state = MAIN_MENU
        self.__active_powerups: dict[str, int] = {}
        self.__init_screen()
        self.__reset_actors()
        self.__init_menu_buttons()
        self.__init_game_over_buttons()

    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(WINDOW_TITLE)

    def __reset_actors(self) -> None:
        self.__paddles_sprites = pygame.sprite.GroupSingle()
        self.__balls_sprites = pygame.sprite.Group()
        self.__bricks_sprites = pygame.sprite.Group()
        self.__powerups_sprites = pygame.sprite.Group()

        paddle = Paddle(
            pygame.Vector2(590, 700),
            pygame.Vector2(100, 10),
            pygame.Vector2(0, 0)
        )
        ActorPseudoSprite(paddle, pygame.Color("white"), self.__paddles_sprites)

        ball = Ball(
            pygame.Vector2(random.randint(100, 1180), 680),
            pygame.Vector2(10, 10),
            pygame.Vector2(random.randint(-15,15), -10)
        )
        BallSprite(ball, pygame.Color("green"), self.__balls_sprites)

        for row in range(3):
            for col in range(14):
                brick = Brick(
                    pygame.Vector2(45 + col * 85, 100 + row * 20),
                    pygame.Vector2(80, 15),
                    pygame.Vector2(0, 0),
                    3
                )
                BrickSprite(brick, pygame.Color("red"), self.__bricks_sprites)

    def __start_new_game(self) -> None:
        self.__reset_actors()
        self.__game_state = PLAYING

    def __return_to_menu(self) -> None:
        self.__game_state = MAIN_MENU

    def __init_menu_buttons(self) -> None:
        self.__menu_buttons = pygame.sprite.Group()
        Button(
            pygame.Vector2(WINDOW_SIZE[0] / 2, 360),
            pygame.Color("white"),
            pygame.Color("#333333"),
            pygame.Color("#555555"),
            "Jouer",
            self.__menu_buttons,
            size=pygame.Vector2(200, 80)
        )
        Button(
            pygame.Vector2(WINDOW_SIZE[0] / 2, 480),
            pygame.Color("white"),
            pygame.Color("#333333"),
            pygame.Color("#555555"),
            "Quitter (Q)",
            self.__menu_buttons,
            size=pygame.Vector2(150, 50)
        )
        for button in self.__menu_buttons.sprites():
            button.center_at_width()

    def __init_game_over_buttons(self) -> None:
        self.__game_over_buttons = pygame.sprite.Group()
        Button(
            pygame.Vector2(WINDOW_SIZE[0] / 2, 360),
            pygame.Color("white"),
            pygame.Color("#333333"),
            pygame.Color("#555555"),
            "Recommencer (R)",
            self.__game_over_buttons
        )
        Button(
            pygame.Vector2(WINDOW_SIZE[0] / 2, 440),
            pygame.Color("white"),
            pygame.Color("#333333"),
            pygame.Color("#555555"),
            "Menu (M)",
            self.__game_over_buttons
        )
        Button(
            pygame.Vector2(WINDOW_SIZE[0] / 2, 520),
            pygame.Color("white"),
            pygame.Color("#333333"),
            pygame.Color("#555555"),
            "Quitter (Q)",
            self.__game_over_buttons,
            size=pygame.Vector2(120, 50)
        )
        for button in self.__game_over_buttons.sprites():
            button.center_at_width()

    def __game_over(self) -> None:
        self.__game_state = GAME_OVER

    def __draw_text(
        self,
        text: str,
        size: int,
        color: pygame.Color,
        position: tuple[int, int],
        center: bool = False
    ) -> None:
        font = pygame.font.SysFont(None, size)
        rendered = font.render(text, True, color)
        rect = rendered.get_rect()
        if center:
            rect.center = position
        else:
            rect.topleft = position
        self.__screen.blit(rendered, rect)

    def __draw_menu(self) -> None:
        self.__screen.fill(pygame.color.THECOLORS["black"])
        self.__draw_text("Casse Briques De Bea et Wiss", 72, pygame.Color("white"), (WINDOW_SIZE[0] // 2, 160), center=True)
        self.__draw_text("Cliquez sur un bouton ou appuyez sur ESPACE pour jouer", 30, pygame.Color("white"), (WINDOW_SIZE[0] // 2, 240), center=True)
        self.__draw_text("Gauche / Droite ou utilisez la souris pour déplacer la raquette", 30, pygame.Color("white"), (WINDOW_SIZE[0] // 2, 300), center=True)
        self.__menu_buttons.draw(self.__screen)

    def __draw_game_over(self) -> None:
        self.__screen.fill(pygame.color.THECOLORS["black"])
        self.__draw_text("ÉCHEC !", 72, pygame.Color("red"), (WINDOW_SIZE[0] // 2, 180), center=True)
        self.__draw_text("La balle est tombée.", 36, pygame.Color("white"), (WINDOW_SIZE[0] // 2, 260), center=True)
        self.__draw_text("Utilisez les boutons ci-dessous", 28, pygame.Color("white"), (WINDOW_SIZE[0] // 2, 320), center=True)
        self.__game_over_buttons.draw(self.__screen)

    def __handle_menu_event(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.QUIT:
                self.__is_running = False
                pygame.quit()
                sys.exit()
            case pygame.MOUSEMOTION:
                for button in self.__menu_buttons.sprites():
                    button.set_hovered(button.rect.collidepoint(event.pos))
            case pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.__menu_buttons.sprites():
                        if button.rect.collidepoint(event.pos):
                            if button.text == "Jouer":
                                self.__start_new_game()
                            elif button.text == "Quitter (Q)":
                                self.__is_running = False
                                pygame.quit()
                                sys.exit()
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_SPACE:
                        self.__start_new_game()
                    case pygame.K_q | pygame.K_ESCAPE:
                        self.__is_running = False
                        pygame.quit()
                        sys.exit()

    def __handle_playing_event(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.QUIT:
                self.__is_running = False
                pygame.quit()
                sys.exit()
            case pygame.MOUSEMOTION:
                if self.__paddles_sprites.sprite is not None:
                    if pygame.mouse.get_focused():
                        self.__paddles_sprites.sprite.actor.position = pygame.Vector2(pygame.mouse.get_pos())
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_LEFT:
                        if self.__paddles_sprites.sprite is not None:
                            self.__paddles_sprites.sprite.actor.speed = -PADDLE["speed"].copy()
                    case pygame.K_RIGHT:
                        if self.__paddles_sprites.sprite is not None:
                            self.__paddles_sprites.sprite.actor.speed = PADDLE["speed"].copy()
                    case pygame.K_ESCAPE:
                        self.__return_to_menu()
            case pygame.KEYUP:
                match event.key:
                    case pygame.K_LEFT | pygame.K_RIGHT:
                        if self.__paddles_sprites.sprite is not None:
                            self.__paddles_sprites.sprite.actor.speed = NULL_PYGAME_VECTOR2.copy()

    def __handle_game_over_event(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.QUIT:
                self.__is_running = False
                pygame.quit()
                sys.exit()
            case pygame.MOUSEMOTION:
                for button in self.__game_over_buttons.sprites():
                    button.set_hovered(button.rect.collidepoint(event.pos))
            case pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.__game_over_buttons.sprites():
                        if button.rect.collidepoint(event.pos):
                            if button.text == "Recommencer (R)":
                                self.__start_new_game()
                            elif button.text == "Menu (M)":
                                self.__return_to_menu()
                            elif button.text == "Quitter (Q)":
                                self.__is_running = False
                                pygame.quit()
                                sys.exit()
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_r:
                        self.__start_new_game()
                    case pygame.K_m:
                        self.__return_to_menu()
                    case pygame.K_q | pygame.K_ESCAPE:
                        self.__is_running = False
                        pygame.quit()
                        sys.exit()

    # Créer les bords de l'écran
    def __draw_screen_borders(self) -> None:
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
        for actor_pseudo_sprite in list(self.__balls_sprites) + list(self.__powerups_sprites):
            actor = actor_pseudo_sprite.actor
            
            if actor.position.x <= WINDOW_BORDER_LINE_OFFSET:
                actor.on_collide_border("left")
            if actor.position.x + actor.size.x >= WINDOW_SIZE[0] - WINDOW_BORDER_LINE_OFFSET:
                actor.on_collide_border("right")
                
            if actor.position.y <= WINDOW_BORDER_LINE_OFFSET:
                actor.on_collide_border("top")
            if actor.position.y + actor.size.y >= WINDOW_SIZE[1]:
                actor.on_collide_border("bottom")
                
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
        
        is_piercing = "piercing_ball" in self.__active_powerups # Vrai ou Faux

        for ball_sprite, bricks_sprites in collisions.items():
            ball = ball_sprite.actor
            for brick_sprite in bricks_sprites:
                brick = brick_sprite.actor
                ball_rect = ball_sprite.rect
                brick_rect = brick_sprite.rect
                overlap_x = min(ball_rect.right, brick_rect.right) - max(ball_rect.left, brick_rect.left)
                overlap_y = min(ball_rect.bottom, brick_rect.bottom) - max(ball_rect.top, brick_rect.top)
                
                if overlap_x < overlap_y:
                    collision_axis = "horizontal"
                else:
                    collision_axis = "vertical"
                
                # REBOND UNIQUEMENT SI NON-TRANSPERÇANT
                if not is_piercing:
                    ball.on_collide_actor(brick, collision_axis=collision_axis)
                
                brick.hit()
                if brick.health <= 0:
                    brick_sprite.kill()
                    # 50% de chance de loot un power-up (comme fait à l'étape précédente)
                    if random.random() < 0.50: 
                        pu_pos = pygame.Vector2(
                            brick.position.x + (brick.size.x / 2) - 7.5, 
                            brick.position.y
                        )
                        pu = PowerUp(pu_pos)
                        PowerUpSprite(pu, pygame.Color("yellow"), self.__powerups_sprites)
    def __apply_random_powerup(self) -> None:
        if self.__paddles_sprites.sprite is None:
            return
        
        paddle = self.__paddles_sprites.sprite.actor
        balls = [sprite.actor for sprite in self.__balls_sprites.sprites()]
        if not balls: return

        effect = random.randint(1, 7)
        current_time = pygame.time.get_ticks()

        match effect:
            case 1:
                # 1. Agrandir la raquette (10s)
                paddle.set_size(pygame.Vector2(200, 10))
                self.__active_powerups["enlarge_paddle"] = current_time + 10000
                self.__active_powerups.pop("shrink_paddle", None) # Annule l'effet inverse
            
            case 2:
                # 2. Rapetissir la raquette (10s)
                paddle.set_size(pygame.Vector2(50, 10))
                self.__active_powerups["shrink_paddle"] = current_time + 10000
                self.__active_powerups.pop("enlarge_paddle", None)
            
            case 3:
                # 3. Balle ralentie (5s)
                for b in balls:
                    b.speed.y = 5 if b.speed.y > 0 else -5
                self.__active_powerups["slow_ball"] = current_time + 5000
                self.__active_powerups.pop("fast_ball", None)
            
            case 4:
                # 4. Balle accélérée (5s)
                for b in balls:
                    b.speed.y = 15 if b.speed.y > 0 else -15
                self.__active_powerups["fast_ball"] = current_time + 5000
                self.__active_powerups.pop("slow_ball", None)
            
            case 5:
                # 5. Balles supplémentaires (+10 balles)
                is_slow = "slow_ball" in self.__active_powerups
                is_fast = "fast_ball" in self.__active_powerups
                
                for _ in range(10):
                    new_ball = Ball(
                        pygame.Vector2(random.randint(100, 1180), 680),
                        pygame.Vector2(10, 10),
                        pygame.Vector2(random.randint(-15, 15), -10)
                    )
                    # Appliquer la vitesse en cours si un power-up de vitesse est actif
                    if is_slow: new_ball.speed.y = -5
                    elif is_fast: new_ball.speed.y = -15
                    
                    BallSprite(new_ball, pygame.Color("green"), self.__balls_sprites)
            
            case 6:
                # 6. Balle invisible (2s)
                self.__active_powerups["invisible_ball"] = current_time + 2000
            
            case 7:
                # 7. Balle transperçante (10s)
                self.__active_powerups["piercing_ball"] = current_time + 10000
    def __handle_powerups_paddle_collisions(self) -> None:
        collisions = pygame.sprite.groupcollide(
            self.__powerups_sprites,
            self.__paddles_sprites,
            True,  # True = détruit le powerup
            False  # False = ne détruit pas la raquette
        )
        for powerup in collisions:
            self.__apply_random_powerup()
    
    def __update_powerups_timers(self) -> None:
        current_time = pygame.time.get_ticks()
        expired_effects = []

        # Identifier les effets expirés
        for effect, end_time in self.__active_powerups.items():
            if current_time >= end_time:
                expired_effects.append(effect)

        # Nettoyer et réinitialiser
        for effect in expired_effects:
            del self.__active_powerups[effect]

            if effect in ("enlarge_paddle", "shrink_paddle"):
                if self.__paddles_sprites.sprite is not None:
                    # Taille par défaut de la raquette
                    self.__paddles_sprites.sprite.actor.set_size(pygame.Vector2(100, 10))
            
            elif effect in ("slow_ball", "fast_ball"):
                # Vitesse y par défaut de la balle (10)
                for sprite in self.__balls_sprites.sprites():
                    b = sprite.actor
                    b.speed.y = 10 if b.speed.y > 0 else -10

    def __update_actors(self) -> None:
        self.__paddles_sprites.update()
        self.__balls_sprites.update()
        self.__bricks_sprites.update()
        self.__powerups_sprites.update()

    def __draw_actors(self) -> None:
        self.__paddles_sprites.draw(self.__screen)
        self.__bricks_sprites.draw(self.__screen)
        self.__powerups_sprites.draw(self.__screen)
        
        # Gestion du clignotement des balles
        if "invisible_ball" in self.__active_powerups:
            current_time = pygame.time.get_ticks()
            # Fait clignoter la balle toutes les 150 millisecondes
            if (current_time // 150) % 2 == 0:
                self.__balls_sprites.draw(self.__screen)
        else:
            # Affichage normal
            self.__balls_sprites.draw(self.__screen)

    def __check_game_over(self) -> None:
        if len(self.__balls_sprites) == 0:
            self.__game_over()

    def run(self) -> None:
        self.__is_running = True

        while self.__is_running:
            self.__clock.tick_busy_loop(FPS)
            for event in pygame.event.get():
                if self.__game_state == MAIN_MENU:
                    self.__handle_menu_event(event)
                elif self.__game_state == PLAYING:
                    self.__handle_playing_event(event)
                elif self.__game_state == GAME_OVER:
                    self.__handle_game_over_event(event)

            if self.__game_state == MAIN_MENU:
                self.__draw_menu()
            elif self.__game_state == PLAYING:
                self.__screen.fill(pygame.color.THECOLORS["black"])
                self.__draw_screen_borders()
                self.__update_actors()
                self.__update_powerups_timers()
                self.__handle_borders_collisions()
                self.__handle_balls_paddle_collisions()
                self.__handle_balls_bricks_collisions()
                self.__handle_powerups_paddle_collisions()
                self.__draw_actors()
                self.__check_game_over()
            elif self.__game_state == GAME_OVER:
                self.__draw_game_over()

            # Rafraîchir l'affichage
            pygame.display.flip()

# Instancier le jeu (Singleton)
game = Game()
# Démarrer le jeu
game.run()
