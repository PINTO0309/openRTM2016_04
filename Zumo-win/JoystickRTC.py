#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file JoystickRTC.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
import pygame

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>

# ジョイスティックの取得、一覧作成
#pygame.init()
pygame.joystick.init()
JoyN=pygame.joystick.get_count()
if JoyN==0:# ジョイスティックがなければプログラム停止
        exit(1)
JoyNS=""
JoyND={}
DefN=None
for i in range(JoyN):
        Name=pygame.joystick.Joystick(i).get_name().strip()
        JoyND[Name]=i
        JoyNS+=Name+","
        if DefN is None:
                DefN=Name
JoyNS=JoyNS[:-1]

# This module's spesification
# <rtc-template block="module_spec">
joystickrtc_spec = ["implementation_id", "JoystickRTC",
		 "type_name",         "JoystickRTC",
		 "description",       "ModuleDescription",
		 "version",           "1.0.0",
		 "vendor",            "VenderName",
		 "category",          "Category",
		 "activity_type",     "STATIC",
		 "max_instance",      "1",
		 "language",          "Python",
		 "lang_type",         "SCRIPT",
		 "conf.default.JoyStick", DefN,
		 "conf.__widget__.JoyStick", "radio",
		 "conf.__constraints__.JoyStick", "("+JoyNS+")",
		 ""]
# </rtc-template>

##
# @class JoystickRTC
# @brief ModuleDescription
#
#
class JoystickRTC(OpenRTM_aist.DataFlowComponentBase):

	##
	# @brief constructor
	# @param manager Maneger Object
	#
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_Axis = RTC.TimedDoubleSeq(RTC.Time(0,0),[])
		"""
		"""
		self._AxisOut = OpenRTM_aist.OutPort("Axis", self._d_Axis)
		self._d_Trackball = RTC.TimedDoubleSeq(RTC.Time(0,0),[])
		"""
		"""
		self._TrackballOut = OpenRTM_aist.OutPort("Trackball", self._d_Trackball)
		self._d_Button = RTC.TimedBooleanSeq(RTC.Time(0,0),[])
		"""
		"""
		self._ButtonOut = OpenRTM_aist.OutPort("Button", self._d_Button)
		self._d_Hat = RTC.TimedShortSeq(RTC.Time(0,0),[])
		"""
		"""
		self._HatOut = OpenRTM_aist.OutPort("Hat", self._d_Hat)





		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""

		 - Name:  JoyStick
		 - DefaultValue: N
		"""
		self._JoyStick = [DefN]

		# </rtc-template>



	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry()
	#
	# @return RTC::ReturnCode_t
	#
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("JoyStick", self._JoyStick, "N")

		# Set InPort buffers

		# Set OutPort buffers
		self.addOutPort("Axis",self._AxisOut)
		self.addOutPort("Trackball",self._TrackballOut)
		self.addOutPort("Button",self._ButtonOut)
		self.addOutPort("Hat",self._HatOut)

		# Set service provider to Ports

		# Set service consumers to Ports

		# Set CORBA Service Ports

		return RTC.RTC_OK

	#	##
	#	#
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	#
	#	# @return RTC::ReturnCode_t
	#
	#	#
	#def onFinalize(self):
	#
	#	return RTC.RTC_OK

	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK

	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK

		##
		#
		# The activated action (Active state entry action)
		# former rtc_active_entry()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onActivated(self, ec_id):
                # ジョイスティックの初期化
                JoyName=self._JoyStick[0]
                self.JS=pygame.joystick.Joystick(JoyND[JoyName])
                self.JS.init()
                self.AN=self.JS.get_numaxes()
                self.TN=self.JS.get_numballs()
                self.BN=self.JS.get_numbuttons()
                self.HN=self.JS.get_numhats()
                print JoyName
                print "Axis     ",self.AN
                print "Trackball",self.TN
                print "Button   ",self.BN
                print "Hat      ",self.HN
                return RTC.RTC_OK

		##
		#
		# The deactivated action (Active state exit action)
		# former rtc_active_exit()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onDeactivated(self, ec_id):
                # ジョイスティックの破棄
                self.JS.quit()
		return RTC.RTC_OK

		##
		#
		# The execution action that is invoked periodically
		# former rtc_active_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onExecute(self, ec_id):
                # 値の取得、送信
                pygame.event.pump()
                Ax=[]
                Tr=[]
                Bn=[]
                Ht=[]
                for i in xrange(self.AN):# 軸
                        x=self.JS.get_axis(i)
                        Ax.append(x)
                for i in xrange(self.TN):# トラックボール
                        x,y=self.JS.get_ball(i)
                        Tr.append(x)
                        Tr.append(y)
                for i in xrange(self.BN):# ボタン
                        x=self.JS.get_button(i)==1
                        Bn.append(x)
                for i in xrange(self.HN):# ハット
                        x,y=self.JS.get_hat(i)
                        Ht.append(x)
                        Ht.append(y)
                #print Ax,Tr,Bn,Ht,"\r",
                self._d_Axis.data     =Ax
                self._d_Trackball.data=Tr
		self._d_Button.data   =Bn
		self._d_Hat.data      =Ht
		OpenRTM_aist.setTimestamp(self._d_Axis)
		OpenRTM_aist.setTimestamp(self._d_Trackball)
		OpenRTM_aist.setTimestamp(self._d_Button)
		OpenRTM_aist.setTimestamp(self._d_Hat)
		self._AxisOut.write()
		self._TrackballOut.write()
		self._ButtonOut.write()
		self._HatOut.write()

		return RTC.RTC_OK

	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK

	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK

	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK

	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK

	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK




def JoystickRTCInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=joystickrtc_spec)
    manager.registerFactory(profile,
                            JoystickRTC,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    JoystickRTCInit(manager)

    # Create a component
    comp = manager.createComponent("JoystickRTC")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

