"""
    @author: hainq@gviet.vn
    @since: Feb 2014
    @last update: Feb 2014
"""
import traceback
import sys
import importlib
from handler import log

class Dispatcher:
    instance=None

    def call(self,type_,id_,protocol, param_dict):
        logtype=param_dict.get('logtype',1)
        del param_dict['logtype']
        if logtype == 1:
            return log.userlog(type_,id_,protocol, **param_dict)
        elif logtype==2:
            return log.matchlog(type_,id_,protocol, **param_dict)
    
    @staticmethod
    def get_dispatcher():
        if Dispatcher.instance is None:
            Dispatcher.instance=Dispatcher()
            return Dispatcher.instance
        return Dispatcher.instance
            
   
if __name__=='__main__':
    x=Dispatcher.get_dispatcher()
    y=Dispatcher.get_dispatcher()
    z=Dispatcher.get_dispatcher()
    
    print x is y, y is z     