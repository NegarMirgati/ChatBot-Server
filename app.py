from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.storage import SQLStorageAdapter
import mysql.connector
from datetime import datetime
import time
import emoji
import trainChat
from chatterbot.trainers import ListTrainer
import subprocess
import os
import sys
import re
import cv2

mydb = mysql.connector.connect(
  host="localhost",
  user="moodledude",
  passwd="passwordformoodledude",
  database="moodle"
)

app = Flask(__name__)

english_bot =trainChat.process()
multiple_question_state = 0
multiple_question_parameters = {'state' : 0}

def findName(id):
  mycursor = mydb.cursor()
  st = "SELECT  username FROM mdl_user WHERE id=%s"
  id_ = (id,)
  mycursor.execute(st,id_)
  myresult = mycursor.fetchall()
  for x in myresult:
    return x[0]


def find_userInfo(username):
  mycursor = mydb.cursor()
  st = "SELECT  firstname,lastname,email FROM mdl_user WHERE username=%s"
  username_ = (username,)
  mycursor.execute(st,username_)
  myresult = mycursor.fetchall()
  for x in myresult:
    return "بله شما"+"<br />"+x[0]+" " +x[1]+"<br />"+" هستیدوایمیل شما "+"<br />"+x[2]+" \N{winking face}"
    


"""to find grade of one course------------- """
def find_itemInfo2(courseid, id):
  mycursor = mydb.cursor()
  st = "SELECT itemname FROM mdl_grade_items WHERE id=%s AND courseid=%s"
  id_ = (id,courseid)
  mycursor.execute(st,id_)
  myresult = mycursor.fetchall()
  for x in myresult:
    return x[0]

def find_gradeOfOneCourse(userid,cn):
  outstr = ""
  courseid=find_courseId(cn)
  if (courseid is None):
    return "چنین درسی وجود نداره:("
  os.system("php webservice/demo.php %s %s"%(courseid,userid))
  out = subprocess.check_output("php webservice/demo.php %s %s"%(courseid,userid), shell=True)
  result=str(out)
  
  first=2
  for m in re.finditer(',', result):
    outstr+= result[first:m.start()]+"<br />"
    #print(result[first:m.start()])
    first=m.start()+1
  return ":نمره ی فعالیت های شما"+"<br />"+outstr  

  
def find_courseId(courseName):
  mycursor = mydb.cursor()
  st = "SELECT id FROM mdl_course WHERE fullname=%s "
  courseName_ = (courseName,)
  mycursor.execute(st,courseName_)
  myresult = mycursor.fetchall()
  for x in myresult:
    return x[0]

""" to find grade of all items' user--------------------- """
def find_courseName(course_id):
  mycursor = mydb.cursor()
  st = "SELECT fullname FROM mdl_course WHERE id=%s ORDER BY fullname"
  courseid_ = (course_id,)
  mycursor.execute(st,courseid_)
  myresult = mycursor.fetchall()
  for x in myresult:
    return x[0]

def has_uploaded_syllabus(course_name):
  mycursor = mydb.cursor()
  st = """SELECT name FROM mdl_resource AS r
  JOIN mdl_course AS c ON c.id = r.course  
  WHERE (c.fullname =%s) AND
  (LOWER(r.name) LIKE '%outline%' OR r.name LIKE '%برنامه%') """
  courseName_ = (course_name,)
  mycursor.execute(st, courseName_)
  myresult = mycursor.fetchall()
  if(len(myresult) == 0):
    return 'برنامه درس هنوز آپلود نشده'
  else :
    return "برنامه درس رو می تونی تو فایل {} ببینی".format(str(myresult[0][0]))

def has_uploaded_midterm_grades(course_name):
  mycursor = mydb.cursor()
  st = """SELECT name FROM mdl_resource AS r
  JOIN mdl_course AS c ON c.id = r.course  
  WHERE (c.fullname =%s) AND
  ((LOWER(r.name) LIKE '%midterm%' AND LOWER(r.name) NOT LIKE '%[s]olution%' AND LOWER(r.name) NOT LIKE ' %[s]ample%') OR
  (r.name LIKE '%میانترم%' AND r.name NOT LIKE '%پاسخ%')) """
  courseName_ = (course_name,)
  mycursor.execute(st, courseName_)
  myresult = mycursor.fetchall()
  if(len(myresult) == 0):
    return 'فکر کنم نمرات هنوز آپلود نشده'
  else :
    return "نمرات میانترمو می تونی تو فایل {} ببینی".format(str(myresult[0][0]))


