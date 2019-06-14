class Wall:
    def __init__ (self, Name, Height):
        self.Name = Name
        self.Side = Name.split (' ')[0]
        self.ID = 0

        self.X = 0
        self.Y = 0
        self.OriginalX = self.X
        self.OriginalY = self.Y

        self.IsObstacle = False

        self.Width = 0
        self.Height = Height

        self.Speed = 0

        self.Color = (0, 0, 0)

    def __str__ (self):
        return f'<Wall::{self.Name}>'
