#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import urllib2
import csv

def lerCsv(inFile,outFile):
	csvIn = open(inFile)
	csvOut = open(outFile,'w')

	fieldNames = ['title', 'abstract', 'keywords', 'doi', 'url', 'bibtex']
	reader = csv.DictReader(csvIn)
	writer = csv.DictWriter(csvOut, fieldnames=fieldNames,  delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

	writer.writeheader()  
	row_number = 1

	for row in reader:
		
		print row_number,
		
		rowOut = consultarAbstractKeywords(row['URL'])

		bibtex = montarBibtex(row, rowOut, row_number)

		writer.writerow({'title': row['Item Title'], 
			             'abstract' : rowOut['abstract'], 
			             'keywords' : rowOut['keywords'],
			             'doi' : row['Item DOI'], 
			             'url' : row['URL'],
			             'bibtex' : bibtex
			            })			 
		row_number = row_number + 1		
	csvIn.close()
	csvOut.close()

def consultarAbstractKeywords(url):
	fo = urllib2.urlopen(url)
	page = fo.read()

	keyword = re.search("\'Keywords\'\:\'(?P<keyword>.*?)\,\\n", page)
	#title = re.search('<meta name="citation_title" content="(?P<title>.*?)"\/>', page)
	abstract = re.search('<h2 class=\"Heading\">Abstract<\/h2><p class=\"Para\">(?P<abstract>.*?)<\/p>', page)
	print "Lendo URL [" + url + "]"

	if not abstract:
	   print "    nao achou abstract"
	else: 	
		abstract = abstract.group('abstract')

	if not keyword:
	   print "    nao achou keywords"
	else: 	
		keyword = keyword.group(1)

	return {'abstract' : abstract, 'keywords' : keyword}

def montarBibtex(row, rowOut, row_number):
	bibtex = "@"

	if row['Content Type'] == "Chapter":
	   bibtex = bibtex + "inproceedings"
	elif row['Content Type'] == "Article":
	   bibtex = bibtex + "article"
	else:
	   bibtex = bibtex + "article"
	   print "Tipo bibtex [" + row['Content Type'] + "] desconhecido. Assumindo article",

	bibtex = bibtex + "{"  

	last_name = row['Authors'].split()

	if len(last_name) == 0:
		last_name = "ref"
	elif last_name == "PhD" or last_name == "MSc" or last_name == "BSc" or last_name == "Jr":
	   last_name = last_name[0]
	else:
	   last_name = last_name[1] 		

	reference = last_name + row['Publication Year'] + "_" + str(row_number)

	bibtex = bibtex + reference + ", " 
	bibtex = bibtex + "title = {" + row['Item Title'] + "}, " 
	bibtex = bibtex + "author = {" + row['Authors'] + "}, "  
	bibtex = bibtex + "year = {" + row['Publication Year'] + "}, "  
	if rowOut['abstract']: 
	    bibtex = bibtex + "abstract = {" + rowOut['abstract'] + "}, "  
	if rowOut['keywords']:
		bibtex = bibtex + "keywords = {" + rowOut['keywords'] + "} "  
	bibtex = bibtex + "}"

	return bibtex

lerCsv("res.csv","saida.csv")		