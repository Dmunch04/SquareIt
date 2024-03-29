import Game

def Run ():
    # Initialze the game object
    TestGame = Game.Game ()

    # Add game objects
    # -- X, Y, Width, Height
    TestGame.AddEnemy (100, 100, 50, 50)
    TestGame.AddBomb (200, 200, 50, 50)

    # Load mods
    # -- Path
    #TestGame.ModLoader.Load ('Game Mods/TestMod.json')
    TestGame.LoadConfig ('Game Mods/TestMod.json')
    TestGame.LoadExtension ('Game Mods.Plugin')

    # Remove game objects
    # -- ID
    #TestGame.RemoveEnemy (1)
    #TestGame.RemoveEnemy (2)

    # Start/Run the game
    TestGame.Start ()

if __name__ == '__main__':
    Run ()
