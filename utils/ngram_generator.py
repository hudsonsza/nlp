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

"""N-Gram Generator:
  Generate n-grams from cleaned wikipedia dumps. Follow the above directory
  structure:

  language (ISO code, 2 letters)
    directory AA
      wiki_00 - file with cleaned text
      wiki_01 - file with cleaned text
      ...
      wiki_99 - file with cleaned text
    directory AB
    ...

  This structure is created by the WikiExtractor.py script.

  This script will create n-grams for one language and save the n most commons

  Usage example:

    ls -1 clean/ | parallel python utils/ngram_generator.py 1,2,3 1000 {} clean/{} data/ngram/

"""

import os
import core.ngram
import sys

if __name__ == '__main__':

  ns        = sys.argv[1]
  top       = int (sys.argv[2])

  language  = sys.argv[3]
  inputdir  = sys.argv[4]
  outputdir = sys.argv[5]

  if ',' in ns:
    ns = [int (n) for n in ns.split(',')]
  else:
    ns = [int (ns)]

  for n in ns:

    # create n-gram for this language
    gram = core.ngram.NGram (n)

    for root, dirname, filenames in os.walk (inputdir):
      for filename in filenames:
        dump = os.path.join (root, filename)

        if os.path.isfile (dump):
          gram.processFile (dump)

    outputFile = language + '_' + str(n) + 'gram_' + str(top) + '.txt'
    outputFile = os.path.join (outputdir, outputFile)

    gram.saveTop (outputFile, top)