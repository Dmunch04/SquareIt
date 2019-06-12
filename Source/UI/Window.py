import pygame

class Window:
    def __init__ (self, Title, Width, Height):
        self.Title = Title
        self.Width = Width
        self.Height = Height

        pygame.init ()
        pygame.font.init ()

        self.Window = pygame.display.set_mode ((Width, Height))
        pygame.display.set_caption (Title)

        self.BackgroundColor = (255, 255, 255)
        self.FontRegular = pygame.font.Font ('Assets/Fonts/Roboto-Regular.ttf', 18)
        self.FontColor = (30, 30, 30)

    def UpdateTitle (self, _Title):
        """ Update the windows title """

        self.Title = str (_Title)

        pygame.display.set_caption (self.Title)

    def UpdateSize (self, _Width, _Height):
        """ Update the windows width and height """

        self.Width = int (_Width)
        self.Height = int (_Height)

        self.Window = pygame.display.set_mode ((self.Width, self.Height))

    def UpdateWidth (self, _Width):
        """ Update the windows width """

        self.Width = int (_Width)

        self.Window = pygame.display.set_mode ((self.Width, self.Height))

    def UpdateHeight (self, _Height):
        """ Update the windows height """

        self.Height = int (_Height)

        self.Window = pygame.display.set_mode ((self.Width, self.Height))

    def DrawObjects (self, _Screen, _Objects):
        """ Draw all the given objects """

        for Object in _Objects:
            pygame.draw.rect (
                _Screen,
                Object.Color,
                (
                    Object.X,
                    Object.Y,
                    Object.Width,
                    Object.Height
                )
            )

    def DrawNotification (self, _Object):
        """ Show the first notification """

        Notifications = list (_Object.Notifications)
        Notification = Notifications[0]

        ID = Notification
        Notification = _Object.Notifications[Notification]

        if Notification['Duration'] <= 0:
            del _Object.Notifications[ID]

            return

        Text = self.FontRegular.render (
            Notification["Text"],
            True,
            self.FontColor
        )

        _Object.Screen.blit (
            Text,
            (self.Width - (len (Notification['Text']) * 10), self.Height - 50)
        )

        _Object.Notifications[ID]['Duration'] -= 1

    def Run (self):
        return self.Window
