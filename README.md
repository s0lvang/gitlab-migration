#Gitlab-Migration


This repository contains 5 scripts to import all your projects from one private
gitlab-server to another. It might be handy if you're hosting gitlab at
githost.io or some other service with no terminal access.

An admin user to both gitlab servers is required.

###HOW TO

1. Clone this repository
2. Edit all the files with your private-token and the url of your host.
3. Run gitlab/_export.py, and wait until its finished.
   you might want to wait a little longer because it takes some time for gitlab
   to generate all the exports.
4. run gitlab\_download.py
5. Create all of the users at your new gitlab server. NB! Its important that
   all users have the same username as they had on your old server.
6. *cd users/*  run gitlab\_import\_private.py it imports all of the personal projects to your
   new server.
7. Edit the idmapping dictionary in gitlab\_import.py, the old userids must
   correspond with the new ones.
8. *cd groups/* run gitlab\_import.py NB! its important that the directories in
   groups\ does not contain any special characters.
9. If everything went well you should have all your groups and projects
   imported. With issues as well.
10. If things did not work out for you. run gitlab\_delete.py and try again.



###Things i'm sorry for :(

1. Unreadable code (the curl-expressions got out of hand) you can try with
   urllib
2. Inneffective code. There's so many calls to the gitlab-api that i got lost.
3. Breaking your heart.
