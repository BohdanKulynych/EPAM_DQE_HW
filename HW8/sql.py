import argparse
import sqlite3
import csv
import os

# execute by     python sql.py -p 'BI'
parser = argparse.ArgumentParser(description='Enter name of project after -p')
parser.add_argument('-p', '--project', nargs='+', type=str, help='Enter project name', required=True)
args = parser.parse_args()


def if_db_exists(db_name):
    """

    :param db_name: database name
     check if db exists and recreate it
    """
    if os.path.exists(db_name):
        os.remove(db_name)
        sqlite3.connect(db_name)
    else:
        pass


def create_tables(conn):
    """
    :param conn: connection to database
    :return: create tables in db
    """
    cursor = conn.cursor()
    cursor.executescript(
        """
        CREATE TABLE Project
                  (
                  Name VARCHAR(255) PRIMARY KEY,
                  Description VARCHAR(255),
                  Deadline date       
                  );
               
        CREATE TABLE Tasks 
                  (
                  ID NUMBER PRIMARY KEY,
                  Priority INT NOT NULL,
                  Details VARCHAR(255),
                  Status VARCHAR(255) NOT NULL, 
                  Deadline DATE,
                  Completed DATE,
                  Project VARCHAR(255)        
                  )
        """

    )


def check_null(items):
    """

    :param items: table data (in lists)
    :return: change empty positions in db to NONE (NULL)
    """
    for index, item in enumerate(items):
        if item.strip() == '':
            items[index] = None


def fill_tables(conn):
    """

    :param conn: connection to db
    :return: filled tables from csv data

    """

    cursor = conn.cursor()
    with open('project.csv', 'r') as projects_data:
        # read csv as dict and take necessary data using dict keys(db col names)
        projects = csv.DictReader(projects_data)

        project_values = [[project['Name'], project['Description'], project['Deadline']] for project in projects]

        for project_items in project_values:
            # check nulls
            check_null(project_items)
            # query for fill tables
            cursor.execute('INSERT INTO Project (Name,Description,Deadline) VALUES (?, ?, ?)', project_items)
            conn.commit()

    with open('tasks.csv', 'r') as tasks_data:
        tasks = csv.DictReader(tasks_data)

        tasks_values = [[task['ID'], task['Priority'],
                         task['Details'], task['Status'], task['Deadline'], task['Completed'],
                         task['Project']] for task in tasks]

        for task_items in tasks_values:
            check_null(task_items)
            cursor.execute('INSERT INTO Tasks (ID,Priority,Details,Status,Deadline,Completed,Project)'' '
                           'VALUES (?, ?, ?, ?, ?, ?,?)', task_items)
            conn.commit()


def execute_query(conn):
    """

    :param conn: connection to db
    :return: result of query execution
    """
    cursor = conn.cursor()
    # need it for use project wth 2 or more words using argparse
    arg_str = ' '.join(args.project)
    try:
        cursor.execute("SELECT * FROM Tasks WHERE Project = " + arg_str)
    except:
        pass
    result = cursor.fetchall()
    conn.close()
    return result


if __name__ == "__main__":
    name = "task_management.db"
    if_db_exists(name)
    conn = sqlite3.connect(name)
    create_tables(conn)
    fill_tables(conn)
    print(execute_query(conn))
