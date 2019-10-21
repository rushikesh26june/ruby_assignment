# Product Database Update Application
Product Master table update

## Usage
1.	**Requirements**:  
    a.	Packages: Anaconda, Python3  
    b.	Database: MySql   
    
2.	**Configure Settings**:  
    a.	Install MySql Server: https://dev.mysql.com/downloads/mysql/    
    b.  Install Mysql Workbench: https://dev.mysql.com/downloads/workbench/   
    c.  Create Schema in MySql workbench with name: 'ruby_assignment'
    d.  Import sql dump file (`dump.sql`) present in root directory to create table structure as required
          
3.	**Database update Application**:  
    a.	Run driver.py   
    b.  Run Postman to invoke the application at `localhost:5000/invoke_master`    
    c.  Send a POST request: with the required input specified in 'input.json'
