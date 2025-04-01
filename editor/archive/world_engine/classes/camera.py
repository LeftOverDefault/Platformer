from world_engine.utils.imports import *


class Camera(pygame.sprite.Group):
    def __init__(self, display_surface, config) -> None:
        super().__init__()
        self.display_surface = display_surface

        self.config = config

        self.offset = pygame.Vector2()
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        
        # self.y_sorts = Layer(True, False)

        # self.camera_delay = 25
        self.keyboard_speed = 175
        self.mouse_speed = 4

        self.camera_borders = {'left': 50, 'right': 50, 'top': 25, 'bottom': 25}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = (self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right']))
        h = (self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom']))
        self.camera_rect = pygame.Rect(l,t,w,h)


        self.left_border = self.camera_borders['left']
        self.top_border = self.camera_borders['top']
        self.right_border = (pygame.display.get_surface().get_width()) - self.camera_borders['right']
        self.bottom_border = (pygame.display.get_surface().get_height()) - self.camera_borders['bottom']

        self.layers = {}
        for layer in self.config.layers:
            self.layers[layer] = {}

    
    def keyboard_control(self, delta_time):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2()

        if keys[pygame.K_w]:
            direction.y = -1
        elif keys[pygame.K_s]:
            direction.y = 1
        else:
            direction.y = 0
        
        if keys[pygame.K_a]:
            direction.x = -1
        elif keys[pygame.K_d]:
            direction.x = 1
        else:
            direction.x = 0

        if direction.magnitude() > 0:
            direction = direction.normalize()

        self.offset += direction * self.keyboard_speed * delta_time


    def mouse_control(self, delta_time):
        pygame.event.set_grab(True)
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset_vector = pygame.math.Vector2()


        if self.top_border < mouse.y < self.bottom_border:
            if mouse.x < self.left_border:
                mouse_offset_vector.x = mouse.x - self.left_border
            if mouse.x > self.right_border:
                mouse_offset_vector.x = mouse.x - self.right_border
        elif mouse.y < self.top_border:
            if mouse.x < self.left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(self.left_border,self.top_border)
            if mouse.x > self.right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(self.right_border,self.top_border)
        elif mouse.y > self.bottom_border:
            if mouse.x < self.left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(self.left_border,self.bottom_border)
            if mouse.x > self.right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(self.right_border,self.bottom_border)

        if self.left_border < mouse.x < self.right_border:
            if mouse.y < self.top_border:
                mouse_offset_vector.y = mouse.y - self.top_border
            if mouse.y > self.bottom_border:
                mouse_offset_vector.y = mouse.y - self.bottom_border

        self.offset += mouse_offset_vector * self.mouse_speed * delta_time


    def draw(self):
        for sprite in self:
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)


    def update(self, delta_time):
        self.keyboard_control(delta_time)
        # self.mouse_control(delta_time)
