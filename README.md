# Natural-to-SQL
Implemented data cleaning and manipulation techniques and generated a Feature-based CFG for parsing user input and convert it into a SQL statement as part of my Data Analytics Cognitive Computing course project.

Approach 1 (Feature-based CFG):
• Get the details of the database and the database schema which will be used to form the grammar. 
• Write the initial part of the grammar which includes rules for the column and table name. 
• Parse the entire database and map all possible values in the database and write these new rules to the grammar. 
• Using the ﬁnal generated grammar, parse the natural language query and generate the SQL query. 
• Run the generated SQL query and display the results. 

Approach 2:
Different data cleaning and manipulation steps were taken to convert the user input to extract relevant information and generate the corresponding SQL statement.
• First convert the words to lower-case for uniformity.
• Tokenize the sentence using word tokenize from the NLTK library and then remove stopwords and escape characters.
• StanfordPOSTagger and WordNetLemmatizer was used for POS tagging and lemmatization to find root words.
• The final SQL query is generated from the remaining root words. 
• Run the generated SQL query and display the results.
