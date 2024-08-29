from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from pdf2docx import Converter
import os

app = Flask(__name__)

# Répertoire de stockage pour les fichiers téléchargés
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        if file and file.filename.endswith('.pdf'):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Convertir le PDF en DOCX
            docx_filename = filename.replace('.pdf', '.docx')
            docx_path = os.path.join(app.config['UPLOAD_FOLDER'], docx_filename)
            
            converter = Converter(file_path)
            converter.convert(docx_path, start=0, end=None)
            converter.close()
            
            return redirect(url_for('conversion_result', filename=docx_filename))
    
    return render_template('index.html')

@app.route('/result/<filename>')
def conversion_result(filename):
    return render_template('result.html', filename=filename)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
