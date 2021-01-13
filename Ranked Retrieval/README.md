# Ranked Retrieval Model for the index					
**Technology: Python.<br>
•	Created a ranked retrieval system based on vector relevance model. The scores for the ranking are computed using cosine similarity for every query-document pair.<br>
•	Two term weighting functions are used: ‘maxtf’ and ‘Okapi’ term weighting.<br>**

Resources Used: Wordnet Lemmatizer, Stopwords, Averaged_perceptron_tagger from nltk library.

Files: HW3.py, Cranfield directory and hw3.queries file from directory
Python version used: 2.7.5(UTD Server), 3.7.1 (personal machine)

Steps for Execution:

1. To log into csgrads1 server:
	    
    Using unix (OSX/linux): use the 'ssh' command
	    
    Using Windows: use an ssh client (like PuTTY).
    
    The full hostname for csgrads1 is: csgrads1.utdallas.edu 
    Log onto it with the UTD Netid Credentials.

2. Copy ONLY the HW3.py python script from the unzipped folder onto the csgrads1 server (on your own home directory on csgrads1) (e.g. using ftp applications like FileZilla, WinSCP)

3. Change the file permissions by using 'chmod' command like
	
    {csgrads1:~} chmod 777 HW3.py
    or manually by going into properties and selecting all R,W,X for Owner,Group,Others. Refresh the directory.

4. The next steps are executed to ensure correct python version and libraries are downloaded and used.
	
    1. {csgrads1:~} unset PYTHONPATH
    2. {csgrads1:~} unset PYTHONHOME
	  3. {csgrads1:~} python    (# python version will be displayed)
		  		>>> exit()
	  4. {csgrads1:~} pip install nltk --user				(# install nltk)
	
	Ignore the upgrade pip warning.

5. Import Wordnet Lemmatizer, Stopwords libraries by running the following command:
	   
     {csgrads1:~} python
		 
        >>> import nltk
        >>> nltk.download('punkt')
        >>> nltk.download('stopwords')
        >>> nltk.download('wordnet')
        >>> nltk.download('averaged_perceptron_tagger')
	
6. Run the HW3.py file passing Cranfield directory path and query file path under single quotes as a command line argument like
	  
    {csgrads1:~} python HW3.py '/people/cs/s/sanda/cs6322/Cranfield' '/people/cs/s/sanda/cs6322/hw3.queries'
   
7. The output will get printed on the terminal console.  (Also available in the HW3.txt file)
