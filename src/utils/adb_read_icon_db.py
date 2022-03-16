# https://pynative.com/python-sqlite-blob-insert-and-retrieve-digital-data/

import sqlite3
import os
import logging

log = logging.getLogger()

sqliteConnection = False

def writeToFile(data, icon_dir_path, icon_name):
    # Check that the path specified exists, if not, create it
    if not os.path.isdir(icon_dir_path):
        os.makedirs(icon_dir_path)
    
    # Write icon file from SQL Blob
    log.debug('Attempting to save ' + icon_name)
    with open(icon_dir_path + icon_name, 'wb') as notif_icon:
        if not data == None:
            notif_icon.write(data)
            log.debug('BLOB data stored into: ' + icon_dir_path + icon_name)


def findPkgVal(cursor, pkg):
    table_iter = 0
    comp_names = cursor.execute("SELECT componentName FROM icons")
    for item in comp_names:
        comp_name = ''.join(item)
        if comp_name.startswith(pkg):
            return comp_name
    
def readBlobData(pkg, db_path):
    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        log.debug("Connected to SQLite")

        compName = findPkgVal(cursor, pkg)
        if not compName == None:
            sql_fetch_blob_query = """SELECT * from icons where componentName = ?"""
            cursor.execute(sql_fetch_blob_query, (compName,))
            record = cursor.fetchall()
            for row in record:
                name = row[6]
                photo = row[4]
                photo_dir_path = "src/web/static/icons/adb_icons/"
                photo_name =  name + ".png"
                writeToFile(photo, photo_dir_path, photo_name)

            cursor.close()
        else:
            return None
        return "static/icons/adb_icons/" + photo_name

    except sqlite3.Error as error:
        log.error("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            log.debug("sqlite connection is closed")

if __name__ == "__main__":
    readBlobData("com.android.contacts", "app_icons.db")
