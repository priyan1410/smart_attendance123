from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Replace these with your MySQL database credentials
db_config1 = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Suriy@24',
    'database': 'attendance'
}

db_config2 = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Suriy@24',
    'database': 'percentage'
}

# Connect to MySQL database
db_connection = mysql.connector.connect(**db_config1)
db_cursor = db_connection.cursor()

con2=mysql.connector.connect(**db_config2)
cur2=con2.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_type = request.form['user_type']
        
        if user_type == 'faculty':
            return render_template('faculty_login.html')
        elif user_type == 'student':
            re=con2.cursor()
            qry="SELECT * FROM perc"
            re.execute(qry,)
            result=re.fetchall()
            db_cursor.execute("SELECT * FROM atten")
            students = db_cursor.fetchall()
            return render_template('student_login.html', students=students,res=result)
    
    return render_template('index.html')

@app.route('/faculty_login', methods=['POST'])
def faculty_login():
    password = request.form['word']
    
    if password == 'Suriy@24':
        return render_template('faculty_options.html')
    else:
        return "Invalid password"

@app.route('/faculty_options', methods=['post'])
def faculty_options():
    opti = request.form['option']
    if opti == 'attendance':
        return render_template('select_subject.html')
    elif opti == 'edit':
        return render_template('edit_options.html')

@app.route('/select_subject', methods=['post'])
def select_subject():
    subject = request.form['subject']
    # Fetch student names from the database
    db_cursor.execute("SELECT stname FROM atten")
    students = db_cursor.fetchall()  # Call the function with the subject parameter
    return render_template('mark_attendance.html', subject=subject, students=students)

def addatten(sub):
    re=con2.cursor()
    sql="select {} from perc".format(sub)
    re.execute(sql)
    result=re.fetchone()
    for i in result:
        ne=i+1
    re=con2.cursor()
    qry="update perc set {}=%s ".format(sub)
    user=(ne,)
    re.execute(qry,user)
    con2.commit()
    
@app.route('/mark_attendance', methods=['POST'])  # Use 'POST' instead of 'patch'
def mark_attendance():
    subject = request.form['subject']
    addatten(subject)
    for student in request.form:
        if student != 'subject':
            attendance_status = request.form[student]
            if attendance_status == 'present':
                # Update attendance in the database
                db_cursor.execute("UPDATE atten SET {} = {} + 1 WHERE stname = %s".format(subject, subject), (student,))
                db_connection.commit()

    return render_template('suc_att.html')


@app.route('/suc_att', methods=['post'])
def suc_att():
    option = request.form['option']
    if option == 'return':
        return redirect(url_for('index'))

@app.route('/edit_options', methods=['POST'])
def edit_options():
    option = request.form['edit_option']
    
    if option == 'insert':
        return render_template('insert_student.html')
    elif option == 'update':
        return render_template('update_student.html')
    elif option == 'view_all':
        db_cursor.execute("SELECT * FROM atten")
        students = db_cursor.fetchall()
        return render_template('view_students.html', students=students)
    elif option == 'delete':
        return render_template('delete_student.html')
    
@app.route('/insert_student', methods=['GET', 'POST'])
def insert_student():
    if request.method == 'POST':
        name = request.form['name']
        tamil = request.form['tamil']
        english = request.form['english']
        db_cursor = db_connection.cursor()
        sql = "INSERT INTO atten (stname, tamil, english) VALUES (%s, %s, %s)"
        db_cursor.execute(sql, [name, tamil, english])
        db_connection.commit()
        db_cursor.close()
        return render_template('suc_ist.html')

@app.route('/suc_ist', methods=['post'])
def suc_ist():
    option = request.form['option']
    if option == 'return':
        return redirect(url_for('index'))

    
@app.route('/update_student', methods=['GET', 'POST'])
def update_student():
    if request.method == 'POST':
        reg = request.form['reg']
        name = request.form['name']
        tamil = request.form['tamil']
        english = request.form['english']
        db_cursor = db_connection.cursor()
        sql = "UPDATE atten SET stname=%s, tamil=%s, english=%s WHERE reg=%s"
        db_cursor.execute(sql, [name, tamil, english, reg])
        db_connection.commit()
        db_cursor.close()
        return render_template('suc_upt.html')

@app.route('/suc_upt', methods=['post'])
def suc_upt():
    option = request.form['option']
    if option == 'return':
        return redirect(url_for('index'))
        
 
@app.route('/delete_student', methods=['GET', 'POST'])   
def delete_student():
    if request.method=='POST':
        student_id = request.form['reg']
        db_cursor = db_connection.cursor()
        sql = "DELETE FROM atten WHERE reg = %s"
        db_cursor.execute(sql, [student_id])
        db_connection.commit()
        return render_template('suc_del.html')
    
@app.route('/suc_del', methods=['post'])
def suc_del():
    option = request.form['option']
    if option == 'return':
        return redirect(url_for('index'))
   

# Add more routes and templates for insert, update, view_all, and delete functionalities

if __name__ == '__main__':
    app.run(debug=True)