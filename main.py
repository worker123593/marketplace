import datetime
import os
from flask import Flask, render_template, redirect, request, abort, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from data import db_session, products_api
from data.products import Products
from data.users import User
from forms.products import ProductsForm
from forms.purchase import PurchaseForm
from forms.removal import RemovalProductForm
from forms.user import RegisterForm, LoginForm
from products_resource import ProductsListResource, ProductsResource
from users_resource import UserResource, UserListResource
from flask import make_response


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
api.add_resource(ProductsListResource, '/api/v2/products')
api.add_resource(ProductsResource, '/api/v2/products/<int:products_id>')
api.add_resource(UserListResource, '/api/v2/users')
api.add_resource(UserResource, '/api/v2/users/<int:user_id>')


@app.route('/')
def lobby():
    db_sess = db_session.create_session()
    answ = db_sess.query(Products).all()
    products = []
    while True:
        if len(answ) >= 6:
            products.append(answ[0:6])
            answ = answ[5:]
        else:
            products.append(answ[0:])
            break
    return render_template("index.html", products=products, title='Интернет-магазин')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=not form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/product/<int:id_num>')
def viewing_product(id_num):
    db_sess = db_session.create_session()
    product = db_sess.query(Products).get(id_num)
    return render_template('viewing_product.html', product=product, title=product.title)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(name=form.name.data, email=form.email.data, about=form.about.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=not form.remember_me.data)
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/edit_product/<int:id_num>', methods=['GET', 'POST'])
@login_required
def edit_product(id_num):
    form = ProductsForm()
    db_sess = db_session.create_session()
    products = db_sess.query(Products).filter(Products.id == id_num, Products.user == current_user).first()
    if products:
        if request.method == "GET":
            form.title.data = products.title
            form.content.data = products.content
            form.price.data = products.price

        if request.method == 'POST':
            products.title = form.title.data
            products.content = form.content.data
            products.price = form.price.data
            products.date_change = datetime.datetime.now()
            db_sess.commit()
            p = request.files['file'].read()
            with open(f'static/img/{products.id}_1.png', 'wb') as img:
                img.write(p)
            return redirect(f'/product/{products.id}')
    else:
        abort(404)
    return render_template('products.html', title='Редактирование объявления', form=form, name=products.id)


@app.route('/removing_product/<int:id_num>', methods=['GET', 'POST'])
@login_required
def removing_product(id_num):
    form = RemovalProductForm()
    db_sess = db_session.create_session()
    product = db_sess.query(Products).filter(Products.id == id_num, Products.user == current_user).first()
    if not product:
        abort(404)
    if form.validate_on_submit():
        db_sess.delete(product)
        db_sess.commit()
        os.remove(f'static/img/{product.id}_1.png')
        return redirect('/')
    return render_template('removing_product.html', form=form, product=product, title='Снятие объявления')


@app.route('/products', methods=['GET', 'POST'])
@login_required
def add_products():
    form = ProductsForm()
    products = Products()
    db_sess = db_session.create_session()
    users_products = db_sess.query(Products).all()
    if not users_products or len(users_products) == users_products[-1].id:
        filename = str(len(users_products) + 1)
    else:
        data = enumerate(users_products, 1)
        a = list(filter(lambda x: x[0] != x[1].id, data))[0][0]
        products.id = a
        filename = str(a)
    if request.method == 'POST':
        products.title = form.title.data
        products.content = form.content.data
        products.price = form.price.data
        p = request.files['file'].read()
        with open(f'static/img/{filename}_1.png', 'wb') as img:
            img.write(p)
        current_user.products.append(products)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('products.html', title='Новое объявление', form=form, name=filename)


@app.route('/purchase/<int:id_num>', methods=['GET', 'POST'])
def purchase(id_num):
    form = PurchaseForm()
    db_sess = db_session.create_session()
    product = db_sess.query(Products).get(id_num)
    if form.validate_on_submit():
        return redirect('/')
    return render_template('purchase.html', title='Оформление заказа', form=form, product=product)


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(401)
def unregistered_user(_):
    return make_response(jsonify({'error': 'Bad Request'}), 401)


@app.errorhandler(500)
def internal_server_error(_):
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(products_api.blueprint)
    app.run(port=8080, host='127.0.0.1')


if __name__ == "__main__":
    main()
