def CallPluginFunctions (_Plugins, _Function, *_Args):
    for Plugin in _Plugins:
        if _Function in dir (Plugin):
            Method = getattr (Plugin, _Function)

            if _Args:
                Method (*_Args)

            else:
                Method ()
