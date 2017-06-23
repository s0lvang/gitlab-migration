import json
import subprocess as s



fromprivate_token="hb9naBDbrCi26ZdsFnt4"  #fill in your private_token, from  curl --request POST "https://gitlab.example.com/api/v4/session?login=john_smith&password=strongpassw0rd"

fromhost= "https://git.itpartner.no"   #fill in the hostname of your gitlab-server

toprivate_token="hb9naBDbrCi26ZdsFnt4"  #fill in your private_token, from  curl --request POST "https://gitlab.example.com/api/v4/session?login=john_smith&password=strongpassw0rd"

tohost= "https://git.itpartner.no"   #fill in the hostname of your gitlab-server

def main():
     users=json.loads(s.check_output('curl -k -s "' + fromhost + '/api/v4/users" --header "PRIVATE-TOKEN: '+ fromprivate_token + '"', shell=True).decode("utf-8"))
     for user in users:
        createUser(user)
        raise OSError

def createUser(user):
    print('curl -k -s --request POST --data "username=' +user["username"]+ '&reset_password=true&email='+user["email"]+'&name='+user["username"]+'&admin='+str(user["is_admin"])+'" "' + tohost +'/api/v4/users" --header "PRIVATE-TOKEN: '+ toprivate_token + '"' )
     
     


def addSSHkey():
     pass

 

main()