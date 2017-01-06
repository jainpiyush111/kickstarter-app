import psycopg2 as pg


def get_connection():
    conn = pg.connect(
        database='nwpzolgh',
        user='nwpzolgh',
        password='wZbR4Q7D1YpI0PI0velMGKyFkKxPEuHi',
        host='elmer.db.elephantsql.com',
        port=5432)
    return conn


def authenticate(username, password):
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT username, password from "public"."user" where username='%s' and password='%s'"""
    query = query % (username, password)
    cursor.execute(query)
    rows = cursor.fetchall()
    try:
        if (rows[0][0] == username) and (rows[0][1] == password):
            return 1
        else:
            return 0
    except Exception as error:
        return error
    connection.close()


def get_data(username, password):
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT * from "public"."user" where username='%s' and password='%s'"""
    query = query % (username, password)
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.close()
    return rows


def show_project(userid):
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT * from "public"."projects" where "user_id"='%s'"""
    query = query % (userid)
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.close()
    return rows


def pledge(pledge):
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT * from "public"."projects" where id='%s'"""
    query = query % (pledge)
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.close()
    return rows
