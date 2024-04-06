from flask import *
from database import *
from api import api

app=Flask(__name__)

app.secret_key='stpauls'
app.register_blueprint(api,url_prefix='/api')

@app.route('/',methods=['get','post'])
def home():
	 
	 return render_template('login.html')
@app.route('/login',methods=['get','post'])
def login():
	if 'submit' in request.form:
		username=request.form['username']
		password=request.form['password']
		q="SELECT * FROM `login` WHERE `username`='%s' AND `password`='%s'"%(username,password)
		res=select(q)
		if res:
			user=res[0]['usertype']
			session['log_id']=res[0]['login_id']
			if user=='admin':
				return redirect(url_for('admin_home'))
		else:
			flash('ivalid username or password')
	return render_template('login.html')


#####################################################Admin################################
@app.route('/admin_home',methods=['get','post'])
def admin_home():
	
	return render_template('admin_home.html')

@app.route('/admin_view_user',methods=['get','post'])
def admin_view_user():
	data={}
	q="SELECT * FROM `user`"
	data['view']=select(q)

	return render_template('admin_view_user.html',data=data)

@app.route('/admin_complaints',methods=['get','post'])
def admin_complaints():
    data={}
    q="SELECT * FROM `complaints` INNER JOIN `user` USING(`user_id`)"
    res=select(q)
    data['view']=res
    j=0
    for i in range(1,len(res)+1):
        if 'submit' +str(i) in request.form:
            reply=request.form['reply'+str(i)]
            q="UPDATE `complaints` SET `reply`='%s' WHERE `complaint_id`='%s' "%(reply,res[j]['complaint_id'])
            update(q)
            flash('success')
            return redirect(url_for('admin.admin_complaints'))
        j=j+1
    return render_template('admin_complaints.html',data=data)
 
app.run(debug=True,port=5104,host="0.0.0.0")