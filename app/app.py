from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import currency_rate
from user_account import UserAccount
from forms import SignUpForm, LoginForm, CurrencyExchangeForm, TransferFundsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///currencyconvertor.db'
db = SQLAlchemy(app)


"""Model for Users."""


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    currency = db.Column(db.String)
    account = db.relationship('Account', backref='user')


"""Model for User Account."""


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float)
    account_holder = db.Column(db.String, db.ForeignKey('user.id'))


db.create_all()


@app.route("/")
def homepage():
    """View function for Home Page."""
    get_currencies_list()
    return render_template("home.html")


@app.route("/about")
def about():
    """View function for About Page."""
    return render_template("about.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """View function for signup"""
    form = SignUpForm()
    if form.validate_on_submit():
        new_user = User(full_name=form.full_name.data, email=form.email.data, password=form.password.data,
                        currency=form.currency.data)
        db.session.add(new_user)

        acc = UserAccount()
        new_acc = Account(balance=acc.balance, account_holder=new_user.id)
        db.session.add(new_acc)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("signup.html", form=form,
                                   message="This Email already exists in the system! Please Login instead.")
        finally:
            db.session.close()
        return render_template("signup.html", message="Successfully signed up")
    return render_template("signup.html", form=form, currencies=get_currencies_list())


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, password=form.password.data).first()
        if user is None:
            return render_template("login.html", form=form, message="Wrong Credentials. Please Try Again.")
        else:
            session['user'] = user.id
            return render_template("details.html", user=user, form=form, message="Welcome !")
    return render_template("login.html", form=form)


@app.route("/details/<int:user_id>", methods=["POST", "GET"])
def user_details(user_id):
    """View function for Showing Details of Each User."""
    form = EditUserForm()
    user = User.query.get(user_id)
    if user is None:
        print("Nothing")
        # abort(404, description="No Pet was Found with the given ID")
    if form.validate_on_submit():
        user.full_name = form.full_name.data
        user.email = form.email.data
        user.currency = form.currency.data
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return render_template("details.html", user=user, form=form, message="A User with this name already exists!")
    return render_template("details.html", user=user, form=form)


@app.route("/wallet/<int:user_id>")
def show_wallet(user_id):
    user = User.query.get(user_id)
    form = CurrencyExchangeForm()
    if user is None:
        print("Nothing")
        # abort(404, description="No Pet was Found with the given ID")
    account = Account.query.get(user_id)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return render_template("wallet.html", user=user, account=account, form=form, currencies=get_currencies_list())


@app.route("/transferfunds", methods=["POST", "GET"])
def transferfunds():
    form = TransferFundsForm()
    return render_template("transferfunds.html", form=form)


@app.route("/transfer", methods=["POST", "GET"])
def transfer():
    from_user = request.args.get('from_user')
    to_user = request.args.get('to_user')
    amount = request.args.get('amount')
    update_balance(from_user, amount, 'withdraw')
    update_balance(to_user, amount, 'deposit')


def update_balance(user_id, amount, action):
    user = User.query.get(user_id)
    if user is not None:
        acc = Account.query.get(user_id)

    if action is "withdraw":
        acc.withdraw(amount)
    elif action is "deposit":
        UserAccount.deposit(amount)


@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('homepage', _scheme='http', _external=True))


@app.route("/currencyexchange", methods=["POST", "GET"])
def exchange_rate():
    """View function for exchange rate"""
    user_id = session.get('user')
    acc = Account.query.get(user_id)
    from_currency = request.args.get('from_currency')
    to_currency = request.args.get('to_currency')
    return currency_rate.get_latest_rate(from_currency, to_currency, acc.balance)
 #   return redirect(url_for('show_wallet', user=session.get('user'), _scheme='http', _external=True))


def get_currencies_list():
    rate_list = []
    rate_dict = currency_rate.get_rates()
    for rate in rate_dict:
        rate_list.append(rate)
    return rate_list


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

