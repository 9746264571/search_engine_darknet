import requests
import json
import pymongo
import xlrd
import re
import sys
from flask import jsonify
from flask import Flask, render_template, request,redirect,url_for
from flask import flash
from elasticsearch import Elasticsearch
from pymongo import MongoClient
from werkzeug import secure_filename
res = requests.get('http://localhost:9200')
es = Elasticsearch([{'host' : 'localhost', 'port' :9200}])
client = MongoClient()
print("connected to database")
loc=("")
db = client["darklinks"]
links = db.links
app = Flask(__name__)
app.secret_key = "cyberdome"
app.config['UPLOAD_FOLDER']="uploads_links"
#print(res.content)
@app.route('/')
def search():
    cntt = links.count()
    return render_template('main.html',count = cntt)

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        wb = xlrd.open_workbook(f.filename)
        sheet = wb.sheet_by_index(0)
        for i in range(sheet.nrows):
           try:
               links.insert_one({"url" : sheet.cell_value(i,0)})
              #print(sheet.cell_value(2,0))
           except pymongo.errors.DuplicateKeyError:
               print("duplicate")
        cunt = links.count()
        llit = []
        for x in links.find({},{"_id":0,"url":1}):
            for key,val in x.items():
                llit.append(val)
        flash("Data added Successfully")
        return "<html><body bgcolor='black'><center><h3 style='color:orange'>Data Added Successfully</h3><br><a style='color:red' href='http://localhost:5000/db'>go back...</a></center></body></html>"
        


@app.route('/db')
def db():
    count = links.count()
    llist = []
    for x in links.find({},{"_id":0,"url":1}):
        for key,val in x.items():
            llist.append(val)
    
    return render_template('db.html',count=count,llist=llist)

