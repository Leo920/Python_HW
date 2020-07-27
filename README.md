# Python_HW 

## 簡述 

Python 基礎練習，主要分兩部分:


1. csv檔案讀取、儲存
2. API存取資料庫內容




## filesave.py 

可以透過user輸入檔名，讀取指定csv檔。建立資料庫的名稱、Table目前直接寫死在程式，未來優化部分，可以將對資料庫的操作整理成一個模組，方便程式碼重複利用。

table schema

ColumnName | Type 
---------- | ---- 
bill_PayerAccountId | NUMERIC 
lineItem_UnblendedCost | REAL 
lineItem_UnblendedRate | REAL 
lineItem_UsageAccountId | NUMERIC 
lineItem_UsageAmount | REAL 
lineItem_UsageStartDate | TEXT 
lineItem_UsageEndDate | TEXT 
product_ProductName | TEXT 

以bill_PayerAccountId、lineItem_UsageAccountId兩個欄位建立index，因為提供的資料並沒有適合當作PK的欄位組合，因此未設定PK

## api_demo.py 

建立兩支API功能

###第一支API : select_getitemcost

輸入 lineItem_UsageAccountId ，回傳該ID各項產品的lineItem_UnblendedCost總合，先不列出Cost為0的項目

####URL : /mydataTest?usageid=lineItem_UsageAccountId

####輸出內容:

 ```JSON
            [
                ["product_ProductName_A",sum(lineItem_UnblendedCost)],
                ["product_ProductName_B",sum(lineItem_UnblendedCost)], ...
            ]
  ```
  
###第二支API : select_usageamount

輸入 lineItem_UsageAccountId ，回傳各項產品**每日**使用量。我認為這題較為複雜，各項產品使用的紀錄從單日使用到一整個月每日使用都有；目前想到最直接的解決方法是先撈出各項產品名稱，再依照各項產品抓出有使用的日期區間，再依照該日期區間，抓取每日的使用量。這樣迴圈地跑法會效能會非常不佳，未來要繼續尋找其他方式進行優化，另外也可以想辦法顯示資料抓取進度，避免user無止盡得等待。

####URL : /mydataTest?dailyusageid=lineItem_UsageAccountId

####輸出內容:

 ```JSON
            [
                "product_ProductName_A",
                [
                  "YYYY-MM-01" , [sum(lineItem_UsageAmount)] ,
                  "YYYY-MM-02" , [sum(lineItem_UsageAmount)] , ...
                ]
                "product_ProductName_B",
                [
                  "YYYY-MM-01" , [sum(lineItem_UsageAmount)] ,
                  "YYYY-MM-02" , [sum(lineItem_UsageAmount)] , ...
                ]
                ...
            ]
  ```
