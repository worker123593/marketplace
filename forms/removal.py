from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired


class RemovalProductForm(FlaskForm):
    reason = RadioField('asdasd', validators=[DataRequired()],
                        choices=('Продал на этом сайте', 'Продал где-то ещё', 'Другая причина'),
                        default='Продал на этом сайте')
    # leave = SubmitField(label='Оставить активным')
    # remove = SubmitField(label='Снять с публикации')
    submit = SubmitField('Применить')