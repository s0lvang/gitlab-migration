# curl -k -v --http1.1 --referer "https://git.itpartner.no/import/gitlab_project/new?namespace_id=31&path=Test-import"  --request POST -F "authenticity_token=R23lDHNHba7bDCF0Xfo6T79a0iCH7wTR4N3vNMiBRHY5pVyGI84JpOoLvUULXcoxm0gw7WnIZt02CDVKC6sF8g==" -F "utf8=true" -F "namespace_id=31" -F "file=Test-import2.tar.gz" "https://git.itpartner.no/august/import/gitlab_project" --header "PRIVATE-TOKEN: hb9naBDbrCi26ZdsFnt4" --cookie cookie
import os
import subprocess as s


private_token="hb9naBDbrCi26ZdsFnt4"  #fill in your private_token, from  curl --request POST "https://gitlab.example.com/api/v4/session?login=john_smith&password=strongpassw0rd"

host= "https://git.itpartner.no"   #fill in the hostname of your gitlab-server



groups=os.listdir("/home/august/Documents/itpartner/git.itpartner.no")

def main():
    for group in groups:
        createGroup(group)


def createGroup(group):
    s.check_output('curl -k -s  --request POST "' + host + '/api/v4/groups?name='+group+'&path='+ group+'" --header "PRIVATE-TOKEN: hb9naBDbrCi26ZdsFnt4"' )
    
    namespaceid=json.loads(s.checkoutput('curl -k -s --header "PRIVATE-TOKEN: 9koXpg98eAheJpvBs5tK" '+ host +' api/v4/namespaces?search='+group).decode("utf-8"))["id"]
    os.chdir(group)
    projects=os.listdir()
    for project in projects:
        importProject(project, namespaceid)

def importProject(project, namespaceid):

    authTok = s.check_output('curl -k -s "' + url +  '/import/gitlab_project/new?namespace_id='+str(namespaceid)+'&path='+project[:len(project)-7]+'" --header "PRIVATE-TOKEN: '+ private_token + '  " --cookie-jar cookie  | grep csrf-token', shell=True).decode("UTF-8")[33:121]
    
    s.check_output('curl -k -v --http1.1 --referer ' + url +  '/import/gitlab_project/new?namespace_id='+str(namespaceid)+'&path='+project[:len(project)-7] ' --request POST -F "authenticity_token=' +authTok+'" -F "utf8=true" -F "namespace_id="'+str(namespaceid)+' -F "file='+ project+ '"https://git.itpartner.no/august/import/gitlab_project" --header "PRIVATE-TOKEN: "'+private_token+' --cookie cookie')
