def get_ungraded_assignments(userId, courseName):
  mycursor = mydb.cursor()
  mycursor.execute('SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;')
  st = """SELECT 
  a.name
  FROM mdl_assign_submission AS asb
  JOIN mdl_assign AS a ON a.id = asb.assignment
  JOIN mdl_user AS u ON u.id = asb.userid
  JOIN mdl_course AS c ON c.id = a.course 
  WHERE asb.status = "submitted" AND c.fullname =%s and u.id = %s AND NOT EXISTS (SELECT * FROM mdl_assign_grades g WHERE g.userid = u.id AND g.assignment = a.id);
  """
  params = (courseName, userId)
  print(params)
  mycursor.execute(st, params)
  myresult = mycursor.fetchall()
  if(len(myresult) == 0):
    return "همه ی تمرین هایی که بارگزاری کرده اید نمره دهی شده اند."
  else :
    retval = "اسامی تمرین هایی که بارگزاری کردی ولی نمره اشون هنوز نیومده : " + "<br />"
    for x in myresult :
      retval += x[0] + "<br/>"
      print(x[0])
    return retval
  mycursor.close()
 
#find all grade with course name
def find_all_gradesOfUser(userId):
  mycursor = mydb.cursor()
  st = """SELECT it.finalgrade, gg.courseid,gg.itemname
  FROM mdl_grade_grades it
  JOIN mdl_grade_items gg ON gg.id=it.itemid 
  WHERE it.userid=%s
  ORDER BY gg.courseid"""
  userId_ = (userId,)
  mycursor.execute(st,userId_)
  myresult = mycursor.fetchall()
  outstr = ""
  name1=" "
  for x in myresult:
    flag = 0
    courseName= find_courseName(x[1])
    if courseName!=name1:
      name1 = courseName
      outstr+= courseName+"در درس"+":"+"<br />"
      outstr+="نمره فعالیت هایت این گونه است"+"<br />"
      flag = 1
    itemName = x[2]  
    if not (itemName is None):
      if not (x[0] is None):
        outstr+=itemName+":"+str(x[0])+"<br />"
      else:  
        outstr+=itemName+" وارد نشده است"
      outstr+="<br />"
      #print(outstr)
  if outstr!="":   
    return outstr
  else:
    return "\N{disappointed face}هیچ نمره ای ثبت نشده است!"  
"""-----------------------------------------"""

def find_UserCourse(id):
  mycursor = mydb.cursor()
  st = "SELECT fullname FROM mdl_course WHERE id IN (SELECT courseid FROM  mdl_enrol WHERE id IN(SELECT enrolid FROM mdl_user_enrolments WHERE userid=%s)) "
  id_ = (id,)
  mycursor.execute(st,id_)
  myresult = mycursor.fetchall()
  st2 = " "
  for x in myresult:
    st2+= x[0] + ", "
  return "این هم لیست درس های شما"+"<br />"+st2

def find_UserEmail(name):
  splitname = name.split()
  mycursor = mydb.cursor()
  st = "SELECT  email FROM mdl_user WHERE firstname=%s AND lastname=%s"
  fn = (splitname[0],splitname[1])
  ln = (splitname[1],)

  mycursor.execute(st,fn)
  myresult = mycursor.fetchall()
  for x in myresult:
    return x[0]

def find_email(st1):
  quoted = re.compile('"([^"]*)"')
  print (' '.join(st1))
  extracted = quoted.findall(' '.join(st1))
  if len(extracted) > 0:   
    print('ECTRACTEEEEEEED',extracted[0]) 
    output = find_UserEmail(extracted[0])
  else:
    output ='لطفا نام و نام خانوادگی را بین "" قرار دهید'
  if not (output is None):
    return output
  else:
    return "ایمیلی با چنین نامی ثبت نشده"+"\N{eyes}"  

