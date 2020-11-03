"""
file: NaturalToSQL.py
language: python3.7
author: np9603@cs.rit.edu Nihal Surendra Parchand
author: rk4447@cs.rit.edu Rohit Kunjilikattil
author: vc6346@rit.edu Viraj Chaudhari
"""

''' Libraries imported '''

import os
java_path = "C:/Program Files/Java/jdk-10.0.2/bin/java.exe"
os.environ['JAVAHOME'] = java_path

import nltk
nltk.internals.config_java("C:/Program Files/Java/jdk-10.0.2/bin/java.exe")
import re
from nltk import tokenize
from nltk import RegexpTokenizer
from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize
import pymysql
import pymysql.cursors
import pandas as pd
import nltk
from tkinter import *
from tkinter import ttk
from nltk import load_parser
from tabulate import tabulate
from pandastable import Table,TableModel
nltk.download('book_grammars')
table_names_list = []


def initial_connection():
    """
    This function is used to connect the database and display the database information
    """

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='Mysql@1234',
                                 db='world',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:

        with connection.cursor() as cursor:
            ''' Executes the query to show all table names in the database '''
            cursor.execute("Show tables;")
            res = cursor.fetchall()
            for table in res:
                for value in table.values():
                    table_names_list.append(value)
            print("\nTables in the database: ",table_names_list)

            ''' Executes the query to display the information about each table '''
            for table in table_names_list:
                print("\nTable Details for",table)
                df = pd.read_sql("Describe " + str(table), connection)
                # print(df.to_string())
                print(tabulate(df,headers=list(df.columns.values),tablefmt='psql'))

            ''' Executes the query to display the sample subset of each table '''
            for table in table_names_list:
                print("\nSample subset of data of table",table)
                df = pd.read_sql("SELECT * FROM " + str(table) +" limit 8", connection)
                # print(df.to_string())
                print(tabulate(df,headers=list(df.columns.values),tablefmt='psql'))

            # for table in table_names_list:
            city_df = pd.read_sql("SELECT * FROM city", connection)
            country_df = pd.read_sql("SELECT * FROM country", connection)
            countrylanguage_df = pd.read_sql("SELECT * FROM countrylanguage", connection)

            city_df = city_df.replace('[^A-Za-z0-9]+','',regex=True)
            country_df = country_df.replace('[^A-Za-z0-9]+', '', regex=True)
            countrylanguage_df = countrylanguage_df.replace('[^A-Za-z0-9]+', '', regex=True)

            city_df_dict = {index:list(city_df[index].unique()) for index in city_df.columns}
            country_df_dict = {index:list(country_df[index].unique()) for index in country_df.columns}
            countrylanguage_df_dict = {index:list(countrylanguage_df[index].unique()) for index in countrylanguage_df.columns}

            with open("testgrammar.fcfg", 'w', encoding='utf-8', errors='ignore') as f:
                f.write("""% start S

S[SEM=(?sel + ?cn + FROM + ?tn)] -> SEL[SEM=?sel] CN[SEM=?cn] TN[SEM=?tn]
S[SEM=(?sel + ?cn + FROM + ?tn + ?where + ?c)] -> SEL[SEM=?sel] CN[SEM=?cn] TN[SEM=?tn] WH[SEM=?where] C[SEM=?c]

SEL[SEM='SELECT'] -> 'Which' | 'What' | 'Give' | 'List' | 'Show' | 'which' | 'what' | 'give' | 'list' | 'show'

CN[SEM=(?cn1 + ?cn2)] -> CN[SEM=?cn1] CN[SEM=?cn2]
CN[SEM=(?cn1 + ?comma + ?cn2)] -> CN[SEM=?cn1] CM[SEM=?comma] CN[SEM=?cn2]

CM[SEM=','] -> ',' | 'and'

C[SEM=(?c1 + ?and + ?c2)] -> C[SEM=?c1] AND[SEM=?and] C[SEM=?c2]
C[SEM=(?cn + ?op + ?c)] -> CN[SEM=?cn] OP[SEM=?op] C[SEM=?c]
C[SEM=(?cn + ?op + ?val)] -> CN[SEM=?cn] OP[SEM=?op] V[SEM=?val]
C[SEM=(?cn + ?between + ?val1 + ?and + ?val2)] -> CN[SEM=?cn] BT[SEM=?between] V[SEM=?val1] AND[SEM=?and] V[SEM=?val2]

BT[SEM='BETWEEN'] -> 'between' | 'range'
AND[SEM='AND'] -> 'and' | 'AND'

V[SEM=(?val1 + ?val2)] -> V[SEM=?val1] V[SEM=?val2]
V[SEM='#V#'] -> '#V#'
V[SEM=''] -> 'than' | 'and'

WH[SEM='WHERE'] -> 'where' | 'with'

CN[SEM='*'] -> 'all'
CN[SEM='DISTINCT'] -> 'distinct' | 'unique'
CN[SEM='name'] -> 'names' | 'city names' | 'name'
CN[SEM='ID'] -> 'ids' | 'Ids' | 'City Id' | 'City ID' | 'ID' | 'Id'
CN[SEM='CountryCode'] -> 'countrycode' | 'CountryCode' | 'Countrycode' | 'countryCode'
CN[SEM='District'] -> 'district' | 'Districts' | 'city district' | 'District'
CN[SEM='Population'] -> 'population' | 'Population' | 'people'
CN[SEM='Code'] -> 'code' | 'Code' | 'Codes'
CN[SEM='Code2'] -> 'code2' | 'Code2' | 'Codes2'
CN[SEM='Continent'] -> 'continent' | 'Continent' | 'Continents'
CN[SEM='Region'] -> 'region' | 'Region' | 'Regions' | 'regions'
CN[SEM='Language'] -> 'language' | 'Language' | 'languages'
CN[SEM='IsOfficial'] -> 'official' | 'Official'
CN[SEM=''] -> 'of' | 'data' | 'is' | 'number'

TN[SEM='city'] -> 'city' | 'City' | 'cities' | 'Cities'
TN[SEM='country'] -> 'country' | 'Country' | 'countries' | 'Countries'
TN[SEM='countrylanguage'] -> 'countrylanguage' | 'Countrylanguage' | 'CountryLanguage' | 'country language' | 'Country Language'| 'Country language' | 'country Language'

OP[SEM=(?op1 + ?op2)] -> OP[SEM=(?op1)] OP[SEM=(?op2)]
OP[SEM=''] -> 'to' | 'than' | 'in'
OP[SEM='='] -> 'is' | 'equal'
OP[SEM='>'] -> 'above' | 'more' | 'greater' | 'larger' | 'bigger'
OP[SEM='<'] -> 'below' | 'less' | 'lesser' | 'smaller'""")

            with open("testgrammar.fcfg",'a',encoding='utf-8',errors='ignore') as f:
                for key,value in city_df_dict.items():
                    f.write("\n")
                    if key == "Name":
                        for val in city_df_dict[key]:
                            if val is not "":
                                f.write("""C[SEM='\"""" + str(val) + "\"'] -> '" + str(val) + "'\n")
                    elif key == "CountryCode":
                        for val in city_df_dict[key]:
                            if val is not "":
                                f.write("""C[SEM='\"""" + str(val) + "\"'] -> '" + str(val) + "'\n")
                    elif key == "District":
                        for val in city_df_dict[key]:
                            if val is not "":
                                f.write("""C[SEM='\"""" + str(val) + "\"'] -> '" + str(val) + "'\n")

                for key,value in country_df_dict.items():
                    f.write("\n")
                    if key == "Code":
                        for val in country_df_dict[key]:
                            if val is not "":
                                f.write("""C[SEM='\"""" + str(val) + "\"'] -> '" + str(val) + "'\n")
                    if key == "Name":
                        for val in country_df_dict[key]:
                            if val is not "":
                                f.write("""C[SEM='\"""" + str(val) + "\"'] -> '" + str(val) + "'\n")
                    if key == "Continent":
                        for val in country_df_dict[key]:
                            if val is not "":
                                f.write("""C[SEM='\"""" + str(val) + "\"'] -> '" + str(val) + "'\n")
                    if key == "Region":
                        for val in country_df_dict[key]:
                            if val is not "":
                                f.write("""C[SEM='\"""" + str(val) + "\"'] -> '" + str(val) + "'\n")

                    if key == "LocalName":
                        for val in country_df_dict[key]:
                            if val is not "":
                                f.write("""C[SEM='\"""" + str(val) + "\"'] -> '" + str(val) + "'\n")
                    if key == "GovernmentForm":
                        for val in country_df_dict[key]:
                            if val is not "":
                                f.write("""C[SEM='\"""" + str(val) + "\"'] -> '" + str(val) + "'\n")
                    if key == "HeadOfState":
                        for val in country_df_dict[key]:
                            if val is not "":
                                f.write("""C[SEM='\"""" + str(val) + "\"'] -> '" + str(val) + "'\n")
                    if key == "Code2":
                        for val in country_df_dict[key]:
                            if val is not "":
                                f.write("""C[SEM='\"""" + str(val) + "\"'] -> '" + str(val) + "'\n")

                for key,value in countrylanguage_df_dict.items():
                    f.write("\n")
                    if key == "CountryCode":
                        for val in countrylanguage_df_dict[key]:
                            if val is not "":
                                f.write("""C[SEM='\"""" + str(val) + "\"'] -> '" + str(val) + "'\n")
                    if key == "Language":
                        for val in countrylanguage_df_dict[key]:
                            if val is not "":
                                f.write("""C[SEM='\"""" + str(val) + "\"'] -> '" + str(val) + "'\n")
                    if key == "IsOfficial":
                        for val in countrylanguage_df_dict[key]:
                            if val is not "":
                                f.write("""C[SEM='\"""" + str(val) + "\"'] -> '" + str(val) + "'\n")

    finally:
        connection.close()

