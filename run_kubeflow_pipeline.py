import sys
import kfp

if __name__ == '__main__':
	pipeline_name = "Train Diabetes Prediction model"

	pipelines = kfp.Client().list_pipelines().pipelines

	for pipeline in pipelines:
	    if pipeline.name == pipeline_name:
	        pipeline_id = pipeline.id
	        break
	else:
	    raise Exception(f"No pipeline found with name: {pipeline_name}")

	experiment_name = 'Diabetes Prediction Experiment'
	experiment = kfp.Client().create_experiment(experiment_name)

	params = {}
	if len(sys.argv[1:]) != 0:
		all_args = sys.argv[1:]
		for i in range(len(all_args)):
			if i%2 == 0:
				continue
			params[all_args[i-1]] = all_args[i]

	run_name = f"Run of {pipeline_name}"
	kfp.Client().run_pipeline(experiment.id, run_name, pipeline_id=pipeline_id, params=params)
