import asyncio
import pygame

import core.constants as const
import core.setup as setup
import core.globals as globals
import core.assets as assets
import core.input as input
from components.statemachine import StateMachine
from scenes.world_1 import World1


def run() -> None:
    screen = pygame.display.get_surface()
    pygame.display.set_caption( const.CAPTION )
    pygame.display.set_icon( assets.ICON )
    scene_manager = StateMachine( World1 )
    asyncio.run( game_loop( screen, setup.clock, scene_manager ) )


def fullscreen() -> None:
    if globals.fullscreen == True:
        setup.window = pygame.display.set_mode( const.WINDOW_SIZE, pygame.SCALED | pygame.FULLSCREEN, const.WINDOW_SETUP[ "vsync" ] )
    else:
        setup.window = pygame.display.set_mode( const.WINDOW_SIZE, pygame.SCALED, const.WINDOW_SETUP[ "vsync" ] )


async def game_loop( surface: pygame.Surface, clock: pygame.Clock, scene_manager: StateMachine ) -> None:
    mouse_buffer: input.InputBuffer = [ input.InputState.NOTHING for _ in input.MouseButton ]

    action_buffer: input.InputBuffer = [ input.InputState.NOTHING for _ in input.Action ]

    last_action_mapping_pressed = [ input.action_mappings[action][0] for action in input.Action ]

    print( "Starting game loop" )

    while True:
        elapsed_time = clock.tick( const.FPS )
        dt = elapsed_time / 1000.0  # Convert to seconds
        dt = min( dt, const.MAX_DT )  # Clamp delta time

        running = input_event_queue()

        if not running:
            terminate( surface )

        update_action_buffer( action_buffer, last_action_mapping_pressed )
        update_mouse_buffer( mouse_buffer )

        scene_manager.execute( surface, dt, action_buffer, mouse_buffer )

        if ( action_buffer[ input.Action.DEBUG ] == input.InputState.PRESSED ):
            globals.debug = not globals.debug


        if globals.debug == True:
            debug_str = f"FPS {clock.get_fps():.0f}" # \nDT {dt}"
            debug_text = assets.DEBUG_FONT.render( debug_str, False, const.WHITE, const.BLACK )
            surface.blit( debug_text, ( 0, 0 ) )


        # Keep these calls together in this order
        pygame.display.flip()
        await asyncio.sleep( 0 )  # Very important, and keep it 0


def input_event_queue() -> bool:
    '''
    Pumps the event queue and handle application events
    Return: False if should terminate, else True
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.WINDOWFOCUSLOST:
            pass
        elif event.type == pygame.WINDOWFOCUSGAINED:
            pass
        elif event.type == pygame.VIDEORESIZE:
            pass

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            globals.fullscreen = not globals.fullscreen
            fullscreen()


        # HACK: For quick development
        # NOTE: It overrides exitting fullscreen when in browser
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return False

    return True


def update_action_buffer( action_buffer: input.InputBuffer, last_action_mapping_pressed: list[ pygame.key ] ) -> None: # type: ignore
    # get_just_pressed() and get_just_released() do not work with web ;(
    keys_held = pygame.key.get_pressed()
    for action in input.Action:
        if ( action_buffer[ action ] == input.InputState.NOTHING ):
            # Check if any alternate keys for the action were just pressed
            for mapping in input.action_mappings[ action ]:
                if mapping == last_action_mapping_pressed[ action ]:
                    continue

                # If an alternate key was pressed than last recorded key
                if keys_held[ mapping ]:
                    # Set that key bind as the current bind to 'track'
                    last_action_mapping_pressed[ action ] = mapping

        if keys_held[ last_action_mapping_pressed[ action ] ]:
            if ( action_buffer[ action ] == input.InputState.NOTHING or action_buffer[ action ] == input.InputState.RELEASED ):
                action_buffer[ action ] = input.InputState.PRESSED
            elif ( action_buffer[ action ] == input.InputState.PRESSED ):
                action_buffer[ action ] = input.InputState.HELD
        else:
            if ( action_buffer[ action ] == input.InputState.PRESSED or action_buffer[ action ] == input.InputState.HELD ):
                action_buffer[ action ] = input.InputState.RELEASED
            elif ( action_buffer[ action ] == input.InputState.RELEASED ):
                action_buffer[ action ] = input.InputState.NOTHING


def update_mouse_buffer( mouse_buffer: input.InputBuffer ) -> None:
    # get_just_pressed() and get_just_released() do not work with web ;(
    mouse_pressed = pygame.mouse.get_pressed()
    for button in input.MouseButton:
        if mouse_pressed[button]:
            if ( mouse_buffer[ button ] == input.InputState.NOTHING or mouse_buffer[ button ] == input.InputState.RELEASED ):
                mouse_buffer[ button ] = input.InputState.PRESSED
            elif ( mouse_buffer[ button ] == input.InputState.PRESSED ):
                mouse_buffer[ button ] = input.InputState.HELD
        else:
            if ( mouse_buffer[ button ] == input.InputState.PRESSED or mouse_buffer[ button ] == input.InputState.HELD ):
                mouse_buffer[ button ] = input.InputState.RELEASED
            elif ( mouse_buffer[ button ] == input.InputState.RELEASED ):
                mouse_buffer[ button ] = input.InputState.NOTHING


def terminate( surface: pygame.Surface ) -> None:
    print("Terminated application")

    pygame.mixer.stop()
    surface.fill( const.BLACK )

    pygame.quit()
    raise SystemExit
