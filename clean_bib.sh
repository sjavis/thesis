#!/bin/bash

# Remove empty lines, abstract, url, etc
sed -i '/^\s*$/d' library.bib
remove_fields=('abstract' 'url' 'doi' 'issn' 'isbn' 'annote' 'month' 'file' 'keywords' 'copyright' 'pmid' 'eprint' 'langid')
for field in "${remove_fields[@]}"; do
  sed -i "/^\s*$field =.*},\?$/d" library.bib
  sed -i "/^\s*$field =\s*{/,/},\?$/d" library.bib
  sed -i "/^\s*$field =.*$/d" library.bib
done
