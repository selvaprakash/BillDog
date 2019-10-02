#!/usr/bin/python2.7

import os
from flask import Flask, flash,request, redirect, url_for, render_template,send_from_directory,send_file
from werkzeug.utils import secure_filename
import Consolidated
import requests
import datetime

URL='https://www.pythonanywhere.com/user/selvaprakash/files'

UPLOAD_FOLDER = '/home/selva/BillDog/'
t=datetime.datetime.now()

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
        if 'file' not in request.files:
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
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            #print current_app.root_path
            #return redirect(url_for('uploaded_file',filename=csv_file_name))
            #file_full_path=UPLOAD_FOLDER+csv_file_name
            return render_template('screen_config.html')
    return render_template('scr_fileupload.html')

@application.route('/scr_fileupload_api', methods=['GET', 'POST'])
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