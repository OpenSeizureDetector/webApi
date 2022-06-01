#!usr/bin/python3

import json
import sdAlg

class OsdAlg(sdAlg.SdAlg):
    def __init__(self, settingsStr, debug=True):
        print("OsdAlg.__init__() - settingsStr=%s" % settingsStr)
        print("OsdAlg.__init__(): settingsStr=%s (%s)"
                               % (settingsStr, type(settingsStr)))
        super().__init__(settingsStr, debug)
        
    def processDp(self, dpStr):
        self.logD("OsdAlg.processDp: dpStr=%s." % dpStr)
        retVal = {"alarmState": 0}
        return(json.dumps(retVal))
                  
if __name__ == "__main__":
    print("osdAlg.OsdAlg.main()")
    settingsObj = {
        "alarmFreqMin" : 3,
        "alarmFreqMax" : 8,
        "alarmThreshold" : 100,
        "alarmRatioThreshold" : 57
        }
    alg = OsdAlg(json.dumps(settingsObj),True)
