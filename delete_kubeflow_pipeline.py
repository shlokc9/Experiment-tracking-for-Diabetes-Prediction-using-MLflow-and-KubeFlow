import kfp

pipeline_name = "Train Diabetes Prediction model"

pipelines = kfp.Client().list_pipelines().pipelines

for pipeline in pipelines:
    if pipeline.name == pipeline_name:
        pipeline_id = pipeline.id
        break
else:
    raise Exception(f"No pipeline found with name: {pipeline_name}")

kfp.Client().pipelines.delete_pipeline(pipeline_id)
