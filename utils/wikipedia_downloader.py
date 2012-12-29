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

#
# Download lastest wikipedia dumps bziped with all articles
#
# 

import os
import re
import urllib2

class WikipediaDownloader:

	DOWNLOAD_CHUNK_SIZE = 8096 # 8 Kb

	WIKI_MIRROR = 'http://wikipedia.c3sl.ufpr.br/'
	DATE_REGEX  = re.compile('href="([0-9]{4}[01][0-9][0-3][0-9])/"')

	# ex. http://wikipedia.c3sl.ufpr.br/ptwiki/20121210/ptwiki-20121210-pages-articles-multistream.xml.bz2
	URL_DUMP_FORMAT = '%s/%swiki/%s/%swiki-%s-pages-articles-multistream.xml.bz2'

	# ex. ptwiki-20121210-pages-articles-multistream.xml.bz2
	OUTPUT_FILE_FORMAT  = '%swiki-%s-pages-articles-multistream.xml.bz2'

	def __init__ (self, languages, outputDir, verbose = False):

		self.languages = languages
		self.verbose   = verbose
		self.outputDir = outputDir

		if not os.path.isdir(self.outputDir):
			os.makedirs (self.outputDir)

	def download (self):

		for language in self.languages:
			if self.verbose:
				print "[+] Getting", language, "wiki dump"

			self.downloadLanguage(language)

	def downloadLanguage (self, language):

		url = self.WIKI_MIRROR + language + 'wiki/'

		if self.verbose:
			print "    [+] Downloading", url

		data = ''

		try:
			handler = urllib2.urlopen(url)
			data    = handler.read()
			handler.close()
		except IOError as e:
			if self.verbose:
				print "        [!] Error downloading", url, "(", e.strerror, ")"

			return

		dates = self.DATE_REGEX.findall(data)

		# get the newer dump
		dates.sort()
		dumpDate = dates[-1]

		url = self.URL_DUMP_FORMAT % (self.WIKI_MIRROR, language, dumpDate, language, dumpDate)

		outputFile = self.OUTPUT_FILE_FORMAT % (language, dumpDate)
		outputFile = os.path.join(self.outputDir, outputFile)

		if self.verbose:
			print "    [+] Downloading", url

		if os.path.isfile (outputFile):
			if self.verbose:
				print "        [-] File already downloaded", outputFile

			return

		try:
			handler = urllib2.urlopen(url)
			output  = open(outputFile, 'wb')

			while True:
				data = handler.read(self.DOWNLOAD_CHUNK_SIZE)
				output.write(data)

				# end of file
				if len(data) < self.DOWNLOAD_CHUNK_SIZE:
					break

			output.close()
			handler.close()

		except IOError as e:
			if self.verbose:
				print "        [!] Error downloading", url, "(", e.strerror, ")"

			# delete the corrupted file
			if os.path.isfile (outputFile):
				os.unlink (outputFile)


if __name__ == '__main__':

	languages = ['ar', 'bg', 'ca', 'cs', 'da', 
	'de', 'el', 'en', 'eo', 'es', 'et', 'eu', 
	'fa', 'fi', 'fr', 'gl', 'he', 'hr', 'hu', 
	'id', 'it', 'ja', 'ko', 'lt', 'mk', 'ms', 
	'nl', 'no', 'pl', 'pt', 'ro', 'ru', 'sh',
	'sk', 'sl', 'sr', 'sv', 'th', 'tr', 'uk',
	'vi', 'zh', ]

	downloader = WikipediaDownloader(languages, 'downloads', True)
	downloader.download()
