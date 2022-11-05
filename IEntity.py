import pygame


class IEntity:
    """
    Class to define base signature of all objects
    """

    def update(self, events: list[pygame.event.Event], dt):
        pass

    def draw(self, surf: pygame.Surface):
        pass