from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, EmailField, TelField
from wtforms.validators import DataRequired


class PurchaseForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    telephon = TelField('Телефон', validators=[DataRequired()])
    position = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Купить')

