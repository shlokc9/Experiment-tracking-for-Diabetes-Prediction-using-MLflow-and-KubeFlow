#!/bin/bash

args_array=("$@")

exec_command="papermill Diabetes-Prediction.ipynb Diabetes-Prediction.ipynb"

for i in "${!args_array[@]}"
do
  if [ $(($i % 2)) -eq 0 ]; then
      exec_command+=" -p"
  fi
  exec_command+=" "
  exec_command+=${args_array[$i]}
done

echo "Executing command : $exec_command"
$exec_command
