import json
import subprocess as s
from urllib.parse import quote_plus
import os
import time

#A script for deleting all your groups and projects. just in case something goes
#wrong during import

private_token=""  #fill in your private_token, from  curl --request POST "https://gitlab.example.com/api/v4/session?login=john_smith&password=strongpassw0rd"

host= ""

def main():
    input("Are you sure?")
    input("Are you really sure?")
    input("Are you really really sure?")
    input("Are you really really really sure?")
    print("you fucked up")

    time.sleep(1)



    print("I HAVE BECOME DEATH, DESTROYER OF WORLDS!")

    time.sleep(1)
    #getting all the groups through an api-call
    groups = json.loads(s.check_output('curl -k -s '+ host +'/api/v4/groups --header "PRIVATE-TOKEN: ' + private_token + '"', shell=True).decode('UTF-8'))
    #getting all of the users through an api-call
    users=json.loads(s.check_output('curl -k -s "' + host + '/api/v4/users" --header "PRIVATE-TOKEN: '+ private_token + '"', shell=True).decode("utf-8"))

    #loop loop looping through
    for user in users:
        deleteUserprojects(user["username"])



    for group in groups:
        deleteGroup(group["id"], group["name"])






def deleteGroup(id, name):
    #api-call to get all projects in the group
    projects=json.loads(s.check_output('curl -k -s '+ host +'/api/v4/groups/'+ str(id) +'/projects --header "PRIVATE-TOKEN: ' + private_token + '"', shell=True).decode('UTF-8'))
    for project in projects:
        deleteProject(project["id"])

    #deleting the group.
    print(s.check_output('curl -k -v -X DELETE '+ host +  '/api/v4/groups/'+str(id)+' --header "PRIVATE-TOKEN: '+ private_token + '"' , shell=True))




def deleteUserprojects(name):
    #getting all the private projects.
    projects=json.loads(s.check_output('curl -k -s '+ host +'/api/v4/projects?search='+ name + ' --header "PRIVATE-TOKEN: ' + private_token + '"', shell=True).decode('UTF-8'))
    for project in projects:
        deleteProject(project["id"])


def deleteProject(id):
    #api-call for deleting projects.
    print(s.check_output('curl -k -v -X DELETE '+ host +  '/api/v4/projects/'+str(id)+' --header "PRIVATE-TOKEN: '+ private_token + '"' , shell=True))





main()





