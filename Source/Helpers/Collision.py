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
