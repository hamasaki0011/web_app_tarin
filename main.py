from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload():
    
    file = request.files['file']
    print("file", file)
    
    if not file:
        return 'ファイルアップロードされていません.', 400
    if file.filename.endswith('.csv'):
        rows = []
        csv_file = file.stream.read().decode()
        # csv_file = file.stream.read().decode("SHIFT-JIS")
        csv_reader = csv.reader(csv_file.splitlines(), delimiter=',')
        for row in csv_reader:
            rows.append(row)
        return render_template('table.html', rows=rows)
    else:
        return 'CSVファイルではありません.', 400

if __name__ == '__main__':
    app.run(debug=True)