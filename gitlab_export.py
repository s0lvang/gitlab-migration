import json 
import subprocess as s

from urllib.parse import quote_plus



private_token="hb9naBDbrCi26ZdsFnt4" #fill in your private_token, from  curl --request POST "https://gitlab.example.com/api/v4/session?login=john_smith&password=strongpassw0rd"

host= "https://git.itpartner.no"  #fill in the hostname of your gitlab-server

def main():
    groups = json.loads(s.check_output('curl -k -s '+ host +'/api/v4/groups --header "PRIVATE-TOKEN: ' + private_token + '"', shell=True).decode('UTF-8'))
    
    for group in groups:
        createGroup(group["id"])
        




def createGroup(id):
    projects=json.loads(s.check_output('curl -k -s '+ host +'/api/v4/groups/'+ str(id) +'/projects --header "PRIVATE-TOKEN: ' + private_token + '"', shell=True).decode('UTF-8'))
    for project in projects:
        exportProject(project["web_url"])
        print("imbreaking")
        raise OSError



def exportProject(url):
    
    authTok = s.check_output('curl -k -s ' + url +  '/edit --header "PRIVATE-TOKEN: '+ private_token + '  " --cookie-jar cookie  | grep csrf-token', shell=True).decode("UTF-8")
    
    url_authTok = quote_plus(authTok[33:121])
    
    final_url='curl -k -v --http1.1 --referer '+ url + '/edit  --request POST --data "_method=post&authenticity_token='+ url_authTok +'" "' + url+'/export" --header "PRIVATE-TOKEN: ' + private_token +'" --cookie cookie'
    
    s.check_output(final_url, shell=True)






main()
    

    
    

