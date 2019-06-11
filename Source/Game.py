# We do this here, to disable the annoying pygame welcome message
import contextlib
with contextlib.redirect_stdout (None):
    import pygame

import importlib

# File imports
from UI import Window
from Helpers import Collision
from Modding import ModLoader, Plugin
from Objects import Bomb, Enemy, Player

class Game:
    def __init__ (self):
        self.Window = Window.Window ('Game', 800, 600)
        self.ModLoader = ModLoader.Loader ()
        self.Player = Player.Player (0, 0, 50, 50)
        self.Enemies = []
        self.Bombs = []
        self.Objects = []

        self.Screen = None

        self.Extensions = []
        self.Plugins = []
        self.CallableEvents = [
            'EventStart',
            'EventEnd',
            'EventGameOver'
        ]

        self.Notifications = {}
        self.Messages = {
            "GameOver": "You Died!"
        }

    def Restart (self):
        pass

    def LoadExtension (self, _Path):
        """ Loads an extension file """

        Extension = importlib.import_module (_Path)

        if 'Setup' in dir (Extension):
            Extension.Setup (self)

        self.Extensions.append (Extension)

    def AddPlugin (self, _Class):
        """ Adds a plugin class to the games plugins """

        self.Plugins.append (_Class)

    def AddNotification (self, _Text, _Duration, _Priority = False):
        """ Add a notification the the waiting list """

        if _Priority:
            Notifications = {}
            Notifications['Died'] = {
                'Text': _Text,
                'Duration': _Duration
            }

            Notifications.update (self.Notifications)

            self.Notifications = Notifications

        else:
            self.Notifications[str (len (self.Notifications) + 1)] = {
                'Text': _Text,
                'Duration': _Duration
            }

    def AddEnemy (self, _X, _Y, _Width, _Height):
        """ Add an enemy to the screen """

        self.Enemies.append (
            Enemy.Enemy (
                len (self.Enemies) + 1,
                _X,
                _Y,
                _Width,
                _Height
            )
        )

    def RemoveEnemy (self, _ID):
        """ Remove an enemy by it's ID """

        del self.Enemies[_ID - 1]

    def AddBomb (self, _X, _Y, _Width, _Height):
        """ Add a bomb to the screen """

        self.Bombs.append (
            Bomb.Bomb (
                len (self.Bombs) + 1,
                _X,
                _Y,
                _Width,
                _Height
            )
        )

    def RemoveBomb (self, _ID):
        """ Remove a bomb by it's ID """

        del self.Bombs[_ID - 1]

    def Start (self):
        """ Run the game """

        # Initialize the window
        self.Screen = self.Window.Run ()

        # Call the start event in all plugins
        Plugin.CallPluginFunctions (self.Plugins, 'EventStart')

        # Check if there's any mod data
        if self.ModLoader.Data:
            # Use the mods data
            self.ModLoader.SetData (self)

        Run = True

        while Run:
            # Loop through all pygames events
            for Event in pygame.event.get ():
                # If we've hit the close button ...
                if Event.type == pygame.QUIT:
                    # ... Stop the loop
                    Run = False

                # Movement / Keyboard intereaction
                elif Event.type == pygame.KEYDOWN:
                    # Move left
                    if Event.key == pygame.K_LEFT:
                        self.Player.X -= self.Player.Speed

                        # Make sure we don't get out of the screen
                        if self.Player.X < 0:
                            self.Player.X = 0

                    # Move right
                    elif Event.key == pygame.K_RIGHT:
                        self.Player.X += self.Player.Speed

                        # Make sure we don't get out of the screen
                        if self.Player.X > self.Window.Width - self.Player.Width:
                            self.Player.X = self.Window.Width - self.Player.Width

                    # Move up
                    elif Event.key == pygame.K_UP:
                        self.Player.Y -= self.Player.Speed

                        # Make sure we don't get out of the screen
                        if self.Player.Y < 0:
                            self.Player.Y = 0

                    # Move up
                    elif Event.key == pygame.K_DOWN:
                        self.Player.Y += self.Player.Speed

                        # Make sure we don't get out of the screen
                        if self.Player.Y > self.Window.Height - self.Player.Height:
                            self.Player.Y = self.Window.Height - self.Player.Height

            # Reset background (neccessary)
            self.Screen.fill (self.Window.BackgroundColor)

            # Fill up the objects list
            self.Objects = self.Enemies + self.Bombs
            self.Objects.append (self.Player)

            # Draw all objects
            self.Window.DrawObjects (self.Screen, self.Objects)

            if self.Notifications:
                # Draw the first notification to the screen
                self.Window.DrawNotification (self)

            # Create a new objects list, so we can remove the player from it
            Objects = self.Objects
            Objects.remove (self.Player)

            # Collision check
            for Object in Objects:
                # Check if we've hit something
                IsHit = Collision.CheckCollision (self.Player, Object)

                # We've hit a bad thing! We die
                if IsHit:
                    # Call the death event in all plugins
                    Plugin.CallPluginFunctions (self.Plugins, 'EventGameOver')

                    # We actually shouldn't do anything here, and just let
                    # the plugins handle what should be done. But we will
                    # restart the game ofc.
                    """
                    # Print the death message
                    print (self.Messages['GameOver'])

                    # Stop the loop
                    Run = False
                    """
                    self.Restart ()

            # Update the display
            pygame.display.update ()

        # Call the end event in all plugins
        Plugin.CallPluginFunctions (self.Plugins, 'EventEnd')

        # When the while loop is done, close the window
        pygame.quit ()