def convertTime(timestamp):
  dt_object = datetime.fromtimestamp(timestamp)
  time = dt_object.strftime("%d-%b-%Y (%H:%M:%S.%f)")
  return time

def get_quizes_names(courseName):
  course_id = find_courseId(courseName)
  if (course_id is None):
    return "!درسی با این اسم رو شما ثبت نام نکردی"
  mycursor = mydb.cursor()
  st = """SELECT quiz.name
  FROM mdl_quiz AS quiz
  WHERE quiz.course = %s AND quiz.timeclose < %s
  ORDER BY quiz.id ASC; """
  params = (course_id, time.time())
  mycursor.execute(st, params)
  myresult = mycursor.fetchall()
  if(len(myresult) >= 1) : 
    multiple_question_parameters['courseId'] = course_id
    multiple_question_parameters['state'] = 1
    retval = "سوالای این کوییز هارو می تونی ببینی :‌" + "<br/> "
    for x in myresult :
      retval += x[0] + "<br />"
    retval += "اسم کوییزی که میخوای رو برام تای‍پ کن."
    return retval
  else :
    return "کوییزی جهت نمایش وجود نداره."

def get_quizes_questions(quizName):
  mycursor = mydb.cursor()
  st = """ SELECT q.name, q.questiontext
  FROM mdl_quiz AS quiz
  JOIN mdl_quiz_slots qs on quiz.id = qs.quizid
  JOIN mdl_question AS q on q.id = qs.questionid
  WHERE quiz.course = %s AND quiz.timeclose < %s AND quiz.name LIKE %s;
;
  """
  params = (multiple_question_parameters['courseId'], time.time(), quizName)
  mycursor.execute(st, params)
  myresult = mycursor.fetchall()
  multiple_question_parameters['state'] = 0
  if(len(myresult) >= 1) : 
    retval = "سوالات این کوییز : " +  "<br />"
    for x in myresult:
      retval += x[0] + " : " + x[1] + "<br />"
    return retval
  else :
    return "سوالی جهت نمایش وجود نداره."

def find_UncloseQuiz(id):
  mycursor = mydb.cursor()
  st="SELECT name,timeclose,course FROM mdl_quiz WHERE timeclose>%s AND course IN(SELECT id FROM mdl_course  WHERE id IN (SELECT courseid FROM  mdl_enrol WHERE id IN(SELECT enrolid FROM mdl_user_enrolments WHERE userid=%s))) ORDER BY course"
  id_ = (time.time(),id)
  mycursor.execute(st,id_)
  myresult = mycursor.fetchall()
  str1=""
  str2=""
  name1=""
  for x in myresult:
    closedTime= convertTime(x[1])
    courseName = find_courseName(x[2])
    if courseName !=name1:
      name1=courseName
      str2+="در '"+ courseName+"'<br /> "
      str2+="کویزها با تاریخ بسته شدن اشان اینگونه است"+"<br />"
    str2+=x[0]+" ,closed time:"+closedTime+"<br />"
  if str2=="":
    return "کویز انجام نشده ای ندارید "+"<br />"+"\N{smiling face with smiling eyes}\N{smiling face with smiling eyes}"+"<br />"
  else:
    return str1+str2


def find_courseTeacher(courseName):
  mycursor = mydb.cursor()
  st="""(SELECT u.firstname,u.lastname FROM mdl_course ic 
  JOIN mdl_context con ON con.instanceid = ic.id 
  JOIN mdl_role_assignments ra ON con.id = ra.contextid AND con.contextlevel = 50
  JOIN mdl_role r ON ra.roleid = r.id
  JOIN mdl_user u ON u.id = ra.userid
  WHERE r.id = 3 AND ic.id = %s
  )"""
  courseid = find_courseId(courseName)
  if (courseid is None):
    return "!درسی با این اسم رو شما ثبت نام نکردی"
  id_ = (courseid,)
  mycursor.execute(st,id_)
  myresult = mycursor.fetchall()
  str2=""
  for x in myresult:
    str2+=x[0]+" "+x[1]+", "
  if str2!="": 
    return "استاد:"+"<br />"+str2 
  else:
    return "برای این درس نام هیچ استادی ثبت نشده است"+ " \N{worried face}"  

