# Product Database Update Application

Product Master table application

## Usage
1.	**Requirements**:  
    a.	Packages: Anaconda, Python3  
    b.	Database: MySql   

2.	**Configure Settings**:  
    a.	Install MySql Server: https://dev.mysql.com/downloads/mysql/    
    b.  Install Mysql Workbench: https://dev.mysql.com/downloads/workbench/   
    c.  Create Schema in MySql workbench with name: 'ruby_assignment' 

3.	**Database update Application**:  
    a.	Run driver.py   
    b.  Run Postman to invoke the application at the endpoint: `localhost:5000/invoke_master`    
    c.  Requests:
    1. Create Master Table:  POST request with sample json: `test/test_req_create.json`         
    2. Insert Row in Master Table: POST request with sample json: `test/test_req_insert.json`      
    3. Append/ Make changes to existing row: 
    a. GET Request: Product Sku id and Master Table name to be passed in query params. e.g. `127.0.0.1:8080/invoke_master?sku_id=RI-12&master_table_name=master_group`
    b. POST Request: Sample JSON: `test/test_req_append.json`
4. **Sample POSTMAN Collection**: `internship.postman_collection.json`
