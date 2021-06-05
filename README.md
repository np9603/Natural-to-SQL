# Natural-to-SQL

The goal of this project is to create a tool that would convert natural language sentence (english sentence) to SQL statements that can be queried to a MySQL database for information retrieval. With the help of regex patterns, initial data is preprocessed to filter out unnecessary symbols and include only alphabets and numbers. Feature-based CFG is generated for parsing user input and convert it into a SQL statement as part of my Data Analytics Cognitive Computing course project.

Approach 1 (Feature-based CFG):

• Get the details of the database and the database schema which will be used to form the grammar.

• Write the initial part of the grammar which includes rules for the column and table name.

• Parse the entire database and map all possible values in the database and write these new rules to the grammar.

• Using the ﬁnal generated grammar, parse the natural language query and generate the SQL query.

• Run the generated SQL query and display the results. 

The start of the grammar begins with S. There are two types of SELECT statements that we have implemented. The first one is the basic select statement which is of the format SELECT column name FROM table name. The second select statement is of the format SELECT column name FROM table name WHERE condition. The CN describes the rules for column name. It can either have one column name or more than one column names separated by commas. The C tells us about the grammar built for parsing conditions. I have implemented the grammar to incorporate one or more than one conditions. The grammar also supports queries that have values in some range with the help of BETWEEN. For accessing different integer values provided by the user (for example - if the user wants to see , we converted the values to a different value so that it could parse any number and retrieve the results from the SQL database. The OP defines the rules for operators like less than (<), more than (>), and equal(=).

![image](https://user-images.githubusercontent.com/46695666/120894638-7e2e1a80-c5e7-11eb-9078-2ec62d16fc35.png)

![image](https://user-images.githubusercontent.com/46695666/120894652-8ede9080-c5e7-11eb-95e0-ad91b72af0cc.png)

An example of how a natural language sentence is converted into its corresponding SQL statement

Natural Language Sentence - Which cities are located in China

![image](https://user-images.githubusercontent.com/46695666/120894844-7753d780-c5e8-11eb-85d0-5d044158e8f2.png)

SQL statement mapped through FCFG

![image](https://user-images.githubusercontent.com/46695666/120894873-97839680-c5e8-11eb-80a9-162f6384bae1.png)

Approach 2:
Different data cleaning and manipulation steps were taken to convert the user input to extract relevant information and generate the corresponding SQL statement.

• First convert the words to lower-case for uniformity.

• Tokenize the sentence using word tokenize from the NLTK library and then remove stopwords and escape characters.

• StanfordPOSTagger and WordNetLemmatizer was used for POS tagging and lemmatization to find root words.

• The final SQL query is generated from the remaining root words. 

• Run the generated SQL query and display the results.


# Demo 

Query 1 - List all data of cities

![image](https://user-images.githubusercontent.com/46695666/120894729-f563ae80-c5e7-11eb-8749-d0e1f2a03241.png)

![image](https://user-images.githubusercontent.com/46695666/120894751-0f04f600-c5e8-11eb-9530-a4c2f329db5d.png)


Query 2 - Show ID , name , countrycode , district , population of cities where ID less than 10

![image](https://user-images.githubusercontent.com/46695666/120894756-17f5c780-c5e8-11eb-92cb-420323d09b50.png)

![image](https://user-images.githubusercontent.com/46695666/120894772-32c83c00-c5e8-11eb-8db3-f5ef8f141804.png)


Query 3 - Show ID , name , countrycode , district , population of cities where ID less than 10

![image](https://user-images.githubusercontent.com/46695666/120894775-38258680-c5e8-11eb-9d56-1190b663a61b.png)

![image](https://user-images.githubusercontent.com/46695666/120894780-3e1b6780-c5e8-11eb-8e3a-7e66e991bab0.png)





# References

1. https://dev.mysql.com/doc/index-other.html
2. https://github.com/nltk/nltk_teach/tree/master/examples/grammars/book_grammars
3. https://docs.python.org/3/library/tkinter.html
