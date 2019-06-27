# Module imports
import pygame

# File imports
from Objects import Wall
from Modding import CallPluginFunctions

def CheckInput (_Input, _Player, _Window, _Plugins):
    # Move left
    if _Input.key == pygame.K_LEFT:
        _Player.X -= _Player.Speed

        # Make sure we don't get out of the screen
        if _Player.X < 0:
            # Call the collision event in all plugins, for this wall
            CallPluginFunctions (_Plugins, 'EventCollision', Wall ('Left Wall', _Window.Height))

            # Set the player's X to 0
            _Player.X = 0

    # Move right
    elif _Input.key == pygame.K_RIGHT:
        _Player.X += _Player.Speed

        # Make sure we don't get out of the screen
        if _Player.X > _Window.Width - _Player.Width:
            # Call the collision event in all plugins, for this wall
            CallPluginFunctions (_Plugins, 'EventCollision', Wall ('Right Wall', _Window.Height))

            # Set the player's X to the max width
            _Player.X = _Window.Width - _Player.Width

    # Move up
    elif _Input.key == pygame.K_UP:
        # Call the collision event in all plugins, for this wall
        _Player.Y -= _Player.Speed

        # Make sure we don't get out of the screen
        if _Player.Y < 0:
            # Call the collision event in all plugins, for this wall
            CallPluginFunctions (_Plugins, 'EventCollision', Wall ('Top Wall', _Window.Width))

            # Set the player's Y to 0
            _Player.Y = 0

    # Move up
    elif _Input.key == pygame.K_DOWN:
        _Player.Y += _Player.Speed

        # Make sure we don't get out of the screen
        if _Player.Y > _Window.Height - _Player.Height:
            # Call the collision event in all plugins, for this wall
            CallPluginFunctions (_Plugins, 'EventCollision', Wall ('Bottom Wall', _Window.Width))

            # Set the player's Y to the max height
            _Player.Y = _Window.Height - _Player.Height
