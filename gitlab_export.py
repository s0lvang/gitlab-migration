import json
import subprocess as s

from urllib.parse import quote_plus

#A script to make exportfiles.

private_token="" #fill in your private_token, from  curl --request POST "https://gitlab.example.com/api/v4/session?login=john_smith&password=strongpassw0rd"

host= ""  #fill in the hostname of your gitlab-server

def main():
    #getting all groups
    groups = json.loads(s.check_output('curl -k -s '+ host +'/api/v4/groups --header "PRIVATE-TOKEN: ' + private_token + '"', shell=True).decode('UTF-8'))
    #getting all users
    users=json.loads(s.check_output('curl -k -s "' + host + '/api/v4/users" --header "PRIVATE-TOKEN: '+ private_token + '"', shell=True).decode("utf-8"))
    print(users)

    for user in users:
        createUser(user["username"])


    for group in groups:
        createGroup(group["id"])







def createGroup(id):
    #getting all projects in group.
    projects=json.loads(s.check_output('curl -k -s '+ host +'/api/v4/groups/'+ str(id) +'/projects --header "PRIVATE-TOKEN: ' + private_token + '"', shell=True).decode('UTF-8'))

    for project in projects:
        exportProject(project["web_url"])


def createUser(name):

    #getting all the projects
    projects=json.loads(s.check_output('curl -k -s '+ host +'/api/v4/projects?search='+ name + ' --header "PRIVATE-TOKEN: ' + private_token + '"', shell=True).decode('UTF-8'))

    for project in projects:
        exportProject(project["web_url"])





def exportProject(url):
    #getting the rails authorizationtoken
    authTok = s.check_output('curl -k -s ' + url +  '/edit --header "PRIVATE-TOKEN: '+ private_token + '  " --cookie-jar cookie  | grep csrf-token', shell=True).decode("UTF-8")

    #making it url-friendly
    url_authTok = quote_plus(authTok[33:121])

    #curl-expression for exporting. this was harder than you think.
    final_url='curl -k -v --http1.1 --referer '+ url + '/edit  --request POST --data "_method=post&authenticity_token='+ url_authTok +'" "' + url+'/export" --header "PRIVATE-TOKEN: ' + private_token +'" --cookie cookie'

    s.check_output(final_url, shell=True)






main()





