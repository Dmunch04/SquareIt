from DavesLogger import Logs

class Collection (dict):
    __slots__ = (
        'Instance',
        'Index'
    )

    def __init__ (self, Instance = dict, Indexor = 'ID'):
        dict.__init__ (self)

        self.Instance = Instance
        self.Index = Indexor

    def __add__ (self, _Value):
        """ Adds support for using + on this """

        if isinstance (_Value, Collection):
            if isinstance (_Value.Instance, self.Instance):
                [self.Add (Item) for Item in _Value]

        elif isinstance (_Value, self.Instance):
            self.Add (_Value)

        else:
            raise Logs.Error ('Item is not a collection or instance of')

    def __iadd__ (self, _Value):
        """ Adds support for using += on this """

        self.__add__ (_Value)

    def __setitem__ (self, _Key, _Value):
        """ Adds support for using this[Key] = Value on this """

        if not isinstance (_Value, self.Instance):
            Logs.Error (f'{_Value} is not instance of {self.Instance}!')

        dict.__setitem__ (self, _Key, _Value)

    def Add (self, _Item):
        """ Adds a new item to the collection """

        if not isinstance (_Item, self.Instance):
            Logs.Error (f'{_Item} is not instance of {self.Instance}!')

        Index = getattr (_Item, self.Index, None)

        if Index is None:
            Logs.Error (f'{self.Index} of {repr (_Item)} is invalid!')

        self[Index] = _Item

    def Remove (self, _Item):
        """ Removes an item from the collection """

        if isinstance (_Item, self.Instance):
            if getattr (_Item, self.Index, None) is not None:
                del self[getattr (_Item, self.Index)]

        else:
            if _Item in self:
                del self[_Item]

    def RemoveIf (self, **_Attributes):
        """ Removes an item from the collection, if something """

        for Key, Value in reversed (self.items ()):
            if self.HasAttributes (_Value, **_Attributes):
                del self[Key]

    def RemoveIndex (self, _Index):
        """ Removes an item from the collection, by it's id """

        del self[_Index]

    def HasAttributes (self, _Object, **_Attributes):
        """ Checks if _Object has _Attributes """

        for Key, Value in _Attributes.items ():
            if not getattr (_Object, Key, None) == Value:
                return False

        return True

    def Has (self, _ID):
        """ Check if the collection contains an object with the given id """

        if isinstance (_Key, self.Instance):
            return self.__contains__ (_ID)

        for Item in self:
            if getattr (Item, self.Index, None) == _ID:
                return True

        return False

    def Find (self, _Condition):
        """ Find all objects which meets the callable condition """

        return [Item for Item in self if _Condition (Item)]

    def FindOne (self, _Condition):
        """ Find first object which meets the callable condition """

        for Item in self:
            if _Condition (Item):
                return _Item

    def Get (self, _ID = None, **_Attributes):
        """ Get an item from the collection by it's id, an attributes to filter """

        _Attributes['ID'] = _ID or _Attributes.get ('ID')

        return self.FindOne (lambda X: self.HasAttributes (X, **_Attributes))

    def GetAll (self):
        """ Returns all the items in the collection as a list """

        return [self[Item] for Item in self]