def find_courseChief(courseName):
    mycursor = mydb.cursor()
    st="""(SELECT u.firstname,u.lastname FROM mdl_course ic 
    JOIN mdl_context con ON con.instanceid = ic.id 
    JOIN mdl_role_assignments ra ON con.id = ra.contextid AND con.contextlevel = 50
    JOIN mdl_role r ON ra.roleid = r.id
    JOIN mdl_user u ON u.id = ra.userid
    WHERE r.id = 9 AND ic.id = %s
    )"""
    courseid = find_courseId(courseName)
    if (courseid is None):
      return "!درسی با این اسم رو شما ثبت نام نکردی"
    id_ = (courseid,)
    mycursor.execute(st,id_)
    myresult = mycursor.fetchall()
    str2=""
    res_len = len(myresult)
    for x in myresult:
      if(res_len >= 2):
        str2+=x[0]+" "+x[1]+", "
        res_len -= 1
      else :
         str2+=x[0]+" "+x[1]
    if str2!="": 
      return "چیف تی ای درس " + str2 + "ه"
    else:
      return "برای این درس نام هیچ چیف تی ای ثبت نشده است"+ " \N{worried face}"  

def find_UnclosedAssignment(id):
  mycursor = mydb.cursor()
  st="SELECT name,duedate,course,id FROM mdl_assign WHERE duedate>%s AND course IN(SELECT id FROM mdl_course  WHERE id IN (SELECT courseid FROM  mdl_enrol WHERE id IN(SELECT enrolid FROM mdl_user_enrolments WHERE userid=%s)))"
  id_ = (time.time(),id)
  mycursor.execute(st,id_)
  myresult = mycursor.fetchall()
  str1=""
  name1=""
  
  for x in myresult:
    closedTime= convertTime(x[1])
    courseName = find_courseName(x[2])
    os.system("php webservice/demo5.php %s %s"%(x[3],id))
    out = subprocess.check_output("php webservice/demo5.php %s %s"%(x[3],id), shell=True)
    result=str(out)
    if courseName != name1:
      name1 = courseName
      str1+=" در درس'"+courseName+"'"+"<br />"
      str1+="فعالیت ها با تاریخ بسته شدن اشان این گونه است:"+" \N{worried face}"+"<br />"
    str1+=x[0]+": "+closedTime+"<br />"+"<br />"
    first=2
    str1+=":تعداد شرکت کنندگان"
    for m in re.finditer(',', result):
      str1+= result[first:m.start()]+"<br />"  
      #print(result[first:m.start()])
      first=m.start()+1
    str1+="تعداد کسانی که این تکلیف را انجام دادند:"
    str1+=result[first:]+"<br />"
  if str1=="":
    return "هیچ تمرین یا فعالیت  نزدیکی وجود ندارد"
  else:
    return str1
def find_event(id):
  st1 = find_UncloseQuiz(id)
  st2 = find_UnclosedAssignment(id)
  return st1+st2

def find_date():
  currentDT = datetime.now()
  return currentDT.strftime("%Y-%m-%d %H:%M:%S")

def find_userInfo2(userid):
  mycursor = mydb.cursor()
  st = "SELECT  firstname,lastname FROM mdl_user WHERE id=%s"
  username_ = (userid,)
  mycursor.execute(st,username_)
  myresult = mycursor.fetchall()
  for x in myresult:
   #   print(x)
    return x[0]+" "+x[1]


