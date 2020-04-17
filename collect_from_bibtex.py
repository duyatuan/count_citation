#! /usr/bin/env python
import time
import random
import sys
import os
import scholar
from scholar import *
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
from bibtexparser.customization import homogenize_latex_encoding

def search_phrase(querier, article):
  query = SearchScholarQuery()
  query.set_phrase(article['title'])
  query.set_scope(True)
  querier.send_query(query)
  articles = querier.articles
  duplicate = 0
  if len(articles) > 1:
    print('There are more than 1 results ({}) with the search phrase: {}. Only return one with the highest citation and with the same year'.format(len(articles), article['title']))
    duplicate = 1
  max_citations = 0;
  for art in articles:
    num_citations = art.__getitem__('num_citations')
    year = art.__getitem__('year')
    if num_citations > max_citations and year == article['year']:
      max_citations = num_citations
  result = {}
  result['num_citations'] = max_citations
  result['duplicate'] = duplicate
  time.sleep(random.randint(60, 300))
  return result

def parse_bibtex(filename):
  with open(filename) as bibtex_file:
    parser = BibTexParser()
    parser.customization = convert_to_unicode
    #parser.customization = homogenize_latex_encoding
    bib_db = bibtexparser.load(bibtex_file, parser=parser)
  print("Parsed the bibtex file, there are {} entries\n".format(len(bib_db.entries)))
  all_articles = []
  for entry in bib_db.entries:
    title = "{}".format(entry['title'])
    title = title.replace("  ", " ").replace("\n", " ").replace("\r", "").replace("{","").replace("}","")
    year = "{}".format(entry['year'])
    if 'author' in entry:
      author = entry['author']
      author = author.encode('ascii', 'ignore').decode('ascii')
      author = author.replace("  ", " ").replace("\n", " ").replace("\r", "").replace("{","").replace("}","")
    else:
      continue
    article = {}
    article['title'] = title
    article['year'] = year
    article['author'] = author
    all_articles.append(article)
  print(all_articles)
  return all_articles

def get_result_num_citation(result):
  return result['num_citations']

def main():
  ScholarConf.LOG_LEVEL = 1 
  ScholarUtils.log('info', 'using log level %d' % ScholarConf.LOG_LEVEL)
  querier = ScholarQuerier()
  settings = ScholarSettings()
  settings.set_citation_format(ScholarSettings.CITFORM_BIBTEX)
  querier.apply_settings(settings)

  conferences = ['cases_2000', 'cases_2001', 'cases_2002', 'cases_2003', 'cases_2004', 'cases_2005']
  #conferences = ['cases_2000', 'cases_2001', 'cases_2002', 'cases_2003', 'cases_2004', 'emsof_2001', 'emsof_2002', 'emsof_2003', 'emsof_2004', 'codes_isss_2003', 'codes_isss_2004']
  #conferences = ['codes_isss_2004_2']

  for conf in conferences:
    print('============================================')
    print('============================================')
    print('START CONFERENCE: {}'.format(conf))
    print('============================================')
    print('============================================')
    all_results = []
    f = open("result20/{}.csv".format(conf), "w")
    f.write("Title\tAuthor\tYear\tNum Citations\tDuplicate\n")
    #parse bibtex file
    all_articles = parse_bibtex('{}.bib'.format(conf))
    count = 0
    for article in all_articles:
      result = search_phrase(querier, article)
      article.update(result)
      all_results.append(article)
      print('Title = {},  num citations = {}'.format(article['title'], result['num_citations']))
    all_results.sort(key=get_result_num_citation, reverse=True)
    for result in all_results:
      f.write("{}\t{}\t{}\t{}\t{}\n".format(result['title'], result['author'], result['year'], result['num_citations'], result['duplicate']))
      count = count + 1
      if count >= 15:
        print('Reaching 15 acticles count, sleep for 30-45 minutes')
        time.sleep(random.randint(60*30, 60*45))
        count = 0
    f.close()

if __name__ == "__main__":
  sys.exit(main())

