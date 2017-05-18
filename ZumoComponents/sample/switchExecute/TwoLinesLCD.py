#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file TwoLinesLCD.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")
import re
#import RPi.GPIO as GPIO
import codecs
import os
import subprocess

# Import RTM module
import RTC
import OpenRTM_aist

# Global
LCDLocation = ""


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
twolineslcd_spec = ["implementation_id", "TwoLinesLCD", 
		 "type_name",         "TwoLinesLCD", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "kiyosedaiki", 
		 "category",          "LC", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.LCDLocation", "0x3e",

		 "conf.__widget__.LCDLocation", "text",

         "conf.__type__.LCDLocation", "string",

		 ""]
# </rtc-template>

##
# @class TwoLinesLCD
# @brief ModuleDescription
# 
# 
class TwoLinesLCD(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		#inputLines_arg = [None] * ((len(RTC._d_TimedString) - 4) / 2)
		self._d_inputLines = RTC.TimedStringSeq(RTC.Time(0,0),0)
		"""
		"""
		self._InputIn = OpenRTM_aist.InPort("Input", self._d_inputLines)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  LCDLocation
		 - DefaultValue: 0x3e
		"""
		self._LCDLocation = ['0x3e']
		
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
		self.bindParameter("LCDLocation", self._LCDLocation, "0x3e")
		
		# Set InPort buffers
		self.addInPort("Input",self._InputIn)
		
		# Set OutPort buffers
		
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
		location = self._LCDLocation
		location = str(location).replace('[','').replace(']','')
		location = re.sub('\'','',location)

		global LCDLocation
		LCDLocation = location

		self.startupLCD()

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
	def startupLCD(self):#初期設定
		os.system('i2cset -y 1 ' + LCDLocation + ' 0 0x38 0x39 0x14 0x78 0x5f 0x6a i')
		time.sleep(0.5)
		os.system('i2cset -y 1 ' + LCDLocation + ' 0 0xc 0x1 i')
		time.sleep(0.5)
		os.system('i2cset -y 1 ' + LCDLocation + ' 0 0x6 i')
		time.sleep(0.5)
		
	def convertChara(self,line):#キャラクタコード変換
		characterCodes = ''
		line = line.replace('\t','')
		i = 0
		changedWord = codecs.encode(line,'hex_codec')
		num = len(changedWord)
		if num != 1:
			while i != num:
				characterCodes = characterCodes +' 0x' + changedWord[i] + changedWord[i+1]
				i = i + 2
		else:
			characterCodes = ' 0x' + changedWord

		return characterCodes

	def indicate1(self,line):#１行目表示
		print line
		
		os.system('i2cset -y 1 ' + LCDLocation + ' 0 0x80 b')
		os.system('i2cset -y 1 0x3e 0x40' + line + ' 0x76 0x65 i')

	def indicate2(self,line):#２行目表示
		print line
		os.system('i2cset -y 1 ' + LCDLocation + ' 0 0xc0 b')
		os.system('i2cset -y 1 0x3e 0x40' + line + ' 0x76 0x65 i')
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
		wordlist = []
		if self._InputIn.isNew():
			loglist = self._InputIn.read()
			num = len(loglist.data)
			for line in loglist.data:
				wordlist.append(self.convertChara(line))

			i = 0
			while i != num:
                                os.system('i2cset -y 1 0x3e ' + LCDLocation + ' 0 0x01')
				if num == 1:
					self.indicate1(wordlist)
				else:
					if i == num-1:#1行用
						self.indicate1(wordlist[i])
					else:#２行以上の表示
						self.indicate1(wordlist[i%num])
						self.indicate2(wordlist[(i+1)%num])
				i = i + 1

				time.sleep(1)

			sleepTime = num * 0.5
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
	



def TwoLinesLCDInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=twolineslcd_spec)
    manager.registerFactory(profile,
                            TwoLinesLCD,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    TwoLinesLCDInit(manager)

    # Create a component
    comp = manager.createComponent("TwoLinesLCD")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

