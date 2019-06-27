class MyPlugin:
    def __init__ (self, Game):
        self.Game = Game

    def EventInit (self):
        self.Game.Window.SetWidth (1280)

        self.Game.DoRestart = False

        print ('MyPlugin [v1.0.0] has been loaded!')

    def EventFrame (self):
        """
        Object = self.Game.Enemies.GetAll ()[0]

        Object.Move ('d')
        """
        pass

    def EventFixedFrame (self):
        Object = self.Game.Enemies.GetAll ()[0]

        Object.Move ('d')

    def EventStart (self):
        print ('Start', self.Game.Window.Width)

        self.Game.AddNotification (
            'Game has started',
            1000
        )

        Object = self.Game.Enemies.GetAll ()[1]

        for I in range (5):
            Object.Move ('r')

    def EventGameOver (self):
        #print ('Death')

        self.Game.AddNotification (
            'You died!',
            1000,
            _Priority = True
        )

    def EventCollision (self, _Object):
        if _Object.IsObstacle:
            # It's an enemy/bomb
            self.Game.AddNotification ('Hit obstacle!', 100, _Priority = True)

        else:
            # It's a wall
            self.Game.AddNotification ('Hit wall!', 100, _Priority = True)

        #print (f'HIT: {_Object}!')
        #print (f'We hit: {_Object.Name} @ ({_Object.X}, {_Object.Y})')

    def EventEnd (self):
        print ('End')

def Setup (_Game):
    _Game.AddPlugin (MyPlugin (_Game))
