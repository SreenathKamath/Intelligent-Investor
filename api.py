from flask import *
from database import *

api=Blueprint('api',__name__)

@api.route('/login')
def login():
	data={}
	username=request.args['username']
	password=request.args['password']
	q="select *,concat(firstname,'',lastname) as  zname from login inner join user using (login_id) where username='%s' and password='%s'"%(username,password)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	return str(data)


@api.route('/User_registration')
def User_registration():
	data={}
	fname=request.args['firstname']
	lanme=request.args['lastname']
	place=request.args['place']
	phone=request.args['phone']
	email=request.args['email']
	username=request.args['username']
	password=request.args['password']
	

	q1="SELECT * FROM login WHERE `username`='%s'"%(username)
	res=select(q1)
	if res:
		data['status']="duplicate"
		data['method']="User_registration"
	else:

		q=" INSERT INTO `login` VALUES(NULL,'%s','%s','user')"%(username,password)
		print(q)
		result=insert(q)
		qr="INSERT INTO `user` VALUES(NULL,'%s','%s','%s','%s','%s','%s')"%(result,fname,lanme,place,phone,email)
		id=insert(qr)
		if id > 0:
			data['status']="success"
		else:
			data['status']="failed"
		data['method']="User_registration"	
	return str(data)


@api.route('/view_complaint')
def view_complaint():
    data={}
    log_id=request.args['log_id']
    q="SELECT * FROM `complaints` WHERE `user_id`=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')"%(log_id)
    res=select(q)
    if res:
        data['status']="success"
        data['data']=res
    else: 
        data['status']="failed"
    data['method']="view_complaint"
    return str(data)

@api.route('/Customer_send_complaint')
def Customer_send_complaint():
    data={}
    log_id=request.args['log_id']
    complaint=request.args['complaint']
    q="INSERT INTO `complaints` VALUES(NULL,(SELECT `user_id` FROM `user` WHERE `login_id`='%s'),'%s','pending',NOW())"%(log_id,complaint)
    print(q)
    res=insert(q)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    data['method']="Customer_send_complaint"
    return str(data)

@api.route('/view_income')
def view_income():
    data={}
    log_id=request.args['log_id']
    q="SELECT * FROM `income` WHERE `user_id`=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')"%(log_id)
    res=select(q)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    data['method']="view_income"
    return str(data)

@api.route('/User_add_incomes')
def User_add_incomes():
    data={}
    log_id=request.args['log_id']
    income=request.args['income']
    q="SELECT * FROM `total_balance` where `user_id`=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')"%(log_id)
    res=select(q)
    if res:
        q="UPDATE `total_balance` SET `balance_amount`=`balance_amount`+'%s' WHERE (SELECT `user_id` FROM `user` WHERE `login_id`='%s')"%(income,log_id)
        update(q)
    else:
        q="INSERT INTO `total_balance` VALUES(NULL,(SELECT `user_id` FROM `user` WHERE `login_id`='%s'),'%s')"%(log_id,income)
        insert(q)
    q="INSERT INTO `income` VALUES(NULL,(SELECT `user_id` FROM `user` WHERE `login_id`='%s'),'%s',NOW())"%(log_id,income)
    print(q)
    res=insert(q)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    data['method']="User_add_incomes"
    return str(data)

@api.route('/User_balance')
def User_balance():
    data={}
    log_id=request.args['log_id']
    q="SELECT * FROM `total_balance` WHERE `user_id`=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')"%(log_id)
    res=select(q)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    data['method']="User_balance"
    return str(data)

@api.route('/view_category')
def view_category():
    data={}
    log_id=request.args['log_id']
    q="SELECT * FROM `category` WHERE `user_id`=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')"%(log_id)
    res=select(q)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    data['method']="view_category"
    return str(data)

@api.route('/User_add_category')
def User_add_category():
    data={}
    log_id=request.args['log_id']
    category=request.args['category']
    q="INSERT INTO `category` VALUES(NULL,(SELECT `user_id` FROM `user` WHERE `login_id`='%s'),'%s')"%(log_id,category)
    print(q)
    res=insert(q)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    data['method']="User_add_category"
    return str(data)

@api.route('/catdelete')
def catdelete():
    data={}
    # log_id=request.args['log_id']
    category_ids=request.args['category_ids']
    q="DELETE FROM `category` WHERE `category_id`='%s'"%(category_ids)
    print(q)
    res=delete(q)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    data['method']="catdelete"
    return str(data)


@api.route('/User_view_category')
def User_view_category():
    data={}
    log_id=request.args['log_id']
    # category_ids=request.args['category_ids']
    q="SELECT * FROM `category` WHERE `user_id`=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')"%(log_id)
    res=select(q)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    data['method']="User_view_category"
    return str(data)


@api.route('/view_buget')
def view_buget():
    data={}
    log_id=request.args['log_id']
    q="SELECT * FROM `budget_limit` WHERE `user_id`=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')"%(log_id)
    res=select(q)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    data['method']="view_buget"
    return str(data)

