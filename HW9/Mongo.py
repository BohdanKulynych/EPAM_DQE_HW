import csv
from pymongo import MongoClient
from typing import List, Dict



def connect_mongo(db_name: str):
    """
    :param db_name: name of database
    :return: db object
    """
    client = MongoClient('localhost', 27017)
    db = client[db_name]
    if db_name in client.list_database_names():
        client.drop_database(db_name)
    return db


def get_data(csv_file: str) -> List:
    """
    :param csv_file: csv filename
    :return: list of dicts data
    """
    users_data: List = []
    with open(csv_file) as file:
        reader = csv.DictReader(file)
        for line in reader:
            users_data.append(line)
    return users_data


def insert_collection(db, collection_name: str, data: List):
    """
    :param db: db object
    :param collection_name: name of collection(table)
    :param data: data to insert
    :return: collection obj
    """

    collection = db[collection_name]
    collection.insert_many(data)
    return collection


def get_status(collection, status: str) -> Dict:
    """
    :param collection: collection obj
    :param status: status of project
    :return: project with selected status
    """
    return collection.find({'Status': status})


def main():

    db = connect_mongo('project_management')
    project_data = get_data('project.csv')
    tasks_data = get_data('tasks.csv')
    projects = insert_collection(db, 'project', project_data)
    tasks = insert_collection(db, 'tasks', tasks_data)
    result = get_status(tasks, 'canceled')
    for data in result:
        print(data)

main()
