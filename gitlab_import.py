import os
import subprocess as s
import json
from urllib.parse import quote_plus
from urllib.parse import quote

idmapping= {1:1,2:9,3:6,4:8,5:4,7:5,10:7,13:3,11:11}
#Map old userids to the new ones, this has to be done manually. sorry..
#You can find member-IDs through an API-call

#####NEW HOST######

private_token= ""
#fill in your private_token, from  curl --request POST
#"https://gitlab.example.com/api/v4/session?login=john_smith&password=strongpassw0rd"

host=""    #fill in the hostname of your gitlab-server



#####OLD HOST######
host2= ""

private_token2= ""



groups= os.listdir()

def main():
    for group in groups:
        createGroup(group)
        os.chdir("../")



def createGroup(group):

    pathgroup=group.replace(" ", "") #removing spaces so the path is correct.
    #please remove any special characters from the names of your repository.

    print(group)


    s.check_output('curl -k -s --request POST "' +
                host + '/api/v4/groups?'+'name='+ pathgroup +
                    '&path=' + pathgroup +'&visibility=internal" --header '
                        '"PRIVATE-TOKEN: '+ private_token+'"',
                        shell=True).decode("utf-8")  ##creating a new group




    # a call to gitlabs namespace-api
    stuff=s.check_output('curl -s --header '
                         '"PRIVATE-TOKEN: ' + private_token + '" "'+
                         host +'/api/v4/namespaces?search='+pathgroup+'"'
                         , shell=True).decode("utf-8")

    print(stuff)

    namespaceid= json.loads(stuff)[0]["id"]

    os.chdir(group)
    projects=os.listdir()
    #looping through the tar.gz exports. make sure the path does not contain
    #any special characters


    for project in projects:
        importProject(project, namespaceid)
        addMembers(project)



def importProject(project, namespaceid):

    #This is the curl requests for importing to gitlab. it's quite ugly.

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


    print(s.check_output(call, shell=True))





def addMembers(project):
    #getting the ID of the imported project
    projectid=json.loads(s.check_output('curl -k -s --header "PRIVATE-TOKEN: ' +
    private_token + '" "'+ host +
    '/api/v4/projects/?search='+
    project[:len(project)-7]+'"', shell=True).decode("utf-8"))[0]["id"]


    #requesting the ID of the old project
    project=json.loads(s.check_output('curl -k -s --header "PRIVATE-TOKEN: ' +
    private_token2 + '" "'+
    host2 +'/api/v4/projects/?search='
    +project[:len(project)-7]+'"', shell=True).decode("utf-8"))

    projectid2=project[0]["id"]
    namespaceid2=project[0]["namespace"]["path"]

    #sets the project visibility to internal
    s.check_output('curl -k -s -X PUT --header "PRIVATE-TOKEN: '+ private_token+'" --data "visibility=internal" "'+host+'/api/v4/projects/'+str(projectid)+'"',shell=True)

    #requesting members of the group
    groupmembers=(json.loads(s.check_output('curl -k -s --header '
    '"PRIVATE-TOKEN: '+ private_token2+'" "'+
    host2+'/api/v4/groups/'+str(namespaceid2)+'/members"'
    ,shell=True).decode("utf-8")))

    #requesting the members of the project
    members=json.loads(s.check_output('curl -k -s --header '
    '"PRIVATE-TOKEN: '+ private_token2+'" "'+
    host2+'/api/v4/projects/'+str(projectid2)+'/members"'
    ,shell=True).decode("utf-8"))


    for mem in members:
        #USER-id
        ids=mem.get("id",1)

        #Member is added as master in the new project.
        s.check_output('curl -k -s -X POST --data '
                '"user_id='+str(idmapping.get(ids,1))+'&access_level=40"'
                ' --header "PRIVATE-TOKEN: '+ private_token+'"'
                ' "'+host+'/api/v4/projects/'+str(projectid)+'/members"'
                , shell=True)

    # an if-sentence to prevent a crash
    if(isinstance(groupmembers, list)):


        #adding the groupmembers as owner of the new group
        for gmem in groupmembers:
            ids = gmem.get("id", 1)
            s.check_output('curl -k -s -X POST --data "user_id='+str(idmapping.get(ids,1))+'&access_level=50"  --header "PRIVATE-TOKEN: '+ private_token+'" "'+host+'/api/v4/groups/'+str(namespaceid2)+'/members"', shell=True)


    importIssues(projectid, projectid2)


def importIssues(pid, pid2):

    #getting all the issues of one project. if you have more than a hundred
    #issues i feel sorry for you.
    issues = json.loads(s.check_output('curl -k -s '+ host2 +
        '/api/v4/projects/'+str(pid2)+'/issues?per_page=100 --header '
        '"PRIVATE-TOKEN: ' + private_token2 + '"', shell=True).decode('UTF-8'))


    for issue in issues:
        assignees=issue.get('assignee',{})

        #assigning the issues to the new users.
        if (assignees):
            ids=assignees.get("id",1)
            s.check_output('curl --request PUT --header "PRIVATE-TOKEN: ' + private_token+'" "'+
            host + '/api/v4/projects/'+str(pid)+'/issues/'+str(issue["iid"])+'?assignee_ids='+str(idmapping.get(ids,1))+'"',  shell=True)









main()











