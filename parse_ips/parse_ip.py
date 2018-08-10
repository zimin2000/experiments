import re, sys

# Version 1
# >>> re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '111.1.1.1 5551.1.1.223')
# or
# >>> re.findall(r'[12]?[0-9]?[0-9]\.[12]?[0-9]?[0-9]\.[12]?[0-9]?[0-9]\.[12]?[0-9]?[0-9]', '111.1.1.1 5551.1.1.223')
#
# Problems:
#   - will accept 999.999.999.999 or 257.1.1.1
#   - will extract from, but accept 9123.1.1.1  (will accept as 123.1.1.1)
#
# Can use this to filter good IPs:
#
#        for o in ip.strip('.'):
#            if int(o) > 255: break
#        else:
#            IPS[ip] += 1
#   
#  or this
#
#      if len(filter(lambda x: int(x) > 255, ip.strip('.'))) > 0:
#
#  Version 2: 
# >>> re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', '111.1.1.1 5551.1.1.223')
#  Problems:
#    - still can accept 1.2.3.4.5.6.7 (as . is \b)
#    - and 266.x.x.x
#  
#  Version 3:
# >>> re.findall(r'(?:(?<=[^\d\.])|^)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:(?=[^\d\.])|$)', '111.1.1.1 551.1.1.223')
#  The only known problem is 266.x.x.x
#
#  Version 4: (the best)
# >>> re.findall(r'(?:(?<=[^\d\.])|^)'+
#                '(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.'+
#                '(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.'+
#                '(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.'+
#                '(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])'+
#                '(?:(?=[^\d\.])|$)', l):
#
#  The only question is if 000.000.000.000 is a valid IP adddress.
#
#  Version 4a: 
#
# >>> re.findall(r'(?:(?<=[^\d\.])|^)'+
#                '(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\.'+
#                '(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\.'+
#                '(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\.'+
#                '(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])'+
#                '(?:(?=[^\d\.])|$)', l):
#

def approach1(f):
    IPS = set()

    for l in f:
        for ip in re.findall(r'(?:(?<=[^\d\.])|^)'+
                             '(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\.'+
                             '(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\.'+
                             '(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\.'+
                             '(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])'+
                             '(?:(?=[^\d\.])|$)', l):

            IPS.add(ip)

    return list(IPS)

#
# This is an uglier approach, but it is a kind of universal findall for the poor people.
#

def approach2(f):
    IPS = set()
    
    for l in f:
        while len(l) > 0:
            m = re.match(r'(^|.*[^\d\.])(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})([^\d\.].*|$)', l)
            if not m:
                break

            _, ip, l = m.groups()

            if len(list(filter(lambda x: int(x) > 255, ip.split('.')))) <= 0:
                IPS.add(ip)

    return list(IPS)


print(approach2(sys.stdin))
