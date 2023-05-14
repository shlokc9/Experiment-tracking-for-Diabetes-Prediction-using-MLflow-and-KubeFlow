import kfp
from kfp import dsl
from kubernetes.client.models import V1EnvVar
from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()
service = v1.read_namespaced_service(name="mlflow", namespace="mlflow")
node_port = service.spec.ports[0].node_port
nodes = v1.list_node()
node_ip = nodes.items[0].status.addresses[0].address


@dsl.pipeline(
    name='Diabetes prediction pipeline',
    description='A pipeline that trains a diabetes prediction model.'
)
def my_pipeline(
    n_estimators = 100, criterion = 'squared_error', max_depth = "None", min_samples_split = 2,
    min_samples_leaf = 1, min_weight_fraction_leaf = 0.0, max_features = 1.0, max_leaf_nodes = "None",
    min_impurity_decrease = 0.0, bootstrap = True, oob_score = False, n_jobs = "None", random_state = "None",
    verbose = 0, warm_start = False, ccp_alpha = 0.0, max_samples = "None", min_impurity_split = "None"
):
    train_op = dsl.ContainerOp(
        name='Train Diabetes Prediction model',
        image='shlokc/diabetes-prediction-exp-tracking:v1.0.0',
        # Please specify all the hyperparameters in this list of arguments
        arguments=[
            "n_estimators", n_estimators,
            "criterion", criterion,
            "max_depth", max_depth,
            "min_samples_split", min_samples_split,
            "min_samples_leaf", min_samples_leaf,
            "min_weight_fraction_leaf", min_weight_fraction_leaf,
            "max_features", max_features,
            "max_leaf_nodes", max_leaf_nodes,
            "min_impurity_decrease", min_impurity_decrease,
            "bootstrap", bootstrap,
            "oob_score", oob_score,
            "n_jobs", n_jobs,
            "random_state", random_state,
            "verbose", verbose,
            "warm_start", warm_start,
            "ccp_alpha", ccp_alpha,
            "max_samples", max_samples,
            "min_impurity_split", min_impurity_split
        ]
    )
    train_op.add_env_variable(V1EnvVar(name='MLFLOW_TRACKING_URI', value=f"http://{node_ip}:{node_port}"))


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(my_pipeline, 'diabetes-prediction-pipeline.zip')
    kfp.Client().upload_pipeline(pipeline_name='Train Diabetes Prediction model', pipeline_package_path="diabetes-prediction-pipeline.zip")
