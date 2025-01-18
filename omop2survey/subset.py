import os
import pandas_gbq


def get_survey_map():
    survey_map_sql = """ SELECT DISTINCT survey FROM `""" + os.environ["WORKSPACE_CDR"] + """.ds_survey` """
    survey_map_df = pandas_gbq.read_gbq(survey_map_sql, dialect="standard",
                                        use_bqstorage_api=("BIGQUERY_STORAGE_API_ENABLED" in os.environ),
                                        progress_bar_type="tqdm_notebook")
    survey_map = {i + 1: survey for i, survey in enumerate(survey_map_df['survey'].tolist())}
    return survey_map


def show_survey_options():
    survey_map = get_survey_map()
    for key, value in survey_map.items():
        print(f"{key}: {value}")
    print("\nExample usage in Python: selecting 'Social Determinants of Health' (assuming it is the 7th option)")
    print("# selected_survey_df = omop2survey.import_survey_data(7)")
    print("# print(selected_survey_df.head(5))")

    print("\nExample usage in R: selecting 'Social Determinants of Health' (assuming it is the 7th option)")
    print("# selected_survey_df <- omop2survey$import_survey_data(7)")
    print("# head(selected_survey_df)")


def import_survey_data(selection):
    survey_map = get_survey_map()

    survey_name = survey_map.get(selection)

    if survey_name is None:
        raise ValueError(f"Invalid selection. Please choose a number between 1 and {len(survey_map)}.")

    dataset_sql = f"""
        SELECT DISTINCT
            answer.person_id,
            answer.survey,
            answer.question_concept_id,
            answer.question,
            answer.answer_concept_id,
            answer.answer
        FROM
            `{os.environ["WORKSPACE_CDR"]}.ds_survey` answer
        WHERE
            answer.survey = '{survey_name}'
    """

    print("Executing SQL query:")
    print(dataset_sql)

    survey_df = pandas_gbq.read_gbq(
        dataset_sql,
        dialect="standard",
        use_bqstorage_api=("BIGQUERY_STORAGE_API_ENABLED" in os.environ),
        progress_bar_type="tqdm_notebook"
    )

    print(f"The number of unique person_ids in the dataset: {survey_df['person_id'].nunique()}")
    return survey_df
