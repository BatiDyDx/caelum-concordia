import json
import sys
import os 
#Abrimos el archivo JSON con la información de los usuarios
def getJSON(filePath):
    with open(filePath, 'r') as file:
        return json.load(file)

users_list = getJSON('./src/users.json')['users']

#Definimos un objeto llamado Users
class Users:
    def __init__(self, username, password):
        """
        :param username: str
        :param password: str
        :return: None
        """
        self.username = username
        self.password = password

    def __repr__(self):
        """
        Representacion visual del usuario
        :return: str
        """
        return f"<User:{self.username}, Password:{self.password}>"

#Para cada elemento en el archivo, instanciamos un objeto
users = []
for i in range(len(users_list)):
    users.append(Users(users_list[i]['username'], users_list[i]['password']))
