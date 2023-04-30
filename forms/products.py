from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, FileField
from wtforms.validators import DataRequired


class ProductsForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    content = TextAreaField("Содержание", validators=[DataRequired()])
    price = IntegerField("Цена", validators=[DataRequired()])
    img = FileField('Выберите фотографию', validators=[DataRequired()])
    submit = SubmitField('Применить')

