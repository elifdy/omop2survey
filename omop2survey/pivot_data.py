import pandas as pd
import os
import subprocess


def pivot_text(data, file_name='pivot_t.csv'):
    pivot_df = data.pivot_table(index='person_id',
                                columns='question_concept_id',
                                values='answer_text',
                                aggfunc='first')

    pivot_df.columns = ['q' + str(col) for col in pivot_df.columns]
    pivot_df.to_csv(file_name)
    my_bucket = os.getenv('WORKSPACE_BUCKET')
    args = ["gsutil", "cp", f"./{file_name}", f"{my_bucket}/data/"]
    output = subprocess.run(args, capture_output=True)
    if output.returncode == 0:
        print(f"Pivoted dataset with text values saved and uploaded successfully to: {my_bucket}/data/{file_name}")
    else:
        print("Failed to upload the file:", output.stderr.decode())


def pivot(data, file_name='pivot_n.csv'):
    pivot_df = data.pivot_table(index='person_id',
                                columns='question_concept_id',
                                values='answer_numeric',
                                aggfunc='first')

    pivot_df.columns = ['q' + str(col) for col in pivot_df.columns]
    pivot_df.to_csv(file_name)
    my_bucket = os.getenv('WORKSPACE_BUCKET')
    args = ["gsutil", "cp", f"./{file_name}", f"{my_bucket}/data/"]
    output = subprocess.run(args, capture_output=True)
    if output.returncode == 0:
        print(f"Pivoted dataset with text values saved and uploaded successfully to: {my_bucket}/data/{file_name}")
    else:
        print("Failed to upload the file:", output.stderr.decode())

