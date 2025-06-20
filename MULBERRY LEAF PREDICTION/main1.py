from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from silk_worm import pred_silkworm_diseases
from silk_leaf import pred_leaf_diseases

from price import price_app
from models import db, User
from forms import LoginForm, RegisterForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# Register the blueprint from the price.py file
app.register_blueprint(price_app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/price')
def price():
   
    pdf_files = price_app.index()   

@app.route('/')
def index():
    return render_template('main_index.html')

@app.route('/team1')
def team1():
    return render_template('index_silk.html')

@app.route('/team2')
def team2():
    return render_template('index_leaf.html')

@app.route('/fla_k')
def fla_k():
    return render_template('silkworm_Flacheria_ka.html')

@app.route('/fla_e')
def fla_e():
    return render_template('silkworm_Flacheria.html')

@app.route('/gra_k')
def gra_k():
    return render_template('silkworm_Grasseria_ka.html')

@app.route('/gra_e')
def gra_e():
    return render_template('silkworm_Grasseria.html')

@app.route('/mus_k')
def mus_k():
    return render_template('silkworm_muscardin_ka.html')

@app.route('/mus_e')
def mus_e():
    return render_template('silkworm_muscardin.html')

@app.route('/pab_k')
def pab_k():
    return render_template('silkworm_pabrin_ka.html')

@app.route('/pab_e')
def pab_e():
    return render_template('silkworm_pabrin.html')

@app.route('/home')
def home():
    return render_template('main.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/week1_k')
def week1_k():
    return render_template('week1_k.html')

@app.route('/week1')
def week1():
    return render_template('week1.html')

@app.route('/week2_k')
def week2_k():
    return render_template('week2_k.html')

@app.route('/week2')
def week2():
    return render_template('week2.html')

@app.route('/week3_k')
def week3_k():
    return render_template('week3_k.html')

@app.route('/week3')
def week3():
    return render_template('week3.html')

@app.route('/week4_k')
def week4_k():
    return render_template('week4_k.html')

@app.route('/week4')
def week4():
    return render_template('week4.html')

@app.route('/week5_k')
def week5_k():
    return render_template('week5_k.html')

@app.route('/week5')
def week5():
    return render_template('week5.html')

pages = {
    'week1': 'week1.html',
    'week2': 'week2.html',
    'week3': 'week3.html',
    'week4': 'week4.html',
    'week5': 'week5.html'
}


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, "pbkdf2:sha256", 150000)
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/stage', methods=['GET', 'POST'])
def stage():
    if request.method == 'POST':
        # Get the user input from the request form
        input = request.form['input']

        # Check if the user input matches a page in the dictionary
        if input in pages:
            # If it does, render the corresponding page
            page = pages[input]
            return render_template(page)
        else:
            # If it doesn't, return an error message
            return "Error: Page not found."
    else:
        # If the request method is GET, return the form for user input
        return render_template('index_stage.html')

@app.route('/predict1', methods=['GET', 'POST'])
def predict1():
    if request.method == 'POST':
        file = request.files['image']
        file_path = 'static/uploads/' + file.filename
        file.save(file_path)
        pred, output_page = pred_silkworm_diseases(tomato_plant=file_path)
        return render_template(output_page, pred_output=pred, user_image=file_path)
    return render_template('index_silk.html')

control = {
    'Leaf rust disease': [
        'Choose rust-resistant plant varieties.',
        'Remove and destroy infected plant debris.',
        'Practice crop rotation to disrupt the disease cycle.',
        'Monitor plants regularly for early detection of leaf rust.',
    ],
    'Leaf Spot Disease': [
        'Remove infected leaves and debris.',
        'Use appropriate chemicals.',
        'Avoid overwatering.',
        'Trim affected parts.',
        'Regular monitoring.',
        
    ],
    'Mulberry Stem Canker': [
        'Remove and destroy infected mulberry stems and leaves.',
        'Cut infected branches at least 20 cm below visible signs of infection.',
        'Maintain proper irrigation, fertilization, and spacing between trees.',
        'Avoid planting mulberry trees in previously infected areas.',
        'Consider using resistant or tolerant mulberry tree varieties.',
        
    ],
    'Powdery Mildew': [
        'Rotate crops and avoid planting the same crop in the same location consecutively.',
        'Avoid overhead irrigation and keep leaves dry.',
        'Prune and remove infected plant parts regularly.',
        'Provide adequate spacing between plants to improve air circulation.',
        
    ],
    'Root Knot Disease': [
        'Remove and destroy infected plant residues to prevent nematode buildup.',
        'Incorporate organic matter to improve soil and indirectly suppress nematode populations.',
        'Cover the soil with plastic sheets during hot months to kill nematodes.',
        'Avoid overwatering to minimize nematode activity.',
        'Regularly check for root knot disease symptoms and take action promptly.',
        
    ],
    'leaf is healthy': []
}

@app.route('/predict2', methods=['GET', 'POST'])
def predict2():
    if request.method == 'POST':
        file = request.files['image']
        file_path = 'static/uploads/' + file.filename
        file.save(file_path)
        pred, output_page = pred_leaf_diseases(tomato_plant=file_path)
        return render_template(output_page, pred_output=pred, c_m=control[pred], user_image=file_path)
    return render_template('index_leaf.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

