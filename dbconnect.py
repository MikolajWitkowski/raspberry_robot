from psycopg2 import connect


def connection():
	username='pi'
	passwd = 'raspiDB'
	hostname='127.0.0.1'
	db_name='users'
	
	conn = connect(user=username, password=passwd, host=hostname, database=db_name)
	conn.autocommit = True
	c = conn.cursor()
	
	return c, conn
