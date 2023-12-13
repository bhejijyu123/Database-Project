from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random

app = Flask(__name__)


# Connect to the database
def get_db_connection():
  conn = sqlite3.connect('database.db')

  # cursor = conn.cursor()
  # with open('schema.sql', 'r') as f:
  #   sql = f.read()
  # cursor.executescript(sql)  
  # conn.commit()
  # print("---Data Base formulation working ---")
  return conn


# Login page
@app.route('/')
def home():
  get_db_connection()
  return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    print("This is username ---\n\n\\n\n\n\n\n\n", username, password)
    conn = sqlite3.connect('database.db')
    
    student = conn.execute('SELECT * FROM students WHERE username = ? AND password = ?', (username, password)).fetchall()
    if student:
      if username == "admin":
        
        return render_template("addStudent.html")
      #Logged in then
      print("--WORKING ==")
      return studentInformation(username)
    else:
      return render_template('login.html',
                             error='Invalid username or password')
  else:
    return render_template('login.html', error='')


@app.route('/studentInformation', methods=["POST", "GET"])
def studentInformation(username):
  conn = sqlite3.connect('database.db')
  class_info = conn.execute(
    'SELECT * FROM  student_course as a JOIN student_info as b ON a.id = b.student_id JOIN student_advisor as c ON c.student_id = a.id  WHERE id = ? ',
    (username, )).fetchall()

  print(class_info)
  advisor = conn.execute(
    'SELECT * FROM  professor_info WHERE instructor_id = ? ',
    (class_info[0][12], )).fetchall()

  print("This is working===")

  print(advisor)
  return render_template("student_infor.html",
                         courses=class_info,
                         professor=advisor)
  advisor = conn.execute(
    'SELECT * FROM  professor_info WHERE     instructor_id = ? ',
    (class_info[0][12], )).fetchall()
  print("This is working===")
  print(advisor)
  return render_template("student_infor.html",
                         courses=class_info,
                         professor=advisor)

#delete 
@app.route('/delete_form', methods=['POST'])
def delete_form():
  conn = get_db_connection()
  username = request.form['id']
  pw = request.form['pw']

  student = conn.execute(
    'SELECT * FROM students WHERE username = ? and password = ? ',
    (username, pw)).fetchone()

  if student:
    conn.execute("DELETE FROM students WHERE username = ?", (username, ))
    conn.execute("DELETE FROM student_course WHERE id = ?", (username, ))
    #conn.execute("DELETE FROM student_course WHERE id = ?" , (username))
  conn.commit()
  return redirect(url_for('login'))

#update 
@app.route('/process_form', methods=['POST'])
def process_form():
  conn = get_db_connection()
  course = request.form['numCourse']
  newCourse = request.form['newCourse']
  username = request.form['username']
  student = conn.execute('SELECT * FROM students WHERE username = ?',
                         (username, )).fetchone()

  print(course)
  if student:
    if course == "Course 1":
      conn.execute('UPDATE student_course SET class1 = ? WHERE id = ?',
                 (newCourse, username))
    elif course == "Course 2":
      conn.execute('UPDATE student_course SET class2 = ? WHERE id = ?',
                 (newCourse, username))
    elif course == "Course 3":
      conn.execute('UPDATE student_course SET class3 = ? WHERE id = ?',
                 (newCourse, username))
    elif course == "Course 4":
      conn.execute('UPDATE student_course SET class4 = ? WHERE id = ?',
                 (newCourse, username))
      

  class_info = conn.execute(
    'SELECT * FROM  student_course as a JOIN student_info as b ON a.id = b.student_id JOIN student_advisor as c ON c.student_id = a.id  WHERE id = ? ',
    (username, )).fetchall()
  print(class_info)
  advisor = conn.execute(
    'SELECT * FROM  professor_info WHERE instructor_id = ? ',
    (class_info[0][12],)).fetchall()
  conn.commit()
  conn.close()
  return render_template("student_infor.html",
                         courses=class_info,
                         professor=advisor)


@app.route('/courses')
def courses():
  conn = sqlite3.connect('database.db')
  courses = conn.execute("SELECT * FROM course_info").fetchall()
  conn.close()
  return render_template('courses.html', courses=courses)


@app.route('/staffs')
def staffs():
  conn = sqlite3.connect('database.db')
  cursor = conn.cursor()
  staffs = conn.execute("SELECT * FROM professor_info").fetchall()
  conn.close()
  return render_template('staff_directory.html', staffs=staffs)


#add student already xa new function name needed
#ekchoti comment garana yo ma format milaidi halxu

#insert 
@app.route('/addNewStudent', methods=["POST", "GET"])
def addNewStudent():
  conn = get_db_connection()
  name = request.form['name']
  email = request.form['email']
  pronouns = request.form['pronouns']
  intented_major = request.form['intended_major']
  class1 = request.form['class1']
  class2 = request.form['class2']
  class3 = request.form['class3']
  class4 = request.form['class4']
  school_year = request.form['school_year']
  id = random.randint(100, 1000)
  a = conn.execute(f"SELECT * from student_info where student_id = {id}").fetchall()
  while (len(a) != 0):
    id = random.randint(1, 1000)
    a = conn.execute(f"SELECT * from student_info where student_id = {id}").fetchall()
  
  conn.execute("insert into student_info values (?, ?, ?, ?, ?, ?);",
               (id, name, email, pronouns, intented_major, school_year))
  
  conn.execute(f"INSERT INTO students (username, password) VALUES ({id}, 'Password');")

  print(id, name, email, pronouns, intented_major, class1, class2, class3, class4)
  conn.execute(f"INSERT INTO student_course (id, class1, class2, class3, class4) VALUES ({id}, '{class1}', '{class2}', '{class3}', '{class4}');")
  
  instructor_id = conn.execute(f"select instructor_id from professor_info where department_id = '{intented_major}' order by RANDOM() LIMIT 1;").fetchall()
  
  conn.execute("INSERT INTO student_advisor (student_id, advisor_id) values (?, ?)",
    (id, int(instructor_id[0][0])))
  print(id)
  conn.commit()
  conn.close()
  return render_template("/addStudent.html")


@app.route('/contact')
def contact():
  return render_template('contact_us.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81)
