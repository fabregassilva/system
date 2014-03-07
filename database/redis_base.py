"""
    @author: Hainq@gviet.vn
    @since: Mar 2014
"""

import redis
import time
import msgpack


class Redis_Connection(redis.StrictRedis):
    """
        Singleton pattern
        one instance should be create once when application start
    """
    instance=None
    def __init__(self,redis_host='localhost', redis_port=6379, redis_db=0):
        super(Redis_Connection,self).__init__(redis_host,redis_port,redis_db)

    @staticmethod
    def get_instance(host='localhost',port=6379,db=0):
        if Redis_Connection.instance is None:
            Redis_Connection.instance=Redis_Connection(host,port,db)
        return Redis_Connection.instance
    
if __name__=='__main__':
    red=Redis_Connection()
    red.rpush('l1',*['hainq',1,2,3,4])
    