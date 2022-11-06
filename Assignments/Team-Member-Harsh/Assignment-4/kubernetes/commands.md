```
ibmcloud login
ibmcloud plugin install ks
ibmcloud ks cluster config -c cdhb1smf00ts46su3a1g
kubectl config current-context # verification command
kubectl apply -f nest-sample-deployment.yaml
kubectl apply -f nest-sample-service.yaml
ibmcloud ks worker ls --cluster mycluster-free # get public ip address of node
curl 169.51.207.13:32000
```