@app.route('/result',methods = ['POST'])
def result():
    if request.method == 'POST':
        result = request.form['search']
        html = " <html> <head><title>Results</title><style>#child{border: 1px solid green;}</style></head><body bgcolor='black'>"
        #if '+' in result:
            #lst = re.split('+',result)
        i = request.form['gp']
        if i == "title" :
            if '+' in result:
                lst = result.split("+")
                jlst = ' '.join(lst)
                x = es.search(index='darklinks',body={"_source":["url","title"],"query":{"match": {"html":jlst}},"highlight":{"fields":{"html":{} }}},size = 500)
            elif '-' in result:
                lst = result.split("-")
                jlst = ' '.join(lst)
                x = es.search(index='darklinks',body={"_source":["url","title"],"query":{"match_phrase": {"html":jlst}},"highlight":{"fields":{"html":{} }}},size = 500)
            else:
                x = es.search(index='darklinks',body={"_source":["url","title"],"query":{"match":{"html":result}},"highlight":{"fields":{"html":{} }}},size = 500)
          
            for hit in x['hits']['hits']:
                html += "<div id='child'>"
                html +="<h3 style='color:red'>%(title)s<br></h3>" %hit["_source"]
                html +="<a href=%(url)s>%(url)s</a><br>" % hit["_source"]
                html +="<xmp style='color:green'>"
                html += "%s" % hit["highlight"]
                html +="</xmp></div>"
            return html    
            
        elif i== "meta":
            if '+' in result:
                lst = result.split("+")
                jlst = ' '.join(lst)
                x = es.search(index='darklinks',body={"_source":["url","meta"],"query":{"match": {'meta':jlst}},"highlight":{"fields":{"meta":{} }}},size = 500)
            elif '-' in result:
                lst = result.split("-")
                jlst = ' '.join(lst) 
                x = es.search(index='darklinks',body={"_source":["url","meta"],"query":{"match_phrase": {'meta':jlst}},"highlight":{"fields":{"meta":{} }}},size = 500)   
            else:
                x = es.search(index='darklinks',body={"_source":["url","meta"],"query":{"match": {'meta':result}},"highlight":{"fields":{"meta":{} }}},size = 500)        
            for hit in x['hits']['hits']:
                html += "<div id='child'>" 
                html += "<a  href=%(url)s>%(url)s</a><br>" %hit["_source"]
                html += "<p style='color:red'>%(meta)s</p><br>" %hit["_source"]
                html += "<xmp style='color:green'>"
                html += "%s" %hit["highlight"]
                html += "</xmp></div></body></html>"
            return html
            if not x:
                html += "<center><h3>No Results Returned</h3></center>"
            return html
        elif i== "html":
            if '+' in result:
                lst = result.split("+")
                jlst = ' '.join(lst)
                x = es.search(index='darklinks',body={"_source":["url","html"],"query":{"match": {'html' :jlst}},"highlight":{"fields":{"html":{} }}},size = 500)
            elif '-' in result:
                lst = result.split("-")
                jlst = ' '.join(lst) 
                x = es.search(index='darklinks',body={"_source":["url","html"],"query":{"match_phrase": {'html' :jlst}},"highlight":{"fields":{"html":{} }}},size = 500)
            else:
                 x = es.search(index='darklinks',body={"_source":["url","html"],"query":{"match": {'html' :result}},"highlight":{"fields":{"html":{} }}},size = 500)    
            for hit in x['hits']['hits']:
                html += "<div id='child'>"
                html += "<a href=%(url)s>%(url)s</a><br>" %hit["_source"]
                html += "<xmp style='color:green'>"
                html += "%s" %hit["highlight"]
                html += "</xmp></div>"
            html += "</body></html>"
            return html
        elif i== "plain":
            if '+' in result:
                lst = result.split("+")
                jlst = ' '.join(lst) 
                x = es.search(index='darklinks',body={"_source":["url","plain"],"query":{"match":{"plain":jlst}},"highlight":{"fields":{"plain":{} }}},size = 500)
            elif '-' in result:
                lst = result.split("-")
                jlst = ' '.join(lst)     
                x = es.search(index='darklinks',body={"_source":["url","plain"],"query":{"match_phrase":{"plain":jlst}},"highlight":{"fields":{"plain":{} }}},size = 500)
            else:
                x = es.search(index='darklinks',body={"_source":["url","plain"],"query":{"match":{"plain":result}},"highlight":{"fields":{"plain":{} }}},size = 500)    
            for hit in x['hits']['hits']:
                html += "<div id='child'>"
                html += "<a href=%(url)s>%(url)s</a><br>" %hit["_source"]
                html += "<xmp style='color:white'>"
                html += "%s" %hit["highlight"]
                html += "</xmp></div>"
            return html
        else:
            if '+' in result:
                lst = result.split("+")
                jlst = ' '.join(lst) 
                x = es.search(index='darklinks',body={"_source":["url","title","html"],"query":{"match": {'html' :jlst}},"highlight":{"fields":{"html":{} }}},size = 500)
            elif '-' in result:
                lst = result.split("-")
                jlst = ' '.join(lst)  
                x = es.search(index='darklinks',body={"_source":["url","title","html"],"query":{"match_phrase": {'html' :jlst}},"highlight":{"fields":{"html":{} }}},size = 500)
            else:
                x = es.search(index='darklinks',body={"_source":["url","title","html"],"query":{"match": {'html' :result}},"highlight":{"fields":{"html":{} }}},size = 500)
        for hit in  x['hits']['hits']:
            html += "<div id='child'>"
            html += "<h3 style='color:red'>%(url)s</h3><br>"
            html += "<a href=%(url)s>%(url)s<br></a>" %hit["_source"]
            html += "<p style='color:green'>"
            html += "%s" %hit["highlight"]
            html += "</p></div>"
        return html

  
@app.route('/dbres',methods = ['POST','GET'])
def dbres():
    cou = links.count()
    lixt = []
    for x in links.find({},{"_id":0,"url":1}):
        for key,val in x.items():
            lixt.append(val)
    if request.method == 'POST':
        result = request.form['link']
        act = request.form.get('sel')
        links.create_index("url",unique = True)
        #return render_template('db.html')
        if str(act) == "in":
        
            try:
               links.insert_one({"url" : result})
               print("<p>Link inserted successfully </p>")
               flash("Link inserted successfully")
            except:
                print("<p>Link already exists</p>")
                
                flash("Link already exists")
        elif str(act) == "del":
            try:
               links.delete_one({"url" : result})
               print("<p>Link deleted successfully </p>")
               flash("Link deleted successfully")
            except:
                print("<p>error</p>")
                
    return render_template('db.html',count=cou,llist=lixt)
if __name__ == '__main__':
    app.run(debug = True)
