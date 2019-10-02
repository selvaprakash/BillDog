import requests
import json
import base64
import os
import re
import sys
import io
import pandas as pd
import csv
import numpy as np

from google.cloud import vision
from google.cloud.vision import types
from google.cloud import storage
#client = storage.Client()
#bucket = client.get_bucket('billdata')
#blob = bucket.get_blob('remote/path/to/file.txt')

#image_file= arg1


def detect_text(path): # Currently this is not being used
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    #print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])	

        print('bounds: {}'.format(','.join(vertices)))

def find_bound_coor(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    df = pd.DataFrame(columns=["Word", "X1", "Y1", 'X2', 'Y2'])

    response = client.text_detection(image=image)
    texts = response.text_annotations
    #print('Texts:')
    #print texts
    ind=0
    for text,i in zip(texts,range(0,len(texts))):

			# Send the same to Data Frame to be sent for Processing
			df=df.append({'Word_Count':i,'Word':(text.description),'X2':0,'Y2':0,"X1":format(text.bounding_poly.vertices[0].x),"Y1":format(text.bounding_poly.vertices[0].y)},ignore_index=True)
			df=df.append({'Word_Count':i,'Word':(text.description),'X1':0,'Y1':0,"X2":format(text.bounding_poly.vertices[1].x),"Y2":format(text.bounding_poly.vertices[1].y)},ignore_index=True)
			#df=df.append({'Word':(text.description),"X":format(text.bounding_poly.vertices[2].x),"Y":format(text.bounding_poly.vertices[2].y)},ignore_index=True)
			#df=df.append({'Word':(text.description),"X":format(text.bounding_poly.vertices[3].x),"Y":format(text.bounding_poly.vertices[3].y)},ignore_index=True)

    df1=df.groupby(['Word_Count','Word']).max()
    df1.to_csv("D:\Others\BillDog\Bill_contents_coor_bill2.csv")
    #print df1.sort(['Word_Count'])
    #df1.sort(['Word_Count']).to_csv("D:\Others\BillDog\Bill_contents_co_or.csv")
    df1 = df1.reset_index()
    df1.fillna(0)
    #df1 = pd.DataFrame.from_csv("D:\Others\BillDog\Bill_contents_coor_bill2.csv")
    dfy2 = pd.to_numeric(df1['Y2'])
    dfy2 = dfy2.to_frame()
    #print dfy2
    #standardizing Y co-ords
    for i in range(0, len(dfy2)):
        if abs(dfy2.iloc[i, 0] - dfy2.iloc[i - 1, 0]) <= 10:
            dfy2.iloc[i, 0] = dfy2.iloc[i - 1, 0]
            #print df.iloc[i,0]
    #print 'dfy2',dfy2
    df1['Y2']=dfy2['Y2']
    #print 'df1',df1
    df1.to_csv("D:\Others\BillDog\co-or-diffY0.csv")
    df1.reset_index()
    #print df1
    df1.X1=df1.X1.astype(int)
    df1.X2 = df1.X2.astype(int)
    df1.Y1 = df1.Y1.astype(int)
    df2 = df1.groupby(['Y2'])['X1'].min().sort_index( ascending=True)
    df2=df2.to_frame()
    df3 = df1.groupby(['Y2'])['X2'].max().sort_index( ascending=True)
    df3=df3.to_frame()
    df4=df2.join(df3, how='inner', lsuffix='Y2', rsuffix='Y2')
    df4.reset_index(inplace=True)
    df4.Y2 = df4.Y2.astype(int)
    df4['diff']=df4.X2-df4.X1
    df4.sort_values('Y2',inplace=True)
    df4['diff1']=df4.Y2-df4.Y2.shift(1)
    #df4= pd.DataFrame(df4).reset_index(drop=True)
    #print df4.sort_values('Y2')
    print df4
    #df4.to_csv("D:\Others\BillDog\co-or-diffY.csv")
    #print df4.filter(['diff']).mode()
    #print (df4.filter(['diff1']).mean()[0])
    #print (2*df4.filter(['diff1']).mean()[0])-3
    #print (2*df4.filter(['diff1']).mean()[0])
    y_start_end = df4.loc[df4['diff1']>(2*df4.filter(['diff1']).fillna(0).mean()[0]-10)]
    y_start_end = df4.loc[df4['diff1']>(2*df4.filter(['diff1']).fillna(0).mean()[0]-10)]
    #print 2*df4.filter(['diff1']).fillna(0).mean()[0]
    return y_start_end
    #y_start=y_start_end.iloc[0][0]
    #print y_start
    #y_end = y_start_end.iloc[2][0]
    #print y_end

def detect_text_uri(path): # User Google API to detect Text in the Image
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    df = pd.DataFrame(columns= ["Word","X","Y"])
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    #print('Texts:')
    #print texts
    ind=0
    for text in texts:

			# Send the same to Data Frame to be sent for Processing
			df=df.append({'Word':(text.description).encode('utf-8'),"X":format(text.bounding_poly.vertices[0].x),"Y":format(text.bounding_poly.vertices[0].y)},ignore_index=True)

    print df
    df.to_csv('/home/selva/PycharmProjects/BillDog/CSV/df.csv',sep='|')
    return df

def process_text(df1,min_x,max_x,min_y,max_y,df_coords,df_fields):

    #df = pd.DataFrame.from_csv("D:\Others\BillDog\Bill_contents.csv", index_col=None)
    df=df1
    #print 'df',df

    ####
    dfy2 = pd.to_numeric(df['Y'])
    dfy2 = dfy2.to_frame()
    dfy2.sort_values('Y', inplace=True)
    for i in range(0, len(dfy2)):
        if abs(dfy2.iloc[i, 0] - dfy2.iloc[i - 1, 0]) <= 10:
            dfy2.iloc[i, 0] = dfy2.iloc[i - 1, 0]
            # print df.iloc[i,0]
    #print 'dfy2', dfy2
    df['Y'] = dfy2['Y']
    ####

    df = df.loc[(df['Y']).astype(int) > min_y]

    df = df.loc[(df['Y']).astype(int) < max_y]
    df = df[['Word', 'X', 'Y']]
    df = df.reset_index().drop(labels='index',axis=1)
    df_c = df[['Word', 'X', 'Y']]
    #print df

    df['X']=pd.to_numeric(df['X'])
    int_array={}
    int_df=pd.DataFrame( columns=["Word","X","Y"])
    print 'df ', df
    df_c = df.groupby('Y')['Word'].apply(lambda x: "{%s}" % ' '.join(x))
    print ('df_c', df_c)
    print 'len',len(df_coords)
    for i in range(len(df_coords)):
        if i == 0:
            df_filter = (df.loc[(df.X >= df_coords[i]) & (df.X <= df_coords[i + 1] - 1)])
            print 'df_filter 0', df_filter
            int_df = (df_filter.iloc[:,0:3])
            int_df = int_df.groupby(['Y'])['Word'].apply(' '.join).reset_index()
            print 'int df grouped', int_df
            # int_df.rename(columns={"Word":df.iloc[i].loc['Field']},
            #                inplace=True)
        elif i < len(df_coords)-1:
            print df_coords[i],df_coords[i+1]
            print (df.loc[(df.X >= df_coords[i]) & (df.X <= df_coords[i+1] - 1)])
            #for j in range(len(df)):
            df_filter = (df.loc[(df.X > df_coords[i]) & (df.X < df_coords[i + 1] - 1)])
            print 'df_filter i', df_filter
            #int_array[str(i)] = (df_filter.iloc[:,0:3])
            int_df1 = (df_filter.iloc[:,0:3])
            # int_df1.rename(columns={"Word":df.iloc[i].loc['Field']},
            #                inplace=True)
            int_df1=int_df1.groupby(['Y'])['Word'].apply(' '.join).reset_index()
            int_df = int_df.merge(int_df1, how='outer', on ="Y")

                #print 'worked'
            #int_array[i].append(np.array(df.loc[(df.X > df_coords[i]) & (df.X < df_coords[i+1] - 1)]))
        else:
            print 'max ',df_coords[i], max_x
            df_filter= (df.loc[(df.X >= df_coords[i]) & (df.X <= max_x)])
            #int_array[str(i)] = (df_filter.iloc[i, 0])
            int_df1 = (df_filter.iloc[:,0:3])
            # int_df1.rename(columns={"Word":df.iloc[i].loc['Field']},
            #      inplace=True)
            int_df1 = int_df1.groupby(['Y'])['Word'].apply(' '.join).reset_index()

            int_df = int_df.merge(int_df1, how='outer',on ="Y")
        #int_array.update(int_array[i])
        #print 'int_array i', int_array
        print 'int df', int_df
        #df_c = df_c.groupby('Y')['Word'].apply(lambda x: "{%s}" % ' '.join(x))
    #int_df=pd.DataFrame.from_dict(int_array,orient='index')
    #print df_c
    print 'int_array final', int_df

    int_df_print = int_df.drop(columns= ['Y'])
    int_df_print.columns = df_fields
    print 'Printed DF', int_df_print

    pd.DataFrame.to_csv(int_df_print,'/home/selva/PycharmProjects/BillDog/CSV/int_df_print.csv')

    print('Done! Done! Done!')

def main(df_coords,inp_file):
    df = pd.DataFrame( columns=["Word","X","Y"])
    #y_start_end=find_bound_coor('/home/selva/BillDog/ExcelBill.png')
    df1=detect_text_uri(inp_file)
    #print 'df1',df1
    #y_start=y_start_end.iloc[0][0]
    #print y_start
    #y_end = y_start_end.iloc[2][0]
    #print y_end

    #df_coords.astype('int32').sort_values()


    print 'df_coords',df_coords
    min_x=df_coords['Coord_X'].min()
    min_y = df_coords['Coord_Y'].min()
    max_x= df_coords['Coord_X'].max()
    max_y= df_coords['Coord_Y'].max()
    print 'min max coords', min_x,max_x,min_y,max_y
    df_coords = (df_coords.loc[(df_coords.Field != 'maxxy')])
    process_text(df1,min_x,max_x,min_y,max_y,df_coords.iloc[:,1],df_coords.iloc[:,0])

# if __name__ == '__main__':
#     main(item_x,qty_x,price_x,amt_x)