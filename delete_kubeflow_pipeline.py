import kfp

pipeline_name = "Train Diabetes Prediction model"

pipelines = kfp.Client().list_pipelines().pipelines

for pipeline in pipelines:
    if pipeline.name == pipeline_name:
        pipeline_id = pipeline.id
        break

kfp.Client().pipelines.delete_pipeline(pipeline_id)
