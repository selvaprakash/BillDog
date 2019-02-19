#!/usr/bin/python2.7

import pandas as pd
import io
import os
import cv2

from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='d:\BillD\BillDog-018b2ee1875d.json'
image_path='D:\BillD\\new\gfqty.png'
csv_file="'D:\BillD\\new\gfqty_png.csv"
rotated_img="'D:\BillD\\new\gfqty_png_rotated1.jpg"


def detect_text(path,csv_file):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    df = pd.DataFrame(columns=["Word_Count","Word", "X1", "Y1", 'X2', 'Y2'])
    #print (df.columns)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    #print('Texts:')
    #print texts
    ind=0

    # Take First Word

    for text,i in zip(texts,range(0,len(texts))):

    	# Send the same to Data Frame to be sent for Processing
        df=df.append({'Word_Count':i,'Word':(text.description).encode("ascii", "ignore")  ,'X2':0,'Y2':0,"X1":format(text.bounding_poly.vertices[0].x),"Y1":format(text.bounding_poly.vertices[0].y)},ignore_index=True)
        df=df.append({'Word_Count':i,'Word':(text.description).encode("ascii", "ignore"),'X1':0,'Y1':0,"X2":format(text.bounding_poly.vertices[1].x),"Y2":format(text.bounding_poly.vertices[1].y)},ignore_index=True)
			#df=df.append({'Word':(text.description),"X":format(text.bounding_poly.vertices[2].x),"Y":format(text.bounding_poly.vertices[2].y)},ignore_index=True)
    	#df=df.append({'Word':(text.description),"X":format(text.bounding_poly.vertices[3].x),"Y":format(text.bounding_poly.vertices[3].y)},ignore_index=True)

    #df=df.reset_index()
    #print (df.columns)
    #df=df.set_index('index')
    #df=df.reset_index(drop=True)

    df1= df.groupby(['Word_Count','Word']).max()
    #df.to_csv(csv_file)
    #df1= (df.groupby(df['Word_Count']).max())
    df1=df1.reset_index()
    df1=df1.loc[df1['Word_Count']>0]

    #print (df.columns)
    #print (df1)

    df1.to_csv(csv_file,sep='|')
    #print (df1)
    return


def main():
    df_all = detect_text(image_path,csv_file)
    #print df_all



if __name__ == '__main__':
    main()