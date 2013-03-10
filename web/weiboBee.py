#!/usr/bin/env python  
# -*- coding: utf-8 -*- 
from flask import url_for, Flask,render_template,request,session,redirect,Response,g,jsonify,send_from_directory
import sys,os,time,urllib,urllib2,json,MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config.from_pyfile('config.py')
PATH = os.path.dirname(__file__)

@app.route('/mession')
def mession():
    g.cur.execute("SELECT * FROM mession WHERE user_name = 'root'")
    result = g.cur.fetchall()
    return jsonify(result=[{"name":man[1],"status":man[2],"pic":man[3]} for man in result])

@app.route('/weibo')
def weibo():
    name = request.args.get('name')
    g.cur.execute("SET NAMES utf8")
    g.conn.commit()
    g.cur.execute("SELECT * FROM context WHERE target_name = '%s' ORDER BY hot DESC LIMIT 9" % name)
    result = g.cur.fetchall()
    return jsonify(result=[{"content":man[1],"time":man[2].strftime("%Y-%m-%d %H:%M:%S"),"own":man[4],"othercontext":man[5],"hot":man[7]} for man in result])
    
@app.route('/download/<name>/<int:count>')
def download(name,count):
    get_context(name,count,g)
    return send_from_directory(app.config['UPLOAD_FOLDER'],name+'.txt',as_attachment=True)
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    connect_db()
    g.cur.execute('SET NAMES utf8')
    g.conn.commit()
    g.cur.execute("SELECT * FROM man WHERE screen_name = '%s'" % name)
    result = g.cur.fetchall()
    return render_template('user.html',user = {"name":result[0][0],"pic":result[0][1],"location":result[0][2],"follower":result[0][3],"friends":result[0][4],"status":result[0][5]})

@app.route('/check')
def check():
    name = request.args.get('name')
    g.cur.execute("SELECT COUNT(*) FROM mession WHERE user_name = 'root' and target_name = '%s'" % name)
    name_count = g.cur.fetchall()
    if not name_count[0][0] == 0 :
        return jsonify(result="这个名字您已经备份过了")
    parm = {"access_token":app.config["TOKEN"],
            "screen_name":name}
    url = "https://api.weibo.com/2/users/show.json?" + urllib.urlencode(parm)
    try:
        result = json.loads(urllib2.urlopen(url).read())
    except urllib2.HTTPError :
        return jsonify(result="抱歉，您确定真有这个昵称？")
    g.cur.execute("INSERT INTO man VALUES('%s','%s','%s',%d,%d,%d)" % (result["screen_name"],result["profile_image_url"],result["location"],result["followers_count"],result["friends_count"],result["statuses_count"]) )
    g.conn.commit()
    return jsonify(result="good")

@app.route('/add')
def add():
    name = request.args.get('name')
    g.cur.execute("SELECT pic_url FROM man WHERE screen_name = '%s'" % name)
    pic = g.cur.fetchall()
    g.cur.execute("INSERT INTO mession VALUES('root','%s','0','%s')"%(name,pic[0][0]))
    g.conn.commit()
    return redirect(url_for('index'))

@app.after_request
def get_close(response):
    g.cur.close()
    g.conn.close()
    return response

@app.before_request
def connect_db():
    with open("/home/dotcloud/environment.json") as f :
        evn = json.loads(f.read())
    g.conn =  MySQLdb.Connection(host=evn["DOTCLOUD_DB_MYSQL_HOST"], 
                                 user=evn["DOTCLOUD_DB_MYSQL_LOGIN"], 
                                 passwd=evn["DOTCLOUD_DB_MYSQL_PASSWORD"], 
                                 db='arber',
                                 port=int(evn["DOTCLOUD_DB_MYSQL_PORT"]),
                                 charset='utf8')
    g.cur = g.conn.cursor()

def get_context(name,num,g):
    g.cur.execute("SET NAMES utf8")
    sql = "SELECT * FROM context WHERE target_name='%s'" % name
    if not num == 0 :
        sql = "SELECT * FROM context WHERE target_name='%s' ORDER BY hot DESC LIMIT %d" % (name,num) 
    g.cur.execute(sql)
    context = g.cur.fetchall()
    file = open(os.path.join(os.path.join(PATH,'static/result'),name + '.txt'),'w')
    file.close()
    for con in context :
        file = open(os.path.join(os.path.join(PATH,'static/result'),name + '.txt'),'a')
        text = '\n' + con[2].strftime("%Y-%m-%d %H:%M:%S")+'\n'+con[1]+'\n'
        if con[4] == 1 :
            text += con[5] + '\n'
        if not con[3] == 'no picture':
            text += con[3] 
        text += ("热度 : " + str(con[7]) + '\n')
        file.write(text)
        file.close()

if __name__ == "__main__":
    app.run()
