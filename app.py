from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_mysqldb import MySQL
import MySQLdb


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure MySQL database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ritesh123'
app.config['MYSQL_DB'] = 'agro'

mysql = MySQL(app)

# Create necessary database tables
def create_tables():
    cursor = mysql.connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_prices (
        id INT AUTO_INCREMENT PRIMARY KEY,
        crop_name VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2) NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS smart_farming (
        id INT AUTO_INCREMENT PRIMARY KEY,
        technique TEXT NOT NULL
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customerLogin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL ,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
 """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS farmerLogin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL ,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
 """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipment_rental (
        id INT AUTO_INCREMENT PRIMARY KEY,
        equipment_name VARCHAR(255) NOT NULL,
        rental_cost DECIMAL(10, 2) NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customerRegistration (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(100) NOT NULL ,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS farmersRegistration (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        farm_name VARCHAR(255) NOT NULL,
        farm_location VARCHAR(255) NOT NULL,
        crop_type VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

    mysql.connection.commit()
    cursor.close()

class Customer:
    @staticmethod
    def get_by_email(email):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM customerRegistration WHERE email = %s"
        cursor.execute(query, (email,))
        customer = cursor.fetchone()
        cursor.close()
        return customer

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/index.html')
def index1():
    return render_template('index.html')
@app.route('/register.html')
def register():
    return render_template('register.html')


# Route to handle farmer registration form submission
@app.route('/farmerRegistration.html', methods=['GET', 'POST'])
def farmer_register():
    if request.method == 'POST':
        # Get the data from the form
        name = request.form['name']
        email = request.form['email']
        farm_name = request.form['farm_name']
        farm_location = request.form['farm_location']
        crop_type = request.form['crop_type']

        # Insert the data into the farmersRegistration table
        cursor = mysql.connection.cursor()
        query = """INSERT INTO farmersRegistration (name, email, farm_name, farm_location, crop_type) 
                   VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(query, (name, email, farm_name, farm_location, crop_type))
        mysql.connection.commit()  # Commit the transaction to save the data
        cursor.close()

        # Flash message to indicate successful registration
        flash('Farmer account registered successfully!', 'success')

        # Render the farmer registration page with the flash message
        return render_template('farmerRegistration.html')

    # If the method is GET, simply render the form
    return render_template('farmerRegistration.html')


# Route to handle farmer registration form submission
@app.route('/farmerRegistration', methods=['GET', 'POST'])
def farmer_register1():
    if request.method == 'POST':
        # Get the data from the form
        name = request.form['name']
        email = request.form['email']
        farm_name = request.form['farm_name']
        farm_location = request.form['farm_location']
        crop_type = request.form['crop_type']

        # Insert the data into the farmersRegistration table
        cursor = mysql.connection.cursor()
        query = """INSERT INTO farmersRegistration (name, email, farm_name, farm_location, crop_type) 
                   VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(query, (name, email, farm_name, farm_location, crop_type))
        mysql.connection.commit()  # Commit the transaction to save the data
        cursor.close()

        # Flash message to indicate successful registration
        flash('Farmer account registered successfully!', 'success')

        # Render the farmer registration page with the flash message
        return render_template('farmerRegistration.html')

    # If the method is GET, simply render the form
    return render_template('farmerRegistration.html')

@app.route('/customerRegistration.html', methods=['GET', 'POST'])
def customer_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # Insert the customer data into the database
        cursor = mysql.connection.cursor()
        query = """INSERT INTO customerregistration (name, email) VALUES (%s, %s)"""
        cursor.execute(query, (name, email))
        mysql.connection.commit()
        cursor.close()

        # Flash message indicating successful registration
        flash('Customer account registered successfully!', 'success')

        # Redirect to the registration page or a new page after successful registration
        return render_template('customerRegistration.html')

    # If the method is GET, simply render the registration form
    return render_template('customerRegistration.html')

@app.route('/customerRegistration', methods=['GET', 'POST'])
def customer_registerflash():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # Insert the customer data into the database
        cursor = mysql.connection.cursor()
        query = """INSERT INTO customerregistration (name, email) VALUES (%s, %s)"""
        cursor.execute(query, (name, email))
        mysql.connection.commit()
        cursor.close()

        # Flash message indicating successful registration
        flash('Customer account registered successfully!', 'success')

        # Redirect to the registration page or a new page after successful registration
        return render_template('customerRegistration.html')

    # If the method is GET, simply render the registration form
    return render_template('customerRegistration.html')




'''  not use 
# Route to handle customer registration form submission
@app.route('/customerRegistration.html', methods=['POST'])
def customer_register():
    return render_template('customerRegister.html')
   '''
@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/customerLogin.html', methods=['GET', 'POST'])
def customerLogin():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        # Simulate checking the database (this is just an example)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM customerRegistration WHERE email = %s AND name = %s", (email, name))
        customer = cursor.fetchone()
        cursor.close()

        if customer:
            session['user_id'] = customer[0]  # Assuming the customer table has ID as the first column
            session['user_name'] = customer[1]  # Assuming the customer table has Name as the second column
            flash('Login successful!', 'success')
            return redirect(url_for('customerDashboard'))
        else:
            flash('Customer not found with this email and name.', 'danger')

    return render_template('customerLogin.html')
@app.route('/customerLogin', methods=['GET', 'POST'])
def customerLogin1():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        # Simulate checking the database (this is just an example)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM customerRegistration WHERE email = %s AND name = %s", (email, name))
        customer = cursor.fetchone()
        cursor.close()

        if customer:
            session['user_id'] = customer[0]  # Assuming the customer table has ID as the first column
            session['user_name'] = customer[1]  # Assuming the customer table has Name as the second column
            flash('Login successful!', 'success')
            return redirect(url_for('customerDashboard'))
        else:
            flash('Customer not found with this email and name.', 'danger')

    return render_template('customerLogin.html')


# Customer Dashboard route
@app.route('/customerDashboard.html')
def customer_dashboard():

    return render_template('customerDashboard.html')

@app.route('/customerDashboard')
def customer_dashboard1():
    return render_template('customerDashboard.html')

# Define the farmer dashboard route
@app.route('/farmerDashboard.html')
def farmer_dashboard():
    # For now, we'll pass a dummy farmer username (replace with actual username logic)
    return render_template('farmerDashboard.html', farmer_username='Ritesh')

# Define the upload_grain route
@app.route('/upload_grain', methods=['POST'])
def upload_grain():
    if request.method == 'POST':
        crop_name = request.form['crop_name']
        price = request.form['price']
        image = request.files['image']  # Handle image file (you can save it as needed)

        # Here, you can process the uploaded grain information (save to DB, etc.)

        # After successful upload, redirect the user back to the dashboard (or another page)
        return redirect(url_for('farmer_dashboard'))


@app.route('/farmerLogin.html')
def farmerLogin():
    return render_template('farmerLogin.html')


@app.route('/market_prices', methods=['GET', 'POST'])
def market_prices():
    if request.method == 'POST':
        crop_name = request.form['crop_name']
        cursor = mysql.connection.cursor()
        query = "SELECT price FROM market_prices WHERE crop_name = %s"
        cursor.execute(query, (crop_name,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            flash(f'The market price for {crop_name} is {result[0]} per unit.')
        else:
            flash(f'Market price for {crop_name} not found.')

    return render_template('market_prices.html')

@app.route('/smart_farming', methods=['GET', 'POST'])
def smart_farming():
    if request.method == 'POST':
        farming_technique = request.form['technique']
        cursor = mysql.connection.cursor()
        query = "INSERT INTO smart_farming (technique) VALUES (%s)"
        cursor.execute(query, (farming_technique,))
        mysql.connection.commit()
        cursor.close()
        flash('Farming technique submitted successfully!')

    return render_template('smart_farming.html')

@app.route('/equipment_rental', methods=['GET', 'POST'])
def equipment_rental():
    if request.method == 'POST':
        equipment_name = request.form['equipment_name']
        rental_cost = request.form['rental_cost']
        cursor = mysql.connection.cursor()
        query = "INSERT INTO equipment_rental (equipment_name, rental_cost) VALUES (%s, %s)"
        cursor.execute(query, (equipment_name, rental_cost))
        mysql.connection.commit()
        cursor.close()
        flash('Equipment rental information added successfully!')

    return render_template('equipment_rental.html')
@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    flash('You have logged out.', 'info')
    return redirect(url_for('index'))  # Redirect to the home page or login page


@app.route('/about.html')
def about():
    return render_template('about.html')
@app.route('/contact.html')
def contact():
    return render_template('contact.html')
@app.route('/faq.html')
def faq():
    return render_template('faq.html')
@app.route('/services.html')
def services():
    return render_template('services.html')

@app.route('/privacy_policy.html')
def privacy_policy():
    return render_template('privacy_policy.html')



@app.route('/booking')
def booking():
    crop_id = request.args.get('crop_id')
    crop_name = request.args.get('crop_name')
    return render_template('booking.html', crop_id=crop_id, crop_name=crop_name)

@app.route('/submit-booking', methods=['POST'])
def submit_booking():
    customer_name = request.form['customer_name']
    address = request.form['address']
    phone = request.form['phone']
    crop_id = request.form['crop_id']
    crop_name = request.form['crop_name']
    
    # Logic for saving booking or proceeding to payment
    # For now, just print out the details (you can store it in a database)

    print(f"Booking Details: Name: {customer_name}, Address: {address}, Phone: {phone}, Crop: {crop_name} ({crop_id})")
    
    # Redirect or render a success page (or payment page)
    return render_template('booking_confirmation.html', customer_name=customer_name, crop_name=crop_name)



if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True) 