"""
    @author: hainq@gviet.vn
    @since: Feb 2014
    @last update: Feb 2014
"""


from twisted.internet import reactor
import sqlalchemy
import sqlalchemy.engine
import MySQLdb
import time
import redis
from sqlalchemy import sql, MetaData



class MySQL_Manager:
    def __init__(self,user='', password='', interface='', port='',db=''):
        string_connect = 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8' % (user, password, interface, port, db)
        self.instance=sqlalchemy.create_engine(string_connect, encoding='utf-8', convert_unicode=True,pool_recycle=10)
        
    def query(self,obj, *multiparams, **params):
        """
            return result proxy sqlalchemy
        """
        connect=self.instance.connect()
        return connect.execute(obj, *multiparams, **params)
        

    
