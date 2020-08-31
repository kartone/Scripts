import pandas as pd

df = pd.read_csv('./log.txt', sep='\s+')
df.drop(df.columns[[1, 4, 5, 6, 8,9,10,13,14]], axis = 1, inplace = True) 
df.columns = ['Timestamp', 'Remote', 'Local', 'Status', 'Query', 'UserAgent']
df['Remote'] = df['Remote'].apply(lambda x: x[ 0 : x.index(':')])
df['Local'] = df['Local'].apply(lambda x: x[ 0 : x.index(':')])

ddf= df.loc[df['Remote'] == '54.154.28.200']

print(ddf)

#ddf = df.value_counts(['Remote', 'Local']).reset_index(name='Counts')
# pd.set_option('display.max_columns', None)
#print(ddf)