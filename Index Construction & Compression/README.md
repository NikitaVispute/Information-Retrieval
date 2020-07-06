Resources Used: 
	Wordnet Lemmatizer, PorterStemmer, Stopwords from nltk library
	Pickle package for serializing and de-serializing a Python object structure so that it can be saved on disk. Pickle serializes the object (list,dict,etc.) before writing it to file. 

Required Files: HW2.py and Cranfield directory
Python version used: 2.7.5(UTD csgrads1 Server), 3.7.1 (Windows 10 personal machine)

Steps to execute the program: 

1. To log into csgrads1 server:
	
	Using unix (OSX/linux): use the 'ssh' command
	
	Using Windows: use an ssh client (like PuTTY).
    The full hostname for csgrads1 is: csgrads1.utdallas.edu 
    Log onto it with the UTD Netid Credentials.

2. Copy ONLY the HW2.py python script from the unzipped folder onto the csgrads1 server (on your own home directory on csgrads1) (e.g. using ftp applications like FileZilla, WinSCP)

3. Change the file permissions by using 'chmod' command like
	
	{csgrads1:~} chmod 777 HW2.py
   
   or manually by going into properties and selecting all R,W,X for Owner,Group,Others. Refresh the directory.

4. The next steps are executed to ensure correct python version and libraries are downloaded and used.
	
	1. {csgrads1:~} unset PYTHONPATH
	2. {csgrads1:~} unset PYTHONHOME
	3. {csgrads1:~} python    (# python version will be displayed)
		>>> exit()
	4. {csgrads1:~} pip install setuptools -U --user 	(# setuptools is to be installed for correct installation of nltk 3.4.5 for python 2.7.5 on cs1grads)
	5. {csgrads1:~} pip install nltk --user			(# install nltk)
	
	Ignore the upgrade pip warning.

5. Now execute the file HW2.py with Cranfield folder path name passed as argument on the csgrads1 server terminal.
   	
	{csgrads1:~} python HW2.py '/people/cs/s/sanda/cs6322/Cranfield'
   
   If you have the Cranfield folder in the same directory as the location of the copied program HW2.py, then,
   	
	{csgrads1:~} python HW2.py './Cranfield'

6. The stopwords and wordnet packages will be downloaded and the program will execute.
   Once its done executing, refresh your home directory.
   You will see 5 files:
	1. HW2.txt
	2. Index_Version1.compressed 
	3. Index_Version1.uncompress
	4. Index_Version2.compressed
	5. Index_Version2.uncompress

   The entire output for the program will get printed into the HW2.txt file and the other 4 files will be generated. 
   Also refer to the Report for the program description and generated output explanation.  
