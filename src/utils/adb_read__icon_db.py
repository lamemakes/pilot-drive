# https://pynative.com/python-sqlite-blob-insert-and-retrieve-digital-data/

import sqlite3

sqliteConnection = False

def writeToFile(data, icon_name):
    with open(icon_name, 'wb') as notif_icon:
        if not data == None:
            notif_icon.write(data)
            print('BLOB data stored into: ' + icon_name + '\n')

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
        print("Connected to SQLite")

        compName = findPkgVal(cursor, pkg)
        print(compName)
        if not compName == None:
            sql_fetch_blob_query = """SELECT * from icons where componentName = ?"""
            cursor.execute(sql_fetch_blob_query, (compName,))
            record = cursor.fetchall()
            for row in record:
                name = row[6]
                photo = row[4]
                photoPath = "icons/" + name + ".png"
                writeToFile(photo, photoPath)

            cursor.close()
        else:
            photoPath = None
        return photoPath

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")

if __name__ == "__main__":
    readBlobData("com.android.contacts", "app_icons.db")
