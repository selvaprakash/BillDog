import pandas as pd
import cleanup_text_file
import csv

df = pd.read_csv('D:\BillD\CSV\gofrugal.png_final_clean_20180827042607.csv', sep='|')
df = df.loc[df['Y1'] > 55]  # & df['Y1']<175 & df['X1']<400
df = df.loc[df['X1'] > 5]
df = df.loc[df['Y1'] < 175]
df = df.loc[df['X1'] < 400]
print df
df['Word']=df['Word'].astype(str)
df=df[['X1','Y1','X2','Y2','Word']]
df=df.reset_index()
#df=pd.DataFrame(columns=df['Word','Y1'])
sepchar=[]
colpos=[66]
for i in range(0,len(df)):
    print df.loc[i]['X1']
    if (df.loc[i]['X1']>66 and df.loc[i]['X1']<70):
        print df.loc[i]['X1'],  df.loc[i]['Word']
        sepchar.append(',')
    else :
        print df.loc[i]['X1'], df.loc[i]['Word']
        sepchar.append(' ')
    # print sepchar
#print df
df['sepchar']=sepchar
print df
df['wordsepchar']=df['sepchar']+df['Word']
print df['wordsepchar']
df = df.groupby('Y1')['wordsepchar'].apply(lambda (x): x.str.cat(sep='', na_rep='?'),)
df=df.to_frame()
print list(df.columns.values)
#df= df['wordsepchar']
print df
df.to_csv('D:\BillD\CSV\gofrugal_part1.csv',quoting=csv.QUOTE_NONE, quotechar="",  escapechar=" ")