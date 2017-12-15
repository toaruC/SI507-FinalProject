# Database Goes Here
import psycopg2
import psycopg2.extras
import csv
from config import *

### SETUP database connection and cursor here.
DEBUG = False

def get_connection_and_cursor():
    try:
        if db_password != "":
            db_connection = psycopg2.connect("dbname='{0}' user='{1}' password='{2}'".format(db_name, db_user, db_password))
            print("Success connecting to database")
        else:
            db_connection = psycopg2.connect("dbname='{0}' user='{1}'".format(db_name, db_user))
    except:
        print("Unable to connect to the database. Check server and credentials.")
        sys.exit(1) # Stop running program if there's no db connection.

    db_cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    return db_connection, db_cursor


conn, cur = get_connection_and_cursor()

### CREATE tables and all database setup here.
def create_tables():
    # Table Users
    if DEBUG:
        print("Create TABLE Users")
    cur.execute("DROP TABLE IF EXISTS Users CASCADE")
    cur.execute("""CREATE TABLE IF NOT EXISTS Users(
                    id VARCHAR(255) PRIMARY KEY,
                    name VARCHAR(40) UNIQUE,
                    profile_url VARCHAR(255)
                    )"""
                )

    # Table Posts
    if DEBUG:
        print("Create TABLE Posts")

    cur.execute("DROP TABLE IF EXISTS Posts")
    cur.execute("""CREATE TABLE IF NOT EXISTS Posts(
                    id VARCHAR(255) PRIMARY KEY,
                    owner VARCHAR(255),
                    img_url VARCHAR(255),
                    num_of_likes INTEGER,
                    post_url VARCHAR(255),
                    num_of_tags INTEGER,
                    tags TEXT
                    )"""
                )

    conn.commit() # Necessary to save changes in database

# Insert data (from SI507F17_finalproject_oauth) into the database here.

def insert_users(ins_user_list):
    for user in ins_user_list:
        cur.execute("""INSERT INTO
                        Users(id, name, profile_url)
                        VALUES (%s, %s, %s)""",
                        (user.id, user.name, user.profile_url,)
                    )
        if DEBUG:
            print("insert userid: {0} | username: {1}".format(user.id, user.name))
    conn.commit()

def insert_posts(ins_post_list):
    for post in ins_post_list:
        if post.tags:
            cur.execute("""INSERT INTO
                            Posts(id, owner, img_url, num_of_likes, post_url, num_of_tags, tags)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                            (post.id, post.owner, post.img_url, str(post.num_of_likes), post.post_url, str(post.num_of_tags),";".join(post.tags),)
                        )
        else:
            cur.execute("""INSERT INTO
                            Posts(id, owner, img_url, num_of_likes, post_url, num_of_tags, tags)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                            (post.id, post.owner, post.img_url, str(post.num_of_likes), post.post_url, str(post.num_of_tags),"",)
                        )
        if DEBUG:
            print("insert postid: {0} | owner: {1} | likes: {2} | num_of_tags: {3}".format(post.id, post.owner, str(post.num_of_likes), str(post.num_of_tags)))
    conn.commit()

# QUERY Func
def execute_and_print(query, numer_of_results=1):
    cur.execute(query)
    results = cur.fetchall()
    for r in results[:numer_of_results]:
        print(r)
    print('--> Result Rows:', len(results))
    print()
    return results
