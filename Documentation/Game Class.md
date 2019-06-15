## Game Class

> The main class of SquareIt. This class is the core

This is the class you'll be working with, when making plugins. So take a good look ;)

<br>

### Attributes:
- **Window -> Window Object:**
    This attribute holds all the information of the window, and
    can only be tweaked in the init.

- **Player -> Player Object:**
    This is the player object. It holds things such as x, y, width
    and height for the player. This can be changed anytime.

- **DoRestart -> Bool:**
    This is a bool for whether the game should do a graphics restart
    when the player hits an object.

- The rest of the attributes are not suggested you do anything with.
  You can simply use this classes functions to update them.

<br>

### Functions:
- **Restart -> None:**
    Restarts the game graphics.

- **LoadConfig -> Path:**
    Loads a JSON config file. You need to put the full relative path
    to the file!

- **LoadExtension -> Path:**
    Loads the extension at the path. Please not, that / should be .
    and you shouldn't put the .py file ending!

- **AddNotification -> Text, Duration (Frames), Priority = False:**
    Adds a notification to the notification queue. When the notification
    is at the top of the queue, it will be displayed in the lower
    right corner. If you set priority to true, then it will be added
    as number one in the queue, and will therefor be displayed right
    away.

- **AddEnemy -> X, Y, Width, Height:**
    Adds a new enemy to the screen, with the given position and size.

- **RemoveEnemy -> ID:**
    Removes an enemy from the screen. The ID is the number of the enemy.
    So if you've added 3 enemies, and wanna remove number 3, then the ID
    is 3.

- **AddBomb -> X, Y, Width, Height:**
    Adds a new bomb to the screen, with the given position and size.

- **RemoveBomb -> ID:**
    Removes an bomb from the screen. The ID is the number of the bomb.
    So if you've added 7 bombs, and wanna remove number 4, then the ID
    is 4.

- **Start -> None:**
    This starts the game, and makes the window open. This is also in
    the beginning of this function, the start event will be sent to
    the plugins.
