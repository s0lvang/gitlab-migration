import os
import subprocess as s
import json
from urllib.parse import quote
#A script for importing private projects.
#Please make sure all of the users has created an account on the new server.
#You could possibly create all the users yourself through your own script

private_token=""  #fill in your private_token, from  curl --request POST "https://gitlab.example.com/api/v4/session?login=john_smith&password=strongpassw0rd"

host= ""   #fill in the hostname of your gitlab-server


groups=os.listdir()

def main():
    for group in groups:
        findUser(group)
        os.chdir("../")



def findUser(name):


    print(name)
    #getting the namespaceid of the user.
    namespaceidcall=s.check_output('curl -k -s --header "PRIVATE-TOKEN: ' +
                                   private_token + '" "'+ host +
                                   '/api/v4/namespaces?search='+name+'"'
                                   , shell=True).decode("utf-8")
    #getting the userid. THERE IS WAY TO MANY IDs IN GITLAB!!
    useridcall=s.check_output('curl -k -s --header "PRIVATE-TOKEN: ' +
                              private_token + '" "'+ host +
                              '/api/v4/users/?search='+name+'"',
                              shell=True).decode("utf-8")


    namespaceid=json.loads(namespaceidcall)[0]["id"]
    userid=json.loads(useridcall)[0]["id"]

    os.chdir(name)
    projects=os.listdir()
    for project in projects:
        importProject(project, namespaceid, userid)

def importProject(project, namespaceid, userid):
    #curl expressions for importing. You could do these with urllib
    authTok = s.check_output('curl -k -s "' + host +
            '/import/gitlab_project/new?namespace_id='+str(namespaceid)+
            '&path='+project[:len(project)-7]+'" --header "PRIVATE-TOKEN: '+
            private_token + '" --cookie-jar ../../cookie  | grep csrf-token'
            , shell=True).decode("UTF-8")[33:121]

    call='curl -k -v --http1.1  --request POST -F "authenticity_token=' + authTok +'" -F "utf-8=✓" -F "namespace_id='+str(namespaceid)+ '" -F "file=@'+ project + '" -F "path='+project[:len(project)-7]+ '" "' + host + '/import/gitlab_project" --header ' '"PRIVATE-TOKEN: '+ private_token +'" --cookie ../../cookie'

    print(s.check_output(call, shell=True))


    projectidCall=s.check_output('curl -k -s --header "PRIVATE-TOKEN: ' +
                                 private_token + '" "'+ host
                                 +'/api/v4/projects/'
                                 '?search='+project[:len(project)-7]+'"'
                                 , shell=True).decode("utf-8")

    #getting the id of your newly imported project.
    projectid=json.loads(projectidCall)[0]["id"]

    #giving the user acsess to his own private project. makes sense right?
    s.check_output('curl -k -s -X POST --data "user_id='+str(userid)+
                   '&access_level=40" "'+host+'/api/v4/projects/'+str(projectid)+
                   '/members" --header "PRIVATE-TOKEN: ' + private_token + '"'
                   , shell=True)





main()









