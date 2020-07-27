import flask
from flask import jsonify , request
import sqlite3
import datetime
import time

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# 設定要連結的資料庫、存放的Table名稱
db_name = "myhwbd.db"
tbName = "SalesItem"

# 第一個API
def select_getitemcost(UsageAccountId_):
    con = sqlite3.connect(db_name)
    # 先不列出Cost為0的項目
    SQLcmd = "select product_ProductName , SUM(lineItem_UnblendedCost) from " + tbName + ''' where 
    lineItem_UsageAccountId = ? and lineItem_UnblendedCost <> 0 group by product_ProductName '''
    cursor=con.execute(SQLcmd, [UsageAccountId_]) 
    get_datas = cursor.fetchall()
    con.close()
    return get_datas

# 第二支API
def select_usageamount(UsageAccountId_):
    con = sqlite3.connect(db_name)
    # 先撈出所有產品
    SQLcmd = '''select product_ProductName
    from ''' + tbName + ''' where lineItem_UsageAccountId = ? and lineItem_UsageAmount <> 0
    group by product_ProductName '''
    cursor=con.execute(SQLcmd, [UsageAccountId_]) 
    # test_datas = c.execute("select * from TestTable where lineItem_UsageAccountId = '" + UsageAccountId_ + "'")
    get_product = cursor.fetchall()
    returnlist = []
    for rowA in get_product:
        # print(rowA[0])
        # 依照所有產品撈出日期範圍
        SQLcmd = '''select date(min(lineItem_UsageStartDate)) , date(Max(lineItem_UsageEndDate)) 
            from '''+ tbName +''' where lineItem_UsageAccountId = ? and product_ProductName = ? '''
        cursor=con.execute(SQLcmd, [UsageAccountId_ , rowA[0]]) 
        get_dates = cursor.fetchall() 
        # for rowB in get_date :
        #     print(rowA , rowB)
        product_daily = []   
  
        StartDate = time.strptime(get_dates[0][0], "%Y-%m-%d")
        EndDate = time.strptime(get_dates[0][1], "%Y-%m-%d")
        StartDate = datetime.date(StartDate[0], StartDate[1], StartDate[2])
        EndDate =  datetime.date(EndDate[0], EndDate[1], EndDate[2])
        # 抓出該產品每日總用量
        while StartDate <= (EndDate): 
            SQLcmd = '''select SUM(lineItem_UsageAmount)
            from ''' + tbName + ''' where lineItem_UsageAccountId = ? and product_ProductName = ? 
            and date(lineItem_UsageStartDate) <= ? and date(lineItem_UsageEndDate) >= ?'''
            cursor=con.execute(SQLcmd, [UsageAccountId_ , rowA[0] , StartDate , StartDate]) 
            get_sum = cursor.fetchall()
            product_daily = product_daily + [StartDate.strftime("%Y-%m-%d") , get_sum[0]]

            StartDate = StartDate + datetime.timedelta(days = 1)   
        returnlist = returnlist + [rowA[0] , product_daily]
    con.close() 
    return returnlist


@app.route('/', methods=['GET'])
def home():
    return "<h1>Leo's Flask API demo</h1>"


@app.route('/mydataTest', methods=['GET'])
def mydataTest():
    if 'usageid' in request.args:
        id_usageid = request.args['usageid']
        getmydata = select_getitemcost(id_usageid)
        return jsonify(getmydata)
    elif 'dailyusageid' in request.args:
        id_dailyusageid = request.args['dailyusageid']
        getmydata = select_usageamount(id_dailyusageid)
        return jsonify(getmydata)
    
app.run()