#!python3
import pymysql.cursors

def get_connection():

    #inicia conexão com banco
    connection = pymysql.connect(
        host='127.0.0.1',
        user='fer',
        password='fer',
        db='investimento',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )

    return connection


def execute_update(sql):
    try:
        
        connection = get_connection()

        with connection.cursor() as cursor:  
            cursor.execute(sql)
        connection.commit()

        connection.close()

        return True

    except Excpetion as e:
        return False
    finally:
        return True

