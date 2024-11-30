from pymysql import Connection
con = None
try:
    con = Connection(
        host="localhost",
        port=3306,
        user="DB_python",
        password="Yorkstudy2024",
        database= "DB_python"
    )
    cursor = con.cursor()

    sql = """
            CREATE TABLE 't_student' (
        'id' int(11) NOT NULL AUTO_INCREMENT,
        'name' varchar(10) DEFAULT NULL,
        'age' int(11) DEFAULT NULL,
        PRIMARY KEY ('id')
    )   ENGINE = InnoDB DEFAULT CHARSET = utf8 
    """
    con.select_db("DB_python")

    cursor.execute(sql)
except Exception as e:
    print("error :",e)

finally:
    if con:
        con.close()