import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')


def users_show_all():
    with conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                    SELECT *
                    FROM users
                    WHERE 
                    ''', )
            for row in cursor:
                print(row)


def user_show_college(college):
    # college = (1 корпус, 2 корпус, 3 корпус, 4 корпус)
    with conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                    SELECT user_id
                    FROM users
                    WHERE college = %s
                    ''', (college,))
            return cursor.fetchall()


def user_delete(user_id):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                    DELETE FROM users
                    WHERE user_id = %s
                    ''', (user_id,))


def user_update(user_id, college):
    with conn:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                UPDATE users
                SET college = %s 
                WHERE user_id = %s
                ''', (college, user_id))


def user_add(user_id, name, college):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                    INSERT INTO users (user_id, name, college)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (user_id) DO NOTHING
                    ''', (user_id, name, college))
