from flask import Flask, render_template, flash, redirect, url_for, session, request  # , logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, DateField, PasswordField, validators, IntegerField, FloatField  # FORM VALIDATION
from passlib.hash import sha256_crypt  # Encrypting PASSWORD
from functools import wraps

app = Flask(__name__)

# CONFIG MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # NO PASSWORD FOR NOW
app.config['MYSQL_DB'] = 'crystaldb2'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # OTHER WISE IT WILL BE A TUPLE

# INITIALIZE MySQL
mysql = MySQL(app)


# CHECK IF USER IS LOGGED
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))  # RETURN THEM TO LOGIN PAGE
    return wrap


# INDEX
@app.route('/')
def index():
    return render_template('home.html')


# ABOUT
@app.route('/about')
def about():
    return render_template('about.html')


# REGISTER FORM CLASS
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    surname = StringField('Surname', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# USER REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))  # Encrypting

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, surname, email, username, password) VALUES(%s, %s, %s, %s, %s)", (name, surname, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))  # WHERE WE WANT TO GO
    return render_template('register.html', form=form)


# USER LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()  # GET FIRST user ROW FETCHED
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['userid'] = cur.execute("SELECT userID FROM users WHERE name = %s", [username])

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


# LOGOUT
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


# NEW EXPERIMENT Class
class ExperimentForm(Form):
    # personName = StringField('Current User', [validators.Length(min=1, max=50)])
    experimentID = StringField('Experiment ID', [validators.Length(min=1, max=50)])
    expDate = DateField('Experiment Date')

    material1 = StringField('Material 1 Name', [validators.Length(min=1, max=50)])
    material1Quantity = StringField('Material 1 Quantity', [validators.Length(min=1, max=50)])
    material1Unit = StringField('Material 1 Unit', [validators.Length(min=1, max=50)])

    solvent1 = StringField('Solvent 1 Name', [validators.Length(min=1, max=50)])
    solvent1Quantity = StringField('Solvent 1 Quantity', [validators.Length(min=1, max=50)])
    solvent1QuantityUnit = StringField('Solvent 1 Unit', [validators.Length(min=1, max=50)])


# ADD EXPERIMENT
@app.route('/add_experiment', methods=['GET', 'POST'])
@is_logged_in
def add_experiment():
    form = ExperimentForm(request.form)
    if request.method == 'POST':
        # userID = 1  # session.username
        experimentID = form.experimentID.data
        expDate = form.expDate.data

        material1 = form.material1.data
        material1Quantity = form.material1Quantity.data
        material1Unit = form.material1Unit.data

        solvent1 = form.solvent1.data
        solvent1Quantity = form.solvent1Quantity.data
        solvent1QuantityUnit = form.solvent1QuantityUnit.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO experiment(experimentID, expDate, material1, material1Quantity, material1QuantityUnit, solvent1, solvent1Quantity, solvent1QuantityUnit) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (experimentID, expDate, material1, material1Quantity, material1Unit, solvent1, solvent1Quantity, solvent1QuantityUnit))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You succesfully added an experiment', 'success')

        return redirect(url_for('add_experiment'))

    return render_template('add_experiment.html', form=form)


# NEW EXPERIMENT Class
class MeasurementForm(Form):
    # personName = StringField('Current User', [validators.Length(min=1, max=50)])
    measurementID = StringField('Measurement ID', [validators.Length(min=1, max=50)])
    crstID = IntegerField('Crystal database ID')
    measrDate = DateField('Measurement Date')

    spaceGroup = StringField('Space group', [validators.Length(min=1, max=50)])
    assymUnitComposition = StringField('Unit composition', [validators.Length(min=1, max=50)])
    canonicalSmileCrystalComp = StringField('Canonical Smile Composition', [validators.Length(min=1, max=50)])
    measurementTemp = FloatField('Temperature')

    cellLengthA = FloatField('Length A')
    cellLengthB = FloatField('Length B')
    cellLengthC = FloatField('Length C')
    cellAngleAlpha = FloatField('Angle Alpha')
    cellAngleBeta = FloatField('Angle Beta')
    cellAngleGamma = FloatField('Angle Gamma')
    cellVolume = FloatField('Volume')
    diffMeasurementDevice = StringField('Device diff', [validators.Length(min=1, max=50)])


# ADD EXPERIMENT
@app.route('/add_measurement', methods=['GET', 'POST'])
@is_logged_in
def add_measurement():
    form = MeasurementForm(request.form)
    if request.method == 'POST':
        measurementID = form.measurementID.data
        crstID = form.crstID.data
        measrDate = form.measrDate.data
        spaceGroup = form.spaceGroup.data
        assymUnitComposition = form.assymUnitComposition.data
        canonicalSmileCrystalComp = form.canonicalSmileCrystalComp.data
        measurementTemp = form.measurementTemp.data
        cellLengthA = form.cellLengthA.data
        cellLengthB = form.cellLengthB.data
        cellLengthC = form.cellLengthC.data
        cellAngleAlpha = form.cellAngleAlpha.data
        cellAngleBeta = form.cellAngleBeta.data
        cellAngleGamma = form.cellAngleGamma.data
        cellVolume = form.cellVolume.data
        diffMeasurementDevice = form.diffMeasurementDevice.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO measurement(measurementID, crstID, measrDate, spaceGroup, assymUnitComposition, canonicalSmileCrystalComp, measurementTemp, cellLengthA, cellLengthB, cellLengthC, cellAngleAlpha, cellAngleBeta, cellAngleGamma, cellVolume, diffMeasurementDevice) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (measurementID, crstID, measrDate, spaceGroup, assymUnitComposition, canonicalSmileCrystalComp, measurementTemp, cellLengthA, cellLengthB, cellLengthC, cellAngleAlpha, cellAngleBeta, cellAngleGamma, cellVolume, diffMeasurementDevice))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You succesfully added measurement', 'success')

        return redirect(url_for('add_measurement'))
    return render_template('add_measurement.html', form=form)


