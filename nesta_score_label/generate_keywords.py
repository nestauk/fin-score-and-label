from nesta_score_label.utils import tidy_text

def messy_list_to_tidy_list(messy_list):
    """
        Converts the messy input list
        to a tidy list
        Returns: list
    """
    all_keywords_tidy = []
    for keyword in messy_list:
        keyword = tidy_text(keyword)
        if len(keyword) > 2:
            all_keywords_tidy.append(keyword)
    return all_keywords_tidy

def kw_column_to_clean_kw_set(keyword_column):
    """
        Creates a set of keywords from the input column
        Returns: set
    """
    list_of_kw_lists = keyword_column.map(lambda x: re.split(r"[,;\/\n]", x))
    all_keywords = [y for x in list_of_kw_lists for y in x]
    trimmed_keywords =[ x.strip() for x in all_keywords]
    tidied_list = messy_list_to_tidy_list(trimmed_keywords)
    return set(tidied_list)

def generate_keywords(input_data, output_filepath = None):
    """
        Generates keywords and saves in the models folder
        Returns: list
    """

    input_keywords = kw_column_to_clean_kw_set(input_data['input_keywords'].fillna(''))
    doc_keywords = kw_column_to_clean_kw_set(input_data['doc_keywords'].fillna(''))

    all_unique_kws = list(input_keywords|doc_keywords)

    if output_filepath:
        with open(output_filepath, 'w') as file:
            file.write('keywords\n')
            for keyword in all_unique_kws: file.write(keyword + '\n')

    return all_unique_kws

if __name__ == '__main__':
    data_folder =  Path(__file__).resolve().parent

    input_data_filepath = data_folder / 'data' / 'input_data.xlsx'
    team_groups_filepath = data_folder / 'data' / 'team_groups.xlsx'

    generate_new_models(input_data_filepath, team_groups_filepath)
