import json 
import subprocess as s
from urllib.parse import quote_plus



private_token="hb9naBDbrCi26ZdsFnt4"
host= "https://git.itpartner.no"

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


   # curl -k -v --http1.1 --referer http://git.itpartner.no/august/Test-import/edit  --request POST --data "_method=post&authenticity_token=p2fNhmB3MOAL5ElODuj%2fZ57NRHuC2DJ8hl0bC5CJ7KX5hR3ybS5nJzKDo5mrFu9ENrZX97f6YhRx45aOoQTzMw%3d%3d" "https://git.itpartner.no/august/Test-import/export" --header "PRIVATE-TOKEN: hb9naBDbrCi26ZdsFnt4" --cookie cookie

   #curl -k -v --http1.1 --referer https://git.itpartner.no/aeco/Cruisedatabase/edit  --request POST --data "_method=post&authenticity_token=cY1BWRuSpMSmcJnoYzb1AW45rGVpnqmx0IagjIdE2bRAAiKs0PY5EpRY0TL6n%2F0JgzKt9r0h9nkg6Nm5B3e4ZA%3D%3D " "https://git.itpartner.no/aeco/Cruisedatabase/export " --header "PRIVATE-TOKEN: hb9naBDbrCi26ZdsFnt4" --cookie cookie




main()
    

    
    

