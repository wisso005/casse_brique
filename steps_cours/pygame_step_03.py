# Importer tout le module Pygame
# Pygame DOIT être installé au préalable via `pip install pygame``
import pygame


# Définir la taille de la fenêtre de Pygame en pixels
WINDOW_SIZE: tuple[int, int]  = (480, 360)


# Définir la classe de l'application elle-même
class Game:
    __screen: pygame.Surface # attribut de l'écran Pygame de l'application
    __is_running: bool # attribut de contrôle de l'activation de l'application

    def __init__(self) -> None:
        # Initialiser tous les éléments de Pygame
        # https://www.pygame.org/docs/ref/pygame.html#pygame.init
        pygame.init()
        self.__is_running = False
        self.__init_screen()
    
    # Initialiser la fenêtre de l'application
    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(WINDOW_SIZE)
    
    # Gérer les événements
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
            # Dessiner un rectangle    
            pygame.draw.rect(self.__screen, pygame.Color(255, 255, 255), ((240, 180), (60, 45)))
            # Rafraîchir l'affichage de tout l'écran
            pygame.display.flip()
            

# Instancier le jeu (Singleton))
game = Game()
# Démarrer le jeu
game.run()