def find_newForum(id):
  mycursor = mydb.cursor()
  st = """SELECT fp.message,fd.course,fp.userid,fp.subject FROM mdl_forum_discussions fd
  JOIN mdl_user_lastaccess ul ON ul.courseid = fd.course
  JOIN mdl_forum_posts fp ON fp.discussion = fd.id
  WHERE ul.userid=%s AND ul.timeaccess< fp.created
  ORDER BY fd.course
  """
  id_ = (id,)
  mycursor.execute(st,id_)
  myresult = mycursor.fetchall()
  st2 = " "
  name = ""
  for x in myresult:
    courseName = find_courseName(x[1])
    username = find_userInfo2(x[2])
    if courseName != name:
      name = courseName
      st2+= ":"+courseName+ "در"
    st2+= username+ ":"+x[3]
  if st2 != " ":
    return ":ببین این افراد در فروم با چه موضوعاتی پیام گذاشتند"+"<br />"+st2 
  else:
    return " \N{smiling face with smiling eyes}هیچ پیام جدیدی در فروم وجود ندارد"  


def find_forumBySubject(subjct):#ul.timeaccess< fp.created
  mycursor = mydb.cursor()
  st = """SELECT fp.message FROM mdl_forum_discussions fd
  JOIN mdl_user_lastaccess ul ON ul.courseid = fd.course
  JOIN mdl_forum_posts fp ON fp.discussion = fd.id
  WHERE fp.subject=%s AND ul.timeaccess< fp.created
  ORDER BY fd.course
  """
  id_ = (subjct,)
  mycursor.execute(st,id_)
  myresult = mycursor.fetchall()
  st2 = "متن کامل پیام:<br />"
  name = ""
  cc=""
  for x in myresult:
    st2+='<div style="color: white; background-color: #EF5350; padding: 10px; border-radius: 2px;">'
    #st2+='<p></span >'
    
    if cc!=x[0]:
      cc=x[0]
      st2+=x[0]
    st2+='</div>'

  if st2!=" ": 
    return st2
  else: 
    return "در فروم پیامی با این موضوع نبود"+"  \N{disappointed face}\N{disappointed face}"

def find_itemGrade(userId,itemName,courseName):
  courseId= find_courseId(courseName)
  if (courseId is None):
    return "چنین درسی وجود ندارد"

  mycursor = mydb.cursor()
  st="""SELECT gg.finalgrade, gg.itemid FROM mdl_grade_grades gg
  JOIN mdl_grade_items gt ON gt.id=gg.itemid
  WHERE gg.userid=%s AND gt.courseid=%s AND gt.itemname=%s
  """
  id_ = (userId,courseId,itemName)
  mycursor.execute(st,id_)
  myresult = mycursor.fetchall()
  st1=""
  str2=""
  for x in myresult:
    if not(x[1] is None) and not(x[0] is None):
      if x[0]<50:
        str2="ای وای نمره ات کمی پایین شده "+" \N{worried face}"+"<br />"
      elif x[0]>89:
        str2="آفررررین چقد خوب شدی" +"\N{grinning face}"+"<br />" 
      return str2+str(x[0]) 
    elif (x[0] is None)and not(x[1] is None) :
      return "هنوزنمره اش وارد نشده"+" \N{upside-down face}"
    else:
        return "فعالیتی با این اسم وجود نداره:(" 
  return "فعالیتی با این اسم وجود نداره:("       

def find_timeLeave(timestamp):
  currentDT = datetime.now()
  dt_object = datetime.fromtimestamp(timestamp)
  tt = currentDT - dt_object
  return tt
def find_lastAccess():
  str1 = "SELECT lastaccess,id,username FROM mdl_user" 
  mycursor = mydb.cursor()
  mycursor.execute(str1)
  myresult = mycursor.fetchall()
  access= list(range(len(myresult)+1))
  for x in myresult:
    time = find_timeLeave(x[0])
    id = int(x[1])
    access[id] = time
  return access  

def find_picture(userid):
  mycursor = mydb.cursor()
  st = "SELECT picture FROM mdl_user WHERE id=%s"
  id_ = (userid,)
  mycursor.execute(st,id_)
  myresult = mycursor.fetchall()
  for x in myresult:
    return x[0]

