#!/usr/bin/env python3

import sys
from subprocess import Popen, PIPE

def run_map_reduce(input_paths, output_path):
    # Define your mapper and reducer scripts
    mapper_script = "mapper.py"
    reducer_script = "reducer.py"

    # Define Hadoop streaming command
    hadoop_cmd = [
        "hadoop", "jar", "/usr/local/hadoop-2.10.2/share/hadoop/tools/lib/hadoop-streaming-2.10.2.jar",
        "-files", mapper_script + "," + reducer_script,  # Upload mapper and reducer scripts to Hadoop nodes
        "-mapper", mapper_script,
        "-reducer", reducer_script,
        "-input"] + input_paths + ["-output", output_path]

    # Run the Hadoop streaming job
    process = Popen(hadoop_cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    # Print output and error messages
    print(stdout.decode("utf-8"))
    print(stderr.decode("utf-8"))
    

if __name__ == "__main__":
    # Input paths and output path
    csv_input_path = "/input1/dataset.txt"
    txt_input_path = "/input1/Vocabulary.txt"
    output_path = "/input1/output16"

    # Run MapReduce job
    run_map_reduce([csv_input_path, txt_input_path], output_path)
