class Player:
    def __init__ (self, X, Y, Width, Height):
        self.ID = 0

        self.X = X
        self.Y = Y
        self.OriginalX = X
        self.OriginalY = Y

        self.IsObstacle = False

        self.Width = Width
        self.Height = Height

        self.Speed = Width * Height / 100

        self.Color = (255, 75, 75)

    def __str__ (self):
        return 'Player'