def find_avatar_path(userid):

  mycursor = mydb.cursor()
  st= "SELECT contenthash FROM mdl_files WHERE userid=%s AND component='user' AND mimetype LIKE '%image%'" 
  id_ = (userid,)
  mycursor.execute(st,id_)
  myresult = mycursor.fetchall()
  path =""
  for x in myresult:
    path= x[0]
    break
  picture = find_picture(userid)
  avatar = 'static/f2.png'
  if picture!=0:  
    avatar='/../../../../var/moodledata/filedir/'+path[0]+path[1]+"/"+path[2]+path[3]+"/"+path
  img = cv2.imread(avatar, 1)
  path2 = 'static'
  cv2.imwrite(os.path.join(path2 , str(userid)+'.png'), img)
  cv2.waitKey(0)


def find_token(userid):
  mycursor = mydb.cursor()
  st="""SELECT token FROM mdl_external_tokens WHERE userid=%s"""
  id_ =(userid,)
  mycursor.execute(st,id_)
  myresult = mycursor.fetchall()
  for x in myresult:
    if not (x is None):
      return x[0]
  return " "  

def add_user(userid,username,password,firstname,lastname,email):
  token = find_token(userid)
  if token==" ":
    return "شما اجازه دسترسی به این کار را ندارید"

  os.system("php webservice/demo1.php %s %s %s %s %s %s"%(username,password,firstname,lastname,email,token))

  outstr="نام کاربری:"+username+"<br />"
  outstr+="رمز عبور:"+password+"<br />"
  outstr+="نام:"+firstname+"<br />"
  outstr+="نام خانوادگی:"+lastname+"<br />"
  outstr+="ایمیل:"+email+"<br />"
  return "کاربر موردنظر ایجادشد"+"<br />"+outstr


