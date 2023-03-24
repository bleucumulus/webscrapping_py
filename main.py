#from requests import get
#from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs
from extractors.indeed import extract_indeed_jobs
from file import save_to_file

#save_to_file(keyword, jobs)

from flask import Flask, render_template, request, redirect, send_file

app = Flask("JobScrapper")

db = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    elif keyword == " ":
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        indeed = extract_indeed_jobs(keyword)
        wwr = extract_wwr_jobs(keyword)
        jobs = indeed + wwr
        db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    elif keyword == " ":
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)
# 127.0.0.1로 했을 때 터미널 창에서 경고가 나오긴 하는데 크롬에 사이트 붙여넣으면 작동됨
app.run("127.0.0.1")
