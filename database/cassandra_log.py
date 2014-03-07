"""
    @author: hainq@gviet.vn
    @since: March 2014
"""
from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement
import time
from twisted.python import log
import traceback
from twisted.internet import reactor

class Cassandra_Log():
    """
        Use as a proxy, singleton pattern
    """
    instance=None
    def __init__(self,interface='127.0.0.1',keyspace=''):
        """
            interface is type off list
        """
        print 'Cassandra_Log::__init__()',interface,keyspace
        cluster=Cluster([interface])
        self.session=cluster.connect(keyspace)
        self.err_query=SimpleStatement("Insert into err(id,time,info) values(%s,%s,%s)")
        self.req_query=SimpleStatement("Insert into req(id,time,info) values(%s,%s,%s)")
        Cassandra_Log.instance=self

            
        
    @staticmethod
    def get_instance(interface='127.0.0.1',keyspace=''):
        if Cassandra_Log.instance is None:
            print 'cassandra_Log::_get_instance None'
            Cassandra_Log.instance=Cassandra_Log(interface,keyspace)
        else:
            print 'Cassandra_Log::_get_not None'
        return Cassandra_Log.instance
    
    
    def log_err(self,info):
        """
            Log error, exception occur within server running
            should running in thread pool
        """
        timestamp=time.time()
        self.session.execute(self.err_query, (int(timestamp)/86400, int(timestamp*1000), info))
    
            
    def log_request(self,info):
        """
            should running in thread pool
        """
        timestamp=time.time()
        self.session.execute(self.req_query, (int(timestamp)/86400, int(timestamp*1000), info ))
       
    @staticmethod 
    def errback_log(failure):
        log.msg(failure.getTraceback())
        