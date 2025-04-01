import pygame


class Player( pygame.sprite.Sprite ):
    def __init__( self, position: tuple[ int, int ] = ( 0, 0 ), collision_sprites=[], group=None ):
        super().__init__( group )
        self.image = pygame.image.load( "assets/textures/entities/player/foxy/sprite/idle/0.png" )
        self.rect = self.image.get_rect( topleft=position )
    

    def input( self ) -> None:
        pass
