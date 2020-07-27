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

第一支API : select_getitemcost
