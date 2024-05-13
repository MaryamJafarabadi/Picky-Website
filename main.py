from website import create_app , db
import csv
from website.models import LabelingInfo , Label , Text
import os
from flask import request , render_template , send_file ##################
from flask_login import current_user


from werkzeug.utils import secure_filename
app = create_app()

# Flag to track if the function has been called before
exported_to_csv = False

button_pressed = False###

@app.route('/download_file', methods=['GET'])#########################33
def download_file():
    # Get the file path from the request or any other source
    file_path = 'D:/internship/UI/flask/website/labeling_info.csv'#request.args.get('file_path')

    # Ensure the file path is valid
    if not file_path:
        return "File path not provided.", 400

    return send_file(file_path, as_attachment=True)

import csv

def export_labeling_info_to_csv():
    global exported_to_csv  # Use the global flag
    if not exported_to_csv:
        with app.app_context():
            labeling_info = LabelingInfo.query.all()
            print(labeling_info)
            # Path to the CSV file where you want to export the data
            # csv_file_path = "/home/picky/mysite/website/labeling_info.csv"
            csv_file_path = 'D:/internship/UI/flask/website/labeling_info.csv'

            # Write data to CSV
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Write column names
                writer.writerow(["Id", "User_SId", "Text", "Label", "PublishDTO"])

                # Write data rows
                for info in labeling_info:
                    writer.writerow([info.id, info.user_id, info.text, info.label, info.date])  # Adjust the columns

        # Set the flag to True after the first call
        #exported_to_csv = True
        
@app.route('/upload_label', methods=['POST'])
def upload_label():
    uploaded_file = request.files.get('file')
    
    if uploaded_file:
        # Save the uploaded file
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(file_path)
        
        # Read the uploaded CSV file and store the data in the database
        data2 = []
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader2 = csv.reader(file)
            for row in csv_reader2:
                data2.append(row[0])
                new_label = Label(label=row[0])
                db.session.add(new_label)
                db.session.commit()

        return render_template("user.html", user = current_user, button_pressed = False)################
    else:
        return 'No file uploaded' 

@app.route('/upload_text', methods=['POST'])
def upload_text():
    uploaded_file = request.files.get('file')
    
    if uploaded_file:
        # Save the uploaded file
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(file_path)
        
        # Read the uploaded CSV file and store the data in the database
        data = []
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                data.append(row[0])
                new_text = Text(context=row[0], count = 0)####
                db.session.add(new_text)
                db.session.commit()

        return render_template("user.html", user = current_user, button_pressed = False)##########################3
    else:
        return 'No file uploaded'
    
@app.route('/button_pressed', methods=['GET'])###
def handle_button_pressed():
    print("buttom pressed     ffffffffffffffffffffff")
    global button_pressed
    button_pressed = True
    export_labeling_info_to_csv()
    button_pressed = False
    return render_template("user.html", user = current_user, button_pressed = True)##############3
    
    
    

if __name__ == '__main__':
    app.run()
    export_labeling_info_to_csv()  # Call the function to export to CSV after the app runs
    exported_to_csv = True
