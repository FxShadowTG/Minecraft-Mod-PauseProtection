# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

@Mod.Binding(name="FightMod", version="0.0.1")
class FightMod(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def FightModServerInit(self):
        serverApi.RegisterSystem("FightMod","FightModServerSystem","FightMod.FightModServerSystem.FightModServerSystem")
        print("服务注册成功")

    @Mod.DestroyServer()
    def FightModServerDestroy(self):
        print("服务销毁成功")

    @Mod.InitClient()
    def FightModClientInit(self):
        clientApi.RegisterSystem("FightMod","FightModClientSystem","FightMod.FightModClientSystem.FightModClientSystem")
        print("客户注册成功")

    @Mod.DestroyClient()
    def FightModClientDestroy(self):
        print("客户销毁成功")
