import os
import subprocess as s
import json
from urllib.parse import quote


private_token="iMhPXXD9mjBA7ufKzgVg"  #fill in your private_token, from  curl --request POST "https://gitlab.example.com/api/v4/session?login=john_smith&password=strongpassw0rd"

host= "http://git01"   #fill in the hostname of your gitlab-server



groups=os.listdir()

def main():
    for group in groups:
        createUser(group)
        os.chdir("../")
        


def createUser(name):
    
   
    print(name)
    
    namespaceidcall=s.check_output('curl -k -s --header "PRIVATE-TOKEN: ' + private_token + '" "'+ host +'/api/v4/namespaces?search='+name+'"', shell=True).decode("utf-8")

    useridcall=s.check_output('curl -k -s --header "PRIVATE-TOKEN: ' + private_token + '" "'+ host +'/api/v4/users/?search='+name+'"', shell=True).decode("utf-8")

    print(useridcall)
    print('curl -k -s --header "PRIVATE-TOKEN: ' + private_token + '" "'+ host +'/api/v4/users/'+name+'"')
    
    namespaceid=json.loads(namespaceidcall)[0]["id"]
    userid=json.loads(useridcall)[0]["id"]

    os.chdir(name)
    projects=os.listdir()
    for project in projects:
        importProject(project, namespaceid, userid)

def importProject(project, namespaceid, userid):

    authTok = s.check_output('curl -k -s "' + host +  '/import/gitlab_project/new?namespace_id='+str(namespaceid)+'&path='+project[:len(project)-7]+'" --header "PRIVATE-TOKEN: '+ private_token + '" --cookie-jar ../../cookie  | grep csrf-token', shell=True).decode("UTF-8")[33:121]
    
    call='curl -k -v --http1.1  --request POST -F "authenticity_token=' + authTok +'" -F "utf-8=✓" -F "namespace_id='+str(namespaceid)+'" -F "file=@'+ project + '" -F "path='+project[:len(project)-7]+'" "' + host + '/import/gitlab_project" --header "PRIVATE-TOKEN: '+ private_token +'" --cookie ../../cookie'

    print(s.check_output(call, shell=True))

    print('curl -k -s --header "PRIVATE-TOKEN: ' + private_token + '" "'+ host +'/api/v4/users/?search='+project[:len(project)-7]+'"')

    projectidCall=s.check_output('curl -k -s --header "PRIVATE-TOKEN: ' + private_token + '" "'+ host +'/api/v4/projects/?search='+project[:len(project)-7]+'"', shell=True).decode("utf-8")
    
    print(projectidCall)
    
    projectid=json.loads(projectidCall)[0]["id"]


    print('\n\n'+call+'\n\n')
    s.check_output('curl -k -s -X POST --data "user_id='+str(userid)+'&access_level=40" "http://git01/api/v4/projects/'+str(projectid)+'/members" --header "PRIVATE-TOKEN: ' + private_token + '"', shell=True)

    
    
    

main()





#curl -k -v --http1.1 --request POST \
#-F "authenticity_token=emhinn2/rMURBlZstCCq/9Bk9Rtd+IRJex+YFFGB6gUgdBV6F7Z57Ns0WsVGJYe7n0PjHLpa#+qLmRmLmuwgdtg==" \
#-F "namespace_id=2" -F "path=Det-er-mulig-aa-importere-til-andre-brukere" \
#-F "utf-8=✓" -F "file=@testimport.tar.gz" \
#"https://git.itpartner.no/import/gitlab_project" \
#--header "PRIVATE-TOKEN: YS1qmjy9KC7k9YanUiPs" --cookie cookie

#curl -k -v --http1.1  --request POST -F "authenticity_token=CeUiH371O3VEKJnIUIjzWcQITyQJFJqY2IdhGutbp00TAIOUK+cAU3ZcHHrkVnLpB0ABBwevLUqJmPcexX8VVQ==" -F "utf-8=✓" -F "namespace_id=21" -F "file=SvalbardReiselivStatistikk.tar.gz" -F "path=SvalbardReiselivStatistikk" "http://git01/import/gitlab_project" --header "PRIVATE-TOKEN: iMhPXXD9mjBA7ufKzgVg" --cookie ../../cookie






