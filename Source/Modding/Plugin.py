def CallPluginFunctions (_Plugins, _Function):
    for Plugin in _Plugins:
        if _Function in dir (Plugin):
            Method = getattr (Plugin, _Function)
            Method ()
