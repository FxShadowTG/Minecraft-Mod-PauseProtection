# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
ServerSystem = serverApi.GetServerSystemCls()


class FightModServerSystem(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        print("服务器准备监听")
        self.ListenEvent()
        print("服务器监听完毕")
        self.playerIdDict = {}
        #默认为true
        self.bagValue = True
        self.chestValue = True
        self.talkValue = True
        
    def ListenEvent(self):
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "AddServerPlayerEvent", self, self.OnAddServerPlayerEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DamageEvent", self, self.OnDamageEvent)
        self.ListenForEvent("FightMod","FightModClientSystem", "OpenBagEvent", self, self.OnOpenBagEvent)
        self.ListenForEvent("FightMod","FightModClientSystem", "CloseBagEvent", self, self.OnCloseBagEvent)
        self.ListenForEvent("FightMod","FightModClientSystem", "OpenChestEvent", self, self.OnOpenChestEvent)
        self.ListenForEvent("FightMod","FightModClientSystem", "CloseChestEvent", self, self.OnCloseChestEvent)
        self.ListenForEvent("FightMod","FightModClientSystem", "OpenChatEvent", self, self.OnOpenChatEvent)
        self.ListenForEvent("FightMod","FightModClientSystem", "StartMoveEvent", self, self.OnStartMoveEvent)
        self.ListenForEvent("FightMod","FightModClientSystem", "SendDataToServerEvent", self, self.OnSendDataToServerEvent)
        self.ListenForEvent("FightMod","FightModClientSystem", "StatusValueEvent", self, self.OnStatusValueEvent)
        print("ok")

    def OnStatusValueEvent(self,args):
        if args == None:
            return
        self.bagValue = args["bagValue"]
        self.chestValue = args["chestValue"]
        self.talkValue = args["talkValue"]
        print(self.bagValue,self.chestValue,self.talkValue)

    def OnSendDataToServerEvent(self,args):
        print("OnSendDataToServerEvent::::::::",args)
        #传当前服务器的值回客户端
        self.NotifyToClient(args["__id__"],"SaveDataEvent", {"bagValue": args["bagValue"],"chestValue": args["chestValue"],"talkValue": args["talkValue"]})

    def OnAddServerPlayerEvent(self,args):
        self.playerIdDict[args["id"]] = 0

    def OnDamageEvent(self,args):
        if(args["entityId"] in self.playerIdDict.keys() and self.playerIdDict[args["entityId"]] == "1"):
            args["knock"] = False
            args["damage"] = 0

    def OnOpenBagEvent(self,args):
        if(args["status"] == "1" and self.bagValue == True):
            self.playerIdDict[args["playerId"]] = "1"

    def OnCloseBagEvent(self,args):
        if(args["status"] == "2" and self.bagValue == True):
            self.playerIdDict[args["playerId"]] = "0"   

    def OnOpenChestEvent(self,args):
        if(args["status"] == "1" and self.chestValue == True):
            self.playerIdDict[args["playerId"]] = "1" 

    def OnCloseChestEvent(self,args):
        if(args["status"] == "2" and self.chestgValue == True):
            self.playerIdDict[args["playerId"]] = "0"  

    def OnOpenChatEvent(self,args):
        if(args["status"] == "3" and self.talkValue == True):
            self.playerIdDict[args["playerId"]] = "3"  

    def OnStartMoveEvent(self,args):
        if(args["status"] == "4" and self.talkValue == True):
            self.playerIdDict[args["playerId"]] = "4"  

    def checkPlayerStatus(self):
        for playerId in self.playerIdDict:
            if(self.playerIdDict[playerId] == "3"):
                print("is 3, don't attack")
                self.playerIdDict[playerId] = "1"
            elif(self.playerIdDict[playerId] == "4"):
                self.playerIdDict[playerId] = "0"

    def Update(self):
        self.checkPlayerStatus()
        pass

    def UnListenEvent(self):
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "AddServerPlayerEvent", self, self.OnAddServerPlayerEvent)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DamageEvent", self, self.OnDamageEvent)
        self.UnListenForEvent("FightMod","FightModClientSystem", "OpenBagEvent", self, self.OnOpenBagEvent)
        self.UnListenForEvent("FightMod","FightModClientSystem", "CloseBagEvent", self, self.OnCloseBagEvent)

    def Destroy(self):
        self.UnListenEvent()
        pass
