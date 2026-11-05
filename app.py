from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")
DB = os.path.join(os.path.dirname(__file__), "ditora.db")

COURSES = [
    {"slug":"dit-basics","title":"DIT Basics","category":"Computer Fundamentals","level":"Beginner","duration":"6 weeks","description":"Computer fundamentals, Windows, office productivity and digital skills.","icon":"▣","color":"blue"},
    {"slug":"web-development","title":"Web Development","category":"Development","level":"Beginner → Intermediate","duration":"8 weeks","description":"Build responsive websites with HTML, CSS and JavaScript.","icon":"⌘","color":"purple"},
    {"slug":"ai-tools","title":"AI & Modern Tools","category":"Artificial Intelligence","level":"Beginner","duration":"4 weeks","description":"Learn practical AI workflows, prompting and productivity tools.","icon":"✦","color":"pink"},
    {"slug":"database-sql","title":"Database & SQL","category":"Data","level":"Beginner → Intermediate","duration":"5 weeks","description":"Understand relational databases and write useful SQL queries.","icon":"◫","color":"green"},
    {"slug":"graphic-design","title":"Graphic Design","category":"Creative","level":"Beginner","duration":"6 weeks","description":"Design visual content, understand typography and build a portfolio.","icon":"◈","color":"orange"},
]
LESSONS = {
"dit-basics":[("Computer kya hai?","Introduction to computers and their main components."),("Hardware & Software","Understand the physical and digital parts of a computer."),("Operating Systems","Explore Windows, files, folders and basic settings.")],
"web-development":[("HTML Foundations","Create the structure of a web page."),("CSS & Responsive Design","Style pages that work on mobile and desktop."),("JavaScript Basics","Add interactions and dynamic behavior.")],
"ai-tools":[("AI ki Bunyad","What AI tools can and cannot do."),("Prompt Writing","Write clearer instructions for better results."),("AI for Productivity","Use AI responsibly for study and work.")],
"database-sql":[("Database Concepts","Tables, records, keys and relationships."),("SQL SELECT","Retrieve and filter information."),("JOIN & Aggregation","Combine tables and summarize data.")],
"graphic-design":[("Design Principles","Balance, contrast, hierarchy and alignment."),("Typography & Color","Choose readable type and meaningful palettes."),("Portfolio Project","Create a polished social media design.")],
}
def db():
    con=sqlite3.connect(DB); con.row_factory=sqlite3.Row; return con
def init_db():
    with db() as con:
        con.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        con.execute("CREATE TABLE IF NOT EXISTS progress(user_id INTEGER, course_slug TEXT, lesson_index INTEGER, PRIMARY KEY(user_id,course_slug,lesson_index))")
init_db()
def current_user():
    if "user_id" not in session: return None
    with db() as con: return con.execute("SELECT id,name,email FROM users WHERE id=?",(session["user_id"],)).fetchone()
@app.route("/")
def home():
    return render_template("index.html", courses=COURSES, user=current_user())
@app.route("/courses")
def courses():
    return render_template("courses.html", courses=COURSES, user=current_user())
@app.route("/course/<slug>")
def course(slug):
    c=next((x for x in COURSES if x["slug"]==slug),None)
    if not c: return "Course not found",404
    user=current_user()
    completed=[]
    if user:
        with db() as con: completed=[r["lesson_index"] for r in con.execute("SELECT lesson_index FROM progress WHERE user_id=? AND course_slug=?",(user["id"],slug))]
    return render_template("course.html", course=c, lessons=LESSONS[slug], completed=completed, user=user)
@app.route("/lesson/<slug>/<int:index>", methods=["GET","POST"])
def lesson(slug,index):
    c=next((x for x in COURSES if x["slug"]==slug),None)
    if not c or slug not in LESSONS or index<0 or index>=len(LESSONS[slug]): return "Lesson not found",404
    user=current_user()
    if request.method=="POST":
        if not user:
            flash("Progress save karne ke liye login karein.")
            return redirect(url_for("login"))
        with db() as con: con.execute("INSERT OR IGNORE INTO progress(user_id,course_slug,lesson_index) VALUES(?,?,?)",(user["id"],slug,index))
        flash("Lesson complete mark ho gaya!")
        return redirect(url_for("course",slug=slug))
    title,description=LESSONS[slug][index]
    return render_template("lesson.html",course=c,index=index,title=title,description=description,total=len(LESSONS[slug]),user=user)
@app.route("/practice")
def practice(): return render_template("practice.html",user=current_user())
@app.route("/dashboard")
def dashboard():
    user=current_user()
    if not user: return redirect(url_for("login"))
    with db() as con: rows=con.execute("SELECT course_slug,lesson_index FROM progress WHERE user_id=?",(user["id"],)).fetchall()
    completed={}
    for r in rows: completed[r["course_slug"]]=completed.get(r["course_slug"],0)+1
    return render_template("dashboard.html",user=user,courses=COURSES,completed=completed)
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name=request.form.get("name","").strip(); email=request.form.get("email","").strip().lower(); password=request.form.get("password","")
        if not name or not email or len(password)<8:
            flash("Naam/email dein aur password kam az kam 8 characters ka ho."); return render_template("auth.html",mode="register",user=current_user())
        try:
            with db() as con: con.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)",(name,email,generate_password_hash(password)))
            flash("Account ban gaya. Ab login karein."); return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Is email se account pehle mojood hai.")
    return render_template("auth.html",mode="register",user=current_user())
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form.get("email","").strip().lower(); password=request.form.get("password","")
        with db() as con: user=con.execute("SELECT * FROM users WHERE email=?",(email,)).fetchone()
        if user and check_password_hash(user["password"],password):
            session["user_id"]=user["id"]; return redirect(url_for("dashboard"))
        flash("Email ya password durust nahi.")
    return render_template("auth.html",mode="login",user=current_user())
@app.route("/logout")
def logout(): session.clear(); return redirect(url_for("home"))
@app.route("/about")
def about(): return render_template("info.html",page="About DITora",user=current_user())
@app.route("/contact")
def contact(): return render_template("info.html",page="Contact",user=current_user())
if __name__=="__main__": app.run(debug=True)
