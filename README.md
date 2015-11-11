# Anagrams
How many unique anagrams are in the scrabble word list? What is the anagram with the largest number of words in the word list? How many words are in this anagram? Use matplotlib (or Excel) to visualize a histogram of the size of the anagrams. That is, make a bar chart where the X-axi from from X = 1 to X =max anagram size. Each bar will represent the number of anagrams of size X


We can store these files in a specific folder, for example c:\ and then run the script. 
To create the database with the anagrams, mySql database with the name anagramdb is needed. I have also commented the database creation section in the script, and in case we do not have a database with this name, we can create one by uncommenting the following code in the script:
# The following code can be used to create a database if it’s not already created before
# try:
# 	cur.execute('CREATE DATABASE anagramDb;')
# 	print 'Database Created : anagramdb' 
# except MySQLdb.Error, e:
	# 'Database Creation Error: ' + str(e)
	This script can be run from : c:\python myAnagrams_v1.py mbsingle.txt
	Run the script as shown below: 
	1.	Save the script in a folder
	2.	Change directory to that folder
	3.	Save the words dictionary “Dictionary.txt” in a specific folder
	4.	Run the following command (Assuming both the above script and Dictionary.txt is stored at c:\)
	C:\python myAnagrams_v1.py c:\Dictionary.txt

