import csv
import sqlite3

# 建立資料庫
def create_table(dbname , tbName):
        try:
            con = sqlite3.connect(dbname)
            SQLcmd = '''CREATE TABLE  IF NOT EXISTS ''' + tbName + ''' 
                    (
                    bill_PayerAccountId NUMERIC ,
                    lineItem_UnblendedCost REAL ,
                    lineItem_UnblendedRate REAL ,
                    lineItem_UsageAccountId NUMERIC ,
                    lineItem_UsageAmount REAL ,
                    lineItem_UsageStartDate TEXT ,
                    lineItem_UsageEndDate TEXT ,
                    product_ProductName TEXT 
                    );'''
            con.execute(SQLcmd) 
            SQLcmd = "CREATE INDEX IF NOT EXISTS idx_ID ON " + tbName + " (bill_PayerAccountId , lineItem_UsageAccountId)"
            con.execute(SQLcmd)
            con.close()  
        except Exception as e:
            return f'Fail: {e}'
          

# 取得檔案內容
def get_data(filename):
    try:
        with open(filename, newline='') as csvFile:
        #轉成一個 dictionary, 讀取 CSV 檔內容，將每一列轉成字典，方便擷取需要的Column
            rows = csv.DictReader(csvFile)
        #取出要的Column
            DataNeeds = [(row['bill/PayerAccountId'],row['lineItem/UnblendedCost'],row['lineItem/UnblendedRate']
                    ,row['lineItem/UsageAccountId'],row['lineItem/UsageAmount'],row['lineItem/UsageStartDate']
                    ,row['lineItem/UsageEndDate'],row['product/ProductName']) for row in rows]
        return DataNeeds
    except Exception as e:
        return f'Fail: {e}'
    
# inser資料
def insert_data(dbname , tbName ,dataimport):
    con = sqlite3.connect(dbname)
    c = con.cursor()
    try:
        for products_insert in dataimport:
            c.execute('''insert into '''+ tbName +'''(bill_PayerAccountId , lineItem_UnblendedCost , lineItem_UnblendedRate,lineItem_UsageAccountId
            ,lineItem_UsageAmount,lineItem_UsageStartDate,lineItem_UsageEndDate,product_ProductName)
            values(?,?,?,?,?,?,?,?)''' , products_insert)
        con.commit()
        con.close()
        return "Success"
    except Exception as e:
        return f'Fail: {e}' 

    
    
# # 手動輸入csv檔名
filename_ = input("请输入csv檔案名稱：")
# filename_ = "output.csv"

# 設定要建立或連線的DB、Table名稱
dbname = "myhwbd.db"
tbName = "SalesItem"

# 呼叫建立DB
create_res = create_table(dbname , tbName)
if type(create_res) == str :
    print("建立失敗:" + create_res)

# 取得csv檔案內容
filecontent = get_data(filename_)
# print(type(filecontent))
if type(filecontent) == list:
    # 資料儲存到DB
    insert_res = insert_data(dbname , tbName , filecontent)
    print(insert_res)
else:
    print("檔案讀取失敗:" + filecontent)