@api.route('/User_add_budget_amount')
def User_add_budget_amount():
    data={}
    log_id=request.args['log_id']
    budget_amount=request.args['budget_amount']
    # category_ids=request.args['category_ids']
    q="SELECT * FROM `budget_limit` WHERE `user_id`=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')"%(log_id)
    result=select(q)
    if result:
        q="UPDATE `budget_limit` SET `budget_amount`=budget_amount+'%s' , `budget_date`=NOW() WHERE `user_id`=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')"%(budget_amount,log_id)
        update(q)
    else:
        q="INSERT INTO `budget_limit` VALUES(NULL,(SELECT `user_id` FROM `user` WHERE `login_id`='%s'),'%s',NOW())"%(log_id,budget_amount)
        insert(q)

    data['status']="success"
    data['method']="User_add_budget_amount"
    return str(data)



@api.route('/view_expence')
def view_expence():
    data={}
    log_id=request.args['log_id']
    category_ids=request.args['category_ids']
    q="SELECT * FROM `expense` inner join category using(category_id) WHERE `user_id`=(SELECT `user_id` FROM `user` WHERE `login_id`='%s') and category_id='%s'"%(log_id,category_ids)
    res=select(q)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    data['method']="view_expence"
    return str(data)





@api.route('/User_add_expense')
def User_add_expense():
    data={}
    log_id=request.args['log_id']
    expense_amount=request.args['expense_amount']
    category_ids=request.args['category_ids']

   
    q="select * from budget_limit where user_id=(SELECT `user_id` FROM `user` WHERE `login_id`='%s') "%(log_id)
    amount=int(float(select(q)[0]['budget_amount']))
    print(amount)
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    q="SELECT SUM(expense_amount) AS total_expense FROM expense inner join category using(category_id) where user_id=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')  "%(log_id)
    print(q)
    expense_result =select(q)
    expense_amounts = int(expense_result[0]['total_expense']) if expense_result[0]['total_expense'] else 0
    print(expense_amounts)
    if amount==expense_amounts:
        print(amount)
        print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
        print(expense_amounts)
        data['status']="lowbalance"
    else:
        q="INSERT INTO `expense` VALUES(NULL,'%s','%s',curdate())"%(category_ids,expense_amount)
        print(q)
        res=insert(q)
        if res:
            data['status']="success"
            data['data']=res
        else:
            data['status']="failed"
    data['method']="User_add_expense"
    return str(data)


@api.route('/view_report')
def view_report():
    data={}
    log_id=request.args['log_id']
    q="SELECT * FROM  `expense` INNER JOIN `category`  USING(`category_id`) INNER JOIN `budget_limit` USING(`user_id`) INNER JOIN `income` USING (`user_id`) WHERE `user_id`=(SELECT `user_id` FROM `user` WHERE `login_id`='%s') group by expense_id"%(log_id)
    print(q)
    res=select(q)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']="failed"
    data['method']="view_report"
    return str(data)
@api.route('/searchreport')
def searchreport():
    data={}
    log_id=request.args['log_id']
    searchitem=request.args['searchitem']+'%'
    q="SELECT * FROM  `expense` INNER JOIN `category`  USING(`category_id`) INNER JOIN `budget_limit` USING(`user_id`) INNER JOIN `income` USING (`user_id`) WHERE expense.`expense_date`  LIKE '%s'  AND  `user_id`=(SELECT `user_id` FROM `user` WHERE  `login_id`='%s')"%(searchitem,log_id)
    print(q)
    res=select(q)
    data['status']="success"
    data['data']=res
    data['method']="view_report"
    return str(data)

    return str(data)
@api.route('/mycommentgraph')
def mycommentgraph():
    data={}
    # q="SELECT * FROM `category` INNER JOIN `expense` USING(`expense_id`)"
    # res=select()
    data['joyPercentage']=20
    data['sadPercentage']=8
    data['shamePercentage']=3
    data['novaluePercentage']=15
    data['method']="mycommentgraph"
    data['status']="success"




    return str(data)
    







# @api.route('/User_add_expense')
# def User_add_expense():
#     data={}
#     log_id=request.args['log_id']
#     expense_amount=request.args['expense_amount']
#     category_ids=request.args['category_ids']

#     # q="UPDATE `total_balance` SET `balance_amount`=`balance_amount`-'%s' WHERE (SELECT `user_id` FROM `user` WHERE `login_id`='%s')"%(expense_amount,log_id)
#     # update(q)
#     q="select * from budget_limit where user_id=(SELECT `user_id` FROM `user` WHERE `login_id`='%s') "%(log_id)
#     amount=int(float(select(q)[0]['budget_amount']))
#     if amount==expense_amount:
#         data['status']="lowbalance"
#     else:
#         q="INSERT INTO `expense` VALUES(NULL,'%s','%s',curdate())"%(category_ids,expense_amount)
#         print(q)
#         res=insert(q)
#         if res:
#             data['status']="success"
#             data['data']=res
#         else:
#             data['status']="failed"
#     data['method']="User_add_expense"
#     return str(data)