
from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3, qrcode, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "gdo_secret"

DB="database.db"

def db():
    return sqlite3.connect(DB)

def level(points):
    if points>=80: return "🟢 ملتزم"
    if points>=50: return "🟡 متوسط"
    return "🔴 خطر"

@app.route("/", methods=["GET","POST"])
def login():
    if request.method=="POST":
        role=request.form["role"]
        code=request.form["code"]
        name=request.form.get("name","")
        teacher=request.form.get("teacher","")
        session.update({"role":role,"code":code,"name":name,"teacher":teacher})
        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dash():
    role=session.get("role")
    code=session.get("code")
    con=db();cur=con.cursor()
    if role=="admin":
        return render_template("admin.html")
    if role=="teacher":
        cur.execute("SELECT * FROM students")
        return render_template("teacher.html",students=cur.fetchall())
    if role=="student":
        cur.execute("SELECT * FROM students WHERE code=?",(code,))
        s=cur.fetchone()
        return render_template("student.html",s=s,lv=level(s[4]))
    if role=="parent":
        cur.execute("SELECT * FROM students WHERE code=? AND name=? AND teacher=?",(code,session["name"],session["teacher"]))
        s=cur.fetchone()
        return render_template("parent.html",s=s,lv=level(s[4]))
    return redirect("/")

@app.route("/attendance/<code>/<status>")
def attendance(code,status):
    con=db();cur=con.cursor()
    cur.execute("SELECT points FROM students WHERE code=?",(code,))
    p=cur.fetchone()[0]
    if status=="absent": p-=5
    if status=="late": p-=3
    if status=="present": p+=2
    cur.execute("UPDATE students SET points=? WHERE code=?",(p,code))
    cur.execute("INSERT INTO attendance(code,date,status) VALUES(?,?,?)",(code,str(datetime.now().date()),status))
    con.commit()
    return redirect("/dashboard")

@app.route("/qr/<code>")
def qr(code):
    img=f"static/{code}.png"
    if not os.path.exists(img):
        qrcode.make(code).save(img)
    return send_file(img)

if __name__=="__main__":
    app.run(debug=True)
