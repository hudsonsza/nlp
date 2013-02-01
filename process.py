#!/bin/env python
#
#  Copyright 2013 Hudson A. de Souza
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import os
from core.ngram import NGram
from core.ngram_similarity import NGramSimilarity

if __name__ == '__main__':

	trigram = NGram (3)
	
	files = [
		{
			'name'	: 'sample text in pt',
			'txt'	: 'data/tests/doc1.txt',
			'dat'	: 'data/tests/doc1.dat'
		},
		{
			'name'	: 'sample text in en',
			'txt'	: 'data/tests/doc2.txt',
			'dat'	: 'data/tests/doc2.dat'
		},
	]
		
	trigram.processFile ('data/tests/pt.txt')
	trigram.saveTop ('data/tests/pt.dat', 1000)
	print "\n[+] Load NGram in data/tests/pt.dat"
	pt = NGramSimilarity ('data/tests/pt.dat')

	docs = []
	for f in files:
		print "\n[+] Process -", f['name']
		
		print "        [-] Process NGram in", f['txt']
		trigram.processFile (f['txt'])
		
		print "        [-] Save NGram in", f['dat']
		trigram.saveTop (f['dat'], 1000)

		print "        [-] Load NGram in", f['dat']
		docs.append(NGramSimilarity (f['dat']))

	print ""
	for doc in docs:
		print doc.filename, 'is', doc.compare(pt)