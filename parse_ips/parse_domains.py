import collections
import urllib.request
import re

URL="https://en.wikipedia.org/wiki/Domain_name"

STOP_DOMAINS = set(['png', 'html', 'svg', 'pdf', 'styles', 'php', 'xml', 'ico', 'txt', 'xhtml', 'asp', 'toc', 'noscript', 'btitle', 'jtitle', 'jpg', 'htm'])

def prase_domains(content):
    DOMAINS = set()
    TOP_DOMAINS = collections.Counter()

    for d in re.findall(r'(?:^|(?<=[^A-Za-z_0-9\.]))[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)+(?:(?=[^A-Za-z_0-9\.])|$)', content):
        top_domain = d.split('.')[-1].lower()

        if (top_domain in STOP_DOMAINS) or (len(top_domain) > 8): continue 
            
        DOMAINS.add(d)
#        TOP_DOMAINS[top_domain] += 1

#    print (TOP_DOMAINS)

    return list(DOMAINS)

# Download the content of a page with description of domains
content = urllib.request.urlopen(URL).read().decode('utf-8')

print(prase_domains(content))
