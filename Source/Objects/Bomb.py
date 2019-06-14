class Bomb:
    def __init__ (self, ID, X, Y, Width, Height):
        self.ID = ID

        self.X = X
        self.Y = Y
        self.OriginalX = X
        self.OriginalY = Y

        self.IsObstacle = True

        self.Width = Width
        self.Height = Height

        self.Speed = Width * Height / 100

        self.Color = (10, 10, 10)

    def __str__ (self):
        return f'<Bomb::{str (self.ID)}>'
