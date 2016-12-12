#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 \file Zumo.py
 \brief ModuleDescription
 \date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
import serial
import struct
import threading
from collections import defaultdict
import math

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# 参考 http://www.mech.tohoku-gakuin.ac.jp/rde/contents/course/robotics/wheelrobot.html
 #転輪幅(メートル)
tread=85*0.001
# ギア比 75.81:1
# モータのシャフト1回転あたりのカウント数 12
# 転輪直径(クローラ込み) 40mm
# 1ポイントあたりの移動距離(メートル)と、逆数
MPCnt=(40*0.001*math.pi)/(75.81*12)#[m/Pt]
CntPM=(75.81*12)/(40*0.001*math.pi)#[Pt/m]
# シリアル通信のタイムアウト
TimeOut=1.0
# 転輪幅の半分
hftr=tread/2
Epsilon=10**(-10)
#ラインセンサの数
LSensCount=5

class Bool4:
    # ブール値を4バイト整数に変換
    # struct.Structの代わりに使用
    @staticmethod
    def pack(v):
        if v:
            return "\x01\x00\x00\x00"
        return "\x00\x00\x00\x00"
    @staticmethod
    def unpack(v):
        if v=="\x00\x00\x00\x00":
            return (False,)
        return (True,)
U_Int=struct.Struct("<L")       # 符号なし整数(4バイト)
S_Int=struct.Struct("<l")       # 符号付き整数(4バイト)
Float=struct.Struct("<f")       # 浮動小数(単精度)
DataS=struct.Struct("BBBBBB")   # 6バイト値
DataM=struct.Struct("B")        # 1バイト値

# シリアライズ用テーブル
# Zumoへ値を送信する時に使用
SendDict=defaultdict(lambda:U_Int,
    {
        0x02:Float,0x03:Float,
        0x04:Bool4,0x05:Bool4,0x06:Bool4,
        0x74:Float,0x75:Float,0x76:Float,
        0x78:Bool4,0x79:U_Int,
    })
# デシリアライズ用テーブル
# Zumoから値が送信された時に使用
ResvDict=defaultdict(lambda:U_Int,
    {
        0x02:Float,0x03:Float,
        0x08:Bool4,0x09:Bool4,0x0A:Bool4,
        0x10:U_Int,0x11:U_Int,0x12:U_Int,0x13:U_Int,0x14:U_Int
    })

CRC_Base=0b1011L
def CalcCRC(data):# CRC値の計算
    CRCV = CRC_Base<<35
    CRCM = 1L<<38
    for i in range(36):
        if data & CRCM:
            data^=CRCV
        CRCV>>=1
        CRCM>>=1
    return data&0x7

def MakeData(ID,Data):# データのシリアライス
    Conv =SendDict[ID]
    Data =U_Int.unpack(Conv.pack(Data))[0]
    Data|=long(ID)<<32
    CRC  =CalcCRC(Data)
    Data =(Data<<3) | CRC
    RetL =[0,0,0,0,0,0x80]
    for i in range(6):
        Sh=7*(5-i)
        Dp=(Data&(0x7f<<Sh))>>Sh
        RetL[i]|=Dp
    return DataS.pack(*RetL)

def DecodeData(Data):# データのデシリアライス
    if len(Data)<6:
        return None,"Too Short"
    DataL=0
    for i in Data:
        DataL=(DataL<<7)|(i&0x7F)
    DataL&=0x3FFFFFFFFFF
    ID  = DataL>>35
    Data=(DataL>>3 )&0xFFFFFFFF
    CRC = DataL     &0x7
    CRCt=CalcCRC(DataL>>3)
    if CRC==CRCt:
        Conv =ResvDict[ID]
        return ID,Conv.unpack(U_Int.pack(Data))[0]
    return None,"CRC ERROR {0} {1}".format(CRC,CRCt)

