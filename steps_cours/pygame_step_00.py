# Importer tout le module Pygame
# Pygame DOIT être installé au préalable via `pip install pygame``
import pygame


# Initialiser tous les éléments de Pygame
# https://www.pygame.org/docs/ref/pygame.html#pygame.init
pygame.init()

# Créer la fenêtre de l'application
screen: pygame.Surface = pygame.display.set_mode((480, 360))

# Initiliser la variable de contrôle d'activité de l'application
is_running: bool = True

'''
    Le principe essentiel à comprendre est que Pygame doit actulaliser
    en permanence l'état de l'application.
'''
# Boucle infinie jusqu'à ce que `is_running` soit définie à `False`
while is_running:
    # Boucle sur tous les événements gérés par Pygame
    for event in pygame.event.get():
        # Test de l'état du type d'événement de Pygame
        if event.type == pygame.QUIT:
            # Mettre la variable de contrôle d'activité de l'application à `False`
            is_running = False
            # Arrêter tous les éléments de Pygame
            pygame.quit()
