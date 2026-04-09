import pygame
import sys

WINDOW_SIZE: tuple[int, int]  = (1280, 720)
WINDOW_TITLE: str = "pygame_step_05" 
FPS: int = 6

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
    
class ActorPseudoSprite:
    __actor: Actor
    __color: pygame.Color
    __rect: pygame.Rect

    def __init__(self, actor: Actor, color: pygame.Color) -> None:
        self.__actor = actor
        self.__color = color
        self.__rect = pygame.Rect((self.__actor.position, self.__actor.size))

    def update(self) -> None:
        # Mettre à jour l'acteur
        self.__actor.update()
        # Mettre à jour la position du rectangle du pseudo-sprite de l'acteur
        self.__rect.update(self.__actor.position, self.__actor.size)
    # Dessiner l'acteur
    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.__color, self.__rect)
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
                             pygame.Vector2(350, 200),
                             pygame.Vector2(80, 15),
                             pygame.Vector2(10, 7.5)
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
    
    def __update_actors(self) -> None:
        for actor_pseudo_sprite in self.__actors_pseudo_sprites:
            actor_pseudo_sprite.update()

    # Dessiner les acteurs
    def __draw_actors(self) -> None:
        for actor_pseudo_sprite in self.__actors_pseudo_sprites:
            actor_pseudo_sprite.draw(self.__screen)

    # Méthode fondamentale utilisée pour exécuter une application Pygame
    def run(self) -> None:
        self.__is_running = True
        # Boucle infinie jusqu'à ce que `self.__is_running` soit définie à `False`
        while self.__is_running:
            self.__clock.tick_busy_loop(FPS)
            for event in pygame.event.get():
                self.__handle_events(event)
            # Mettre à jour les acteurs
            self.__update_actors()
            # Remplir le fonds de l'écran
            self.__screen.fill(pygame.color.THECOLORS["black"])
            # Dessiner les acteurs
            self.__draw_actors()
            # Rafraîchir l'affichage de tout l'écran
            pygame.display.flip()

# Instancier le jeu (Singleton)
game = Game()
# Démarrer le jeu
game.run()
