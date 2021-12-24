from flask import Flask ,url_for, redirect, render_template,send_file, abort,send_from_directory
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
import os
import pandas as pd
from datetime import datetime

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = '5f4d94e1da3bd8871282c8e4b2586a87'
app.config["UPLOAD_FOLDER"]="uploads/excel_uploads"
app.config["BASE_PATH_UPLOAD"] = os.path.dirname(app.instance_path)  +"/"+ app.config["UPLOAD_FOLDER"]

class UploadForm(FlaskForm):
    file = FileField()

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('uploads/excel_uploads' + "/" + filename)

        path_var = os.path.dirname(app.instance_path)  +"/"+ app.config["UPLOAD_FOLDER"] +"/" + filename
        dt = datetime.now()
        ts = dt.strftime("%Y%m%d_%H%M%S")
        tempfilename = f'{ts}{filename}'
        print(tempfilename)
        urlzz = f'{app.config["BASE_PATH_UPLOAD"]}/{tempfilename}' #make the path that we will save the file to.
        print(urlzz)
        df = pd.read_excel(path_var)
        print(df)
        df["x3"] = df["x2"] * 2        
        print(df)
        df.to_excel(urlzz)

        return render_template("download.html",form =form,url=tempfilename) #redirect(url_for('upload'))

    return render_template('upload.html', form=form)



@app.route('/excel_uploads/<path>')
def redownloaded_file(path):
    print (path)
    return send_from_directory(app.config["UPLOAD_FOLDER"], path)

if __name__ =="__main__":
    app.run(debug=True)