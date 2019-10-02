#!/usr/bin/python2.7

import os
from flask import Flask, flash,request, redirect, url_for, render_template,send_from_directory,send_file
from werkzeug.utils import secure_filename
#import Consolidated
import requests
import datetime
import pandas as pd
import img_to_csv


URL='https://www.pythonanywhere.com/user/selvaprakash/files'

UPLOAD_FOLDER = '/home/selva/PycharmProjects/BillDog/static/Uploaded_Images/'
src_img_folder ='/static/Uploaded_Images'
csv_folder='/home/selva/PycharmProjects/BillDog/CSV'
t=datetime.datetime.now()
up_file_loc=''


item_coor='0'
price_coor='0'
qty_coor='0'
amt_coor='0'

item_coor_x='0'
price_coor_x='0'
qty_coor_x='0'
amt_coor_x='0'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

application = Flask(__name__)
application.secret_key = 'my unobvious secret key'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route('/scr_fileupload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'screen_img_file' not in request.files:
            print ('no files')
            flash('No file part')
            return redirect(request.url)
        file = request.files['screen_img_file']


        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print (filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            up_file=os.path.join(application.config['UPLOAD_FOLDER'], filename)
            #print current_app.root_path
            #return redirect(url_for('uploaded_file',filename=csv_file_name))
            #file_full_path=UPLOAD_FOLDER+csv_file_name
            return redirect(url_for('config_screen',up_file = filename))
    return render_template('scr_fileupload.html')



@application.route('/scr_config1')
def config_screen_start():
    return render_template('screen_config.html')

@application.route('/scr_config', methods=['GET', 'POST'])
def config_screen():
    print(request.args['up_file'])
    up_file = request.args['up_file']
    df_field = pd.DataFrame(columns=["Field","Position"])
    df_coord = pd.DataFrame(columns=["Coord_X","Coord_Y", "Position"])
    df_maxxy = pd.DataFrame(columns=["Field", "Coord_X","Coord_Y"])
    if request.method == 'POST':
        print 'inside post'
        #print request.form['field1']
        # item_coor = request.form['item']
        # print item_coor
        # price_coor = request.form['price']
        # qty_coor = request.form['qty']
        # amount_coor = request.form['amount']

        f = request.form
        for field in request.form.items():
            if field[0].startswith('field'):
                df_field = df_field.append({'Field': field[1],'Position': int(field[0][5:]) },ignore_index=True)
            if field[0].startswith('coord'):
                df_coord = df_coord.append({'Coord_X': int(field[1].split(';')[0]),'Coord_Y': int(field[1].split(';')[1]), 'Position': int(field[0][5:])}, ignore_index=True)


        print 'df_field',df_field
        print 'df_coord', df_coord
        print 'df_maxxy',df_maxxy
        df = pd.merge(df_field, df_coord, how='inner',  left_on = 'Position', right_on = 'Position')

        for field in request.form.items():
            if field[0].startswith('maxxy'):
                df = df.append({'Field':'maxxy','Coord_X': int(field[1].split(';')[0]),'Coord_Y': int(field[1].split(';')[1])}, ignore_index=True)
        # df["Position"] = df["Position"].astype(int)
        # df["Y"] = df["Y"].astype(int)
        print 'df',df
        df = df.sort_values(by=['Position']).reset_index().drop(labels=['Position','index'],axis=1)
        print 'df', df

        up_file=UPLOAD_FOLDER+up_file
        print up_file
        img_to_csv.main( df,up_file)
        return render_template('upload_img.html')
    return render_template('screen_config.html')

@application.route('/process_img', methods=['GET', 'POST'])
def upload_file_api():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            csv_file_name=Consolidated.main(UPLOAD_FOLDER+'/'+file.filename)
            excel_file_name='Converted_Bill_'+t.strftime('%Y%m%d%H%M%S')+'.xlsx'
            #print current_app.root_path
            #return redirect(url_for('uploaded_file',filename=csv_file_name))
            #file_full_path=UPLOAD_FOLDER+csv_file_name
            #return (csv_file_name)
            return send_file(csv_file_name,as_attachment=True,mimetype ='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',attachment_filename=excel_file_name)
    return render_template('upload_img.html')
#    return self

'''
@application.route('download/<filename>')
def uploaded_file(filename):
    file_full_path=UPLOAD_FOLDER+filename
    print ('Final File Path', file_full_path)
    return send_file(file_full_path)

    #requests.get(file_full_path)
'''

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()