#何もしない関数
NoFunc=lambda x:None

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
zumo_spec = ["implementation_id", "Zumo",
		 "type_name",         "Zumo",
		 "description",       "ModuleDescription",
		 "version",           "1.0.0",
		 "vendor",            "VenderName",
		 "category",          "Category",
		 "activity_type",     "STATIC",
		 "max_instance",      "1",
		 "language",          "Python",
		 "lang_type",         "SCRIPT",
		 "conf.default.Port", "COM1",
		 "conf.__widget__.Port", "text",
		 ""]
# </rtc-template>

class Zumo(OpenRTM_aist.DataFlowComponentBase):

	"""
	\class Zumo
	\brief ModuleDescription

	"""
	def __init__(self, manager):
		"""
		\brief constructor
		\param manager Maneger Object
		"""
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_VelocityIn = RTC.TimedVelocity2D(RTC.Time(0,0),0)
		"""
		"""
		self._VelocityInIn = OpenRTM_aist.InPort("VelocityIn", self._d_VelocityIn)
		self._d_VelocityOut = RTC.TimedVelocity2D(RTC.Time(0,0),0)
		"""
		"""
		self._VelocityOutOut = OpenRTM_aist.OutPort("VelocityOut", self._d_VelocityOut)
		self._d_PoseOut = RTC.TimedPose2D(RTC.Time(0,0),0)
		"""
		"""
		self._PoseOutOut = OpenRTM_aist.OutPort("PoseOut", self._d_PoseOut)
		self._d_ButtonA = RTC.TimedBoolean(RTC.Time(0,0),0)
		"""
		"""
		self._ButtonAOut = OpenRTM_aist.OutPort("ButtonA", self._d_ButtonA)
		self._d_ButtonB = RTC.TimedBoolean(RTC.Time(0,0),0)
		"""
		"""
		self._ButtonBOut = OpenRTM_aist.OutPort("ButtonB", self._d_ButtonB)
		self._d_ButtonC = RTC.TimedBoolean(RTC.Time(0,0),0)
		"""
		"""
		self._ButtonCOut = OpenRTM_aist.OutPort("ButtonC", self._d_ButtonC)
		self._d_LineSensors = RTC.TimedULongSeq(RTC.Time(0,0),0)
		"""
		"""
		self._LineSensorsOut = OpenRTM_aist.OutPort("LineSensors", self._d_LineSensors)





		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""

		 - Name:  Port
		 - DefaultValue: COM1
		"""
		self._Port = ['COM1']

		# </rtc-template>
		# シリアルポート
		self.SPort=None
		# 最後に計算したX座標,Y座標,角度,時間
		self.X=0
		self.Y=0
		self.A=0
		self.T=0
		# 受信データ
		self.Received=[]
		# 受信データに対するアクション用関数テーブル
		# 引数は1つ(受信したデータ・型はResvDictに依存)
		self.Functions=defaultdict(lambda:NoFunc,
                        {
                                0x02:self.SetLeft,
                                0x03:self.SetRight,

                                0x08:self.ButtonA,
                                0x09:self.ButtonB,
                                0x0A:self.ButtonC,

                                0x10:self.LineSensor0,
                                0x11:self.LineSensor1,
                                0x12:self.LineSensor2,
                                0x13:self.LineSensor3,
                                0x14:self.LineSensor4,
                        })
		self._LSens=[0]*LSensCount


	def SetLeft(self,Data):# 左クローラ速度の受信・保持
		self.VLr=Data*MPCnt
	def SetRight(self,Data):# 右クローラ速度の受信・保持
		self.VRr=Data*MPCnt
	def ButtonA(self,stat):
		self._d_ButtonA.data=stat
		OpenRTM_aist.setTimestamp(self._d_ButtonA)
		self._ButtonAOut.write()
	def ButtonB(self,stat):
		self._d_ButtonB.data=stat
		OpenRTM_aist.setTimestamp(self._d_ButtonB)
		self._ButtonBOut.write()
	def ButtonC(self,stat):
		self._d_ButtonC.data=stat
		OpenRTM_aist.setTimestamp(self._d_ButtonC)
		self._ButtonCOut.write()
	def LineSensor0(self,value):
		self._LSens[0]=value
	def LineSensor1(self,value):
		self._LSens[1]=value
	def LineSensor2(self,value):
		self._LSens[2]=value
	def LineSensor3(self,value):
		self._LSens[3]=value
	def LineSensor4(self,value):
		self._LSens[4]=value

	def onInitialize(self):
		"""

		The initialize action (on CREATED->ALIVE transition)
		formaer rtc_init_entry()

		\return RTC::ReturnCode_t

		"""
		# Bind variables and configuration variable
		self.bindParameter("Port", self._Port, "COM1")

		# Set InPort buffers
		self.addInPort("VelocityIn",self._VelocityInIn)

		# Set OutPort buffers
		self.addOutPort("VelocityOut",self._VelocityOutOut)
		self.addOutPort("PoseOut",self._PoseOutOut)
		self.addOutPort("ButtonA",self._ButtonAOut)
		self.addOutPort("ButtonB",self._ButtonBOut)
		self.addOutPort("ButtonC",self._ButtonCOut)
		self.addOutPort("LineSensors",self._LineSensorsOut)

		# Set service provider to Ports

		# Set service consumers to Ports

		# Set CORBA Service Ports

		return RTC.RTC_OK

	#def onFinalize(self, ec_id):
	#	"""
	#
	#	The finalize action (on ALIVE->END transition)
	#	formaer rtc_exiting_entry()
	#
	#	\return RTC::ReturnCode_t
	#
	#	"""
	#
	#	return RTC.RTC_OK

	#def onStartup(self, ec_id):
	#	"""
	#
	#	The startup action when ExecutionContext startup
	#	former rtc_starting_entry()
	#
	#	\param ec_id target ExecutionContext Id
	#
	#	\return RTC::ReturnCode_t
	#
	#	"""
	#
	#	return RTC.RTC_OK

	#def onShutdown(self, ec_id):
	#	"""
	#
	#	The shutdown action when ExecutionContext stop
	#	former rtc_stopping_entry()
	#
	#	\param ec_id target ExecutionContext Id
	#
	#	\return RTC::ReturnCode_t
	#
	#	"""
	#
	#	return RTC.RTC_OK

	def onActivated(self, ec_id):
		"""

		The activated action (Active state entry action)
		former rtc_active_entry()

		\param ec_id target ExecutionContext Id

		\return RTC::ReturnCode_t

		"""
		# シリアルポートのオープン
		self.SPort=serial.Serial(self._Port[0],timeout=TimeOut)
		# データ送信の開始
		self.Send(0x78,True)
		# 値の初期化
		self.VLr=0
		self.VRr=0
		self.X=0
		self.Y=0
		self.A=0
		self.T=time.time()
		# 受信の開始
		self.recieving=True
		self.RTh=threading.Thread(target=self.Receive)
		self.RTh.start()
		self.Received=[]

		return RTC.RTC_OK

	def onDeactivated(self, ec_id):
		"""

		The deactivated action (Active state exit action)
		former rtc_active_exit()

		\param ec_id target ExecutionContext Id

		\return RTC::ReturnCode_t

		"""
		# データ送信の停止
		self.Send(0x78,False)
		# クローラの停止
		self.Send(0x02,0)
		self.Send(0x03,0)
		#受信の停止
		self.recieving=False
		self.RTh.join()
		# シリアルポートのクローズ
		self.SPort.close()
		self.SPort=None


		return RTC.RTC_OK

	def onExecute(self, ec_id):
		"""

		The execution action that is invoked periodically
		former rtc_active_do()

		\param ec_id target ExecutionContext Id

		\return RTC::ReturnCode_t

		"""
		if self._VelocityInIn.isNew():
                        # 速度入力
                        data=self._VelocityInIn.read().data
                        VX=data.vx
                        VA=data.va
                        VL=VX-hftr*VA
                        VR=VX+hftr*VA
                        self.Send(0x02,VL*CntPM)
                        self.Send(0x03,VR*CntPM)
		# 現在位置推測
		VA=(self.VRr-self.VLr)/tread
		VX=(self.VRr+self.VLr)/2.0
		NT=time.time()
		dT=NT-self.T
		dS=VA*dT
		dL=VX*dT
                if abs(dS)>Epsilon:# dSが大きい場合は調整
                        p=VX/VA
                        dL=2*p*math.sin(dS/2)
                self.X+=dL*math.cos(self.A+dS/2)
                self.Y+=dL*math.sin(self.A+dS/2)
                self.A+=dS
                self.T=NT
		self._d_VelocityOut.data=RTC.Velocity2D(VX,0.0,VA)
		self._d_PoseOut.data=RTC.Pose2D(RTC.Point2D(self.X,self.Y),self.A)
                OpenRTM_aist.setTimestamp(self._d_VelocityOut)
		OpenRTM_aist.setTimestamp(self._d_PoseOut)
		self._VelocityOutOut.write()
		self._PoseOutOut.write()
		#print "X{0:6.2f} Y{1:6.2f} A{2:6.2f} VX{3:6.2f} VY{4:6.2f}\r".format(self.X,self.Y,self.A,VX,VA),
        #ラインセンサデータ出力
		self._d_LineSensors.data=self._LSens
		OpenRTM_aist.setTimestamp(self._d_LineSensors)
		self._LineSensorsOut.write()
		return RTC.RTC_OK
	def Receive(self):# データ受信スレッド用関数
                while self.recieving:
                        Data=self.SPort.read(1)
                        if len(Data)==0:
                                continue
                        Data=DataM.unpack(Data)[0]
                        self.Received.append(Data)
                        #print Data,
                        if Data & 0x80:
                                #print
                                ID,Data=DecodeData(self.Received)
                                print ID,Data
                                self.Functions[ID](Data)
                                self.Received=[]
	def Send(self,ID,Data):# データの送信
		self.SPort.write(MakeData(ID,Data))

	#def onAborting(self, ec_id):
	#	"""
	#
	#	The aborting action when main logic error occurred.
	#	former rtc_aborting_entry()
	#
	#	\param ec_id target ExecutionContext Id
	#
	#	\return RTC::ReturnCode_t
	#
	#	"""
	#
	#	return RTC.RTC_OK

	#def onError(self, ec_id):
	#	"""
	#
	#	The error action in ERROR state
	#	former rtc_error_do()
	#
	#	\param ec_id target ExecutionContext Id
	#
	#	\return RTC::ReturnCode_t
	#
	#	"""
	#
	#	return RTC.RTC_OK

	def onReset(self, ec_id):
		"""

		The reset action that is invoked resetting
		This is same but different the former rtc_init_entry()

		\param ec_id target ExecutionContext Id

		\return RTC::ReturnCode_t

		"""
		# ポートが開いていたら、閉じる
		if self.SPort!=None:
                        self.SPort.close()
                        self.SPort=None
		return RTC.RTC_OK

	#def onStateUpdate(self, ec_id):
	#	"""
	#
	#	The state update action that is invoked after onExecute() action
	#	no corresponding operation exists in OpenRTm-aist-0.2.0
	#
	#	\param ec_id target ExecutionContext Id
	#
	#	\return RTC::ReturnCode_t
	#
	#	"""
	#
	#	return RTC.RTC_OK

	#def onRateChanged(self, ec_id):
	#	"""
	#
	#	The action that is invoked when execution context's rate is changed
	#	no corresponding operation exists in OpenRTm-aist-0.2.0
	#
	#	\param ec_id target ExecutionContext Id
	#
	#	\return RTC::ReturnCode_t
	#
	#	"""
	#
	#	return RTC.RTC_OK




def ZumoInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=zumo_spec)
    manager.registerFactory(profile,
                            Zumo,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    ZumoInit(manager)

    # Create a component
    comp = manager.createComponent("Zumo")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