def natural_to_sql():
    """
    This function creates a GUI which converts natural language queries to SQL queries
    """

    root = Tk()
    root.title("Natural Language to SQL Query Converter")
    root.geometry("800x800+300+300")
    root.configure(background='black')

    user_query = StringVar()

    ''' Prints out a sample grammar from nltk library which will is discussed as alternate approach '''
    # print("\nSample Grammar from nltk library")
    # nltk.data.show_cfg(('grammars/book_grammars/sql1.fcfg'))


    """Functions"""
    def quit():
        root.destroy()

    # Display Function
    def displayResult():
        searchBtn.deiconify()
        root.withdraw()

        cp = load_parser('testgrammar.fcfg')

        ''' Retrieve the user query from the GUI '''
        query = addQuery.get("1.0", END)
        print("User input:", query)
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='Mysql@1234',
                                     db='world',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)



        query_split = query.split()
        query = ['#V#' if index.isdigit() else index for index in query_split]
        numbers = [index for index in query_split if index.isdigit()]
        trees = list(cp.parse(query))

        answer = trees[0].label()['SEM']

        answer = [s for s in answer if s]
        q = ' '.join(answer)
        result_obtained = q

        for number in numbers:
            result_obtained = result_obtained.replace("#V#",number,1)

        print("The resulting SQL query:",result_obtained)

        df = pd.read_sql(result_obtained, connection)
        print(tabulate(df, headers=list(df.columns.values), tablefmt='psql'))

        tabulated_df = tabulate(df, headers=list(df.columns.values), tablefmt='psql')


        lblResultDisplay = Label(searchBtn, text=result_obtained)
        lblResultDisplay.pack(pady=15)
        exit_btn = Button(searchBtn, text='Exit', command=quit,font=("arial", 16, 'bold'), width=10,height=1)
        exit_btn.pack(pady=15)

        lblResultDisplay = Label(searchBtn, text=tabulated_df)
        lblResultDisplay.pack(pady=30)


    # Search Box
    addQuery = Text(root, width=80, height=4)
    addQuery.pack(pady=15)

    # Buttons
    btnQuery = Button(root, text="Convert", font=("arial", 16, 'bold'), width=10,
                      height=1, command=displayResult)

    # Button Packing & Padding
    btnQuery.pack(pady=15)

    """Button Click After UI """

    # Search Button Window For User
    searchBtn = Toplevel(root)
    searchBtn.title("Query Result")
    searchBtn.geometry("800x800+300+300")
    searchBtn.configure(background='black')
    searchBtn.withdraw()
    root.mainloop()


def main():
    """
    This is the main function which calls different methods
    :return:
    """

    ''' This function is used to print out the database structure (table and table information) '''
    initial_connection()
    ''' This function is used to convert the user input query in natural language to SQL query '''
    natural_to_sql()


main()



