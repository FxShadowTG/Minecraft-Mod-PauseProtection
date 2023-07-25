# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()


class NeteaseScreenNode(ScreenNode):
	def __init__(self, namespace, name, param):
		ScreenNode.__init__(self, namespace, name, param)

	def Create(self):
		print("准备create这个UI文件")
		"""
		@description UI创建成功时调用
		"""
		self.optionLabel = self.GetBaseUIControl("/optionLabel")
		self.optionLabelClose = self.optionLabel.GetChildByName("close")

		self.optionLabelBagLabel = self.optionLabel.GetChildByPath("/bagLabel")
		self.bagLabelSwitchToggle = self.optionLabelBagLabel.GetChildByName("switch_toggle")

		self.optionLabelChestLabel = self.optionLabel.GetChildByPath("/chestLabel")
		self.chestLabelSwitchToggle = self.optionLabelChestLabel.GetChildByName("switch_toggle")

		self.optionLabelTalkLabel = self.optionLabel.GetChildByPath("/talkLabel")
		self.talkLabelSwitchToggle = self.optionLabelTalkLabel.GetChildByName("switch_toggle")

		self.optionLabelCloseButton = self.optionLabelClose.asButton()
		self.optionLabelCloseButton.AddTouchEventParams({"isSwallow": True})
		self.optionLabelCloseButton.SetButtonTouchDownCallback(self.CloseOptionLabel)

		self.bagLabelSwitchToggleasSwitchToggle = self.bagLabelSwitchToggle.asSwitchToggle()
		self.chestLabelSwitchToggleasSwitchToggle = self.chestLabelSwitchToggle.asSwitchToggle()
		self.talkLabelSwitchToggleasSwitchToggle = self.talkLabelSwitchToggle.asSwitchToggle()
	
		print("NeteaseScreenNode的Create回调成功")
		self.SetValueStatus()
		print("SetValueStatusOK")

		#关闭事件，关闭后发送数据到服务端先，最后从服务端发送回客户端
	def CloseOptionLabel(self,args):
		print("X")
		#获取背包状态
		bagValue = self.bagLabelSwitchToggleasSwitchToggle.GetToggleState()
		#获取箱子状态
		chestValue = self.chestLabelSwitchToggleasSwitchToggle.GetToggleState()
		#获取聊天状态
		talkValue = self.talkLabelSwitchToggleasSwitchToggle.GetToggleState()
		self.SetRemove()

		#发送事件
		self.SendDataToServerEvent(bagValue,chestValue,talkValue)

	#设置开关状态
	def SetValueStatus(self):
		#读取数据
		print("读取本地数据中")
		compCreateConfigClient = clientApi.GetEngineCompFactory().CreateConfigClient(clientApi.GetLevelId())
		configDict = compCreateConfigClient.GetConfigData("djpfi:protectionData", True)

		self.bagLabelSwitchToggleasSwitchToggle.SetToggleState(configDict["bagValue"])
		self.chestLabelSwitchToggleasSwitchToggle.SetToggleState(configDict["chestValue"])
		self.talkLabelSwitchToggleasSwitchToggle.SetToggleState(configDict["talkValue"])

	#传到服务端
	def SendDataToServerEvent(self,bagValue,chestValue,talkValue):
		print("准备进行通信...")
		clientApi.GetSystem("FightMod","FightModClientSystem").NotifyToServer("SendDataToServerEvent", {"bagValue": bagValue,"chestValue": chestValue,"talkValue": talkValue})
		print("通信结束")

	def Destroy(self):
		"""
		@description UI销毁时调用
		"""
		pass

	def OnActive(self):
		"""
		@description UI重新回到栈顶时调用
		"""
		pass

	def OnDeactive(self):
		"""
		@description 栈顶UI有其他UI入栈时调用
		"""
		pass
