class MyPlugin:
    def __init__ (self, Game):
        self.Game = Game

    def EventInit (self):
        self.Game.Window.UpdateWidth (1280)

        print ('Init')

    def EventStart (self):
        print ('Start', self.Game.Window.Width)

        self.Game.AddNotification (
            'Game has started',
            1000
        )

    def EventGameOver (self):
        #print ('Death')

        self.Game.AddNotification (
            'You died!',
            1000,
            _Priority = True
        )

    def EventEnd (self):
        print ('End')

def Setup (_Game):
    _Game.AddPlugin (MyPlugin (_Game))
