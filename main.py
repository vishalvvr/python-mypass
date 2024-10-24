from cryptography.fernet import Fernet
import argparse
from typing import List, Dict
import os
from pathlib import Path
import tiny_db
import base64
import datetime
import configparser
import pprint

HOME_DIR = os.path.expanduser('~')
CONFIG_FILE = os.path.join(HOME_DIR,"mypass.ini")

def encrypt_password(key, password):
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()

def decrypt_password(key, encrypted_password):
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()

def config_init():
    config = configparser.ConfigParser()
    # if config file doesnot exist then create one and add newly generated key to it
    if not os.path.exists(CONFIG_FILE): 
        key = Fernet.generate_key()
        # Encode the key using base64
        encoded_key = base64.urlsafe_b64encode(key).decode()
        config['mypass'] = {'key': encoded_key}
        # Write the configuration to a file
        with open(CONFIG_FILE, 'w') as conf_obj:
            config.write(conf_obj)
            return key    
    # else check if env is, if not then read key from file and set MYPASS value
    else:
        config.read(CONFIG_FILE)
        # Retrieve the encoded key from the INI file
        encoded_key = config.get('mypass', 'key')
        return base64.urlsafe_b64decode(encoded_key)

def main():
    key = config_init()
    # print(key)
    # print(type(key))
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-a","--add", help="add password to mypass\n syntax: mypass -a '<service>::<username>::<password>'", type=str)
    group.add_argument("-g","--get", help="display your password\n syntax: mypass -g <service>", type=str)
    group.add_argument("-l","--all", help="display all your services \n syntax: mypass --all", action='store_true')
    group.add_argument("-d","--delete", help="delete a service record\n syntax: mypass -d <service>", type=str)
    group.add_argument("-D","--delete-all", help="delete all your services \n syntax: mypass -D", action='store_true')
    group.add_argument("-s","--sync", help="sync your local db with git \n syntax: mypass --sync", action='store_true')
    args = parser.parse_args()
    
    # add new service to mypass
    if args.add:
        ip_data_list = args.add.split("::")
        if len(ip_data_list) == 3:
            data = {
                "service": ip_data_list[0],
                "username": ip_data_list[1],
                "password": encrypt_password(key=key, password=ip_data_list[2])
            }
        else:
            data = {
                "service": ip_data_list[0],
                "username": None,
                "password": encrypt_password(key=key, password=ip_data_list[1])
        }
        data['created_at'] = str(datetime.datetime.now())
        data['updated_at'] = None
        data['is_active'] = True
        tiny_db.add_service(data_dict=data)

    # retrive a service 
    elif args.get:
        output = tiny_db.get_a_service(args.get)
        for index in range(len(output)):
            output[index]['password'] = decrypt_password(key=key, encrypted_password=output[index]['password'])
        pprint.pprint(output)

    # retrive all the service names
    elif args.all:
        output = tiny_db.get_all_service()
        if output:
            print("-------------\nservice-names\n-------------")
            for out in output:
                print(out['service'])
            print("-------------")
        else:
            print("No data")
    
    # delete a service    
    elif args.delete:
        tiny_db.remove_a_service(service_name=args.delete)
    
    # delete all services
    elif args.delete_all:
        tiny_db.remove_all_service()

if __name__ == "__main__":
    # print(generate_key())
    main()