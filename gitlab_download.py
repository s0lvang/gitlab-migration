import json 
import subprocess as s
from urllib.parse import quote_plus
import os


private_token="hb9naBDbrCi26ZdsFnt4"
host= "https://git.itpartner.no"

def main():
    os.mkdir(host[8:])
    os.chdir(host[8:])
    groups = json.loads(s.check_output('curl -k -s '+ host +'/api/v4/groups --header "PRIVATE-TOKEN: ' + private_token + '"', shell=True).decode('UTF-8'))
    
    for group in groups:
        createGroup(group["id"], group["name"])
        os.chdir("../")
        




def createGroup(id, name):
    os.mkdir(name)
    os.chdir(name)
    projects=json.loads(s.check_output('curl -k -s '+ host +'/api/v4/groups/'+ str(id) +'/projects --header "PRIVATE-TOKEN: ' + private_token + '"', shell=True).decode('UTF-8'))
    for project in projects:
        downloadProject(project["web_url"], project["name"])
        print("imbreaking")
        raise OSError



def downloadProject(url, name):
    
    print(s.check_output('curl -k -v -o '+ name+'.tar.gz '+ url +  '/download_export --header "PRIVATE-TOKEN: '+ private_token + '"' , shell=True))
    
    



main()
    

    
    

