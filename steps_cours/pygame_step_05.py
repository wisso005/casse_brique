import pygame
# Importer la méthode de fin d'exécution de Python du module sys
from sys import exit

# Définir la taille de la fenêtre de Pygame en pixels
WINDOW_SIZE: tuple[int, int]  = (480, 360)
WINDOW_TITLE: str = "pygame_step_05" # Titre de la fenêtre du jeu
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


# Définir la classe de l'application elle-même
class Game:
    __screen: pygame.Surface # attribut de l'écran Pygame de l'application
    __is_running: bool # attribut de contrôle de l'activation de l'application
    __clock: pygame.time.Clock # horloge du jeu
    __actor: Actor # acteur du jeu

    def __init__(self) -> None:
        # Initialiser tous les éléments de Pygame
        # https://www.pygame.org/docs/ref/pygame.html#pygame.init
        pygame.init()
        # Initiation de l'horloge
        self.__clock = pygame.time.Clock()
        self.__is_running = False
        self.__init_screen()
    
    # Initialiser la fenêtre de l'application
    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(WINDOW_TITLE)

    def __init_actor(self) -> None:
        self.__actor = Actor(
                             self.__screen,
                             pygame.Color(255, 255, 0),
                             pygame.Vector2(120, 90),
                             pygame.Vector2(60, 45),
                             pygame.Vector2(10, 7.5)
                            )
    
    # Gérer les événements
    def __handle_events(self, event: pygame.event.Event) -> None:
        # Test de l'état du type d'événement de Pygame
        if event.type == pygame.QUIT:
            # Mettre la variable de contrôle d'activité de l'application à `False`
            self.__is_running = False
            # Arrêter tous les éléments de Pygame
            pygame.quit()
            # Terminer le processus Python
            exit()
    
    # Méthode fondamentale utilisée pour exécuter une application Pygame
    def run(self) -> None:
        # Mettre la variable de contrôle d'activité de l'application à `True`
        self.__is_running = True
        '''
            Le principe essentiel à comprendre est que Pygame doit actulaliser
            en permanence l'état de l'application.
        '''
        # Initialiser l'acteur
        self.__init_actor()
        # Boucle infinie jusqu'à ce que `self.__is_running` soit définie à `False`
        while self.__is_running:
            # Maintenir le taux de rafraîchissement
            self.__clock.tick_busy_loop(FPS)
            # Boucle sur tous les événements gérés par Pygame
            for event in pygame.event.get():
                self.__handle_events(event)
            # Mettre à jour l'acteur
            self.__actor.update()
            # Remplir le fonds de l'écran
            self.__screen.fill(pygame.color.THECOLORS["black"])
            # Dessiner l'acteur
            self.__actor.draw()
            # Rafraîchir l'affichage de tout l'écran
            pygame.display.flip()


# Instancier le jeu (Singleton)
game = Game()
# Démarrer le jeu
game.run()
