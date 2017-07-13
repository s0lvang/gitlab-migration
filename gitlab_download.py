import json
import subprocess as s
from urllib.parse import quote_plus
import os
#this script downloads all the project and places them in two directories.
#groups and users.


private_token=""  #fill in your private_token, from  curl --request POST "https://gitlab.example.com/api/v4/session?login=john_smith&password=strongpassw0rd"

host= ""   #fill in the hostname of your gitlab-server

def main():
    #creating directory
    os.mkdir("users")
    os.chdir("users")

    #getting the groups
    groups = json.loads(s.check_output('curl -k -s '+ host +'/api/v4/groups --header "PRIVATE-TOKEN: ' + private_token + '"', shell=True).decode('UTF-8'))

    #get the users
    users=json.loads(s.check_output('curl -k -s "' + host + '/api/v4/users" --header "PRIVATE-TOKEN: '+ private_token + '"', shell=True).decode("utf-8"))


    for user in users:
        createUser(user["username"])
        os.chdir("../")
    #creating directory

    os.mkdir("../groups")
    os.chdir('../groups')


    for group in groups:
        createGroup(group["id"], group["name"])
        os.chdir("../")





def createGroup(id, name):
    os.mkdir(name)
    os.chdir(name)
    #getting all the project urls and names
    projects=json.loads(s.check_output('curl -k -s '+ host +'/api/v4/groups/'+ str(id) +'/projects --header "PRIVATE-TOKEN: ' + private_token + '"', shell=True).decode('UTF-8'))
    for project in projects:
        downloadProject(project["web_url"], project["name"])



def createUser(name):
    os.mkdir(name)
    os.chdir(name)

    #getting all the project urls and names
    projects=json.loads(s.check_output('curl -k -s '+ host +'/api/v4/projects?search='+ name + ' --header "PRIVATE-TOKEN: ' + private_token + '"', shell=True).decode('UTF-8'))

    for project in projects:
        downloadProject(project["web_url"], project["name"])


def downloadProject(url, name):
    #simple get-request to download the files.
    print(s.check_output('curl -k -v -o '+ name+'.tar.gz '+ url +  '/download_export --header "PRIVATE-TOKEN: '+ private_token + '"' , shell=True))





main()





