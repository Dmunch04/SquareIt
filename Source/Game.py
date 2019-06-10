import pygame

from UI import Window
from Helpers import Collision
from Modding import ModLoader
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

        self.Notifications = {}
        self.Messages = {
            "GameOver": "You Died!"
        }

    def AddNotification (self, _Text, _Duration):
        self.Notifications[str (len (self.Notifications) + 1)] = {
            'Text': _Text,
            'Duration': _Duration
        }

    def AddEnemy (self, _X, _Y, _Width, _Height):
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
        del self.Enemies[_ID - 1]

    def AddBomb (self, _X, _Y, _Width, _Height):
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
        del self.Bombs[_ID - 1]

    def Start (self):
        self.Screen = self.Window.Run ()

        Run = True

        while Run:
            if self.ModLoader.Data:
                # Use the mods data
                self.ModLoader.SetData (self)

            for Event in pygame.event.get ():
                if Event.type == pygame.QUIT:
                    Run = False

                # Movement / Keyboard intereaction
                elif Event.type == pygame.KEYDOWN:
                    if Event.key == pygame.K_LEFT:
                        self.Player.X -= self.Player.Speed

                        if self.Player.X < 0:
                            self.Player.X = 0

                    elif Event.key == pygame.K_RIGHT:
                        self.Player.X += self.Player.Speed

                        if self.Player.X > self.Window.Width - self.Player.Width:
                            self.Player.X = self.Window.Width - self.Player.Width

                    elif Event.key == pygame.K_UP:
                        self.Player.Y -= self.Player.Speed

                        if self.Player.Y < 0:
                            self.Player.Y = 0

                    elif Event.key == pygame.K_DOWN:
                        self.Player.Y += self.Player.Speed

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
                # Draw the notifications
                self.Window.DrawNotifications (self)

            # Create a new objects list, so we can remove the player from it
            Objects = self.Objects
            Objects.remove (self.Player)

            # Collision check
            for Object in Objects:
                IsHit = Collision.CheckCollision (self.Player, Object)

                if IsHit:
                    print (self.Messages['GameOver'])

                    Run = False

            pygame.display.update ()

        pygame.quit ()
