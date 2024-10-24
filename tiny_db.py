from tinydb import Query, TinyDB

def add_service(data_dict):
    db = TinyDB('mypass.json')
    db.insert(data_dict)

def get_a_service(serivce_name):
    db = TinyDB('mypass.json')
    q = Query()
    return db.search((q.service == serivce_name) & (q.is_active == True))

def get_all_service():
    db = TinyDB('mypass.json')
    # return db.all()
    return db.search(Query().is_active == True)

def update_a_service(service_name, data_dict):
    db = TinyDB('mypass.json')
    db.update(data_dict, (Query().service == service_name) & (Query().is_active == True))

def remove_a_service(service_name):
    db = TinyDB('mypass.json')
    # db.remove(Query().service == service_name)
    db.update({"is_active": False}, Query().service == service_name)

def remove_all_service():
    db = TinyDB('mypass.json')
    db.truncate()

if __name__ == "__main__":
    remove_a_service("gmail2")
    pass