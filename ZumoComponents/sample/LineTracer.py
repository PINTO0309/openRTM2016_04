#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file LineTracer.py
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
linetracer_spec = ["implementation_id", "LineTracer",
		 "type_name",         "LineTracer",
		 "description",       "ModuleDescription",
		 "version",           "1.0.0",
		 "vendor",            "Konan University",
		 "category",          "Category",
		 "activity_type",     "STATIC",
		 "max_instance",      "1",
		 "language",          "Python",
		 "lang_type",         "SCRIPT",
#		 "conf.default.Threshold", "500",
#		 "conf.default.VX_weight_sensor_DOWN1", "-0.005",
#		 "conf.default.VX_weight_sensor_DOWN2", "0.05",
#		 "conf.default.VX_weight_sensor_DOWN3", "0.1",
#		 "conf.default.VX_weight_sensor_DOWN4", "0.05",
#		 "conf.default.VX_weight_sensor_DOWN5", "-0.005",
#		 "conf.default.VA_weight_sensor_DOWN1", "5.0",
#		 "conf.default.VA_weight_sensor_DOWN2", "3.0",
#		 "conf.default.VA_weight_sensor_DOWN3", "0.0",
#		 "conf.default.VA_weight_sensor_DOWN4", "-3.0",
#		 "conf.default.VA_weight_sensor_DOWN5", "-5.0",
         "conf.default.VX_Gain","[-0.005,0.05,0.1,0.05,-0.005]",
         "conf.default.VA_Gain","[5.0,3.0,0.0,-3.0,-5.0]",

#		 "conf.__widget__.Threshold", "text",
#		 "conf.__widget__.VX_weight_sensor_DOWN1", "text",
#		 "conf.__widget__.VX_weight_sensor_DOWN2", "text",
#		 "conf.__widget__.VX_weight_sensor_DOWN3", "text",
#		 "conf.__widget__.VX_weight_sensor_DOWN4", "text",
#		 "conf.__widget__.VX_weight_sensor_DOWN5", "text",
#		 "conf.__widget__.VA_weight_sensor_DOWN1", "text",
#		 "conf.__widget__.VA_weight_sensor_DOWN2", "text",
#		 "conf.__widget__.VA_weight_sensor_DOWN3", "text",
#		 "conf.__widget__.VA_weight_sensor_DOWN4", "text",
#		 "conf.__widget__.VA_weight_sensor_DOWN5", "text",
         "conf.__widget__.VX_Gain","text",
         "conf.__widget__.VA_Gain","text",

         "conf.__type__.Threshold", "int",
#         "conf.__type__.VX_weight_sensor_DOWN1", "double",
#         "conf.__type__.VX_weight_sensor_DOWN2", "double",
#         "conf.__type__.VX_weight_sensor_DOWN3", "double",
#         "conf.__type__.VX_weight_sensor_DOWN4", "double",
#         "conf.__type__.VX_weight_sensor_DOWN5", "double",
#         "conf.__type__.VA_weight_sensor_DOWN1", "double",
#         "conf.__type__.VA_weight_sensor_DOWN2", "double",
#         "conf.__type__.VA_weight_sensor_DOWN3", "double",
#         "conf.__type__.VA_weight_sensor_DOWN4", "double",
#         "conf.__type__.VA_weight_sensor_DOWN5", "double",

		 ""]
# </rtc-template>

##
# @class LineTracer
# @brief ModuleDescription
#
#
class LineTracer(OpenRTM_aist.DataFlowComponentBase):

	##
	# @brief constructor
	# @param manager Maneger Object
	#
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

#		LineSensors_arg = [None] * ((len(RTC._d_TimedULongSeq) - 4) / 2)
#		self._d_LineSensors = RTC.TimedULongSeq(*LineSensors_arg)
		self._d_LineSensors = RTC.TimedULongSeq(RTC.Time(0,0),0)
		"""
		"""
		self._LineSensorsIn = OpenRTM_aist.InPort("LineSensors", self._d_LineSensors)
#		Velocity_arg = [None] * ((len(RTC._d_TimedVelocity2D) - 4) / 2)
#		self._d_Velocity = RTC.TimedVelocity2D(*Velocity_arg)
		self._d_Velocity = RTC.TimedVelocity2D(RTC.Time(0,0),0)
		"""
		"""
		self._VelocityOut = OpenRTM_aist.OutPort("Velocity", self._d_Velocity)





		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		self.VX_Gain=["[-0.005,0.05,0.1,0.05,-0.005]"]
		self.VA_Gain=["[5.0,3.0,0.0,-3.0,-5.0]"]

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
		#self.bindParameter("Threshold", self._Threshold, "500")
		#self.bindParameter("VX_weight_sensor_DOWN1", self._VX_weight_sensor_DOWN1, "-0.005")
		#self.bindParameter("VX_weight_sensor_DOWN2", self._VX_weight_sensor_DOWN2, "0.05")
		#self.bindParameter("VX_weight_sensor_DOWN3", self._VX_weight_sensor_DOWN3, "0.1")
		#self.bindParameter("VX_weight_sensor_DOWN4", self._VX_weight_sensor_DOWN4, "0.05")
		#self.bindParameter("VX_weight_sensor_DOWN5", self._VX_weight_sensor_DOWN5, "-0.005")
		#self.bindParameter("VA_weight_sensor_DOWN1", self._VA_weight_sensor_DOWN1, "5.0")
		#self.bindParameter("VA_weight_sensor_DOWN2", self._VA_weight_sensor_DOWN2, "3.0")
		#self.bindParameter("VA_weight_sensor_DOWN3", self._VA_weight_sensor_DOWN3, "0.0")
		#self.bindParameter("VA_weight_sensor_DOWN4", self._VA_weight_sensor_DOWN4, "-3.0")
		#self.bindParameter("VA_weight_sensor_DOWN5", self._VA_weight_sensor_DOWN5, "-5.0")
		self.bindParameter("VX_Gain",self.VX_Gain,"[-0.005,0.05,0.1,0.05,-0.005]")
		self.bindParameter("VA_Gain",self.VA_Gain,"[5.0,3.0,0.0,-3.0,-5.0]")

		# Set InPort buffers
		self.addInPort("LineSensors",self._LineSensorsIn)

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
	def onActivated(self, ec_id):
		self.VXG=eval(self.VX_Gain[0])
		self.VAG=eval(self.VA_Gain[0])
		if not all(map(lambda x:isinstance(x,float),self.VXG)):
			return RTC.RTC_ERROR
		if not all(map(lambda x:isinstance(x,float),self.VAG)):
			return RTC.RTC_ERROR
		return RTC.RTC_OK

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
		if self._LineSensorsIn.isNew():# 速度の送信
			sensor_data=self._LineSensorsIn.read().data
			vx=sum(map(lambda x,y:x*y,sensor_data,self.VXG))/(sum(sensor_data)+1)
			vy=0.0
			va=sum(map(lambda x,y:x*y,sensor_data,self.VAG))/(sum(sensor_data)+1)

			self._d_Velocity.data=RTC.Velocity2D(vx,vy,va)
			OpenRTM_aist.setTimestamp(self._d_Velocity)
        	self._VelocityOut.write()

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




def LineTracerInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=linetracer_spec)
    manager.registerFactory(profile,
                            LineTracer,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    LineTracerInit(manager)

    # Create a component
    comp = manager.createComponent("LineTracer")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

