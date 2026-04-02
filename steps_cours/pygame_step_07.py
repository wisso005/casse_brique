import pygame
# Importer la méthode de fin d'exécution de Python du module sys
from sys import exit


WINDOW_SIZE: tuple[int, int]  = (480, 360)
WINDOW_TITLE: str = "pygame_step_07" # Titre de la fenêtre du jeu
FPS: int = 6 # Frame Per Second = taux de rafraîchissement de l'affichage par seconde


# Définir la classe du modèle des acteurs
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

    # Déplacer l'acteur
    ''' Cette méthode est privée ! '''
    ''' 
        Il n'existe pas de solution pour rendre les méthodes
        `publique` via un décorateur comme pour les attributs,
        la seule solution est d'enlever les __ .
    '''
    def __move(self) -> None:
        self.__position += self.__speed

    # Mettre à jour l'acteur
    ''' Cette méthode est publique, car un Actor initié dans la classe Game doit pouvoir y accéder ! '''
    def update(self) -> None:
        self.__move()


# Définir la classe de la représentation graphique des acteurs
class ActorPseudoSprite:
    __actor: Actor
    __color: pygame.Color

    def __init__(self, actor: Actor, color: pygame.Color) -> None:
        self.__actor = actor
        self.__color = color

    # Dessiner l'acteur
    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.__color, (self.__actor.position, self.__actor.size))


class Game:
    __screen: pygame.Surface
    __is_running: bool
    __clock: pygame.time.Clock
    __actors: list[Actor]
    __actors_pseudo_sprites: list[ActorPseudoSprite]

    def __init__(self) -> None:
        pygame.init()
        self.__clock = pygame.time.Clock()
        self.__is_running = False
        self.__init_screen()
        # Initialiser les acteurs
        self.__init_actors()

    # Initialiser la fenêtre de l'application      
    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(WINDOW_TITLE)

    # Initialiser les acteurs
    def __init_actors(self) -> None:
        self.__actors = []
        self.__actors_pseudo_sprites = []
        actor = Actor(
                      pygame.Vector2(120, 90),
                      pygame.Vector2(60, 45),
                      pygame.Vector2(10, 7.5)
                      )
        self.__actors.append(actor)
        actor_pseudo_sprite = ActorPseudoSprite(
                                                  actor,
                                                  pygame.Color(255, 255, 0)
                                                )
        self.__actors_pseudo_sprites.append(actor_pseudo_sprite)


    def __handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.__is_running = False
            pygame.quit()
            # Terminer le processus Python
            exit()

    # Mettre à jour les acteurs
    def __update_actors(self) -> None:
        for actor in self.__actors:
            actor.update()

    # Dessiner les acteurs
    def __draw_actors(self) -> None:
        for actor_pseudo_sprite in self.__actors_pseudo_sprites:
            actor_pseudo_sprite.draw(self.__screen)
    
    def run(self) -> None:
        self.__is_running = True
        while self.__is_running:
            # Maintenir le taux de rafraîchissement
            self.__clock.tick_busy_loop(FPS)
            for event in pygame.event.get():
                self.__handle_events(event)
            # Remplir le fonds de l'écran
            self.__screen.fill(pygame.color.THECOLORS["black"])
            # Mettre à jour les acteurs
            self.__update_actors()
            # Dessiner les acteurs
            self.__draw_actors()
            # Rafraîchir l'affichage de tout l'écran
            pygame.display.flip()


# Instancier le jeu (Singleton)
game = Game()
# Démarrer le jeu
game.run()
