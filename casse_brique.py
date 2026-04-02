import pygame


WINDOW_SIZE: tuple[int, int]  = (1280, 720)

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
    __screen: pygame.Surface # attribut de l'écran Pygame de l'application
    __is_running: bool # attribut de contrôle de l'activation de l'application
    __actor: Actor # acteur du jeu

    def __init__(self) -> None:
        # Initialiser tous les éléments de Pygame
        # https://www.pygame.org/docs/ref/pygame.html#pygame.init
        pygame.init()
        self.__is_running = False
        self.__init_screen()
        self.__init_actor()

    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(WINDOW_SIZE)
        
    def __init_actor(self) -> None:
        self.__actor = Actor(
                             self.__screen,
                             pygame.Color(255, 255, 255),
                             pygame.Vector2(350, 200),
                             pygame.Vector2(80, 15),
                             pygame.Vector2(10, 1)
                            )
        
    # Méthode fondamentale utilisée pour exécuter une application Pygame
    def __handle_events(self, event: pygame.event.Event) -> None:
        # Test de l'état du type d'événement de Pygame
        if event.type == pygame.QUIT:
            # Mettre la variable de contrôle d'activité de l'application à `False`
            self.__is_running = False
            # Arrêter tous les éléments de Pygame
            pygame.quit()
    
    # Méthode fondamentale utilisée pour exécuter une application Pygame
    def run(self) -> None:
        # Mettre la variable de contrôle d'activité de l'application à `True`
        self.__is_running = True
        '''
            Le principe essentiel à comprendre est que Pygame doit actulaliser
            en permanence l'état de l'application.
        '''
        # Boucle infinie jusqu'à ce que `self.__is_running` soit définie à `False`
        while self.__is_running:
            # Boucle sur tous les événements gérés par Pygame
            for event in pygame.event.get():
                self.__handle_events(event)
            self.__actor.update()
            # Dessiner l'acteur
            self.__actor.draw()
            # Rafraîchir l'affichage de tout l'écran
            pygame.display.flip()

# Instancier le jeu (Singleton)
game = Game()
# Démarrer le jeu
game.run()
