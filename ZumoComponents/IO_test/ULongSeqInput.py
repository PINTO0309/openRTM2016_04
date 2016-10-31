#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

import sys
import time
sys.path.append(".")

import RTC
import OpenRTM_aist

ULongSeqinput_spec = ["implementation_id", "ULongSeqInput", 
		 "type_name",         "ULongSeqInput", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "VenderName", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
class ULongSeqInput(OpenRTM_aist.DataFlowComponentBase):
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_In = RTC.TimedULongSeq(RTC.Time(0,0),0)
		self._InIn = OpenRTM_aist.InPort("In", self._d_In)
	def onInitialize(self):
		self.addInPort("In",self._InIn)
		return RTC.RTC_OK
	def onExecute(self, ec_id):
		#--------------------------------------------------------------#
		if self._InIn.isNew():
			d=self._InIn.read()
			print time.strftime("%Y/%m/%d %H:%M:%S %Z")
			for i in d.data:
				print i
		return RTC.RTC_OK
		#--------------------------------------------------------------#
def ULongSeqInputInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=ULongSeqinput_spec)
    manager.registerFactory(profile,
                            ULongSeqInput,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    ULongSeqInputInit(manager)

    # Create a component
    comp = manager.createComponent("ULongSeqInput")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

