import pandas as pd
import re


def_line_spacing=10
def_char_spacing=6
head_line_Y=371
csv_file="/home/selvaprakash/BillD/CSV/Latta.csv"
new_csv_file="/home/selvaprakash/BillD/CSV/Latta_enh_clean.csv"

def cleanup_text_file(csv_file,new_csv_file):
    def_line_spacing=10
    def_char_spacing=6
    df=pd.read_csv(csv_file,sep='|')
    sorted_df = df.sort_values(by=['Y1','X1'])
    df = sorted_df.reset_index(drop=True)
    print (df)
    #df.to_csv("D:\Others\BillDog\CSV\Sorted_Peri1_enh.csv")
    word_space=0
    line_space=0
    word_space_arr=[]
    line_space_arr=[]
    counterX=0
    counterY=0
    if df['X1'].max()>1000 or df['Y1'].max()>1000:
        for i in range(1, len(df)):
            if df.loc[i]['X1']>df.loc[i - 1]['X2']:
                if re.match('[A-Z]', df.loc[i]['Word']):
                    word_space+=((df.loc[i]['X1']) - (df.loc[i - 1]['X2']))
                    counterX+=1
                    #print (type(df.loc[i]['Word']),df.loc[i]['Word'],df.loc[i]['X1'],df.loc[i - 1]['X2'],((df.loc[i]['X1']) - (df.loc[i - 1]['X2'])))
                    word_space_arr.append(((df.loc[i]['X1']) - (df.loc[i - 1]['X2'])))
            elif df.loc[i]['X1']<df.loc[i - 1]['X2']:
                    line_space+=((df.loc[i]['Y1']) - (df.loc[i - 1]['Y1']))
                    line_space_arr.append((df.loc[i]['Y1']) - (df.loc[i - 1]['Y1']))
                    counterY+=1

        avg_word_space=word_space/counterX
        avg_line_space=line_space/counterY
        def_char_spacing=avg_word_space
        def_line_spacing=avg_line_space
    #print (avg_line_space)

    #if df['X1'].max()>1000 or df['Y1'].max()>1000:

    #print ('def_line_space',def_line_spacing)
    df = df.sort_values(by=['Y1','X1'])
    for i in range(1, len(df)):
        if abs((df.loc[i]['Y1']) - (df.loc[i - 1]['Y1'])) <def_line_spacing:
            #print df.loc[i - 1]['Y1'], df.loc[i]['Y1'], df.loc[i - 1]['Word']
            df.at[i,'Y1']=df.loc[i - 1]['Y1']
        else:
            continue

    df = df.sort_values(by=['Y1','X1'])

    sorted_df = df.sort_values(by=['X1'])
    df = sorted_df.reset_index()

    for i in range(1, len(df)):
        if abs((df.loc[i]['X1']) - (df.loc[i - 1]['X1'])) <def_char_spacing:
            #print df.loc[i - 1]['Y1'], df.loc[i]['Y1'], df.loc[i - 1]['Word']
            df.at[i,'X1']=df.loc[i - 1]['X1']
        else:
            continue
    df = df.sort_values(by=['Y1','X1'])
    print (df)
    #df.to_csv(new_csv_file)
    df.to_csv(new_csv_file,sep='|')




def main():
    df_all = cleanup_text_file(csv_file,new_csv_file)
    print (df_all)



if __name__ == '__main__':
    main()