import json 
import subprocess as s
from urllib.parse import quote_plus
import os
import time



private_token="iMhPXXD9mjBA7ufKzgVg"  #fill in your private_token, from  curl --request POST "https://gitlab.example.com/api/v4/session?login=john_smith&password=strongpassw0rd"

host= "http://10.253.18.105"

def main():
    input("Are you sure?")
    input("Are you really sure?")
    input("Are you really really sure?")
    input("Are you really really really sure?")
    print("you fucked up")
    
    time.sleep(1)
    
    
    
    print("I HAVE BECOME DEATH, DESTROYER OF WORLDS!")
  
    time.sleep(1)

    groups = json.loads(s.check_output('curl -k -s '+ host +'/api/v4/groups --header "PRIVATE-TOKEN: ' + private_token + '"', shell=True).decode('UTF-8'))

    users=json.loads(s.check_output('curl -k -s "' + host + '/api/v4/users" --header "PRIVATE-TOKEN: '+ private_token + '"', shell=True).decode("utf-8"))
    
    
    for user in users:
        createUser(user["username"])
         
  
        
    for group in groups:
        createGroup(group["id"], group["name"])
    
        
    



def createGroup(id, name):

    projects=json.loads(s.check_output('curl -k -s '+ host +'/api/v4/groups/'+ str(id) +'/projects --header "PRIVATE-TOKEN: ' + private_token + '"', shell=True).decode('UTF-8'))
    for project in projects:
        downloadProject(project["id"])
        print("imbreaking")
    print(s.check_output('curl -k -v -X DELETE '+ host +  '/api/v4/groups/'+str(id)+' --header "PRIVATE-TOKEN: '+ private_token + '"' , shell=True))
    
    
      

def createUser(name):
    
    projects=json.loads(s.check_output('curl -k -s '+ host +'/api/v4/projects?search='+ name + ' --header "PRIVATE-TOKEN: ' + private_token + '"', shell=True).decode('UTF-8'))
    for project in projects:
        downloadProject(project["id"])


def downloadProject(id):
    
    print(s.check_output('curl -k -v -X DELETE '+ host +  '/api/v4/projects/'+str(id)+' --header "PRIVATE-TOKEN: '+ private_token + '"' , shell=True))
    
    



main()
    

    
    

