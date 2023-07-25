# -*- coding: utf-8 -*-

from mod.common.mod import Mod


@Mod.Binding(name="Script_NeteaseModUz9Dx55D", version="0.0.1")
class Script_NeteaseModUz9Dx55D(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def Script_NeteaseModUz9Dx55DServerInit(self):
        pass

    @Mod.DestroyServer()
    def Script_NeteaseModUz9Dx55DServerDestroy(self):
        pass

    @Mod.InitClient()
    def Script_NeteaseModUz9Dx55DClientInit(self):
        pass

    @Mod.DestroyClient()
    def Script_NeteaseModUz9Dx55DClientDestroy(self):
        pass
