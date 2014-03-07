"""
    author: hainq@gviet.vn
    @since: Feb 2014
"""
from twisted.internet import reactor
import msgpack
import time
from database.redis_base import Redis_Connection
import traceback
from network.message import Message
from twisted.internet.threads import deferToThread
from database.cassandra_log import Cassandra_Log as Logger
from twisted.internet import reactor
from server_service import config
import time

def userlog(type_,id_, protocol, app_id=0, username=0 ,contents=0,response=False):
    try:
        if type_==3:
            protocol.transport.write(handler_ping(id_))
        if app_id==0:
            raise Exception("Client does not provide app_id")
        time_ = time.time()
        time_day = time.strftime("%Y%m%d", time.gmtime(time_))
        value= {'username':username, 'time':int(time_), 'time_day':int(time_day), 'contents':contents}
        value= msgpack.dumps(value)
        d=deferToThread(push_to_redis, 'u_'+str(app_id), value)
        d.addCallback(callback_redis,protocol,type_,id_,response)
        d.addErrback(errback_redis,protocol,type_,id_,response)
    except:
        if config.log_to_cassandra:
            logger=Logger.get_instance()
            d=reactor.deferToThread(logger.log_err,traceback.format_exc())
            d.addErrback(logger.errback)
        else:
            print time.strftime("%d/%m/%Y %H:%M", time.localtime(time.time())), traceback.format_exc()
        if response:
            mess= Message(None, 2, id_, 0).build_data()
            protocol.write(mess)
            


def push_to_redis(key,value):
    try:
        redis=Redis_Connection.get_instance()
        redis.rpush(key,value)
    except Exception as e:
        try:
            print traceback.format_exc()
            Logger.get_instance().log_err(traceback.format_exc())
        except:
            print traceback.format_exc

def matchlog(type_,id_, protocol, app_id=0, match_id=0,contents=0,response=False):
    try:
        if type_==3:
            protocol.transport.write(handler_ping(id_))
        if app_id:
            raise Exception('Client does not provide app_id')
        time_ = time.time()
        time_day = time.strftime("%Y%m%d", time.gmtime(time_))
        value = {'match_id':match_id, 'time':int(time_), 'time_day':int(time_day), 'contents':contents}
        value= msgpack.dumps(value)
        d=deferToThread(push_to_redis('u_'+str(app_id), value))
        d.addCallback(callback_redis,protocol,type_,id_,response)
        d.addErrback(errback_redis,protocol,type_,id_,response)
    except:
        if config.log_to_cassandra:
            logger=Logger.get_instance()
            d=reactor.deferToThread(logger.log_err,traceback.format_exc())
            d.addErrback(logger.errback)
        else:
            print time.strftime("%d/%m/%Y %H:%M", time.localtime(time.time())), traceback.format_exc()
        if response:
            mess= Message(None, 2, id_, 0).build_data()
            protocol.write(mess)

def callback_redis(result, protocol, type_,id_,response=False):

    if response:
        mess= Message(None, 2, id_, 1).build_data()
        protocol.write(mess)
        
def errback_redis(failure, protocol, type_,id_,response=False ):
    if response:
        mess= Message(None, 2, id_, 0).build_data()
        protocol.write(mess)
    

def handler_ping(id_):
    mess=Message()
    mess.set_id(id_)
    mess.set_type(4)
    return mess.build_data() 