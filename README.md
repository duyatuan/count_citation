# count_citation
This is a clone from the repo: https://github.com/ckreibich/scholar.py.git
A wrapper collect_from_bibtex.py is added to parse the bibtex file which contains a collection of articles. Each article will be searched on Google Scholar using the scholar.py to extract the number of citations. The final results will be sorted base on the number of citations and written to a csv file.

Before running, make sure that the bibtex files are placed inside the bibtex folder. In the current implementation, since we don't know when Google is going to block us, it's better to list the files manually in each batch run. For example: 

'''
  conferences = ['cases_2000', 'cases_2001', 'cases_2002', 'cases_2003', 'cases_2004', 'cases_2005']
'''

Run command:

'''
python3 collect_from_bibtex.py
'''

