#!/usr/bin/env python
"""
Simple tool to display topic modeling results generated by NMF, as stored in one or more PKL files.

Requires prettytable:
https://code.google.com/p/prettytable/
"""
import logging as log
from optparse import OptionParser
import unsupervised.nmf, unsupervised.rankings

# --------------------------------------------------------------

def main():
	parser = OptionParser(usage="usage: %prog [options] results_file1 results_file2 ...")
	parser.add_option("-t", "--top", action="store", type="int", dest="top", help="number of top terms to show", default=10)
	parser.add_option("-l","--long", action="store_true", dest="long_display", help="long format display")
	(options, args) = parser.parse_args()
	if( len(args) < 1 ):
		parser.error( "Must specify at least one topic modeling results file produced by NMF" )
	log.basicConfig(level=20, format='%(message)s')
	# number of columns to use when displaying topics
	column_size = 8

	# Load each cached ranking set
	for in_path in args:
		(doc_ids, terms, term_rankings, partition, W, H, labels) = unsupervised.nmf.load_nmf_results( in_path )
		log.info( "- Loaded model with %d topics from %s" % (len(term_rankings), in_path) )
		log.info( "Top %d terms for %d topics:" % (options.top,len(term_rankings)) )
		m = unsupervised.rankings.term_rankings_size( term_rankings )
		# display line by line?
		if options.long_display:
			log.info( unsupervised.rankings.format_term_rankings_long( term_rankings, labels, min(options.top,m) ) )
		else:
			# wrap columns to improve readability
			current = 0
			while current < len(term_rankings):
				current_end = min(current+column_size,len(term_rankings))
				current_rankings = term_rankings[current:current_end]
				current_labels = labels[current:current_end]
				log.info( unsupervised.rankings.format_term_rankings( current_rankings, current_labels, min(options.top,m) ) )
				current += column_size

# --------------------------------------------------------------

if __name__ == "__main__":
	main()