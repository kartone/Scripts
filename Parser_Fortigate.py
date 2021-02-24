import re
from alive_progress import alive_bar

def search_pattern(l,f):
    p = re.compile('.*,'+f+'=(.*?),')
    m = re.match(p,l)
    return m
    
def main():
    pattern_str = ['date','time','type','action','dstcountry','dstip','dstport','logid','rcvdbyte','sentbyte','service','srccountry','srcip','srcport']
    num_lines = sum(1 for line in open('totalone1.csv'))
    #num_lines = 26354677
    with open('totalone1.csv', 'r') as f:
        with open('totalone1_parsed.csv', 'w') as w:
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
