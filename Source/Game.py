# Maybe add a while loop at line 333, so the player can get out of enemies,
# if they get stuck inside!


# We do this here, to disable the annoying pygame welcome message
import contextlib
with contextlib.redirect_stdout (None):
    import pygame

# Module imports
import importlib

# File imports
from UI import Window
from Utilities import Collection
from Modding import Loader, CallPluginFunctions
from Objects import Bomb, Enemy, Player, Wall, Notification
from Helpers import CheckWallCollision, CheckCollisions, CheckCollision

class Game:
    def __init__ (self, DoRestart = True, Tick = 60):
        self.Window = Window ('Game', 800, 600)
        self.ModLoader = Loader ()

        self.Player = Player (0, 0, 50, 50)
        self.Enemies = Collection (Enemy)
        self.Bombs = Collection (Bomb)
        self.Objects = []

        self.Screen = None
        self.Run = True
        self.DoRestart = DoRestart
        self.Tick = Tick

        self.Extensions = []
        self.Plugins = []
        self.CallableEvents = [
            'EventInit'
            'EventStart',
            'EventEnd',
            'EventCollision',
            'EventGameOver',
            'EventRestart',
            'EventFrame',
            'EventFixedFrame'
        ]

        self.Notifications = {}
        self.Messages = {
            'GameOver': 'You Died!'
        }

    def Restart (self):
        """ Restarts the game graphics """

        # Reset the players position
        self.Player.X = self.Player.OriginalX
        self.Player.Y = self.Player.OriginalY

        # Loop through all objects, and reset them
        for Object in self.Objects:
            # Set the x and y to the original x and y
            Object.X = Object.OriginalX
            Object.Y = Object.OriginalY

        # Call the restart event in all plugins
        CallPluginFunctions (self.Plugins, 'EventRestart')

    def LoadConfig (self, _Path):
        """ Loads a JSON config file """

        # Load the file
        self.ModLoader.Load (_Path)

        # Check if there's any mod data
        if self.ModLoader.Data:
            # Use the mods data
            self.ModLoader.SetData (self)

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

        # Call the init event in the plugin
        if 'EventInit' in dir (_Class):
            _Class.EventInit ()

    def AddNotification (self, _Text, _Duration = 500, _Priority = False):
        """ Add a notification the the waiting list """

        # Check if it's a priority notification
        if _Priority:
            # Create a new notification
            Notifications = {}
            Notifications[_Text] = Notification (_Text, _Duration)

            # This makes the new notification as the number one notification
            Notifications.update (self.Notifications)

            # Then set our notifications to the new notifications list
            self.Notifications = Notifications

        # It's not ..
        else:
            # Add a new notification to the notification list
            self.Notifications[str (len (self.Notifications) + 1)] = Notification (_Text, _Duration)

    def AddEnemy (self, _X, _Y, _Width, _Height):
        """ Add an enemy to the screen """

        # Appends a new enemy object
        self.Enemies.Add (
            Enemy (
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
        self.Enemies.RemoveIndex (_ID)

    def AddBomb (self, _X, _Y, _Width, _Height):
        """ Add a bomb to the screen """

        # Appends a new bomb object
        self.Bombs.Add (
            Bomb (
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
        self.Bombs.RemoveIndex (_ID)

    def Start (self):
        """ Run the game """

        # Initialize the window
        self.Screen = self.Window.Run ()
        DeltaTime = pygame.time.Clock ()

        # Call the start event in all plugins
        CallPluginFunctions (self.Plugins, 'EventStart')

        # Create the time and frame time variable
        Time = 0
        FrameTime = self.Tick // 2

        # Keep doing this, while the game is still running
        while self.Run:
            # Set the tick to 60
            DeltaTime.tick (self.Tick)

            # Increase time with 1
            Time += 1

            # Check if time and frame time are the same
            if Time == FrameTime:
                # Call the fixed frame event in all plugins, for this wall
                CallPluginFunctions (self.Plugins, 'EventFixedFrame')

                # Reset the time and frame time
                Time = 0
                FrameTime = int (DeltaTime.get_fps () // 2)

            # Create these variables so we can use them the whole frame
            DidCollide = False
            CollidedObject = None

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
                            # Call the collision event in all plugins, for this wall
                            CallPluginFunctions (self.Plugins, 'EventCollision', Wall ('Left Wall', self.Window.Height))

                            # Set the player's X to 0
                            self.Player.X = 0

                    # Move right
                    elif Event.key == pygame.K_RIGHT:
                        self.Player.X += self.Player.Speed

                        # Make sure we don't get out of the screen
                        if self.Player.X > self.Window.Width - self.Player.Width:
                            # Call the collision event in all plugins, for this wall
                            CallPluginFunctions (self.Plugins, 'EventCollision', Wall ('Right Wall', self.Window.Height))

                            # Set the player's X to the max width
                            self.Player.X = self.Window.Width - self.Player.Width

                    # Move up
                    elif Event.key == pygame.K_UP:
                        # Call the collision event in all plugins, for this wall
                        self.Player.Y -= self.Player.Speed

                        # Make sure we don't get out of the screen
                        if self.Player.Y < 0:
                            # Call the collision event in all plugins, for this wall
                            CallPluginFunctions (self.Plugins, 'EventCollision', Wall ('Top Wall', self.Window.Width))

                            # Set the player's Y to 0
                            self.Player.Y = 0

                    # Move up
                    elif Event.key == pygame.K_DOWN:
                        self.Player.Y += self.Player.Speed

                        # Make sure we don't get out of the screen
                        if self.Player.Y > self.Window.Height - self.Player.Height:
                            # Call the collision event in all plugins, for this wall
                            CallPluginFunctions (self.Plugins, 'EventCollision', Wall ('Bottom Wall', self.Window.Width))

                            # Set the player's Y to the max height
                            self.Player.Y = self.Window.Height - self.Player.Height

                    # Check if we've hit a bad thing
                    IsHit, Object = CheckCollisions (self.Player, self.Objects)

                    # If we hit a bad thing
                    if IsHit:
                        # Call the collision event in all plugins, for this object
                        CallPluginFunctions (self.Plugins, 'EventCollision', Object)

                        # Set the players x and y, back to what it was before doing movement
                        self.Player.X = OldX
                        self.Player.Y = OldY

                        # Set this variable to true, so we know later on we hit something
                        DidCollide = True
                        # Set the object variable to the object we hit
                        CollidedObject = Object

            # Reset background (necessary)
            self.Screen.fill (self.Window.BackgroundColor)

            # Call the frame event in all plugins
            CallPluginFunctions (self.Plugins, 'EventFrame')

            # Fill up the objects list
            self.Objects = self.Enemies.GetAll () + self.Bombs.GetAll ()
            self.Objects.append (self.Player)

            # Draw all objects
            self.Window.DrawObjects (self.Screen, self.Objects)

            # Define the FPS variable
            FPS = str (DeltaTime.get_fps ())
            # This will make sure the FPS maximum has 1 decimal
            FPSFixed = '{:.1f}'.format (float (FPS))

            # Draw the FPS
            self.Window.DrawText (
                self.Screen,
                FPSFixed,
                (
                    self.Window.Width - 50,
                    20
                )
            )

            # Check if our notifications is not empty
            if self.Notifications:
                # Draw the first notification to the screen
                self.Window.DrawNotification (self)

            # Create a new objects list, so we can remove the player from it
            Objects = self.Objects
            Objects.remove (self.Player)

            # Check if we've hit a bad thing
            IsHit, Object = CheckCollisions (self.Player, Objects)

            # Did we hit anything?
            if IsHit:
                # Call the collision event in all plugins, for this object
                CallPluginFunctions (self.Plugins, 'EventCollision', Object)

                # Set this variable to true, so we know later on we hit something
                DidCollide = True
                # Set the object variable to the object we hit
                CollidedObject = Object

            # We've hit a bad thing!
            if DidCollide:
                # Check if we wanna do a restart
                if self.DoRestart:
                    # Call the death event in all plugins
                    CallPluginFunctions (self.Plugins, 'EventGameOver')

                    # Call the restart function, to restart the graphics/objects
                    self.Restart ()

            # Update the display
            pygame.display.update ()

        # Call the end event in all plugins
        CallPluginFunctions (self.Plugins, 'EventEnd')

        # When the while loop is done, close the window
        pygame.quit ()
