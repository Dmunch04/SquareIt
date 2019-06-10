class Player:
    def __init__ (self, X, Y, Width, Height):
        self.X = X
        self.Y = Y
        self.Width = Width
        self.Height = Height

        self.Speed = Width * Height / 100

        self.Color = (255, 75, 75)
