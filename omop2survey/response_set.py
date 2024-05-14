import pandas as pd
import os


def load_survey_data(filename='survey_key.csv'):
    current_dir = os.path.dirname(os.path.realpath(__file__))

    file_path = os.path.join(current_dir, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File path {file_path} does not exist.")
    return pd.read_csv(file_path)


def map_items(input_data):
    special_cases = {
        903087: (-999, "Don't Know"),
        903096: (-998, "Skip"),
        903072: (-997, "Does Not Apply To Me"),
        903079: (-996, "Prefer Not To Answer"),
        903070: (-995, "Other"),
        903092: (-994, "Not Sure"),
        903095: (-993, "None"),
        903103: (-992, "Unanswered"),
        40192432: (-991, "I am not religious"),
        40192487: (-990, "I do not believe in God (or a higher power)"),
        40192520: (-989, "Does not apply to my neighborhood"),
        903081: (-988, "Free Text"),
        596889: (998, "Text"),
        596883: (-994, "Not Sure"),
        1332844: (-994, "Not Sure"),
        903598: (-996, "Prefer Not To Answer"),
        903596: (-996, "Prefer Not To Answer"),
        903601: (-996, "Prefer Not To Answer"),
        903607: (-996, "Prefer Not To Answer"),
        903610: (-996, "Prefer Not To Answer"),
        903604: (-996, "Prefer Not To Answer"),
        43529089: (-997, "No Blood Related Daughters"),
        43529086: (-997, "No Blood Related Siblings"),
        43529092: (-997, "No Blood Related Sons"),
        43529090: (-997, "No Daughters Related")
    }
    survey_data = load_survey_data()

    mapping_numeric = survey_data.groupby('question_concept_id').apply(
        lambda x: dict(zip(x['answer_concept_id'], x['answer_numeric']))).to_dict()

    mapping_text = survey_data.groupby('question_concept_id').apply(
        lambda x: dict(zip(x['answer_concept_id'], x['answer_text'].str.strip()))).to_dict()

    input_data['answer_numeric'] = None
    input_data['answer_text'] = None

    for idx, row in input_data.iterrows():
        question_id = row['question_concept_id']
        answer_id = row['answer_concept_id']
        if answer_id in special_cases:
            input_data.at[idx, 'answer_numeric'], input_data.at[idx, 'answer_text'] = special_cases[answer_id]
        else:
            input_data.at[idx, 'answer_numeric'] = mapping_numeric.get(question_id, {}).get(answer_id, None)
            input_data.at[idx, 'answer_text'] = mapping_text.get(question_id, {}).get(answer_id, None)

        if pd.isna(answer_id) and pd.notna(row['answer']) and str(row['answer']).isdigit():
            input_data.at[idx, 'answer_numeric'] = int(row['answer'])
            input_data.at[idx, 'answer_text'] = str(row['answer'])

        if isinstance(input_data.at[idx, 'answer_text'], (int, float)):
            input_data.at[idx, 'answer_text'] = str(input_data.at[idx, 'answer_text'])

    return input_data


def create_dummies(user_data):
    question_key = load_survey_data()

    select_all_questions = question_key[question_key['select_all'] == 1]['question_concept_id'].unique()

    new_rows = []

    for question_id in select_all_questions:
        select_all_data = user_data[user_data['question_concept_id'] == question_id]
        for index, row in select_all_data.iterrows():
            new_row = row.copy()
            new_row[
                'question_concept_id'] = f"{question_id}_{row['answer_concept_id']}"
            new_rows.append(new_row)

    new_rows_df = pd.DataFrame(new_rows)
    filtered_data = user_data[~user_data['question_concept_id'].isin(select_all_questions)]
    result_data = pd.concat([filtered_data, new_rows_df], ignore_index=True)

    return result_data



def scale(data, variables, score_name, na=False, method='sum'):
    df = data[['person_id'] + variables]

    if na:
        df['valid_count'] = df[variables].apply(lambda x: x[x >= 0].count(), axis=1)
        min_valid_count = len(variables) * 0.8
        df = df[df['valid_count'] >= min_valid_count]
    else:
        df = df.dropna(subset=variables)
        df = df[(df[variables] >= 0).all(axis=1)]

    if method == 'mean':
        df[score_name] = df[variables].mean(axis=1)
    elif method == 'sum':
        df[score_name] = df[variables].sum(axis=1)

    data = pd.merge(data, df[['person_id', score_name]], on='person_id', how='left')


    print('Minimum score calculated:', df[score_name].min())
    print('Maximum score calculated:', df[score_name].max())
    print('Number of person_ids with NaN assigned:', data[score_name].isna().sum())
    print('Number of person_ids with score calculated:', data[score_name].notna().sum())

    return data


def map_answers(input_data):
    special_cases = {
        903087: (-999, "Don't Know"),
        903096: (-998, "Skip"),
        903072: (-997, "Does Not Apply To Me"),
        903079: (-996, "Prefer Not To Answer"),
        903070: (-995, "Other"),
        903092: (-994, "Not Sure"),
        903095: (-993, "None"),
        903103: (-992, "Unanswered"),
        40192432: (-991, "I am not religious"),
        40192487: (-990, "I do not believe in God (or a higher power)"),
        40192520: (-989, "Does not apply to my neighborhood"),
        903081: (-988, "Free Text"),
        596889: (998, "Text"),
        596883: (-994, "Not Sure"),
        1332844: (-994, "Not Sure"),
        903598: (-996, "Prefer Not To Answer"),
        903596: (-996, "Prefer Not To Answer"),
        903601: (-996, "Prefer Not To Answer"),
        903607: (-996, "Prefer Not To Answer"),
        903610: (-996, "Prefer Not To Answer"),
        903604: (-996, "Prefer Not To Answer"),
        43529089: (-997, "No Blood Related Daughters"),
        43529086: (-997, "No Blood Related Siblings"),
        43529092: (-997, "No Blood Related Sons"),
        43529090: (-997, "No Daughters Related")
    }

    survey_data = load_survey_data()

    mapping_numeric = survey_data.groupby('question_concept_id').apply(
        lambda g: g.set_index('answer_concept_id')['answer_numeric'].to_dict()
    ).to_dict()

    mapping_text = survey_data.groupby('question_concept_id').apply(
        lambda g: g.set_index('answer_concept_id')['answer_text'].str.strip().to_dict()
    ).to_dict()

    input_data['answer_numeric'] = pd.NA
    input_data['answer_text'] = pd.NA

    for answer_id, (num, text) in special_cases.items():
        mask = input_data['answer_concept_id'] == answer_id
        input_data.loc[mask, 'answer_numeric'] = num
        input_data.loc[mask, 'answer_text'] = text

    def apply_mappings(row):
        if pd.notna(row['answer_numeric']) and pd.notna(row['answer_text']):
            return row['answer_numeric'], row['answer_text']

        question_id = row['question_concept_id']
        answer_id = row['answer_concept_id']
        numeric = mapping_numeric.get(question_id, {}).get(answer_id, pd.NA)
        text = mapping_text.get(question_id, {}).get(answer_id, pd.NA)
        return numeric, text

    result = input_data.apply(apply_mappings, axis=1, result_type='expand')
    input_data[['answer_numeric', 'answer_text']] = result

    numeric_mask = pd.isna(input_data['answer_concept_id']) & input_data['answer'].apply(lambda x: str(x).isdigit())
    input_data.loc[numeric_mask, 'answer_numeric'] = input_data.loc[numeric_mask, 'answer'].astype(int)
    input_data.loc[numeric_mask, 'answer_text'] = input_data.loc[numeric_mask, 'answer'].astype(str)

    return input_data
