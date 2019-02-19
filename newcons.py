
import pandas as pd
import os
import platform
from detect_text import detect_text
from enhance_image import img_pre_process
from cleanup_text_file import cleanup_text_file
from find_key_words import find_key_words
from find_item_end import find_item_end
from draw_split_lines import draw_split_lines
from arrange_items import arrange_items
#from to_excel import to_excel
import datetime
#from ifnohead import if_no_head
#from sendemail import sendmail
#from topdf import topdf
#import xlsxwriter




os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='D:\BillD\BillDog-018b2ee1875d.json'
src_image='D:\BillD\gofrugal.png' #IMG_20180314_135618731.jpg #IMG_20180603_143723969.jpg
csv_path = 'D:\BillD\CSV\\'
excel_path='D:\BillD\Excel\\'


def main(src_image):

    if platform.system() == 'Windows':
        slash = '\\'
    else:
        slash = '/'

    print slash

    src_path = src_image.rsplit(slash, 1)[0]
    src_file = src_image.rsplit(slash, 1)[1]
    src_file_name=src_file.rsplit('.', 1)[0]
    # print src_path,src_file_name
    t=datetime.datetime.now()
    print (t)
    resi_image=src_path+'/'+src_file_name+'_res_'+t.strftime('%Y%m%d%H%M%S')+'.jpg'
    final_image=src_path+'/'+src_file_name+'_final_'+t.strftime('%Y%m%d%H%M%S')+'.jpg'
    #print (enh_image)
    csv_file=csv_path+src_file+'_final_'+t.strftime('%Y%m%d%H%M%S')+'.csv'
    new_csv_file=csv_path+src_file+'_final_clean_'+t.strftime('%Y%m%d%H%M%S')+'.csv'
    img_to_excel=src_path+'/'+src_file+'_excel_'+t.strftime('%Y%m%d%H%M%S')+'.jpg'
    lined_img=src_path+'/'+src_file+'_line_'+t.strftime('%Y%m%d%H%M%S')+'.jpg'
    #print csv_file
    #print new_csv_file
    #print lined_img


    img_pre_process(src_image,resi_image,final_image,img_to_excel)
    detect_text(final_image,csv_file)
    cleanup_text_file(csv_file,new_csv_file)
    df=pd.read_csv(new_csv_file, sep='|')
    df = df.loc[df['Y1'] > 55 ]#  & df['Y1']<175 & df['X1']<400
    df=df.loc[df['X1'] > 5 ]
    df = df.loc[df['Y1'] < 175]
    df = df.loc[df['X1'] <400]
    df=df.groupby('Y1')['Word'].apply(lambda x: x.sum())


    print df
if __name__=='__main__':
    main(src_image)