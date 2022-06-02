import pandas as pd
import re
data = pd.read_csv('sample.tsv', delimiter='\t')
print(data)
# print(data.iloc[:,0].head())
df = data.dropna(axis=0, how='any')  # remove NaN
# print(df)

log_extract_pattern = re.compile(r'https://') # start with https:// 
ip_pattern = re.compile(r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+') # no ip addr
login_pattern = re.compile(r'(?:login|mail|signin)') # no login or personal mail
porn_pattern = re.compile(r'(?:pornhub|xvideos|xnxx)') # no porn websites
domain_name_pattern = re.compile(r'[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+/$') # probably home page
def regex_filter(val):
    if val:
        m1 = re.search(log_extract_pattern,val) 
        m2 = re.search(ip_pattern,val)
        n1 = re.search(login_pattern,val)
        n2 = re.search(porn_pattern,val)
        p = re.search(domain_name_pattern,val)
        
        if m1!=None and m2==None and n1==None and n2==None and p==None :
            return True
        else:
            return False
    else:
        return False

df_filtered = df[df.iloc[:,0].apply(regex_filter)]
print(df_filtered)

# res = data.apply(lambda row: row[0].match(log_extract_pattern), axis=1)
df_filtered.to_csv("res.tsv", sep='\t', index=False)