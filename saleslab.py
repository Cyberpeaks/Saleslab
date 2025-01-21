from flask import Flask, render_template, request, session, redirect, url_for

import os

#from models import *

from flask_mysqldb import MySQL
from flask_session import Session
from datetime import datetime
import re

app = Flask(__name__)

app.secret_key = 'your secret key'
#engine = create_engine("mysql://myadmin:ol1PHP@20@localhost",echo=True)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ol1PHP*20'
app.config['MYSQL_DB'] = 'GOBT'


mysql = MySQL(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
date = datetime.date(datetime.now())



# ADD ADMINISTRATOR TO DATABASE
@app.route("/adregad", methods = ['POST','GET'])
def add_admin():
    page = "Add Administrator"

    if request.method == 'POST':

        fname = request.form.get("firstname")
        lname = request.form.get("lastname")
        gender = request.form.get("radgender")
        username = request.form.get("username")
        password = request.form.get("pwdUser")
        confPassword = request.form.get("confPass")
    #-------------------------------------------------------------------------------

        cur = mysql.connection.cursor() # connection variable

    #-------------------------------------------------------------------------------
        # This section checks if email already exits
        params = [username]
        count = cur.execute("SELECT * from admins WHERE username=%s", params)
        if count > 0:
            msg = "WARNING: This administrator already exist!"
            return render_template("register_admin_form.html",page = page, msg = msg)
        else:
            pass
    #------------------------------------------------------------------------------
        msg = "Successful"
    # Inserts data in Customers table
        cur.execute("INSERT INTO admins(firstname, lastname, gender, username, password)VALUES(%s, %s, %s, %s, %s)",
        (fname,lname,gender,username,password))
        mysql.connection.commit()
    #-------------------------------------------------------------------------------

        cur.close() #close connection
    else:
        msg = "Please fill the form"

    return render_template("register_admin_form.html",page = page, msg = msg)


# LOGIN AS ADMINISTRATOR
@app.route("/signIn", methods = ['GET','POST'])
def admin_SignIn():
    page = "Admin Login"
    #return render_template("admin_login_form.html", page = page)
    return render_template("login-admin.html", page = page)

@app.route("/adminlog",methods = ['POST','GET'])
def login_Admin():
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admins WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        global account
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            sales_count = row_counter("sales")
            products_count = row_counter("products")
            customers_count = row_counter("customers")
            locations_count = row_counter("locations")
            page = "ADMIN"
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['username'] = account['username']
            session['firstname'] = account['firstname']
            firstname = session['firstname']
            username = session['username']

            salespersons = performance()

            # Redirect to admin index page
#i want to collect account as a parametter
            msg = "Welcome, "
            return render_template("admin_index.html",account=account,sales_count=sales_count,products_count=products_count,customers_count=customers_count,locations_count=locations_count, salespersons = salespersons,msg=msg, page = page, username = username, firstname = firstname)
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
            page = "Oops!"
            return render_template("login_failed.html", msg=msg, page = page)

@app.route("/admin",methods = ['GET'])
def dashboard():
    sales_count = row_counter("sales")
    products_count = row_counter("products")
    customers_count = row_counter("customers")
    locations_count = row_counter("locations")
    page = "ADMIN"
    msg = "Welcome, "
    # Get session data, we can access this data in other routes

    firstname = session.get('firstname')
    username = session.get('username')

    salespersons = performance()

    if salespersons:

        return render_template("admin_index.html",sales_count=sales_count,products_count=products_count,customers_count=customers_count,locations_count=locations_count, salespersons = salespersons,msg=msg, page = page, username = username, firstname = firstname)
    else:
        return render_template("admin_index.html",sales_count=sales_count,products_count=products_count,customers_count=customers_count,locations_count=locations_count, salespersons = salespersons,msg=msg, page = page, username = username, firstname = firstname)

# LOGOUT ADMIN
@app.route('/admin/logout/')
def admin_logout():
    # remove session data
    session.pop('loggedin', None)
    session.pop('username',None)
    session.pop('firstname',None)
    return redirect(url_for('admin_SignIn'))


@app.route('/sales/logout/')
def sales_logout():
    # remove session data
    session.pop('loggedin', None)
    session.pop('username',None)
    session.pop('firstname',None)
    return redirect(url_for('sales_SignIn'))



# VIEW ADMINISTRATORS IN DATABASE
@app.route("/administrators",methods = ['POST','GET'])
def admin_List():
    page = "Administrators"
    firstname = session.get('firstname')
    username = session.get('username')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM admins")
    employees = cursor.fetchall()
    if employees:
        return render_template("list_administrators.html",page = page, employees=employees,firstname=firstname)
    else:
        return 'Empty List'
    # Fetch one record and return result


#ADD EMPLOYEE TO DATABASE
@app.route("/iadempad", methods = ['GET','POST'])
def reg_Emp():
    firstname = session['firstname']
    username = session['username']
    page = "Add Employee"
    msg = "Enter employee details"
    return render_template("register_employee_form.html",msg = msg, page = page,firstname = firstname)

@app.route("/adempad", methods = ['POST','GET'])
def add_Emp():
    page = "Add Employee"
    msg = "Enter employee details"

    firstname = session.get('firstname')
    username = session.get('username')

    if request.method == 'POST':

        fname = request.form.get("firstname")
        lname = request.form.get("lastname")
        dob = request.form.get("dob")
        gender = request.form.get("radgender")
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        doe = request.form.get("doe")
        phone = request.form.get("phone")
    #-------------------------------------------------------------------------------

        cur = mysql.connection.cursor() # connection variable

    #-------------------------------------------------------------------------------
        # This section checks if email already exits
        params = [username]
        count = cur.execute("SELECT * from employees WHERE username=%s", params)
        if count > 0:
            msg = "WARNING: This employee already exist!"
            return render_template("register_employee_form.html",page = page, msg = msg,firstname=firstname)
        else:
            pass
    #------------------------------------------------------------------------------
        msg = "Employee Added Successfully"
    # Inserts data in Customers table
        cur.execute("INSERT INTO employees(firstname,lastname,dob,gender,username,password,role,doe,phone)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (fname,lname,dob,gender,username,password,role,doe,phone))
        mysql.connection.commit()
    #-------------------------------------------------------------------------------

        cur.close() #close connection
    else:
        msg = "Please fill the form"

    return render_template("register_employee_form.html",page = page, msg = msg,firstname=firstname)

        # Show the login form with message (if any)
# -------------------------------------------------------------------------------------------------------------


# VIEW EMPLOYEES IN DATABASE
@app.route("/employees",methods = ['POST','GET'])
def emp_List():
    page = "Employees"
    status = "CURRENT"

    firstname = session.get('firstname')
    username = session.get('username')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SET @n = 0")
    cursor.execute("""SELECT @n := @n+1 AS number,CONCAT(firstname," ",lastname)
    AS name,phone,gender,username,doe FROM employees WHERE status=%s""",[status])
    employees = cursor.fetchall()
    if employees:
        return render_template("list_employee.html",page = page, employees=employees,firstname=firstname)
    else:
        return 'Empty List'
    # Fetch one record and return result


# REMOVE EMPLOYEE Section

#REMOVE EMPLOYEE FORM
@app.route("/select-rem-employee",methods = ['POST','GET'])
def select_rem_main_emp():
    page = "Remove Employee"
    msg = "Choose Employee"
    status = "CURRENT"
    firstname = session.get('firstname')
    username = session.get('username')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM employees WHERE status =%s",[status])
    employees = cursor.fetchall()
    if employees:
        return render_template("remove_employee.html",page = page, employees=employees,msg=msg, firstname=firstname)
    else:
        msg = 'Empty List'
        return render_template("remove_employee.html",page = page, employees=employees,msg=msg, firstname=firstname)
    # Fetch one record and return result

# PROCESS REMOVE EMPLOYEE
@app.route("/del-employee",methods = ['POST','GET'])
def rem_employee():
    page = "Remove Employee"
    msg = "Choose Employee"
    status = "NON-CURRENT"

    firstname = session.get('firstname')
    username = session.get('username')

    selected = request.form['selAnswer']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("UPDATE employees SET status =%s WHERE id=%s",(status,selected))
    mysql.connection.commit()

    msg = "Deleted Successfully!"
    status = "CURRENT"

    cursor.execute("SELECT * FROM employees WHERE status=%s",[status])
    employees = cursor.fetchall()
    return render_template("remove_employee.html",page=page,msg = msg,firstname = firstname, employees=employees)

    # Fetch one record and return result

#END REMOVE EMPLOYEE SECTION

#UPDATE EMPLOYEE SECTION

#UPDATE Employee FORM1
@app.route("/select-update-employee",methods = ['POST','GET'])
def select_update_emp():
    page = " Update Employee"
    msg = "Choose Employee"
    status = "CURRENT"

    firstname = session.get('firstname')
    username = session.get('username')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM employees WHERE status=%s",[status])
    employees = cursor.fetchall()
    if employees:
        return render_template("update_employee.html",page = page, employees=employees,msg=msg, firstname=firstname)
    else:
        msg = 'Empty List'
        return render_template("update_employee.html",page = page, employees=employees,msg=msg, firstname=firstname)
    # Fetch one record and return result

# PROCESS UPDATE SALESPERSON
@app.route("/update-employee-form",methods = ['POST','GET'])
def update_employee_form():
    page = "Update Employee"
    msg = "Edit Employee"
    status = "CURRENT"

    firstname = session.get('firstname')
    username = session.get('username')
    my_username=request.form.get('username')


    status = "CURRENT"
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM employees WHERE username=%s",[my_username])
    employees = cursor.fetchall()
    if employees:
        for employee in employees:
            user_id = employee['id']
            session["user_id"] = user_id
        return render_template("update_employee_form.html",page=page,msg = msg,
        firstname = firstname, employees=employees,user_id=user_id)
    else:
        return "Can not fetch employee"


# PROCESS UPDATE EMPLOYEE
@app.route("/update-employee",methods = ['POST','GET'])
def update_employee():
    page = "Remove Employee"
    msg = "Choose Employee"
    status = "CURRENT"
    employee_id=session.get("user_id",None)


    firstname = session.get('firstname')
    username = session.get('username')

    my_username = request.form.get('username')
    my_firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    phone = request.form.get('phone')
    gender = request.form.get('radgender')
    doe = request.form.get('doe')
    dob = request.form.get('dob')
    position = request.form.get('role')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    my_update = cursor.execute("""UPDATE employees SET firstname=%s,lastname=%s,
    phone=%s,gender=%s,doe=%s,dob=%s,role=%s WHERE id=%s """,
    (my_firstname,lastname,phone,gender,doe,dob,position,employee_id))
    if my_update:
        mysql.connection.commit()
        return emp_List()
    else:
        return "Update Failed!"
    # Fetch one record and return result


# Sales Person Login Section
@app.route("/salesperson", methods = ['GET','POST'])
def sales_SignIn():
    page = "Sales Person Login"
    return render_template("staff_login_form.html", page = page)

@app.route("/saleslog",methods = ['POST'])
def login_Sales():
    msg = ''
    greeting = "Welcome, "
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        sales = "YES"
        status = "CURRENT"
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT * FROM employees WHERE username = %s
        AND password = %s AND sales_permit =%s AND status =%s """, (username,password,sales,status))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            page = "Sales"
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['username'] = account['username']
            session['firstname'] = account['firstname']
            session['id'] = account['id']
            session['sales_permit'] = account['sales_permit']
            firstname = session['firstname']
            id = session['id']

            username = session['username']
            sales_permit = session['sales_permit']
            # Redirect to home page


            firstname = session.get('firstname')
            employee_id = session.get('id')

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SET @n = 0")
            cursor.execute("""SELECT @n := @n+1 AS number, sales.id AS id, sales.sales_Date, sales.quantity,
            sales.remark, products.product_name, sales.unit_price AS Unit_Price, sales.unit_price*sales.quantity AS Amount,
             CONCAT(customers.firstname," ",customers.lastname) AS Customer FROM sales,products,customers
             WHERE sales.product_id = products.id AND sales.customer_id = customers.id
             AND salesPerson_id=%s AND sales_Date=%s""",(employee_id,date))
            mysales = cursor.fetchall()
            if mysales:
                msg = firstname +"'s Sales "
                return render_template("staff_signedIn.html",greeting=greeting,page = page, msg = msg, mysales = mysales, date = date, firstname = firstname)
            else:
                msg ="You have not recorded any sales for today"
                return render_template("staff_signedIn.html",greeting=greeting,page = page, date = date, msg = msg, firstname = firstname)
            # Fetch one record and return result

            return render_template("staff_signedIn.html", msg=msg,sales_permit=sales_permit, page = page, username = username, firstname = firstname)

        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
            page = "Oops!"
            return render_template("login_failed.html",greeting=greeting, msg=msg, page = page)
        return 'Sales Login failed! \n Incorrect username/password!'



#VIEW SALESPERSON IN DATABASE
@app.route("/salespersons",methods = ['POST','GET'])
def salesperson_List():
    firstname = session.get('firstname')
    username = session.get('username')

    page = "Sales Persons"
    sales = "YES"
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SET @n = 0")
    cursor.execute("""SELECT @n := @n+1 AS number,CONCAT(firstname," ",lastname)AS
    name, role,doe FROM employees WHERE sales_permit=%s""",[sales])
    salespersons = cursor.fetchall()
    if salespersons:
        return render_template("list_salesperson.html",page = page, salespersons = salespersons, firstname=firstname)
    else:
        msg = 'Empty List'
        return render_template("list_salesperson.html",page = page,msg=msg,salespersons = salespersons, firstname=firstname)
    # Fetch one record and return result


# SELECT EMPLOYEES IN DATABASE
@app.route("/select-add-sales-persons",methods = ['POST','GET'])
def select_add_emp():
    page = "Add Salesperson"
    msg = "Choose Employee"
    status = "CURRENT"

    firstname = session.get('firstname')
    username = session.get('username')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM employees WHERE status=%s",
    [status])
    employees = cursor.fetchall()
    if employees:
        return render_template("add_sales_person.html",page = page, employees=employees,msg=msg, firstname=firstname)
    else:
        msg = 'Empty List'
        return render_template("add_sales_person.html",page = page, employees=employees,msg=msg, firstname=firstname)
    # Fetch one record and return result



@app.route("/add-persons",methods = ['POST','GET'])
def add_sales_person():
    status="CURRENT"
    page = "Add Salesperson"
    msg = "Choose Employee"

    firstname = session.get('firstname')
    username = session.get('username')

    sales = "YES"
    selected = request.form['selAnswer']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("UPDATE employees SET sales_permit=%s WHERE id=%s",(sales,selected))
    mysql.connection.commit()

    cursor.execute("SELECT * FROM employees WHERE sales_permit=%s AND id=%s",(sales,selected))
    picks = cursor.fetchone()
    if picks:
        msg = "You added"
        session['loggedin'] = True
        session['firstname'] = picks['firstname']
        firstname = session['firstname']

        cursor.execute("SELECT * FROM employees WHERE status=%s",[status])
        employees = cursor.fetchall()
        return render_template("add_sales_person.html",page=page,msg = msg,firstname = firstname, employees=employees)
    else:
        return 'Can not fetch employee'

    # Fetch one record and return result

#REMOVE SALESPERSON FORM
@app.route("/select-rem-sales-persons",methods = ['POST','GET'])
def select_rem_emp():
    page = "Remove Salesperson"
    msg = "Choose Salesperson"
    sales = "YES"

    firstname = session.get('firstname')
    username = session.get('username')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM employees WHERE sales_permit=%s",[sales])
    employees = cursor.fetchall()
    if employees:
        return render_template("remove_sales_person.html",page = page, employees=employees,msg=msg, firstname=firstname)
    else:
        msg = 'Empty List'
        return render_template("remove_sales_person.html",page = page, employees=employees,msg=msg, firstname=firstname)
    # Fetch one record and return result

# PROCESS REMOVE SALESPERSON
@app.route("/del-persons",methods = ['POST','GET'])
def rem_sales_person():
    page = "Remove Salesperson"
    msg = "Choose Employee"

    firstname = session.get('firstname')
    username = session.get('username')

    sales = "NO"
    selected = request.form['selAnswer']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("UPDATE employees SET sales_permit=%s WHERE id=%s",(sales,selected))
    mysql.connection.commit()

    sales  = "YES"
    cursor.execute("SELECT * FROM employees WHERE sales_permit=%s AND id=%s",(sales,selected))
    picks = cursor.fetchone()
    if picks:
        msg = "You removed"
        session['loggedin'] = True
        session['firstname'] = picks['firstname']
        firstname = session['firstname']

        cursor.execute("SELECT * FROM employees WHERE sales_permit=%s",[sales])
        employees = cursor.fetchall()
        return render_template("remove_sales_person.html",page=page,msg = msg,firstname = firstname, employees=employees)
    else:
        return 'Can not fetch employee'

    # Fetch one record and return result


@app.route("/select-customer",methods = ['POST','GET'])
def select_cus():
    firstname = session.get('firstname')
    username = session.get('username')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    if customers:
        return render_template("add_sales.html",customers = customers,username=username)
    else:
        return 'Empty List'
    # Fetch one record and return result


# ADD LOCATION TO DATABASE
@app.route("/add-locations", methods = ['POST','GET'])
def add_location():
    page = "Add Locations"
    firstname = session.get('firstname')
    username = session.get('username')

    if request.method == 'POST':

        local = request.form.get("locality")
        lotown = request.form.get("town")
    #-------------------------------------------------------------------------------

        cur = mysql.connection.cursor() # connection variable

    #-------------------------------------------------------------------------------
        # This section checks if email already exits
    #------------------------------------------------------------------------------
        msg = "Successful"
    # Inserts data in Customers table
        cur.execute("INSERT INTO locations(locality, town)VALUES(%s, %s)",
        (local,lotown))
        mysql.connection.commit()
    #-------------------------------------------------------------------------------

        cur.close() #close connection
    else:
        msg = "Please fill the form"

    return render_template("register_location_form.html",page = page, msg = msg,firstname=firstname)

# VIEW LOCATION STARTS here

#VIEW CUSTOMERS IN DATABASE
@app.route("/location-list",methods = ['POST','GET'])
def location_List():
    page = "Our Customers Locations"
    firstname = session.get('firstname')
    username = session.get('username')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SET @n = 0")
    cursor.execute("""SELECT @n := @n+1 AS number,locality,town FROM locations """)
    locations = cursor.fetchall()
    if locations:
        return render_template("list_locations.html",page = page,
        locations=locations,firstname=firstname)
    else:
        return 'Empty List'
    # Fetch one record and return result

# END OF VIEW LOCATION


# ADD CUSTOMER TO DATABASE
@app.route("/add-customer", methods = ['POST','GET'])
def add_customer():
    firstname = session.get('firstname')
    username = session.get('username')

    page = "Add Customer"

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM locations")
    locations = cursor.fetchall()
    if locations:


        if request.method == 'POST':

            fname = request.form.get("firstname")
            lname = request.form.get("lastname")
            phone = request.form.get("phonecall")
            gender = request.form.get("radgender")
            location = request.form.get("location")
            doee = request.form.get("doe")

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------
                # This section checks if email already exits
            params = [phone]
            count = cursor.execute("SELECT * from customers WHERE phone=%s", params)
            if count > 0:
                msg = "WARNING: This customer already exist!"
                cursor.execute("SELECT * FROM locations")
                locations = cursor.fetchall()
                return render_template("register_customer_form.html",page = page, msg = msg,locations = locations, firstname=firstname)
            else:
                pass
    #------------------------------------------------------------------------------

            msg = "Successful"
            # Inserts data in Customers table
            cursor.execute("INSERT INTO customers(firstname,lastname,phone,gender,location_id,doe)VALUES(%s,%s, %s, %s, %s, %s)",
            (fname,lname,phone,gender,location,doee))
            mysql.connection.commit()
            return render_template("register_customer_form.html",page = page, msg = msg, firstname=firstname)

    #-------------------------------------------------------------------------------
            cur.close() #close connection
        else:
            msg = "Please fill the form"

        return render_template("register_customer_form.html",page = page, locations = locations, firstname=firstname)
    else:
        return 'Empty List! Please add locations first.'

#VIEW CUSTOMERS IN DATABASE
@app.route("/customer-list",methods = ['POST','GET'])
def customer_List():
    page = "Our Customers"
    firstname = session.get('firstname')
    username = session.get('username')
    status = "CURRENT"

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SET @n = 0")
    cursor.execute("""SELECT @n := @n+1 AS number,CONCAT(customers.firstname,
    " ",customers.lastname) AS name, customers.phone AS phone, customers.gender AS
    gender, CONCAT(locations.locality,", ",locations.town) AS location, customers.doe AS doe FROM customers,
    locations WHERE customers.location_id = locations.id AND customers.status=%s""",[status])
    customers = cursor.fetchall()
    if customers:
        return render_template("list_customers.html",page = page, customers = customers, firstname=firstname)
    else:
        return 'Empty List'
    # Fetch one record and return result

# REMOVE CUSTOMER Section

#REMOVE CUSTOMER FORM
@app.route("/select-rem-customer",methods = ['POST','GET'])
def select_rem_main_cust():
    page = "Remove Customer"
    msg = "Choose Customer"
    status = "CURRENT"
    firstname = session.get('firstname')
    username = session.get('username')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM customers WHERE status =%s",[status])
    customers = cursor.fetchall()
    if customers:
        return render_template("remove_customer.html",page = page,
        customers=customers,msg=msg, firstname=firstname)
    else:
        msg = 'Empty List'
        return render_template("remove_customer.html",page = page,
        customers=customers,msg=msg, firstname=firstname)
    # Fetch one record and return result

# PROCESS CUSTOMER PRODUCTS
@app.route("/del-customer",methods = ['POST','GET'])
def remove_customer():
    page = "Remove Customer"
    msg = "Choose Customer"
    status = "NON-CURRENT"

    firstname = session.get('firstname')
    username = session.get('username')

    selected = request.form['selAnswer']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("UPDATE customers SET status =%s WHERE id=%s",(status,selected))
    mysql.connection.commit()

    msg = "Deleted Successfully!"
    status = "CURRENT"

    cursor.execute("SELECT * FROM customers WHERE status=%s",[status])
    customers = cursor.fetchall()
    return render_template("remove_customer.html",page=page,msg = msg,
    firstname = firstname, customers=customers)

    # Fetch one record and return result

#END REMOVE CUSTOMER SECTION

#UPDATE CUSTOMER SECTION

#UPDATE CUSTOMER FORM1
@app.route("/select-update-customer",methods = ['POST','GET'])
def select_update_customer():
    page = " Update Customers"
    msg = "Choose Customer"
    status = "CURRENT"

    firstname = session.get('firstname')
    username = session.get('username')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM customers WHERE status=%s",[status])
    customers = cursor.fetchall()
    if customers:
        return render_template("update_customer.html",page = page,
        customers=customers,msg=msg, firstname=firstname)
    else:
        msg = 'Empty List'
        return render_template("update_customer.html",page = page,
        customers=customers,msg=msg, firstname=firstname)
    # Fetch one record and return result

# PROCESS UPDATE CUSTOMER
@app.route("/update-customer-form",methods = ['POST','GET'])
def update_customer_form():
    page = "Update Customers"
    msg = "Edit Customer"
    status = "CURRENT"

    firstname = session.get('firstname')
    username = session.get('username')
    #company_id=request.form.get('id')
    selected = request.form.get('customer_id')

    status = "CURRENT"
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM customers WHERE id=%s",[selected])
    customers = cursor.fetchall()

    cursor.execute("SELECT * FROM locations")
    locations = cursor.fetchall()
    if customers:
        for customer in customers:
            customer_id = customer['id']
            session["customer_id"] = customer_id
        return render_template("update_customer_form.html",
        page=page,msg = msg,firstname = firstname, customers=customers,
        customer_id=customer_id,locations=locations)
    else:
        return "Can not fetch customers"


# PROCESS UPDATE CUSTOMER
@app.route("/update-customer",methods = ['POST','GET'])
def update_customer():
    page = "Update Customer"
    msg = "Choose Customer"
    status = "CURRENT"

    firstname = session.get('firstname')
    username = session.get('username')

    my_primary = session.get("customer_id")
    cus_fname = request.form.get('firstname')
    cus_lname = request.form.get('lastname')
    phone = request.form.get('phonecall')
    doe = request.form.get('doe')
    gender = request.form.get('radgender')
    address = request.form.get('address')


    location_id = request.form.get('location')


    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    my_update = cursor.execute("""UPDATE customers SET firstname=%s,
    lastname=%s,phone=%s,location_id=%s,gender=%s,address=%s,status=%s
    WHERE id=%s """,(cus_fname,cus_lname,phone,location_id,gender,address,
    status,my_primary))
    if my_update:
        mysql.connection.commit()

        return customer_List()

    else:
        msg = "Update Failed"
        return render_template("error_monitor.html",msg=msg)
    # Fetch one record and return result

# END UPDATE CUSTOMER SESSION
#---------------------------------------------------------------------------------------------------------------------------




# ADD COMPANY TO DATABASE
@app.route("/add-companies")
def adding_companies():
    page = "Add Company"
    firstname = session.get('firstname')
    username = session.get('username')

    msg = "Fill company details."
    return render_template("register_company_form.html",page = page, msg = msg,firstname=firstname)


@app.route("/add-Companies", methods = ['POST','GET'])
def add_company():
    page = "Add Company"
    firstname = session.get('firstname')
    username = session.get('username')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    if companies:
        if request.method == 'POST':
            company = request.form.get("company")
            businesstype = request.form.get("bizt")
            contact = request.form.get("contactperson")
            phone = request.form.get("phonecall")
            email = request.form.get("email")

        #------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------
                    # This section checks if email already exits
            params = [phone]
            count = cursor.execute("SELECT * from companies WHERE phone=%s", params)
            if count > 0:
                msg = "WARNING: This company already exist!"
                return render_template("register_company_form.html",page = page, msg = msg,companies = companies,firstname=firstname)
            else:
                pass
        #------------------------------------------------------------------------------

            msg = company +" added successful"
            # Inserts data in Customers table
            cursor.execute("INSERT INTO companies(companyname,businesstype,contact_person,phone,email)VALUES(%s,%s,%s,%s,%s)",
            (company,businesstype,contact,phone,email))
            mysql.connection.commit()
            return render_template("register_company_form.html",page = page, msg = msg,firstname=firstname)

        #-------------------------------------------------------------------------------
            cur.close() #close connection
        else:
            msg = "Please fill the form"

    return render_template("register_company_form.html",page = page, msg = msg,firstname=firstname)


#VIEW COMPANIES IN DATABASE
@app.route("/company-list",methods = ['POST','GET'])
def company_list():
    firstname = session.get('firstname')
    username = session.get('username')
    page = "Partner Companies"
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    if companies:
        return render_template("list_companies.html",page = page, companies = companies,firstname=firstname)
    else:
        return 'Empty List'
    # Fetch one record and return result


#---------------------------------------------------------------------------------------------------------------------------
# REMOVE COMPANY Section

#REMOVE COMPANY FORM
@app.route("/select-rem-company",methods = ['POST','GET'])
def select_rem_main_comp():
    page = "Remove Company"
    msg = "Choose Company"
    status = "CURRENT"
    firstname = session.get('firstname')
    username = session.get('username')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM companies WHERE status =%s",[status])
    companies = cursor.fetchall()
    if companies:
        return render_template("remove_company.html",page = page, companies=companies,msg=msg, firstname=firstname)
    else:
        msg = 'Empty List'
        return render_template("remove_company.html",page = page, companies=companies,msg=msg, firstname=firstname)
    # Fetch one record and return result

# PROCESS REMOVE COMPANY
@app.route("/del-company",methods = ['POST','GET'])
def remove_company():
    page = "Remove Company"
    msg = "Choose Company"
    status = "NON-CURRENT"

    firstname = session.get('firstname')
    username = session.get('username')

    selected = request.form['selAnswer']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("UPDATE companies SET status =%s WHERE id=%s",(status,selected))
    mysql.connection.commit()

    msg = "Deleted Successfully!"
    status = "CURRENT"

    cursor.execute("SELECT * FROM companies WHERE status=%s",[status])
    companies = cursor.fetchall()
    return render_template("remove_company.html",page=page,msg = msg,firstname = firstname, companies=companies)

    # Fetch one record and return result

#END REMOVE COMPANY SECTION

#UPDATE COMPANY SECTION

#UPDATE COMPANY FORM1
@app.route("/select-update-company",methods = ['POST','GET'])
def select_update_company():
    page = " Update Company"
    msg = "Choose Company"
    status = "CURRENT"

    firstname = session.get('firstname')
    username = session.get('username')


    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM companies WHERE status=%s",[status])
    companies = cursor.fetchall()
    if companies:
        return render_template("update_company.html",page = page,companies=companies,msg=msg, firstname=firstname)
    else:
        msg = 'Empty List'
        return render_template("update_company.html",page = page, companies=companies,msg=msg, firstname=firstname)
    # Fetch one record and return result

# PROCESS UPDATE SALESPERSON
@app.route("/update-company-form",methods = ['POST','GET'])
def update_company_form():
    page = "Update Company"
    msg = "Edit Company"
    status = "CURRENT"

    firstname = session.get('firstname')
    username = session.get('username')
    #company_id=request.form.get('id')
    selected = request.form['company_id']

    status = "CURRENT"
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM companies WHERE id=%s",[selected])
    companies = cursor.fetchall()
    if companies:
        for company in companies:
            selected_id = company['id']
            session["selected_id"] = selected_id

        return render_template("update_company_form.html",
        selected=selected,selected_id=selected_id,page=page,msg = msg,
        firstname = firstname, companies=companies)
    else:
        return "Can not fetch company"


# PROCESS UPDATE EMPLOYEE
@app.route("/update-company",methods = ['POST','GET'])
def update_company():
    page = "Remove Company"
    msg = "Choose Company"
    status = "CURRENT"

    firstname = session.get('firstname')
    username = session.get('username')


    my_primary = session.get("selected_id")
    phone = request.form.get('phone')
    company_name = request.form.get('company')
    producttype = request.form.get('bizt')
    contactp = request.form.get('contactperson')
    email = request.form.get('email')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    my_update = cursor.execute("""UPDATE companies SET phone=%s,companyname=%s,
    businesstype=%s, contact_person=%s,email=%s WHERE id=%s """,
    (phone,company_name,producttype,contactp,email,my_primary))
    if my_update:
        mysql.connection.commit()

        return company_list()
    else:
        msg = "Update Failed"
        return render_template("error_monitor.html",msg)
    # Fetch one record and return result

#---------------------------------------------------------------------------------------------------------------------------




#ADD PRODUCT SECTION ---------------------------------------------------------------------------------------------------------

# ADD PRODUCT TO DATABASE
@app.route("/add-product", methods = ['POST','GET'])
def add_product():
    page = "Add Product"
    firstname = session.get('firstname')
    username = session.get('username')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) # connection variable
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    if companies:
        msg = "Enter product details"
        return render_template("register_product_form.html",page = page, msg = msg,companies = companies,firstname=firstname)
    else:
        msg = "Empty company list! Please add companies first"
        return render_template("register_product_form.html",page = page, msg = msg,companies = companies,firstname=firstname)
        cursor.close() #close connection


@app.route("/add-product-process", methods = ['POST','GET'])
def add_product_pro():
    page = "Add Product"
    firstname = session.get('firstname')
    username = session.get('username')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) # connection variable
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()

    if request.method == 'POST':
        product = request.form.get("product-name")
        company_id = request.form.get("company")
        unit_price = request.form.get("price")
        #-------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------

        #------------------------------------------------------------------------------
        # Inserts data in Customers table
        cursor.execute("INSERT INTO products(product_name,company_id,price)VALUES(%s,%s,%s)",
        (product,company_id,unit_price))
        mysql.connection.commit()
        msg = "Product Added!"
        return render_template("register_product_form.html",page = page, msg = msg,companies = companies,firstname=firstname)
        cursor.close() #close connection
        #-------------------------------------------------------------------------------
    else:
        msg = "Please fill the form"
        return render_template("register_product_form.html",page = page, msg = msg,companies = companies,firstname=firstname)
    return render_template("register_product_form.html",page = page, msg = msg,companies = companies,firstname=firstname)

# END ADD PRODUCTS SECTION ----------------------------------------------------------------------------------------------------

#VIEW PRODUCTS IN DATABASE
@app.route("/product-list",methods = ['POST','GET'])
def list_product():
    page = "Products"
    status = "CURRENT"
    firstname = session.get('firstname')
    username = session.get('username')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SET @n = 0")
    cursor.execute("""SELECT @n := @n+1 AS number,products.product_name AS name,
    products.status AS status,companies.companyname AS company,products.price AS price FROM products,
    companies WHERE products.company_id = companies.id AND products.status=%s """,[status])
    products = cursor.fetchall()
    if products:
        return render_template("list_products.html",page = page,products=products,firstname=firstname)
    else:
        msg ='Empty List'
        return render_template("list_products.html",page = page,products=products,firstname=firstname)
    # Fetch one record and return result



# REMOVE PRODUCTS Section

#REMOVE PRODUCTS FORM
@app.route("/select-rem-product",methods = ['POST','GET'])
def select_rem_main_prod():
    page = "Remove Product"
    msg = "Choose Product"
    status = "CURRENT"
    firstname = session.get('firstname')
    username = session.get('username')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM products WHERE status =%s",[status])
    products = cursor.fetchall()
    if products:
        return render_template("remove_product.html",page = page, products=products,msg=msg, firstname=firstname)
    else:
        msg = 'Empty List'
        return render_template("remove_product.html",page = page, products=products,msg=msg, firstname=firstname)
    # Fetch one record and return result

# PROCESS REMOVE PRODUCTS
@app.route("/del-product",methods = ['POST','GET'])
def remove_product():
    page = "Remove Product"
    msg = "Choose Product"
    status = "NON-CURRENT"

    firstname = session.get('firstname')
    username = session.get('username')

    selected = request.form['selAnswer']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("UPDATE products SET status =%s WHERE id=%s",(status,selected))
    mysql.connection.commit()

    msg = "Deleted Successfully!"
    status = "CURRENT"

    cursor.execute("SELECT * FROM products WHERE status=%s",[status])
    products = cursor.fetchall()
    return render_template("remove_product.html",page=page,msg = msg,firstname = firstname, products=products)

    # Fetch one record and return result

#END REMOVE PRODUCT SECTION

#UPDATE PRODUCT SECTION

#UPDATE PRODUCT FORM1
@app.route("/select-update-product",methods = ['POST','GET'])
def select_update_product():
    page = " Update Products"
    msg = "Choose Products"
    status = "CURRENT"

    firstname = session.get('firstname')
    username = session.get('username')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM products WHERE status=%s",[status])
    products = cursor.fetchall()
    if products:
        return render_template("update_product.html",page = page, products=products,msg=msg, firstname=firstname)
    else:
        msg = 'Empty List'
        return render_template("update_product.html",page = page, products=products,msg=msg, firstname=firstname)
    # Fetch one record and return result

# PROCESS UPDATE SALESPERSON
@app.route("/update-product-form",methods = ['POST','GET'])
def update_product_form():
    page = "Update Product"
    msg = "Edit Product"
    status = "CURRENT"

    firstname = session.get('firstname')
    username = session.get('username')
    #company_id=request.form.get('id')
    selected = request.form['product_id']

    status = "CURRENT"
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM products WHERE id=%s",[selected])
    products = cursor.fetchall()

    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    if products:
        for product in products:
            product_id = product['id']
            session["product_id"] = product_id
        return render_template("update_product_form.html",
        page=page,msg = msg,firstname = firstname, products=products,
        product_id=product_id,companies=companies)
    else:
        return "Can not fetch products"


# PROCESS UPDATE PRODUCT
@app.route("/update-product",methods = ['POST','GET'])
def update_product():
    page = "Update Product"
    msg = "Choose Product"
    status = "CURRENT"

    firstname = session.get('firstname')
    username = session.get('username')

    my_primary = session.get("product_id")
    product_name = request.form.get('product')
    unit_price = request.form.get('price')

    company_id = request.form.get('company')


    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    my_update = cursor.execute("""UPDATE products SET product_name=%s,
    price=%s,company_id=%s,status=%s WHERE id=%s """,(product_name,unit_price,
    company_id,status,my_primary))
    if my_update:
        mysql.connection.commit()

        return list_product()

    else:
        msg = "Update Failed"
        return render_template("error_monitor.html",msg=msg)
    # Fetch one record and return result

#---------------------------------------------------------------------------------------------------------------------------



# ADD SALES TO DATABASE
@app.route("/addsales",methods = ['POST','GET'])
def add_sales():
    page = "Add Sales"
    firstname = session.get('firstname')
    username = session.get('username')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) # connection variable
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    firstname = session.get('firstname')
    employee_id = session.get('id')
    cursor.execute("SELECT * FROM products ORDER BY product_name ASC")
    products = cursor.fetchall()

    cursor.execute("SELECT * FROM customers ORDER BY firstname ASC")
    customers = cursor.fetchall()

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    if products:


        if request.method == 'POST':
            product_s = request.form.get("product")
            my_customer = request.form.get("customer")
            sales_p = request.form.get("salesperson")
            sales_date = request.form.get("sales-date")
            unit_price = request.form.get("unit-price")
            sales_quant = request.form.get("quantity")
            remark_s = request.form.get("remark")

        #-------------------------------------------------------------------------------



        #-------------------------------------------------------------------------------
            # This section checks if email already exits
        #------------------------------------------------------------------------------
            msg = "Successful"
        # Inserts data in Customers table
            cursor.execute("INSERT INTO sales(product_id,customer_id,salesPerson_id,sales_Date,unit_price,quantity,remark)VALUES(%s,%s,%s,%s,%s,%s,%s)",
            (product_s,my_customer,employee_id,date,unit_price,sales_quant,remark_s))
            mysql.connection.commit()
        #-------------------------------------------------------------------------------
        else:
            msg = "Please fill the form"
            return render_template("register_sales_form.html",page = page, msg = msg,date = date, firstname = firstname,products = products, customers = customers)
        return render_template("register_sales_form.html",page = page, msg = msg,date = date, firstname = firstname,products = products, customers = customers)
    else:
        msg = 'Empty company list! Please add products first'
        return render_template("register_sales_form.html",page = page, msg = msg,date = date, firstname = firstname,products = products, customers = customers)

    return render_template("register_sales_form.html",page = page, msg = msg,date = date, firstname = firstname,products = products, customers = customers)
    cursor.close() #close connection

# ADMIN ADD SALES HERE
@app.route("/admaddsales",methods = ['POST','GET'])
def admin_add_sales():
    page = "Admin Add Sales"
    sales = "YES"
    firstname = session.get('firstname')
    username = session.get('username')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) # connection variable
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    firstname = session.get('firstname')
    employee_id = session.get('id')
    cursor.execute("SELECT * FROM products ORDER BY product_name ASC")
    products = cursor.fetchall()

    cursor.execute("SELECT * FROM customers ORDER BY firstname ASC")
    customers = cursor.fetchall()

    cursor.execute("SELECT * FROM employees WHERE sales_permit=%s",[sales])
    salespersons = cursor.fetchall()

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    if products:


        if request.method == 'POST':
            product_s = request.form.get("product")
            my_customer = request.form.get("customer")
            sales_p = request.form.get("salesperson")
            sales_date = request.form.get("sales-date")
            unit_price = request.form.get("unit-price")
            sales_quant = request.form.get("quantity")
            remark_s = request.form.get("remark")

        #-------------------------------------------------------------------------------



        #-------------------------------------------------------------------------------
            # This section checks if email already exits
        #------------------------------------------------------------------------------
            msg = "Successful"
        # Inserts data in Customers table
            cursor.execute("INSERT INTO sales(product_id,customer_id,salesPerson_id,sales_Date,unit_price,quantity,remark)VALUES(%s,%s,%s,%s,%s,%s,%s)",
            (product_s,my_customer,sales_p,date,unit_price,sales_quant,remark_s))
            mysql.connection.commit()
        #-------------------------------------------------------------------------------
        else:
            msg = "Please fill the form"
            return render_template("admin_register_sales_form.html",page = page, msg = msg,
            date = date, firstname = firstname,products = products,
            salespersons=salespersons, customers = customers)
        return render_template("admin_register_sales_form.html",page = page,
         msg = msg,date = date, firstname = firstname,salespersons=salespersons,
         products = products, customers = customers)
    else:
        msg = 'Empty company list! Please add products first'
        return render_template("admin_register_sales_form.html",page = page,
        msg = msg,date = date, firstname = firstname,
        products = products, customers = customers,salespersons=salespersons)

    return render_template("admin_register_sales_form.html",page = page,
     msg = msg,date = date, firstname = firstname,products = products,
     customers = customers,salespersons=salespersons)
    cursor.close() #close connection


#VIEW SALESPERSON IN DATABASE
@app.route("/mysales",methods = ['POST','GET'])
def mysales_List():
    page = "My Sales"
    firstname = session.get('firstname')
    employee_id = session.get('id')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SET @n = 0")
    cursor.execute("""SELECT @n := @n+1 AS number, sales.id AS id, sales.sales_Date, sales.quantity,
    sales.remark, products.product_name, sales.unit_price AS Unit_Price, sales.unit_price*sales.quantity AS Amount,
     CONCAT(customers.firstname," ",customers.lastname) AS Customer FROM sales,products,customers
     WHERE sales.product_id = products.id AND sales.customer_id = customers.id
     AND salesPerson_id=%s AND sales_Date=%s""",(employee_id,date))
    mysales = cursor.fetchall()
    if mysales:
        msg = firstname +"'s Sales "
        return render_template("list_mysales.html",page = page, msg = msg, mysales = mysales, date = date, firstname = firstname)
    else:
        msg ="You have not recorded any sales for today"
        return render_template("list_mysales.html",page = page, date = date, msg = msg, firstname = firstname)
    # Fetch one record and return result


@app.route("/mysales-today",methods = ['POST','GET'])
def mysales_bydate_List():

    page = "My Sales"
    firstname = session.get('firstname')
    employee_id = session.get('id')
    this_day = request.form.get('this_day')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    if request.method == 'POST':

        cursor.execute("SET @n = 0")
        cursor.execute("""SELECT @n := @n+1 AS number, sales.id AS id, sales.sales_Date, sales.quantity,
        sales.remark, products.product_name, sales.unit_price AS Unit_Price, sales.unit_price*sales.quantity AS Amount,
         CONCAT(customers.firstname," ",customers.lastname) AS Customer FROM sales,products,customers
         WHERE sales.product_id = products.id AND sales.customer_id = customers.id
         AND salesPerson_id=%s AND sales_Date=%s""",(employee_id,this_day))
        mysales = cursor.fetchall()
        if mysales:
            msg = firstname +"'s Sales "
            return render_template("list_mysales_bydate.html",page = page,date = date, msg = msg, mysales = mysales,this_day = this_day, firstname = firstname)
        else:
            this_day = str(this_day)
            msg ="You have not recorded any sales for " + this_day
            return render_template("list_mysales_bydate.html",page = page,date = date, this_day=this_day, msg = msg, firstname = firstname)
    else:
        msg = 'Please fill this form'
        return render_template("list_mysales_bydate.html",page = page, date = date,this_day=this_day, msg = msg, firstname = firstname)
    # Fetch one record and return result

#VIEWING SALES BY SALESPERSON BY DATE
@app.route("/sales-today",methods = ['POST','GET'])
def admin_sales_bydate_List():

    page = "Sales"
    firstname = session.get('firstname')

    this_day = request.form.get('this_day')
    sales = "YES"
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM employees WHERE sales_permit=%s",[sales])
    salespersons = cursor.fetchall()
    salesperson_id = request.form.get('salesperson')


    if request.method == 'POST':
        cursor.execute("SELECT firstname FROM employees WHERE id=%s",[salesperson_id])
        firstname = cursor.fetchall()
        cursor.execute("SET @n = 0")
        cursor.execute("""SELECT @n := @n+1 AS number,sales.sales_Date,sales.quantity,sales.remark,products.product_name,
        sales.unit_price AS Unit_Price, sales.unit_price*sales.quantity AS Amount,
        CONCAT(customers.firstname," ",customers.lastname) AS Customer FROM sales,products,customers
        WHERE sales.product_id = products.id AND sales.customer_id = customers.id
        AND salesPerson_id=%s AND sales_Date=%s""",(salesperson_id,this_day))
        mysales = cursor.fetchall()

        if mysales:
            cursor.execute("""SELECT  SUM(sales.unit_price*sales.quantity) AS total
            FROM sales,products WHERE sales.product_id = products.id
            AND salesPerson_id=%s AND sales_Date=%s""",(salesperson_id,this_day))
            mysum = cursor.fetchall()
            msg =  "'s sales for "+ this_day
            return render_template("list_admin_sales_bydate.html",mysum=mysum,firstname=firstname,salesperson_id=salesperson_id,salespersons= salespersons, page = page,date = date, msg = msg, mysales = mysales,this_day = this_day)
        else:
            this_day = str(this_day)
            msg =" has not recorded any sales for " + this_day
            return render_template("list_admin_sales_bydate.html",firstname=firstname,salesperson_id=salesperson_id,salespersons= salespersons,page = page,date = date, this_day=this_day, msg = msg)
    else:
        msg = 'Please fill this form'
        return render_template("list_admin_sales_bydate.html",salesperson_id=salesperson_id,salespersons= salespersons,page = page, date = date,this_day=this_day, msg = msg,firstname=firstname)
    # Fetch one record and return result


#VIEWING ALL SALES BY DATES
@app.route("/all-sales",methods = ['POST','GET'])
def admin_allsales_List():

    page = "Sales"
    firstname = session.get('firstname')
    this_day = request.form.get('this_day')
    sales = "YES"
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)


    if request.method == 'POST':
        cursor.execute("SET @n = 0")
        cursor.execute("""SELECT @n := @n+1 AS number,sales.sales_Date,sales.quantity,sales.remark,products.product_name,
        sales.unit_price AS Unit_Price, sales.unit_price*sales.quantity AS Amount,
        CONCAT(employees.firstname," ",employees.lastname)
        AS Salesperson,CONCAT(customers.firstname," ",customers.lastname)
        AS Customer FROM sales,products,customers,employees WHERE sales.salesPerson_id = employees.id AND
        sales.product_id = products.id AND sales.customer_id = customers.id
        AND employees.sales_permit=%s AND sales_Date=%s""",(sales,this_day))
        mysales = cursor.fetchall()
        if mysales:
            cursor.execute("""SELECT  SUM(sales.unit_price*sales.quantity) AS total FROM sales,products WHERE sales.product_id = products.id
            AND sales_Date=%s""",[this_day])
            mysum = cursor.fetchall()
            msg =  "Showing All Sales for "+ this_day
            return render_template("list_admin_all_sales_bydate.html", page = page,date = date, msg = msg,firstname=firstname, mysales = mysales,this_day = this_day, mysum=mysum)
        else:
            this_day = str(this_day)
            msg =" There are no records of sales for " + this_day
            return render_template("list_admin_all_sales_bydate.html",page = page,date = date, this_day=this_day, msg = msg,firstname=firstname)
    else:
        msg = 'Please fill this form'
        return render_template("list_admin_all_sales_bydate.html",page = page, date = date,this_day=this_day, msg = msg,firstname=firstname)
    # Fetch one record and return result

# VIEWING ALL SALES FOR ALL DATES

@app.route("/all-sales2",methods = ['POST','GET'])
def admin_allsales_List2():

    page = "Sales"
    firstname = session.get('firstname')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SET @n = 0")
    cursor.execute("""SELECT @n := @n+1 AS number,sales.sales_Date,sales.quantity,sales.remark,products.product_name,
    sales.unit_price AS Unit_Price, sales.unit_price*sales.quantity AS Amount, CONCAT(employees.firstname," ",employees.lastname)
    AS Salesperson, CONCAT(customers.firstname," ",customers.lastname) AS Customer
    FROM sales,products,customers,employees WHERE sales.salesPerson_id = employees.id
    AND sales.product_id = products.id AND sales.customer_id = customers.id""")
    mysales = cursor.fetchall()
    if mysales:
        msg =  "Showing All Sales"
        this_day = "ALL"
        cursor.execute("SELECT  SUM(sales.unit_price*sales.quantity) AS total FROM sales,products WHERE sales.product_id = products.id")
        mysum = cursor.fetchall()
        if mysum:
            return render_template("list_admin_all_sales_bydate.html", firstname=firstname,page = page, msg = msg, mysales = mysales, this_day = this_day,mysum = mysum)
        else:
            return render_template("list_admin_all_sales_bydate.html", firstname=firstname,page = page, msg = msg, mysales = mysales, this_day = this_day)
    else:
        msg =" There are no records of sales"
        return render_template("list_admin_all_sales_bydate.html",page = page,firstname=firstname, msg = msg,mysales=mysales)


def row_counter(table):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if table == "sales":
        cursor.execute("SELECT COUNT(*) AS mycount FROM sales")
        counter = cursor.fetchall()
        return counter
    elif table == "products":
        cursor.execute("SELECT COUNT(*) AS mycount FROM products")
        counter = cursor.fetchall()
        return counter
    elif table == "customers":
        cursor.execute("SELECT COUNT(*) AS mycount FROM customers")
        counter = cursor.fetchall()
        return counter
    elif table == "locations":
        cursor.execute("SELECT COUNT(*) AS mycount FROM locations")
        counter = cursor.fetchall()
        return counter
    else:
        pass
    #,customers_count,locations_count

def performance(): # show weekly sales performance
    sales = "YES"
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""select count(*) as count, (100 - count(*)) AS bal,
    SUM(sales.quantity) AS netsales,CONCAT(employees.firstname," ",
    employees.lastname) AS fullname FROM sales,employees
    WHERE YEARWEEK(sales.sales_Date) = YEARWEEK(NOW()) AND
    sales.salesPerson_id = employees.id GROUP BY fullname""")
    salespersons = cursor.fetchall()

    return (salespersons)

def delete(myclass,entity):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""DELETE FROM %s WHERE id =%s""",(myclass,entity))
    mysql.connection.commit()




@app.route("/", methods = ['POST','GET'])
def index():
    page = "Home Page"

    return render_template("main_index.html", page = page)

def main():
    global user_id
    if __name__ == "__main__":
        with app.app_context():
            main()
