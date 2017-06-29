import os
import subprocess as s
import json
from urllib.parse import quote


private_token="iMhPXXD9mjBA7ufKzgVg"  #fill in your private_token, from  curl --request POST "https://gitlab.example.com/api/v4/session?login=john_smith&password=strongpassw0rd"

host= "http://git01"   #fill in the hostname of your gitlab-server



groups=os.listdir()

def main():
    for group in groups:
        createGroup(group)
        os.chdir("../")
        


def createGroup(group):
    
    pathgroup=group.replace(" ", "")
    
    stuff=s.check_output('curl -k -s --request POST "' + host + '/api/v4/groups?'+'name='+pathgroup +'&path=' + pathgroup +'" --header "PRIVATE-TOKEN: '+ private_token+'"',shell=True).decode("utf-8")

    print(stuff)
    namespaceid=json.loads(stuff)["id"]

    #print(json.loads(s.check_output('curl -k -s --header "PRIVATE-TOKEN: ' + private_token + '" "'+ host +'/api/v4/namespaces?search='+group+'"', shell=True).decode("utf-8")))["id"]

    os.chdir(group)
    projects=os.listdir()
    for project in projects:
        importProject(project, namespaceid)

def importProject(project, namespaceid):

    authTok = s.check_output('curl -k -s "' + host +  '/import/gitlab_project/new?namespace_id='+str(namespaceid)+'&path='+project[:len(project)-7]+'" --header "PRIVATE-TOKEN: '+ private_token + '  " --cookie-jar ../../cookie  | grep csrf-token', shell=True).decode("UTF-8")[33:121]
    
    call='curl -k -v --http1.1  --request POST -F "authenticity_token=' + authTok +'" -F "utf-8=✓" -F "namespace_id='+str(namespaceid)+'" -F "file=@'+ project + '" -F "path='+project[:len(project)-7]+'" "' + host + '/import/gitlab_project" --header "PRIVATE-TOKEN: '+ private_token +'" --cookie ../../cookie'

    print('\n\n'+call+'\n\n')
    print(os.listdir())


    print(s.check_output(call, shell=True))


main()





#curl -k -v --http1.1 --request POST \
#-F "authenticity_token=emhinn2/rMURBlZstCCq/9Bk9Rtd+IRJex+YFFGB6gUgdBV6F7Z57Ns0WsVGJYe7n0PjHLpa#+qLmRmLmuwgdtg==" \
#-F "namespace_id=2" -F "path=Det-er-mulig-aa-importere-til-andre-brukere" \
#-F "utf-8=✓" -F "file=@testimport.tar.gz" \
#"https://git.itpartner.no/import/gitlab_project" \
#--header "PRIVATE-TOKEN: YS1qmjy9KC7k9YanUiPs" --cookie cookie

#curl -k -v --http1.1  --request POST -F "authenticity_token=CeUiH371O3VEKJnIUIjzWcQITyQJFJqY2IdhGutbp00TAIOUK+cAU3ZcHHrkVnLpB0ABBwevLUqJmPcexX8VVQ==" -F "utf-8=✓" -F "namespace_id=21" -F "file=SvalbardReiselivStatistikk.tar.gz" -F "path=SvalbardReiselivStatistikk" "http://git01/import/gitlab_project" --header "PRIVATE-TOKEN: iMhPXXD9mjBA7ufKzgVg" --cookie ../../cookie