access = find_lastAccess()
@app.route('/<id>/')
def home(id):   
    file1 = open("info.txt","w")
    file1.write(id) 
    file1.close() 
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
  #read file for id
  file1 = open("info.txt","r+") 
  userId = file1.read() 
  file1.close()
  
  userText = request.args.get('msg')
  print("multiple_params", multiple_question_parameters)
  if(multiple_question_parameters['state'] != 0):
    if(multiple_question_parameters['state'] == 1):
      return get_quizes_questions(userText)+"#"+userId  

  elif "سلام" in userText:
    userName=findName(userId)
    output = userName+"سلام "+ "\N{grinning face}"+"\N{grinning face}"+"\N{smiling face with smiling eyes}"+"<br />"
    if int(access[int(userId)].days)>10:  
      output+="چقدر دیر به دیر میایی.دلم برات تنگ شده بود"+"<br />"+str(access[int(userId)].days)+"<br />"+"روزه که نبودی"
    elif int(access[int(userId)].days) <1:
     output+=" چقد خوشحالم زود به زود میایی"
    return output+"#"+userId
  
  elif "تشکر" in userText:
    return "خواهش می کنم:)"
  
  elif "چطوری"in userText or "حالت چه طوره" in userText or "خوبی" in userText:
    return  emoji.emojize(" :rose:")+"ممنونم"+"#"+userId

  elif "می شناسی" in userText and "من" in userText:
    userName=findName(userId)
    userInfo=find_userInfo(userName)
    output = userInfo
    return output+"#"+userId

  elif "نمره های درس" in userText or "نمره درس" in userText : 
    if userText.find("'")!= -1:
      userText = userText[userText.find("'")+1:]
      courseName = userText[:userText.find("'")]
      return find_gradeOfOneCourse(userId,courseName)+"#"+userId
    else:
      return "'' لطفا نام درس را قرار بده بین"+"#"+userId  
  
  elif "نمره های من" in userText or "نمره ی من" in userText:
    output = find_all_gradesOfUser(userId)
    return output+"#"+userId
  
  elif "نمره" in userText and "در" in userText:
    st1=""
    if userText.find("(")!= -1:
      userText = userText[userText.find("(")+1:]
      itemName = userText[:userText.find(")")]
      if userText.find("'")!= -1: 
        userText = userText[userText.find("'")+1:]
        courseName = userText[:userText.find("'")]
        st1 =find_itemGrade(userId,itemName,courseName)
      else:
        st1= "لطفا با این فرمت تایپ کن <br /> 'course'نمره (تمرین)در "  
    else:
      st1= "لطفا با این فرمت تایپ کن <br /> 'course'نمره (تمرین)در "  
    return st1+"#"+userId   

  elif "درس های من" in userText:
    return find_UserCourse(userId)+"#"+userId
  
  elif "ایمیل" in userText:
    st1 = userText.split()
    return find_email(st1)+"#"+userId
  
  elif "ساعت" in userText or "تاریخ" in userText:
    return emoji.emojize(" :calendar:")+" "+find_date()+"#"+userId 
  
  elif "کوییز" in userText and 'سوال' not in userText:
    return find_UncloseQuiz(userId)+"#"+userId
  
  elif "استاد" in userText: 
    if userText.find("'")!= -1:
      userText = userText[userText.find("'")+1:]
      courseName = userText[:userText.find("'")]
      return find_courseTeacher(courseName)+"#"+userId
    else:
      return ". ''لطفا نام درس را قرار بده بین"+"#"+userId    

  elif "چیف" in userText: 
    if userText.find("'")!= -1:
      userText = userText[userText.find("'")+1:]
      courseName = userText[:userText.find("'")]
      return find_courseChief(courseName)+"#"+userId
    else:
      return ". ''لطفا نام درس را قرار بده بین"+"#"+userId  
  
  elif "تصحیح نشده" in userText:
    if userText.find("'")!= -1:
      userText = userText[userText.find("'")+1:]
      courseName = userText[:userText.find("'")]
      return get_ungraded_assignments(userId, courseName)+"#"+userId
    else:
      return ". ''لطفا نام درس را قرار بده بین"+"#"+userId  
  
  elif "تمرین" in userText or "فعالیت" in userText and "تصحیح" not in userText:
    return find_UnclosedAssignment(userId)+"#"+userId

  elif "چه خبر" in userText or "رویداد" in userText:
    return find_event(userId)+"#"+userId  
    
  elif "فروم" in userText:
    return find_newForum(userId)+"#"+userId

  elif "موضوع" in userText:
    if userText.find("'")!= -1:
      userText = userText[userText.find("'")+1:]
      subject = userText[:userText.find("'")]
      return find_forumBySubject(subject)+"#"+userId
    else:
      return " ''لطفا نام درس را قرار بده بین"+"#"+userId     
  
  elif "ایجادکاربر" in userText:
    userText=userText[userText.find(':')+1:]
    username=userText[:userText.find(',')]
    userText=userText[userText.find(',')+1:]
    password=userText[:userText.find(',')]
    userText=userText[userText.find(',')+1:]
    firstname=userText[:userText.find(',')]
    userText=userText[userText.find(',')+1:]
    lastname=userText[:userText.find(',')]
    userText=userText[userText.find(',')+1:]
    email=userText
    output=add_user(userId,username,password,firstname,lastname,email)
    return output+"#"+userId
  
  elif "syllabus" in userText or "سیلاب" in userText or "برنامه" in userText:
    if userText.find("'")!= -1:
      userText = userText[userText.find("'")+1:]
      courseName = userText[:userText.find("'")]
      return has_uploaded_syllabus(courseName)+"#"+userId
    else:
      return ". ''لطفا نام درس را قرار بده بین"+"#"+userId  

  elif ("میانترم" in userText or "میان ترم" in userText) and ("نمره" in userText or "نمرات" in userText):
    if userText.find("'")!= -1:
      userText = userText[userText.find("'")+1:]
      courseName = userText[:userText.find("'")]
      return has_uploaded_midterm_grades(courseName)+"#"+userId
    else:
      return ". ''لطفا نام درس را قرار بده بین"+"#"+userId  
    
  elif "سوال" in userText and "کوییز" in userText :
    if userText.find("'")!= -1:
      userText = userText[userText.find("'")+1:]
      courseName = userText[:userText.find("'")]
      return get_quizes_names(courseName) + "#" + userId
    else:
      return ". ''لطفا نام درس را قرار بده بین"+"#"+userId  

  else:
    output = str(english_bot.get_response(userText))
    return output+"#"+userId

    


if __name__ == "__main__":
    app.run(host='0.0.0.0')
