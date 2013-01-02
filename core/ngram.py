#
#  Copyright 2012-2013 Humberto R. H. Pereira 
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

"""N-Gram:
  Process text, generating overlapping n-gram statistics

  Overlapping n-grams are substrings with length n where the next substring add
  the next char and remove the last from the actual gram.

  For example a bi-gram (2-gram) from the string "BIGRAM":

  1. $B
  2. BI
  3. IG
  4. GR
  5. RA
  6. AM
  7. A$

  One important observation is about the beginning and the end of the corpus 
  (source string), we use a special char to identify grams from the beginning
  and the end because some score may use. 

  All text is UTF-8

  Usage:

  	trigram = NGram (3)
	
	for filename in os.listdir ('/usr/share/dict/'):
		if os.path.isfile (filename):
			trigram.processFile (filename)

	trigram.saveTop ('trigram_1000.txt', 1000)

"""

import codecs
import collections
import os
import re
import string
import types


def decode_utf8(s):
	if isinstance(s, unicode):
		return s

	return s.decode('utf-8')

class NGram:

	translate_table = dict((ord(char), None) for char in string.punctuation)


	def __init__(self, ngram=3, maintainCase = False):
		self.ngram   = ngram

		self.grams   = collections.defaultdict(int)
		self.endings = collections.defaultdict(int)

		self.maintainCase = maintainCase

	def processFile(self, filename):
		handler = codecs.open (filename, mode='r', encoding='utf-8')
		data    = handler.read ()
		handler.close ()

		self.process (data)

	def process(self, text):
		"""Creates n-grams from characters."""
		ngram = self.ngram

		if not self.maintainCase:
			text = text.lower ()

		# remove punctuation
		text = text.translate (self.translate_table)

		# transform numbers in zero
		text = re.sub(r"\d" , '0', text)

		# normalize multiple tabs / spaces
		text = re.sub(r"\s+", " ", text)
		text = text.strip()

		# Transform to unicode to ensure proper behaviour.
		text = decode_utf8(text)

		# insert beginning and end marks
		text = '$' * (ngram - 1) + text + '$' * (ngram - 1)

		for i in range(len(text) - ngram + 1):
			gram = text[i:i + ngram]
			self.grams[gram] += 1

	def top (self, n):
		"""Return top n grams sorted by occurrence"""
		tuples = zip (self.grams.keys (), self.grams.values ())

		# order by value descending
		tuples.sort (key=lambda tuple: -tuple[1])
		
		# get the n first grams
		tuples = tuples[:n]

		return tuples

	def eliminateFrequences(self, num):
		"""Eliminates all n-grams with a frequency <= num"""
		for x in self.grams.keys ():
			if self.grams[x] <= num:
				value = self.grams[x]
				del self.grams[x]
				self.endings[x[:-1]] -= value

 
	def toString (self, tuples=None):

		if isinstance (tuples, types.NoneType):
			tuples = zip (self.grams.keys (), self.grams.values ())

			# order by value descending
			tuples.sort (key=lambda tuple: -tuple[1])

		ngram  = str (self.ngram)
		case   = str (self.maintainCase)

		return ngram + "\n" \
			+ case   + "\n" \
			+ "\n".join (map (lambda x: x[0] + ' ' + str (x[1]), tuples))

	def save (self, filename):
		handler = codecs.open (filename, mode='w', encoding='utf-8')
		handler.write (self.toString ())
		handler.close ()

	def saveTop (self, filename, n):
		tuples  = self.top (n)

		handler = codecs.open (filename, mode='w', encoding='utf-8')
		handler.write (self.toString (tuples))
		handler.close ()

	def load (self, filename):
		handler = open (filename)
		ngram   = int (handler.readline ())
		case    = (handler.readline ().strip () == 'True')

		for line in handler.readline ():
			gram = line[:ngram]
			perc = int (line[ngram + 1:])

			self.grams[gram] = perc

		self.ngram        = ngram
		self.maintainCase = case

		handler.close ()