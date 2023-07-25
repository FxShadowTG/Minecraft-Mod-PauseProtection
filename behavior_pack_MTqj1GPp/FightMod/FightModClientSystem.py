# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
ClientSystem = clientApi.GetClientSystemCls()
factory = clientApi.GetEngineCompFactory()

class FightModClientSystem(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "UiInitFinished", self, self.OnUIInitFinished)

        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientPlayerInventoryOpenEvent", self, self.OnClientPlayerInventoryOpenEvent)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientPlayerInventoryCloseEvent", self, self.OnClientPlayerInventoryCloseEvent)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientChestOpenEvent", self, self.OnClientChestOpenEvent)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientChestCloseEvent", self, self.OnClientChestCloseEvent)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "PlayerChatButtonClickClientEvent",self, self.OnPlayerChatButtonClickClientEvent)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnClientPlayerStartMove",self, self.OnOnClientPlayerStartMove)
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "HoldBeforeClientEvent",self, self.OnHoldBeforeClientEvent)
        self.ListenForEvent("FightMod","FightModServerSystem", "SaveDataEvent", self, self.OnSaveDataEvent)

        self.timeCount = 0
    
    def OnSaveDataEvent(self,args):
        print("ooooookkkkkkkk")
        print(args)

        data = {}
        data["bagValue"] = args["bagValue"]
        data["chestValue"] = args["chestValue"]
        data["talkValue"] = args["talkValue"]

        compCreateConfigClient = factory.CreateConfigClient(clientApi.GetLevelId())
        configDict = compCreateConfigClient.SetConfigData("djpfi:protectionData",data, True)

        print(configDict)

    def OnUIInitFinished(self,args):
        clientApi.RegisterUI("FightMod","NeteaseScreenNode", "FightMod.uiScript.NeteaseScreenNode.NeteaseScreenNode", "uiCourse.main")
        print("监听UI初始化成功")
    
    def OnClientPlayerInventoryOpenEvent(self,args):
        self.NotifyToServer("OpenBagEvent", {"playerId": clientApi.GetLocalPlayerId(),"status": "1"})

    def OnClientPlayerInventoryCloseEvent(self,agrs):
        self.NotifyToServer("CloseBagEvent", {"playerId": clientApi.GetLocalPlayerId(),"status": "2"})

    def OnClientChestOpenEvent(self,args):
        self.NotifyToServer("OpenChestEvent", {"playerId": clientApi.GetLocalPlayerId(),"status": "1"})

    def OnClientChestCloseEvent(self,args):
        self.NotifyToServer("CloseChestEvent", {"playerId": clientApi.GetLocalPlayerId(),"status": "2"})

    def OnPlayerChatButtonClickClientEvent(self,args):
        self.NotifyToServer("OpenChatEvent", {"playerId": clientApi.GetLocalPlayerId(),"status": "3"})

    def OnOnClientPlayerStartMove(self):
        self.NotifyToServer("StartMoveEvent", {"playerId": clientApi.GetLocalPlayerId(),"status": "4"})

    def OnHoldBeforeClientEvent(self,args):
        print("press")
        playerId = clientApi.GetLocalPlayerId()
        compCreateItem = factory.CreateItem(playerId)
        carriedData = compCreateItem.GetCarriedItem()
        if(carriedData == None):
            return
        if(carriedData['newItemName'] == 'djpfi:protectoption'):
            clientApi.CreateUI("FightMod","NeteaseScreenNode")

    def Update(self):
        if self.timeCount > 30:
            compCreateConfigClient = factory.CreateConfigClient(clientApi.GetLevelId())
            configDict = compCreateConfigClient.GetConfigData("djpfi:protectionData", True)
            self.NotifyToServer("StatusValueEvent", configDict)
            self.timeCount = 0
            print("send1")
        else:
            self.timeCount = self.timeCount + 1

    def UnListenEvent(self):
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientPlayerInventoryOpenEvent", self, self.OnClientPlayerInventoryOpenEvent)
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientPlayerInventoryCloseEvent", self, self.OnClientPlayerInventoryCloseEvent)
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientChestOpenEvent", self, self.OnClientChestOpenEvent)
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "ClientChestCloseEvent", self, self.OnClientChestCloseEvent)

    def Destroy(self):
        self.UnListenEvent()
        pass
