import pygame

from components.button import Button
from components.input_box import InputBox
from components.view import View


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 24)
    view = View(100, 100, 600, 400)

    # Create and add buttons, input boxes, etc. to the view
    button = Button(0, 0, 200, 50, "Click Me", font)
    input_box = InputBox(0, 70, 400, 50, font)
    view.add_child(button, offset=(20, 30))
    view.add_child(input_box, offset=(20, -50))

    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear the screen
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                view.handle_event(event)
                if button.is_pressed(event.pos):
                    print("Button clicked!")
            elif event.type == pygame.MOUSEMOTION:
                view.handle_event(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                view.handle_event(event)

            elif event.type == pygame.KEYDOWN:
                input_box.handle_event(event)
                if event.key == pygame.K_n:
                    input_box.active = True
            elif event.type == pygame.VIDEORESIZE:
                view.reposition_children()

        view.draw(screen)  # Draw the view and all its elements
        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
