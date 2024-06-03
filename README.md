
The **'omop2survey'** Python package offers a comprehensive solution for transforming standardized response codes from the Observational Medical Outcomes Partnership (OMOP) Common Data Model (CDM) survey variables into numeric values, streamlining the data preparation process. By automating the mapping and conversion of response codes, as well as the handling of missing data, it makes data analysis more accessible and reliable. The package provides a range of functions designed to help researchers and data analysts efficiently work through OMOP CDM survey data, ensuring accurate mappings of responses and effective management of data discrepancies. This package is a helpful tool for those working with OMOP CDM survey data, offering a path to more profound and accurate analyses by dramatically lowering the burden of data preprocessing.

The content of Python files in the package can be found below. For examples of how to use the package, see **example.py** for Python and **exampleR.Rmd** for R.

### subset.py

> 
>**get_survey_map()**: Retrieves a distinct list of available surveys from the dataset and maps them to a dictionary. The keys in this dictionary are sequential integers starting from 1, and the values are the survey names. This function makes it easy to reference surveys by their assigned numbers.
> 
> Returns: A dictionary mapping integers to survey names.
>

>
>**show_survey_options()**: Displays the available surveys to the user in a numbered list. This function calls get_survey_map() to retrieve the survey options and then prints each option with its corresponding number. Additionally, it provides an example usage to guide the user on how to select a survey.
> 

>**import_survey_data(selection)**: Imports survey data based on the user's selection. The function first retrieves the survey map using get_survey_map(), then validates the user's selection. If the selection is valid, it constructs and executes an SQL query to fetch the survey data for the selected survey. The resulting DataFrame contains survey responses and is returned for further analysis.
> 
> Parameters: 
> - ***selection***: An integer representing the user's choice of survey. 
> 
> Returns: A DataFrame containing the survey data for the selected survey.
> 


### response_set.py

>
>**map_answers(input_data)**: Maps survey responses to corresponding numeric and text values, and handles survey responses that fall outside the predefined cases.
> 
> Parameters:
> -  ***input_data***: DataFrame containing survey responses with columns question_concept_id and answer_concept_id. 
> 
> Returns: The modified DataFrame with added columns answer_numeric and answer_text containing the mapped values.
>

>**process_answers(input_data)**: Maps survey responses to corresponding numeric and text values by dividing the input survey data into chunks and processes each chunk in parallel using map_answers_chunk(). It handles special case mappings, constructs mappings for numeric and text answers, and utilizes multiprocessing for efficient processing. 
> 
> Parameters:
> - ***input_data***: DataFrame containing survey responses with columns question_concept_id and answer_concept_id. 
> 
> Returns: The modified DataFrame containing the processed survey data with columns answer_numeric and answer_text added.

> 
>**create_dummies(input_data)**: Transforms survey data to include dummy variables for questions that allow multiple answers. 
> Each response is converted into a separate row with a unique identifier, defined as '{question_concept_id}_{answer_concept_id}'. The function then removes the original rows to prevent data redundancy. 
> 
> Parameters: 
> - ***input_data***: DataFrame containing survey responses with columns question_concept_id and answer_concept_id. 
> 
> Returns: A new DataFrame with additional rows for select-all-that-apply questions, properly formatted for further analysis.
> 

> 
>**scale(input_data, variables, scale_name)**: Calculates a composite score for each participant based on specified variables. 
> This function supports handling missing values and can calculate the score as either the sum or the mean of the selected variables. 
> The results include diagnostic print statements about the calculation.
> 
> Parameters:
> - ***input_data***: DataFrame containing the data to be scored.
> - ***variables***: List of columns to be included in the score calculation.
> - ***score_name***: Name of the column where the score will be stored.
> - ***na***: Boolean indicating whether to include participants with missing data in the calculations (na = True or na = False).
> - ***method***: Specifies the method for score calculation (method = 'sum' or method = 'mean').
> 
> Returns: The original DataFrame with an additional column containing the calculated scores for each participant.
> 

### pivot_data.py

>
> **pivot(input_data, file_name)**: Pivots a dataset to structure numeric survey responses in a wide format. The function checks if the specified file exists; if not, it prints an error message and returns. It reads the data from the file into a DataFrame, then pivots this DataFrame so that each row represents a respondent and each column represents a question, with cells containing the numeric answers. 
>  The column names are prefixed with 'q' to denote question IDs. The resulting pivot table is saved to a CSV file and then uploaded to a cloud storage bucket using Google Cloud's gsutil tool.
>
> Parameters:
> - ***input_data***: A pandas DataFrame containing the columns person_id, question_concept_id, and answer_numeric.
> - ***file_name***: Optional; the name of the file to which the pivot table will be saved. Defaults to 'pivot_n.csv'.
>

> 
>**pivot_text(input_data, file_name)**: Similar to pivot_data_numeric, but pivots text responses instead. The resulting pivot table is saved to a CSV file and then uploaded to a cloud storage bucket using Google Cloud's gsutil tool.
>
>Parameters:
> - ***input_data***: A pandas DataFrame containing the columns person_id, question_concept_id, and answer_text.
> - ***file_name***: Optional; the name of the file to which the pivot table will be saved. Defaults to 'pivot_t.csv'.
>

### recode_missing.py
> 
> **recode(input_data)**: Processes input data (either in file format or as a pandas DataFrame) to handle missing values according to a specified list of codes. It replaces a predefined set of numeric codes with pandas NA values to standardize the representation of missing data across the dataset. 
> 
> Parameters:
> - ***input_data***: This can be either a path to a data file (CSV, TXT, or Excel) or a pandas DataFrame. The function adapts its behavior based on the type of input provided.
>
> Returns: A pandas DataFrame with the missing values recoded as pandas NA.

### codebooks.py
>
>**codebook(df)**: Processes input data to generate a structured HTML codebook, which includes a detailed listing of questions and responses formatted neatly. The function first cleans and deduplicates the data, then iteratively builds the formatted data, and finally writes it to an HTML file that is linked for download.
>
> Parameters:
>
> - ***input_data***: DataFrame to be processed into a codebook.
> 
> Returns: The HTML-formatted codebook and an IPython display link to the generated HTML file.
> 


