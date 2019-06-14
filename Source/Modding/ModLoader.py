import json

from Modding import Mod as ModObject

class Loader:
    def __init__ (self):
        self.Mods = []
        self.Data = {}

    def Load (self, _Mod):
        """ Prepare the mod """

        with open (_Mod, 'r') as ModFile:
            ModData = json.loads (ModFile.read ())

        if not ModData['Name'] in self.Mods:
            self.Mods.append (ModData['Name'])

        Name = ModData.get ('Name', 'Untitled')
        Version = ModData.get ('Version', '0.0.1')
        Author = ModData.get ('Author', 'Anonymous')
        Description = ModData.get ('Description', 'A Mod')
        Data = ModData.get ('Data', {})

        if Data:
            self.Data[Name] = Data

        Mod = ModObject (
            Name,
            Version,
            Author,
            Description,
            Data
        )

        return Mod

    def Unload (self, _Mod):
        """ Remove the mod and it's data """

        if _Mod in self.Mods:
            del self.Mods[self.Mods.index (_Mod)]

            self.Data[_Mod] = {}

    def SetData (self, _Object):
        """ Apply the mods data to the game """

        NotificationsToAdd = {}

        for Mod in self.Data:
            Data = self.Data[Mod]

            if Data:
                WindowSettings = Data.get ('Window', {})
                if WindowSettings:
                    Color = WindowSettings.get ('Color', _Object.Window.BackgroundColor)

                    _Object.Window.BackgroundColor = Color

                GameSettings = Data.get ('Game', {})
                if GameSettings:
                    Enemies = GameSettings.get ('Enemies', [])
                    if Enemies:
                        for Enemy in Enemies:
                            X = Enemy.get ('X', 0)
                            Y = Enemy.get ('Y', 0)
                            Width = Enemy.get ('Width', 50)
                            Height = Enemy.get ('Height', 50)

                            _Object.AddEnemy (
                                X,
                                Y,
                                Width,
                                Height
                            )

                    Bombs = GameSettings.get ('Bombs', [])
                    if Bombs:
                        for Bomb in Bombs:
                            X = Bomb.get ('X', 0)
                            Y = Bomb.get ('Y', 0)
                            Width = Bomb.get ('Width', 50)
                            Height = Bomb.get ('Height', 50)

                            _Object.AddBomb (
                                X,
                                Y,
                                Width,
                                Height
                            )

                    Notifications = GameSettings.get ('Notifications', [])
                    if Notifications:
                        for Notification in Notifications:
                            Text = Notification.get ('Text', 'None')
                            Duration = Notification.get ('Duration', 1)

                            NotificationsToAdd[str (len (NotificationsToAdd) + 1)] = {
                                'Text': Text,
                                'Duration': Duration
                            }

                PlayerSettings = Data.get ('Player', {})
                if PlayerSettings:
                    X = PlayerSettings.get ('X', _Object.Player.X)
                    Y = PlayerSettings.get ('Y', _Object.Player.Y)
                    Width = PlayerSettings.get ('Width', _Object.Player.Width)
                    Height = PlayerSettings.get ('Height', _Object.Player.Height)
                    Speed = PlayerSettings.get ('Speed', _Object.Player.Speed)
                    Color = PlayerSettings.get ('Color', _Object.Player.Color)

                    _Object.Player.X = int (X)
                    _Object.Player.Y = int (Y)
                    _Object.Player.OriginalX = int (X)
                    _Object.Player.OriginalY = int (Y)
                    _Object.Player.Width = int (Width)
                    _Object.Player.Height = int (Height)
                    _Object.Player.Speed = int (Speed)
                    _Object.Player.Color = Color

                MessagesSettings = Data.get ('Messages', {})
                if MessagesSettings:
                    for Message in MessagesSettings:
                        if Message in _Object.Messages:
                            _Object.Messages[Message] = MessagesSettings[Message]

                self.Unload (Mod)

                _Object.AddNotification (
                    # Text
                    f'{Mod} has been loaded!',
                    # Duration (Frames)
                    5000
                )

                for Notification in NotificationsToAdd:
                    Notification = NotificationsToAdd[Notification]

                    _Object.AddNotification (
                        # Text
                        str (Notification['Text']),
                        # Duration (Frames)
                        int (Notification['Duration'])
                    )
