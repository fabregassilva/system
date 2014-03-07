"""
    @author: hainq@gviet.vn
    @since: Feb 2014
    @last update: Feb 2014
"""
import sys
import config
sys.path.append(config.pathbase)
from twisted.python import log
from network.server import Server
from database.cassandra_log import Cassandra_Log

if __name__=='__main__':
    print sys.path
    log.startLogging(sys.stdout)
    Cassandra_Log(config.cassandra_interface, config.cassandra_keyspace)
    server_rpc=Server()
    server_rpc.start()
    