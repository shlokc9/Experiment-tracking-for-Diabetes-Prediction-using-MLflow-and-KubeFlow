IMAGE_TAG=v1.0.0

build-experiment:
	docker build -t diabetes-prediction-exp-tracking:$(IMAGE_TAG) .

create-pipeline:
	python3 create_kubeflow_pipeline.py

run-pipeline:
	python3 run_kubeflow_pipeline.py $(filter-out $@,$(MAKECMDGOALS))
%:
	@:

delete-pipeline:
	python3 delete_kubeflow_pipeline.py
