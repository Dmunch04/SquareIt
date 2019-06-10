import json

from Modding import Mod as ModObject

class Loader:
    def __init__ (self):
        self.Mods = []
        self.Data = {}

    def Load (self, _Mod):
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

        Mod = ModObject.Mod (
            Name,
            Version,
            Author,
            Description,
            Data
        )

        return Mod

    def Unload (self, _Mod):
        if _Mod in self.Mods:
            del self.Mods[self.Mods.index (_Mod)]

            self.Data[_Mod] = {}

    def SetData (self, _Object):
        # Load mods
        for Mod in self.Data:
            Data = self.Data[Mod]

            if Data:
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
