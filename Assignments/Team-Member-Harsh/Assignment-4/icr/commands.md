```
ibmcloud plugin install container-registry -r 'IBM Cloud'
ibmcloud login -a https://cloud.ibm.com # select au-syd
ibmcloud cr region-set ap-south
ibmcloud cr namespace-add assingment4
ibmcloud cr login
docker pull harshbhandariv/nest_sample
docker tag nest_sample:latest au.icr.io/assignment4/nest_sample:latest
docker push au.icr.io/assignment4/nest_sample:latest
```
