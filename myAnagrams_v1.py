# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 11:02:19 2015

@author: emrijai
"""
from collections import defaultdict
from itertools import groupby
import matplotlib.pyplot as plt
import sys
import MySQLdb


# function to open and read a file line by line
def  fileopener(args):
    try:
        print args
        with open(args) as f:
            lines = f.read().splitlines()   
        return lines   
    except IOError:
            'IO Error, File Error: ', args    

# function to create a dictionary of all words and save them as key-value pairs           
def get_anagrams(words):
    wordlist = defaultdict(list)
    for mywords in words:
        key = "".join(sorted(mywords))
        wordlist[key].append(mywords)
    return wordlist

# function to return the anagrams as key-value pairs and the count of anagrams per key
# this function can be used to count and find the real anagrams and and seperate them from no-anagrams
def load_all_anagrams(words):
    key_value_pairs = get_anagrams(words)
    #print len(key_value_pairs)
    total_anagrams = 0
    anagram_details = []
    for key, anagrams in key_value_pairs.iteritems():
        if len(anagrams) > 1:
            anagram_items = ( key, anagrams, len(anagrams))
            anagram_details.append(anagram_items)
            total_anagrams +=1   
    return total_anagrams, anagram_details      

#Function to count how many anagrams are of certain lenght and use this to print the bar chart    
def frequencycount(items):
    d = [x[2] for x in items]
    freq = {x:d.count(x) for x in d}
    x, y = freq.keys(), freq.values()
    return x, y

#function to print the bar chart frequeny and counts
def plothist(x,y):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.title("Anagram Length Frequency Count")
    plt.xlabel("Count")
    plt.ylabel("Frequency")
    ax.bar(x, y,color='green')
    plt.show()

# function to connect and create a database
# this function is also used to create a database table (with anagrams informwion)
def create_anagram_database(words):
    print "Enter Database password:"
#    db = MySQLdb.connect(host="127.0.0.1", # your host, usually localhost
#                     user="root", # your username
#                     passwd=  raw_input(), # your password
#                     db="anagramDb") # name of the data base
    # create a Cursor object. It will let
    #  you execute all the queries you need
    
    #Connect to the database, assuming database = anagramDb is already created
    con = MySQLdb.connect(host="127.0.0.1", user="root", passwd=raw_input(), db="anagramdb")
    cur = con.cursor()
    # the following code can be used to create a database if its not already created before
#    try:
#        cur.execute('CREATE DATABASE anagramDb;')
#        print 'Database Created : anagramdb' 
#    except MySQLdb.Error, e:
#        'Database Creation Error: ' + str(e)                
     
    # Use all the SQL you like
    cur.execute("show tables")
    cur.execute("SELECT VERSION()")
    # Fetch a single row using fetchone() method.
    data = cur.fetchone()
    print "Database version : %s " % data
    # Drop table if it already exist using execute() method and create a table
    cur.execute("DROP TABLE IF EXISTS Anagrams")
    sql = """CREATE TABLE Anagrams (
         AnagramKey  CHAR(100) NOT NULL,
         AnagramValues  varchar(300) NOT NULL,
         Anagram_Counts INT )"""
    cur.execute(sql)
    create_table = 'Anagrams'
    
    try:
        cur.execute("""SHOW CREATE TABLE %s""" %('Anagrams'))
    except:
        print "The Table has not yet been created."
        pass
    else:
        print ("The table %s has been created successfully", create_table)  
    
    key_value_pairs = get_anagrams(words)
#    print len(key_value_pairs)
    for key, anagrams in key_value_pairs.iteritems():
        if len(anagrams) > 0:
#            anagram_items = ( key, anagrams, len(anagrams))
#            anagram_details.append(anagram_items)
            try:        
                cur.execute('INSERT INTO Anagrams (AnagramKey, AnagramValues, Anagram_Counts) VALUES ("%s", "%s", "%s");', (key, anagrams, len(anagrams)))
            except:
                print "ERROR"
                raise
    con.commit()    
        
                
def main():
    """ Use command line to give file name 
    Parse the dictionary of words using fileopener function"""
    args = sys.argv[1:2]
#    words = fileopener('Dictionary.txt')    
    for arg in args:
        #fileopener function will return a list of all the words in the text file
        words = fileopener(arg)
    print 'Total Words in the Dictionary : ' + str(len(words))
    # call load_all_anagrams function and create a list of all the anagrams in the file    
    anagram_count, anagram_details = load_all_anagrams(words)
    # sort the list to answer the questions
    sorted_anagram_list = sorted(anagram_details,key=lambda x: x[2])
    
    print 'Q1: How many unique anagrams are in the scrabble word list?' + '\n' + 'Answer : ' + str(len(sorted_anagram_list))
    print 'Q2: What is the anagram with the largest number of words in the word list?' + '\n' + 'Answer : ' + str( [x[0] for x in sorted_anagram_list[-1:]])
    print 'How many words are in this anagram?' + '\n' +'Answer :' + str( [x[2] for x in sorted_anagram_list[-1:]])
    print 'What are those Words : ' + str( [x[1] for x in sorted_anagram_list[-1:]])
    x, y = frequencycount(sorted_anagram_list)    
    print 'visualize a histogram of the size of the anagrams' + '\n' + 'Anagram Length =' + str(x)
    print 'Anagram Length Frequency =' + str( y)
    plothist(x,y)
    
    create_anagram_database(words)
    
if __name__ == '__main__':
    main()