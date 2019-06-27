class Enemy:
    def __init__ (self, ID, X, Y, Width, Height):
        self.ID = ID
        self.Name = f'Enemy{self.ID}'

        self.X = X
        self.Y = Y
        self.OriginalX = X
        self.OriginalY = Y

        self.IsObstacle = True

        self.Width = Width
        self.Height = Height

        self.Speed = Width * Height / 100

        self.Color = (31, 129, 255)

    def __str__ (self):
        return f'<Enemy::{str (self.ID)}>'

    def Move (self, _Direction):
        """ Moves the object in the given direction """

        # Get the direction letter
        Direction = str (_Direction[0]).lower ()

        # Left
        if Direction == 'l':
            self.X -= self.Speed

        # Right
        elif Direction == 'r':
            self.X += self.Speed

        # Up
        elif Direction == 'u':
            self.Y -= self.Speed

        # Down
        elif Direction == 'd':
            self.Y += self.Speed

    def MoveTo (self, _X, _Y):
        """ Moves the object to the specified position """

        self.X = int (_X)
        self.Y = int (_Y)
