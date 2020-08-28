import feedparser
d = feedparser.parse('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000789019&type=10-Q&count=1&output=atom')
print(d['feed'])