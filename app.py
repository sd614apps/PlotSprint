import os
from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from dataset_plotter import read_dataset, plot_dataset
import shutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/datasets'
app.config['PLOT_FOLDER'] = 'uploads/plots'
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xlsx', 'json'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file found', 400
        file = request.files['file']
        if file.filename == '':
            return 'No file selected', 400
        if file and allowed_file(file.filename):
            file = request.files['file']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            file_type = file.filename.rsplit('.', 1)[1].lower()
            dataset, columns = read_dataset(file_path, file_type)

            plot_type = request.form['plot_type']
            x_col = request.form['x_col']
            y_col = request.form['y_col']
            aggregate_fn = request.form['aggregate_function']
            plot_filename = plot_dataset(dataset, plot_type, app.config['PLOT_FOLDER'], x_col, y_col, aggregate_fn)

            return jsonify({"plot_filename": plot_filename, "columns": columns})
    return render_template('index.html')

@app.route('/columns', methods=['POST'])
def get_columns():
    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    file_type = file.filename.rsplit('.', 1)[1].lower()
    dataset, columns = read_dataset(file_path, file_type)
    return jsonify(columns)

@app.route('/plot/<path:filename>')
def plot_image(filename):
    return send_from_directory(app.config['PLOT_FOLDER'], filename)

@app.route('/save', methods=['POST'])
def save_files():
    file_name = request.form.get('file_name')
    plot_name = request.form.get('plot_name')

    saved_datasets_folder = 'saved_datasets'
    saved_plots_folder = 'saved_plots'

    if not os.path.exists(saved_datasets_folder):
        os.makedirs(saved_datasets_folder)
    if not os.path.exists(saved_plots_folder):
        os.makedirs(saved_plots_folder)

    shutil.copy(os.path.join(app.config['UPLOAD_FOLDER'], file_name), saved_datasets_folder)
    shutil.copy(os.path.join(app.config['PLOT_FOLDER'], plot_name), saved_plots_folder)

    return "Files saved successfully."


if __name__ == '__main__':
    app.run(debug=True)
