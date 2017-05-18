#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file ReadingLog.py
 @brief ログの読み取り
 @date $Date$


"""
import sys
import time
sys.path.append(".")
import re

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
readinglog_spec = ["implementation_id", "ReadingLog", 
		 "type_name",         "ReadingLog", 
		 "description",       "ログの読み取り", 
		 "version",           "1.0.0", 
		 "vendor",            "kiyosedaiki", 
		 "category",          "Reader", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.SuccessLog", "SuccessLog.txt",
		 "conf.default.ErrorLog", "ErrorLog.txt",

		 "conf.__widget__.SuccessLog", "text",
		 "conf.__widget__.ErrorLog", "text",

         "conf.__type__.SuccessLog", "string",
         "conf.__type__.ErrorLog", "string",

		 ""]
# </rtc-template>

##
# @class ReadingLog
# @brief ログの読み取り
# 
# 
class ReadingLog(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		#outputLines_arg = [None] * ((len(RTC._d_TimedString) - 4) / 2)
		self._d_outputLines = RTC.TimedStringSeq(RTC.Time(0,0),0)
		"""
		"""
		self._OutputOut = OpenRTM_aist.OutPort("Output", self._d_outputLines)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  SuccessLog
		 - DefaultValue: SuccessLog.txt
		"""
		self._SuccessLog = ['SuccessLog.txt']
		"""
		
		 - Name:  ErrorLog
		 - DefaultValue: ErrorLog.txt
		"""
		self._ErrorLog = ['ErrorLog.txt']
		
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
		self.bindParameter("SuccessLog", self._SuccessLog, "SuccessLog.txt")
		self.bindParameter("ErrorLog", self._ErrorLog, "ErrorLog.txt")
		
		# Set InPort buffers
		
		# Set OutPort buffers
		self.addOutPort("Output",self._OutputOut)
		
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
	
	#	##
	#	#
	#	# The execution action that is invoked periodically
	#	# former rtc_active_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	def onExecute(self, ec_id):
		ErrorLog = self._ErrorLog
		ErrorLog = str(ErrorLog).replace('[','').replace(']','')
		ErrorLog = re.sub('\'','',ErrorLog)
		SuccessLog = self._SuccessLog
		SuccessLog = str(SuccessLog).replace('[','').replace(']','')
		SuccessLog = re.sub('\'','',SuccessLog)

		loglist = []
		if sum(1 for line in open(ErrorLog,'r')) == 0:
			if open(ErrorLog,'r').read() == "":
				line = open(SuccessLog,'r')
				#read successlog.txt
				for log in line:
					loglist.append(log.replace('\n',''))
		else:
			line = open(ErrorLog,'r')
			#read errorlog.txt
			for log in line:
				loglist.append(log.replace('\n',''))


		if loglist != "":
			OpenRTM_aist.setTimestamp(self._d_outputLines)
			self._d_outputLines.data = loglist
			num =  len(self._d_outputLines.data)
			print loglist
			self._OutputOut.write()

		sleepTime = num * 1
		time.sleep(sleepTime)
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
	



def ReadingLogInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=readinglog_spec)
    manager.registerFactory(profile,
                            ReadingLog,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    ReadingLogInit(manager)

    # Create a component
    comp = manager.createComponent("ReadingLog")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

