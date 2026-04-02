import pygame


WINDOW_SIZE: tuple[int, int]  = (480, 360)
WINDOW_TITLE: str = "pygame_step_06" # Titre de la fenêtre du jeu
FPS: int = 6 # Frame Per Second = taux de rafraîchissement de l'affichage par seconde

# Définir la classe des acteurs
class Actor:
    __surface: pygame.Surface
    __color: pygame.Color
    __position: pygame.Vector2
    __size: pygame.Vector2
    __speed: pygame.Vector2
    
    def __init__(self, surface: pygame.Surface, color: pygame.Color, position: pygame.Vector2, size: pygame.Vector2, speed: pygame.Vector2) -> None:
        self.__surface = surface
        self.__color = color
        self.__position = position
        self.__size = size
        self.__speed = speed

    # Modifier l'acteur
    def update(self) -> None:
        self.__position += self.__speed
    
    # Dessiner l'acteur
    def draw(self) -> None:
        pygame.draw.rect(self.__surface, self.__color,(self.__position, self.__size))


class Game:
    __screen: pygame.Surface
    __is_running: bool
    __clock: pygame.time.Clock
    __actors: list[Actor]

    def __init__(self) -> None:
        pygame.init()
        self.__clock = pygame.time.Clock()
        self.__is_running = False
        self.__init_screen()

    # Initialiser la fenêtre de l'application    
    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(WINDOW_TITLE)

    # Initialiser les acteurs
    def __init_actors(self) -> None:
        self.__actors = []
        actor = Actor(
                      self.__screen,
                      pygame.Color(255, 255, 0),
                      pygame.Vector2(120, 90),
                      pygame.Vector2(60, 45),
                      pygame.Vector2(10, 7.5)
                     )
        self.__actors.append(actor)
        
    def __handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.__is_running = False
            pygame.quit()
            exit()

    # Mettre à jour les acteurs
    def __update_actors(self) -> None:
        for actor in self.__actors:
            actor.update()

    # Dessiner les acteurs
    def __draw_actors(self) -> None:
        for actor in self.__actors:
            actor.draw()
    
    def run(self) -> None:
        self.__is_running = True
        # Initialiser les acteurs
        self.__init_actors()
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
