class Notification:
    def __init__ (self, Text, Duration):
        self.Text = str (Text)
        self.Duration = int (Duration)

    def Decrease (self, _Value = 1):
        self.Duration -= int (_Value)
