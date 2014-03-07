"""
    Server config
"""
is_debug=True
maximum_package_size=65536*2
interface='127.0.0.1'
port=9001
backlog=15
pathbase=' /home/hainq/Documents/aptana/server_service'
logfile=pathbase+"/err.log"
import os.path
pathbase=os.path.abspath(os.path.join(pathbase, os.pardir))

"""
    Database config
"""
mysql_port=''
mysql_interface=''
mysql_user=''
mysql_pass=''
mysql_db=''

cassandra_interface='127.0.0.1'
cassandra_port=''
cassandra_keyspace='mytest'
log_to_cassandra=True



redis_interface='127.0.0.1'
redis_port=6379
redis_db=0