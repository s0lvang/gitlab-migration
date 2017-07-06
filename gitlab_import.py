import os
import subprocess as s
import json
from urllib.parse import quote_plus
from urllib.parse import quote
import time

idmapping={1:1,2:3,3:6,4:4,5:8,7:7,10:5,13:9}

private_token="iMhPXXD9mjBA7ufKzgVg"  #fill in your private_token, from  curl --request POST "https://gitlab.example.com/api/v4/session?login=john_smith&password=strongpassw0rd"

host= "http://git01"   #fill in the hostname of your gitlab-server

host2="https://git.itpartner.no"
private_token2="YS1qmjy9KC7k9YanUiPs"


groups=os.listdir()

def main():
    for group in groups:
        createGroup(group)
        os.chdir("../")
        


def createGroup(group):
    
    pathgroup=group.replace(" ", "")
    
    print(group)
    
    
    
    stuff=s.check_output('curl -k -s --request POST "' + 
    host + '/api/v4/groups?'+'name='+ pathgroup +
    '&path=' + pathgroup +'&visibility=internal" --header ' 
    '"PRIVATE-TOKEN: '+ private_token+'"', shell=True).decode("utf-8")
    
    
    stuff=s.check_output('curl -s --header '
    '"PRIVATE-TOKEN: ' + private_token + '" "'+ 
    host +'/api/v4/namespaces?search='+pathgroup+'"'
    , shell=True).decode("utf-8")


    print("\n\n\n"+stuff)
    namespaceid=json.loads(stuff)[0]["id"]

    

    os.chdir(group)
    projects=os.listdir()
    for project in projects:
        importProject(project, namespaceid)
        
        

def importProject(project, namespaceid):



    authTok = s.check_output('curl -k -s "' + host +  
    '/import/gitlab_project/new?namespace_id='+str(namespaceid)+
    '&path='+project[:len(project)-7]+'" --header "PRIVATE-TOKEN: '+ private_token + 
    '" --cookie-jar ../../cookie  | grep csrf-token', shell=True).decode("UTF-8")[33:121]
    
    call=('curl -k -v --http1.1  --request POST -F "authenticity_token=' + authTok +
    '" -F "utf-8=✓" -F "namespace_id='+str(namespaceid)+
    '" -F "file=@'+ project + 
    '" -F "path='+project[:len(project)-7]+
    '" "' + host + '/import/gitlab_project" --header "PRIVATE-TOKEN: '+ 
    private_token +'" --cookie ../../cookie')



    #print(call)

    print(s.check_output(call, shell=True))
    
    projectidCall=s.check_output('curl -k -s --header "PRIVATE-TOKEN: ' + 
    private_token + '" "'+ host +
    '/api/v4/projects/?search='+
    project[:len(project)-7]+'"', shell=True).decode("utf-8")
    
    
    #print(projectidCall)
    projectid=json.loads(projectidCall)[0]["id"]

    projectidCall2=s.check_output('curl -k -s --header "PRIVATE-TOKEN: ' + 
    private_token2 + '" "'+ 
    host2 +'/api/v4/projects/?search='
    +project[:len(project)-7]+'"', shell=True).decode("utf-8")


    
    
    
    
    print(projectidCall2)
    projectid2=json.loads(projectidCall2)[0]["id"]
    namespaceid2=json.loads(projectidCall2)[0]["namespace"]["path"]
    
    



    s.check_output('curl -k -s --request PUT --header ' 
    '"PRIVATE-TOKEN: '+ private_token+
    '" --data "visibility=internal" "'+
    host+'/api/v4/projects/'+str(projectid)+'"'
    ,shell=True)




    
    groupmembers=(json.loads(s.check_output('curl -k -s --header ' 
    '"PRIVATE-TOKEN: '+ private_token2+'" "'+
    host2+'/api/v4/groups/'+str(namespaceid2)+'/members"'
    ,shell=True).decode("utf-8")))
    
    print(groupmembers)

    members=json.loads(s.check_output('curl -k -s --header ' 
    '"PRIVATE-TOKEN: '+ private_token2+'" "'+
    host2+'/api/v4/projects/'+str(projectid2)+'/members"'
    ,shell=True).decode("utf-8"))
    print(members) 


    
    members= members + groupmembers if isinstance(groupmembers, list) else members 
    


    #print('curl -k -s --header ' 
    #'"PRIVATE-TOKEN: '+ private_token2+'" "'+
    #host2+'/api/v4/projects/'+str(projectid2)+'/members"')
    
    print(members)



    for mem in members:
        
        print(mem)
        ids=mem.get("id",1) 
          
    
        s.check_output('curl -k -s -X POST --data "user_id='+str(idmapping.get(ids,1))+'&access_level=40"  --header "PRIVATE-TOKEN: '+ private_token+'" "'+host+'/api/v4/projects/'+str(projectid)+'/members"', shell=True)

    if(isinstance(groupmembers, list)):

        for gmem in groupmembers:
            ids=gmem.get("id",1)
            s.check_output('curl -k -s -X POST --data "user_id='+str(idmapping.get(ids,1))+'&access_level=50"  --header "PRIVATE-TOKEN: '+ private_token+'" "'+host+'/api/v4/groups/'+str(namespaceid2)+'/members"', shell=True)

    
    importIssues(projectid, projectid2)
    

def importIssues(pid, pid2):
    issues = json.loads(s.check_output('curl -k -s '+ host2 +'/api/v4/projects/'+str(pid2)+'/issues?per_page=100 --header "PRIVATE-TOKEN: ' + private_token2 + '"', shell=True).decode('UTF-8')

    )
    for issue in issues:
        assignees=issue.get('assignee',{})
        
        print(assignees)

        if (assignees):
            ids=assignees.get("id",1)
            s.check_output('curl --request PUT --header "PRIVATE-TOKEN: ' + private_token+'" "'+
            host + '/api/v4/projects/'+str(pid)+'/issues/'+str(issue["iid"])+'?assignee_ids='+str(idmapping.get(ids,1))+'"',  shell=True)
            
                 
        




    


createGroup("Leroy")





   





