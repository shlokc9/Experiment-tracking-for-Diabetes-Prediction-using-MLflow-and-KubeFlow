**Experiment tracking for Diabetes Prediction using Kubeflow and MLflow**

-------------------------------------------------------------------------------------------------------


This application trains a simple diabetes prediction model using sklearn library's RandomForestRegressor. The goal here is to experiment with training multiple models using Kubeflow where each model has a unique set of hyperparameters and comparing their performance using MLflow UI.


-------------------------------------------------------------------------------------------------------

***Prerequisites***

1. python >=3.8
2. jupyter
3. docker
4. kubectl
5. helm

-------------------------------------------------------------------------------------------------------

***Setting up the environment***


We will be using a Kind (Kubernetes in Docker) cluster for our use-case here. Use following command to install kind on your linux system
```
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.18.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```
Find more installation options here - https://kind.sigs.k8s.io/docs/user/quick-start/#installation

Now we create a kubernetes cluster with
```
kind create cluster
``` 
Kubeconfig for kubectl is set to this local cluster as soon as it's created

After setting up the cluster, we install Kubeflow as follows
```
export PIPELINE_VERSION=1.8.5
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"
```
Wait for all the pods in kubeflow namespace to turn to "Running" state (Use `kubectl -n kubeflow get pods -w` to monitor pod status)

On a seperate terminal session, verify that the Kubeflow Pipelines UI is accessible by port-forwarding. You can use this UI to manually interact with Kubeflow
```
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```

Now we install MLflow using the following helm commmand
```
helm repo add community-charts https://community-charts.github.io/helm-charts
helm repo update
helm install --create-namespace mlflow --namespace mlflow community-charts/mlflow --version 0.7.19 --set service.type="NodePort"
```
Wait for all the pods in mlflow namespace to turn to "Running" state (Use `kubectl -n mlflow get pods -w` to monitor pod status)

To view the MLflow UI, we need to fetch the MLflow tracking server URI. Run following set of commands to get the URI
```
export NODE_PORT=$(kubectl get --namespace mlflow -o jsonpath="{.spec.ports[0].nodePort}" services mlflow)
export NODE_IP=$(kubectl get nodes --namespace mlflow -o jsonpath="{.items[0].status.addresses[0].address}")
echo http://$NODE_IP:$NODE_PORT
```
If you are using a Ubuntu 20.04 from WSL2 docker desktop on Windows machine, you might have to port forward the mlfow dashboard. See for more info.: **https://stackoverflow.com/questions/69095319/cannot-connect-to-service-on-nodeport-using-kubernetes-on-windows-docker-desktop**
```
kubectl port-forward -n mlflow svc/mlflow 5000:5000
```
Note either of the URI that's applicable in your case. Open it on a browser tab for later use. For understanding purposes let's call it `MLFLOW_TRACKING_URI`

-------------------------------------------------------------------------------------------------------

***Running experiments***

Now since our local Kubernetes cluster is set up with Kubeflow and MLflow, we can create a kubeflow pipeline for the jupyter notebook `Diabetes-Prediction.ipynb` and train multiple RF regressor models each tweaked with new hyperparameter values.

First we need to create a Kubeflow pipeline. Below command will create a kubeflow pipeline set with all the default hyperparameter values  
```
make create-pipeline
```

To run the pipeline with different set of hyperparameters run
```
make run-pipeline [ARGS]
```
where [ARGS] here means space separated command-line arguments in format `<hyperparameter> <hyperparameter-value>`
Resultant command should look similar to `make run-pipeline n_estimators 30 criterion squared_error`

Since we've already port forwarded the Kubeflow UI, you can check status of various experiment runs on http://localhost:8080/

After each experiment run, you can head to `MLFLOW_TRACKING_URI` to check the performance of the model and compare each run. 

To delete pipeline
```
make delete-pipeline
```

-------------------------------------------------------------------------------------------------------

***Clean-up***

To clean up the entire application simply run,
```
kind delete cluster
```

-------------------------------------------------------------------------------------------------------

***Future scope***

Below mentioned are a few points to improve in the application
1. Serving a model as a service to draw inference - Every model that is deemed to be used further should be available to the user
2. Saving models - This is needed since the ultimate goal of the application is to provide the most accurate model to the user
3. Better Kubernetes cluster reliability - This is very important since local clusters may break the application. One can think of running the application on a managed-Kubernetes cluster

-------------------------------------------------------------------------------------------------------

***Demo video***

https://vimeo.com/826600073?share=copy

Please note that the video is long and incomplete because my machine was lagging a lot at the time.
The video is nothing but a visual representation of the steps mentioned in this README and one can verify the same results by executing above steps.

-------------------------------------------------------------------------------------------------------

Thank you for spending your valuable time on this repository! :)
