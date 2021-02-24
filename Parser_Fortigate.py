import sys
import re
from alive_progress import alive_bar

# First argument is the source file to be parsed, output will be saved into the second argument
# First argument should be a merge of all FGT fw logs as they are extracted from firewall or from Fortianalyzer
filename = sys.argv[1]
file_parsed = sys.argv[2]

#filename = ''
#file_parsed = ''

def search_pattern(l,f):
    p = re.compile('.*,'+f+'=(.*?),')
    m = re.match(p,l)
    return m
    
def main():
    # Fields to be extracted from the logs and saved into the output file
    pattern_str = ['date','time','type','action','dstcountry','dstip','dstport','logid','rcvdbyte','sentbyte','service','srccountry','srcip','srcport']
    num_lines = sum(1 for line in open(filename))
    with open(filename, 'r') as f:
        with open(file_parsed, 'w') as w:
            with alive_bar(num_lines) as bar:
                for line in f.readlines():
                    for field in pattern_str:
                        match = search_pattern(line, field)
                        if match is None:
                            s = ','
                        else:
                            if field == 'srcport':
                                s = '{}'.format(match.group(1))
                            else:
                                s = '{},'.format(match.group(1))
                        w.write(s)
                    w.write('\n')
                    bar()
if __name__ == '__main__':
    main()
