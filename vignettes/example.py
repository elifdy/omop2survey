import pandas as pd
import omop2survey as omop2

# Mapping answers to numeric and text values: input data can be text, a CSV file, an Excel file, or a pandas DataFrame.
sample_df = 'sample_survey.csv'
sample_df = pd.read_csv(sample_df)
sample_df_copy = sample_df.copy()
omop2.map_answers(sample_df_copy)
print(sample_df_copy)

# Create a codebook and save it as an HTML file; the codebook contains only variables in the dataset.
# Note: The codebook function can be used to save the file to the GC workspace bucket,
# whereas codebook_html saves the file locally.

omop2.codebook_html(sample_df_copy)

# use codebook function in the cloud environment
# omop2.codebook(sample_df_copy)


# Recode missing values
omop2.recode(sample_df_copy)
print(sample_df_copy.head(5))

# Create dummy coded variables
sample_dummy_df = omop2.create_dummies(sample_df_copy)
print(sample_dummy_df.head(5))

# Convert data from long format to wide format using numeric values.
# The pivot function can be used in the cloud environment.
# Use pivot_local to save files locally.

omop2.pivot_local(sample_df_copy)

# Convert data from long format to wide format using text values.
# The pivot_text function can be used in the cloud environment.
# Use pivot_text_local to save files locally.


omop2.pivot_text_local(sample_df_copy)

# Calculate scale scores using a wide format DataFrame. Scale function takes following arguments,
# dataset, variables, scale_name, na=True/False, method= 'sum' / 'mean'

pivot_df = pd.read_csv('workspace/pivot_n.csv')
variables = ['q43528662', 'q43528663', 'q43528664']
scale_name = 'afford_healthcare'

pivot_scale = omop2.scale(pivot_df, variables, scale_name)  # default na=False, and method='sum'
print(pivot_scale['afford_healthcare'])

scale_name = 'mean_afford_healthcare'
pivot_scale2 = omop2.scale(pivot_scale, variables, scale_name, method='mean')

pivot_scale2.to_csv('workspace/pivot_scale.csv', index=False)

# all functions can be used with pandas dataframes
data = {
    'person_id': [10, 12, 13, 14, 15],
    'question_concept_id': [1, 2, 3, 4, 5],
    'answer_numeric': [-999, 2, -997, 4, 5]
}

df = pd.DataFrame(data)
processed_df = omop2.recode(df)
print(processed_df)
