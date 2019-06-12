def CheckCollision (_Object1, _Object2):
    """
        Checks if _Object1 has collided with _Object2
        If they have collided, it returns True, else
        it returns False

        Source: https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection
    """

    if (
        _Object1.X < _Object2.X + _Object2.Width and
        _Object1.X + _Object1.Width > _Object2.X and
        _Object1.Y < _Object2.Y + _Object2.Height and
        _Object1.Y + _Object1.Height > _Object2.Y
    ):
        return True

    return False

def CheckCollisions (_Object1, _Objects):
    """ Loops through all the given objects, and checks if they've collided """

    for Object in _Objects:
        Result = CheckCollision (_Object1, Object)

        if Result == True:
            return Result, Object

    return False, None

def CheckWallCollision (_Object1, _Width, _Height):
    """ Checks if the players has collided with any of the walls """

    if _Object1.X == 0:
        return True, 'Left Wall'

    elif _Object1.X == _Width - _Object1.Width:
        return True, 'Right Wall'

    elif _Object1.Y == 0:
        return True, 'Top Wall'

    elif _Object1.Y == _Height - _Object1.Height:
        return True, 'Bottom Wall'

    return False, None
