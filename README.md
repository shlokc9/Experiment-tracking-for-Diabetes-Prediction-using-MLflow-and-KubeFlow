**Experiment tracking for Diabetes Prdiction using Kubeflow and MLflow**

-------------------------------------------------------------------------------------------------------


This assignment trains a simple diabetes prediction model using sklearn library's RandomForestRegressor. This goal of this assignment is to experiment with training multiple models using Kubeflow where each model has a unique set of hyperparameters and comparing their performance using MLflow UI.


-------------------------------------------------------------------------------------------------------

***Prerequisites***

1. python >=3.8
2. docker
3. kubectl
4. helm

-------------------------------------------------------------------------------------------------------

***Setting up the environment***


We will be using a Kind (Kubernetes in Docker) cluster for our use-case here. Use following command to install kind on your linux system
```
$ curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.18.0/kind-linux-amd64
$ chmod +x ./kind
$ sudo mv ./kind /usr/local/bin/kind
```
Find more installation options here - https://kind.sigs.k8s.io/docs/user/quick-start/#installation

Now we create a kubernetes cluster with
```
$ kind create cluster
``` 
Kubeconfig for kubectl is set to this local cluster as soon as it's created

After setting up the cluster, we install Kubeflow as follows
```
$ export PIPELINE_VERSION=1.8.5
$ kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
$ kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
$ kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"
```

Verify that the Kubeflow Pipelines UI is accessible by port-forwarding. You can use this UI to manually interact with Kubeflow
```
$ kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```

Now we install MLflow using the following helm commmand
```
$ helm install --create-namespace mlflow --namespace mlflow community-charts/mlflow --version 0.7.19 --set service.type="NodePort"
```

To view the MLflow UI, we need to fetch the MLflow tracking server URI. Run following set of commands to get the URI
```
$ export NODE_PORT=$(kubectl get --namespace mlflow -o jsonpath="{.spec.ports[0].nodePort}" services mlflow)
$ export NODE_IP=$(kubectl get nodes --namespace mlflow -o jsonpath="{.items[0].status.addresses[0].address}")
$ echo http://$NODE_IP:$NODE_PORT
```
Note this URI for later use. For understanding purposes let's call it `MLFLOW_TRACKING_URI`

-------------------------------------------------------------------------------------------------------

***Running experiments***

Now since our local Kubernetes cluster is set up with Kubeflow and MLflow, we can create a kubeflow pipeline for the jupyter notebook `Diabetes-Prediction.ipynb` and train multiple RF regressor models each tweaked with new hyperparameter values.

First we need to create a Kubeflow pipeline. Below command will create a kubeflow pipeline set with all the default hyperparameter values  
```
$ make create-pipeline
```

To run the pipeline with different set of hyperparameters run
```
$ make run-pipeline [ARGS]
```
where [ARGS] here means space separated command-line arguments in format `<hyperparameter> <hyperparameter-value>`
Resultant command should look similar to `make run-pipeline n_estimators 30 criterion squared_error`

Since we've already port forwarded the Kubeflow UI, you can check status of various experiment runs on http://localhost:8080/

After each experiment run, you can head to `MLFLOW_TRACKING_URI` to check the performance of the model and compare each run. 

To delete pipeline
```
$ make delete-pipeline
```

-------------------------------------------------------------------------------------------------------

***Clean-up***

To clean up the entire application simply run,
```
$ kind delete cluster
```
