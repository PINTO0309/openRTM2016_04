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

#参考 http://www.mech.tohoku-gakuin.ac.jp/rde/contents/course/robotics/wheelrobot.html
#転輪幅(メートル)
tread=85*0.001
#ギア比 75.81:1
#モータのシャフト1回転あたりのカウント数 12
#転輪直径(無限軌道込み) 40mm
#1ポイントあたりの移動距離(メートル)と、逆数
MPCnt=(40*0.001*math.pi)/(75.81*12)#[m/Pt]
CntPM=(75.81*12)/(40*0.001*math.pi)#[Pt/m]
#シリアル通信のタイムアウト
TimeOut=1.0
#転輪幅の半分
hftr=tread/2
Epsilon=10**(-10)

class Bool4:
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
U_Int=struct.Struct("<L")
S_Int=struct.Struct("<l")
Float=struct.Struct("<f")
DataS=struct.Struct("BBBBBB")
DataM=struct.Struct("B")

#入力用テーブル
SendDict=defaultdict(lambda:U_Int,
    {
        0x02:Float,0x03:Float,
        0x04:Bool4,0x05:Bool4,0x06:Bool4,
        0x74:Float,0x75:Float,0x76:Float,
        0x78:Bool4,0x79:U_Int
    })
#出力用テーブル
ResvDict=defaultdict(lambda:U_Int,
    {
        0x02:Float,0x03:Float,
        0x08:Bool4,0x09:Bool4,0x0A:Bool4
    })

CRC_Base=0b1011L
def CalcCRC(data):
    CRCV = CRC_Base<<35
    CRCM = 1L<<38
    for i in range(36):
        if data & CRCM:
            data^=CRCV
        CRCV>>=1
        CRCM>>=1
    return data&0x7

def MakeData(ID,Data):
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

def DecodeData(Data):
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





		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""

		 - Name:  Port
		 - DefaultValue: COM1
		"""
		self._Port = ['COM1']

		# </rtc-template>
		self.SPort=None
		self.X=0
		self.Y=0
		self.A=0
		self.T=0
		self.Received=[]
		self.Functions=defaultdict(lambda:NoFunc,
                        {
                                0x02:self.SetLeft,
                                0x03:self.SetRight
                        })


	def SetLeft(self,Data):
		self.VLr=Data*MPCnt
	def SetRight(self,Data):
		self.VRr=Data*MPCnt

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
		self.SPort=serial.Serial(self._Port[0],timeout=TimeOut)
		self.Send(0x78,True)
		self.VLr=0
		self.VRr=0
		self.X=0
		self.Y=0
		self.A=0
		self.T=time.time()
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
		self.Send(0x78,False)
		self.Send(0x02,0)
		self.Send(0x03,0)
		self.recieving=False
		self.RTh.join()
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
                        #速度入力
                        data=self._VelocityInIn.read().data
                        VX=data.vx
                        VA=data.va
                        VL=VX-hftr*VA
                        VR=VX+hftr*VA
                        self.Send(0x02,VL*CntPM)
                        self.Send(0x03,VR*CntPM)
		#現在位置推測
		VA=(self.VRr-self.VLr)/tread
		VX=(self.VRr+self.VLr)/2.0
		NT=time.time()
		dT=NT-self.T
		dS=VA*dT
		dL=VX*dT
                if abs(dS)>Epsilon:#dSが大きい場合は調整
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
		return RTC.RTC_OK
	def Receive(self):#データ受信スレッド用関数
                while self.recieving:
                        Data=self.SPort.read(1)
                        if len(Data)==0:
                                continue
                        Data=DataM.unpack(Data)[0]
                        self.Received.append(Data)
                        if Data & 0x80:
                                ID,Data=DecodeData(self.Received)
                                #print ID,Data
                                self.Functions[ID](Data)
                                self.Received=[]
	def Send(self,ID,Data):
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

