"""
file: NaturalToSQL2.py
language: python3.7
author: np9603@cs.rit.edu Nihal Surendra Parchand
author: rk4447@cs.rit.edu Rohit Kunjilikattil
author: vc6346@rit.edu Viraj Chaudhari
"""

''' Libraries imported '''
from nltk import word_tokenize
from nltk import WordNetLemmatizer
import nltk

text = "list names of cities where countrycode equal AFG"
condition_set = {"in", "having", "where"}
select_list = []
indexVal = -1
gen_query = ""

# condition words:
condition_dict = {"select": ['list', 'give', 'display', 'provide', 'what',
                             'which'],
                  "=": ["equals", "is", "equalto","equal"],
                  ">": ['greater', 'larger', 'greater than', 'bigger', 'bigger '
                                                                       'than',
                        'larger than'],
                  "<": ['less', 'less than', 'smaller than', 'smaller']}

column_names_list = ["id", "name", "countrycode", "district", "population",
                     "code",
                     "continent", "region", "surfacearea", "indepyear",
                     "population",
                     "lifeexpectancy", "gnp", "gnpold", "localname",
                     "governmentform",
                     "headofstate", "capital", "code2", "language",
                     "isofficial",
                     "percentage"]
table_names_list = ["city", "country", "countrylanguage"]

for word in text.lower().split():
    if word not in condition_set:
        # All selection statement column names will be here.
        select_list.append(word)
    else:
        indexVal = text.lower().index(word) + (len(word) - 1) + 1
        break

# All condition statement column names should be checked here.
condition_list = text[indexVal + 1:].split()

# Lemmatizer initialization
wordnet_lemmatizer = WordNetLemmatizer()
tag_list = nltk.pos_tag(word_tokenize(text))
punctuations = "?:!.,;"
''' Tokenizing the query '''
tokens = word_tokenize(text)

for word in tokens:
    if word in punctuations:
        tokens.remove(word)

for i in range(len(select_list)):
    select_list[i] = wordnet_lemmatizer.lemmatize(select_list[i].lower())

for i in range(len(condition_list)):
    condition_list[i] = wordnet_lemmatizer.lemmatize(condition_list[i].lower())


select_column_list = []
condition_column_list = []
operator = ""
noun_list = ["*"]
condition = ""
noun_tags = ["NNS", "NN", "NNP"]

for key, values in condition_dict.items():
    for value in values:
        for val in condition_list:
            if val == value:
                operator = key

print(operator)

for tag in tag_list:
    if tag[1] in noun_tags:
        root_word = wordnet_lemmatizer.lemmatize(tag[0], pos="n")
        root_word = root_word.lower()
        if root_word in table_names_list:
            print("Table name:", root_word)
            table_name = root_word
        if root_word in column_names_list:
            if root_word in column_names_list and root_word in select_list:
                print("Select Column name:", root_word)
                select_column_list.append(root_word)
            if root_word in condition_list:
                print("Condition Column name:", root_word)
                condition_column_list.append(root_word)
        if root_word not in column_names_list and root_word not in \
                table_names_list \
                and root_word != operator and root_word in condition_list:
            value = root_word

if indexVal != -1:
    print("SELECT", *[x for x in select_column_list], "FROM", table_name,
          "WHERE",
          *[x for x in condition_column_list], operator, value)
else:
    print("SELECT", *[x for x in select_column_list], "FROM", table_name)
# print(tag_list)

for word in tokens:
    print("{0:20}{1:20}".format(word,
                                wordnet_lemmatizer.lemmatize(word, pos="n")))

print(select_list)
print(condition_list)
print(column_names_list)
print(table_names_list)
