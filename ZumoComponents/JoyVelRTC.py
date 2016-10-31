#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file JoyVelRTC.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
joyvelrtc_spec = ["implementation_id", "JoyVelRTC", 
		 "type_name",         "JoyVelRTC", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "VenderName", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.VXGain", "-1.0",
		 "conf.default.VAGain", "1.0",
		 "conf.default.PivotButtonN", "0",
		 "conf.default.VXAxisN", "1",
		 "conf.default.VAAxisN", "0",
		 "conf.__widget__.VXGain", "text",
		 "conf.__widget__.VAGain", "text",
		 "conf.__widget__.PivotButtonN", "text",
		 "conf.__widget__.VXAxisN", "text",
		 "conf.__widget__.VAAxisN", "text",
		 ""]
# </rtc-template>

##
# @class JoyVelRTC
# @brief ModuleDescription
# 
# 
class JoyVelRTC(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_Axis = RTC.TimedDoubleSeq(RTC.Time(0,0),[])
		"""
		"""
		self._AxisIn = OpenRTM_aist.InPort("Axis", self._d_Axis)
		self._d_Button = RTC.TimedBooleanSeq(RTC.Time(0,0),[])
		"""
		"""
		self._ButtonIn = OpenRTM_aist.InPort("Button", self._d_Button)
		self._d_Velocity = RTC.TimedVelocity2D(RTC.Time(0,0),0)
		"""
		"""
		self._VelocityOut = OpenRTM_aist.OutPort("Velocity", self._d_Velocity)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  VXGain
		 - DefaultValue: 1.0
		"""
		self._VXGain = [-1.0]
		"""
		
		 - Name:  VAGain
		 - DefaultValue: 1.0
		"""
		self._VAGain = [1.0]
		"""
		
		 - Name:  PivotButtonN
		 - DefaultValue: 0
		"""
		self._PivotButtonN = [0]
		"""
		
		 - Name:  VXAxisN
		 - DefaultValue: 0
		"""
		self._VXAxisN = [1]
		"""
		
		 - Name:  VAAxisN
		 - DefaultValue: 1
		"""
		self._VAAxisN = [0]
		
		# </rtc-template>
		self.Pivot=False


		 
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
		self.bindParameter("VXGain", self._VXGain, "-1.0")
		self.bindParameter("VAGain", self._VAGain, "1.0")
		self.bindParameter("PivotButtonN", self._PivotButtonN, "0")
		self.bindParameter("VXAxisN", self._VXAxisN, "1")
		self.bindParameter("VAAxisN", self._VAAxisN, "0")
		
		# Set InPort buffers
		self.addInPort("Axis",self._AxisIn)
		self.addInPort("Button",self._ButtonIn)
		
		# Set OutPort buffers
		self.addOutPort("Velocity",self._VelocityOut)
		
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
	
	#	##
	#	#
	#	# The activated action (Active state entry action)
	#	# former rtc_active_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	# 
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onActivated(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The deactivated action (Active state exit action)
	#	# former rtc_active_exit()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onDeactivated(self, ec_id):
	#
	#	return RTC.RTC_OK
	
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
                if self._AxisIn.isNew():# 速度の送信
                        d=self._AxisIn.read().data
                        x=d[self._VXAxisN[0]]
                        a=d[self._VAAxisN[0]]
                        vx=x*self._VXGain[0]
                        vy=0
                        if self.Pivot:
                                va=-a*self._VAGain[0]
                        else:
                                va=a*self._VAGain[0]*x
                        self._d_Velocity.data=RTC.Velocity2D(vx,vy,va)
                        OpenRTM_aist.setTimestamp(self._d_Velocity)
                        self._VelocityOut.write()
                if self._ButtonIn.isNew():# 制御方式の変更
                        self.Pivot=self._ButtonIn.read().data[self._PivotButtonN[0]]
                                
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
	



def JoyVelRTCInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=joyvelrtc_spec)
    manager.registerFactory(profile,
                            JoyVelRTC,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    JoyVelRTCInit(manager)

    # Create a component
    comp = manager.createComponent("JoyVelRTC")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