class MorphologyForm(Form):
    expID = IntegerField('Experiment ID')
    crystalDate = DateField('Adding Date')
    crystalType = StringField('Type', [validators.Length(min=1, max=50)])
    crystalShape = StringField('Shape', [validators.Length(min=1, max=50)])
    crystalColor = StringField('Color', [validators.Length(min=1, max=50)])
    crystalSizeA = StringField('Size A', [validators.Length(min=1, max=50)])
    crystalSizeB = StringField('Size B', [validators.Length(min=1, max=50)])
    crystalSizeC = StringField('Size C', [validators.Length(min=1, max=50)])
    crystalMeltingTemp = FloatField('Melting Temperature')


@app.route('/add_morphology', methods=['GET', 'POST'])
@is_logged_in
def add_morphology():
    form = MorphologyForm(request.form)
    if request.method == 'POST':
        expID = form.expID.data
        crystalDate = form.crystalDate.data
        crystalType = form.crystalType.data
        crystalShape = form.crystalShape.data
        crystalColor = form.crystalColor.data
        crystalSizeA = form.crystalSizeA.data
        crystalSizeB = form.crystalSizeB.data
        crystalSizeC = form.crystalSizeC.data
        crystalMeltingTemp = form.crystalMeltingTemp.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO morphology(expID, crystalDate, crystalType, crystalShape, crystalColor, crystalSizeA, crystalSizeB, crystalSizeC, crystalMeltingTemp) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (expID, crystalDate, crystalType, crystalShape, crystalColor, crystalSizeA, crystalSizeB, crystalSizeC, crystalMeltingTemp))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You succesfully added morphology', 'success')

        return redirect(url_for('add_morphology'))
    return render_template('add_morphology.html', form=form)


class MaterialForm(Form):
        compoundName = StringField('Compound Name', [validators.Length(min=1, max=50)])
        chemicalFormula = StringField('Chemical Fomula', [validators.Length(min=1, max=50)])
        canonicalSmile = StringField('Canonical Smile', [validators.Length(min=1, max=50)])
        type = StringField('Type', [validators.Length(min=1, max=50)])
        casNumber = StringField('CAS Number', [validators.Length(min=1, max=50)])
        productNumber = StringField('Product Number', [validators.Length(min=1, max=50)])
        supplier = StringField('Supplier', [validators.Length(min=1, max=50)])


@app.route('/add_material', methods=['GET', 'POST'])
@is_logged_in
def add_material():
    form = MaterialForm(request.form)
    if request.method == 'POST':
        compoundName = form.compoundName.data
        chemicalFormula = form.chemicalFormula.data
        canonicalSmile = form.canonicalSmile.data
        type = form.type.data
        casNumber = form.casNumber.data
        productNumber = form.productNumber.data
        supplier = form.supplier.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO material(compoundName, chemicalFormula, canonicalSmile, type, casNumber, productNumber, supplier) VALUES(%s, %s, %s, %s, %s, %s, %s)", (compoundName, chemicalFormula, canonicalSmile, type, casNumber, productNumber, supplier))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You succesfully added new material', 'success')

        return redirect(url_for('add_material'))
    return render_template('add_material.html', form=form)


class SolventForm(Form):
    solventName = StringField('Solvent Name', [validators.Length(min=1, max=50)])
    chemicalFormula = StringField('Chemical Fomula', [validators.Length(min=1, max=50)])
    canonicalSmile = StringField('Canonical Smile', [validators.Length(min=1, max=50)])
    casNumber = StringField('CAS Number', [validators.Length(min=1, max=50)])
    productNumber = StringField('Product Number', [validators.Length(min=1, max=50)])
    supplier = StringField('Supplier', [validators.Length(min=1, max=50)])


@app.route('/add_solvent', methods=['GET', 'POST'])
@is_logged_in
def add_solvent():
    form = SolventForm(request.form)
    if request.method == 'POST':
        solventName = form.solventName.data
        chemicalFormula = form.chemicalFormula.data
        canonicalSmile = form.canonicalSmile.data
        casNumber = form.casNumber.data
        productNumber = form.productNumber.data
        supplier = form.supplier.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO solvent(solventName, chemicalFormula, canonicalSmile, casNumber, productNumber, supplier) VALUES(%s, %s, %s, %s, %s, %s)", (solventName, chemicalFormula, canonicalSmile, casNumber, productNumber, supplier))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You succesfully added new solvent', 'success')

        return redirect(url_for('add_solvent'))
    return render_template('add_solvent.html', form=form)


# DASHBOARD
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')


# LAUNCH APP
if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
