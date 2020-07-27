# Python_HW 

## 簡述 

Python 基礎練習，主要分兩部分:


1. csv檔案讀取、儲存
2. API存取資料庫內容


## filesave.py 

可以透過user輸入檔名，讀取指定csv檔。建立資料庫的名稱、Table目前直接寫死在程式，未來優化部分，可以將對資料庫的操作整理成一個模組，方便程式碼重複利用。

#### Table Shema

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

利用flask快速建立兩支API功能，但因為沒有實際架設過API，還沒能成功架設可供測試的API，僅附上API的程式碼。預計可以透過AWS等雲端服務，快速進行部屬，應能解決掉自建API server的硬體、網路設定等問題，希望未來能完成API的最後建置作業。

### 第一支API : select_getitemcost

輸入 lineItem_UsageAccountId ，回傳該ID各項產品的lineItem_UnblendedCost總合，先不列出Cost為0的項目

#### URL : /mydataTest?usageid=lineItem_UsageAccountId

#### 輸出內容:

 ```JSON
            [
                ["product_ProductName_A",sum(lineItem_UnblendedCost)],
                ["product_ProductName_B",sum(lineItem_UnblendedCost)], ...
            ]
  ```
  
### 第二支API : select_usageamount

輸入 lineItem_UsageAccountId ，回傳各項產品**每日**使用量。我認為這題較為複雜，各項產品使用的紀錄從單日使用到一整個月每日使用都有；目前想到最直接的解決方法是先撈出各項產品名稱，再依照各項產品抓出有使用的日期區間，再依照該日期區間，抓取每日的使用量。這樣迴圈地跑法會效能會非常不佳，未來要繼續尋找其他方式進行優化，另外也可以想辦法顯示資料抓取進度，避免user無止盡得等待。

#### URL : /mydataTest?dailyusageid=lineItem_UsageAccountId

#### 輸出內容:

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

#### 總結

從頭開始研究Python的開發，不只是不熟悉的語言、開發環境也必須自行上網尋找資料；經過一周的研究、各方前輩與同事的幫助，總算是找到開發的方向。很抱歉未能在期限內完成題目的所有要求，大部分程式功能已完成，但也還有很多地方可以優化，包括例外狀況處理、資料存取的速度優化、本來預計將資料庫操做的功能模組化，也因為對python架構的不熟悉暫時沒能完成；但這段時間內學到的內容非常豐富，相信未來若要繼續進行python的開發，可以更快找出問題，快速上手的
