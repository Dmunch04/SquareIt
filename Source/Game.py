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
    """
        The main class of SquareIt. This class is the core

        Attributes:
            - Window -> Window Object:
                This attribute holds all the information of the window, and
                can only be tweaked in the init.

            - Player -> Player Object:
                This is the player object. It holds things such as x, y, width
                and height for the player. This can be changed anytime.

            - DoRestart -> Bool:
                This is a bool for whether the game should do a graphics restart
                when the player hits an object.

            - The rest of the attributes are not suggested you do anything with.
            You can simply use this classes functions to update them.


        Functions:
            - Restart -> None:
                Restarts the game graphics.

            - LoadExtension -> Path:
                Loads the extension at the path. Please not, that / should be .
                and you shouldn't put the .py file ending!

            - AddNotification -> Text, Duration (Frames), Priority = False:
                Adds a notification to the notification queue. When the notification
                is at the top of the queue, it will be displayed in the lower
                right corner. If you set priority to true, then it will be added
                as number one in the queue, and will therefor be displayed right
                away.

            - AddEnemy -> X, Y, Width, Height:
                Adds a new enemy to the screen, with the given position and size.

            - RemoveEnemy -> ID:
                Removes an enemy from the screen. The ID is the number of the enemy.
                So if you've added 3 enemies, and wanna remove number 3, then the ID
                is 3.

            - AddBomb -> X, Y, Width, Height:
                Adds a new bomb to the screen, with the given position and size.

            - RemoveBomb -> ID:
                Removes an bomb from the screen. The ID is the number of the bomb.
                So if you've added 7 bombs, and wanna remove number 4, then the ID
                is 4.

            - Start -> None:
                This starts the game, and makes the window open. This is also in
                the beginning of this function, the start event will be sent to
                the plugins.
    """

    def __init__ (self):
        self.Window = Window.Window ('Game', 800, 600)
        self.ModLoader = ModLoader.Loader ()
        self.Player = Player.Player (0, 0, 50, 50)
        self.Enemies = []
        self.Bombs = []
        self.Objects = []

        self.Screen = None
        self.Run = True
        self.DoRestart = True

        self.Extensions = []
        self.Plugins = []
        self.CallableEvents = [
            'EventInit'
            'EventStart',
            'EventEnd',
            'EventCollision',
            'EventGameOver',
            'EventRestart',
            'EventFrame'
        ]

        self.Notifications = {}
        self.Messages = {
            "GameOver": "You Died!"
        }

    def Restart (self):
        """ Restarts the game graphics """

        # Reset the players position
        self.Player.X = self.Player.OriginalX
        self.Player.Y = self.Player.OriginalY

        # Loop through all objects, and reset them
        for Object in self.Objects:
            Object.X = Object.OriginalX
            Object.Y = Object.OriginalY

        # Call the restart event in all plugins
        Plugin.CallPluginFunctions (self.Plugins, 'EventRestart')

    def LoadExtension (self, _Path):
        """ Loads an extension file """

        # Import the extension file
        Extension = importlib.import_module (_Path)

        # Check if there's a setup function in that file
        if 'Setup' in dir (Extension):
            # If there is, run it
            Extension.Setup (self)

        # Add the extension to the extension list
        self.Extensions.append (Extension)

    def AddPlugin (self, _Class):
        """ Adds a plugin class to the games plugins """

        # Add the plugin to the plugin list
        self.Plugins.append (_Class)

        # Call the init event in all plugins
        Plugin.CallPluginFunctions (self.Plugins, 'EventInit')

    def AddNotification (self, _Text, _Duration, _Priority = False):
        """ Add a notification the the waiting list """

        # Check if it's a priority notification
        if _Priority:
            # Create a new notification
            Notifications = {}
            Notifications['Died'] = {
                'Text': _Text,
                'Duration': _Duration
            }

            # This makes the new notification as the number one notification
            Notifications.update (self.Notifications)

            # Then set our notifications to the new notifications list
            self.Notifications = Notifications

        # It's not ..
        else:
            # Add a new notification to the notification list
            self.Notifications[str (len (self.Notifications) + 1)] = {
                'Text': _Text,
                'Duration': _Duration
            }

    def AddEnemy (self, _X, _Y, _Width, _Height):
        """ Add an enemy to the screen """

        # Appends a new enemy object
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

        # Removes the enemy at that ID
        del self.Enemies[_ID - 1]

    def AddBomb (self, _X, _Y, _Width, _Height):
        """ Add a bomb to the screen """

        # Appends a new bomb object
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

        # Removes the bomb at that ID
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

        while self.Run:
            IsHitObject, Object = Collision.CheckCollisions (self.Player, self.Objects)
            IsHitWall, Wall = Collision.CheckWallCollision (self.Player, self.Window.Width, self.Window.Height)

            if IsHitObject or IsHitWall:
                # Call the collision event in all plugins
                Plugin.CallPluginFunctions (self.Plugins, 'EventCollision', Object if Object else Wall)

            # Loop through all pygames events
            for Event in pygame.event.get ():
                # If we've hit the close button ...
                if Event.type == pygame.QUIT:
                    # ... Stop the loop
                    self.Run = False

                # Movement / Keyboard intereaction
                elif Event.type == pygame.KEYDOWN:
                    # Create these variables, so we can undo the movement
                    OldX = self.Player.X
                    OldY = self.Player.Y

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

                    # Check if we've hit a bad thing
                    IsHit, Object = Collision.CheckCollisions (self.Player, self.Objects)

                    # If we hit a bad thing
                    if IsHit:
                        # Set the players x and y, back to what it was before doing movement
                        self.Player.X = OldX
                        self.Player.Y = OldY

            # Reset background (necessary)
            self.Screen.fill (self.Window.BackgroundColor)

            # Call the frame event in all plugins
            Plugin.CallPluginFunctions (self.Plugins, 'EventFrame')

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

            # Check if we've hit something
            IsHit, Object = Collision.CheckCollisions (self.Player, Objects)

            # We've hit a bad thing!
            if IsHit:
                # Call the death event in all plugins
                Plugin.CallPluginFunctions (self.Plugins, 'EventGameOver')

                # Check if we wanna do a restart
                if self.DoRestart:
                    # Call the restart function, to restart the graphics/objects
                    self.Restart ()

            # Update the display
            pygame.display.update ()

        # Call the end event in all plugins
        Plugin.CallPluginFunctions (self.Plugins, 'EventEnd')

        # When the while loop is done, close the window
        pygame.quit ()
