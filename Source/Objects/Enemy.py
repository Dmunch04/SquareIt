class Enemy:
    def __init__ (self, ID, X, Y, Width, Height):
        self.ID = ID
        self.X = X
        self.Y = Y
        self.Width = Width
        self.Height = Height

        self.Speed = Width * Height / 2

        self.Color = (31, 129, 255)
