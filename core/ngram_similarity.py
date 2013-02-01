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
import json

class NGramSimilarity(object):
	
	"""docstring for NGramSimilarity"""
	def __init__(self, filename):

		self.filename = filename
		self.load(self.filename)

	def compare(self, other):
		
		if not isinstance(other, NGramSimilarity):
		    raise TypeError("can't compare NGramSimilarity with non-NGramSimilarity")

		somegrams = 0
		allgrams = 0

		for gram in self.grams:
			allgrams += gram[1]
			for i in ( i for i in other.grams if i[0] == gram[0] ):
				somegrams += gram[1]

		return self.similarity(somegrams,allgrams)

	def similarity(self, samegrams, allgrams, warp=1.0):

	    if abs(warp - 1.0) < 1e-9:
	        similarity = float(samegrams) / allgrams
	    else:
	        diffgrams = float(allgrams - samegrams)
	        similarity = ((allgrams ** warp - diffgrams ** warp)
	                / (allgrams ** warp))

	    return similarity

	def load(self, filename):

		handler = open (filename)
		ngram = json.loads(handler.read())

		self.ngram   = ngram['ngram']
		self.case    = ngram['case']
		self.grams    = ngram['grams']
		
		handler.close()
