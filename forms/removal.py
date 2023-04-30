from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired


class RemovalProductForm(FlaskForm):
    reason = RadioField('asdasd', validators=[DataRequired()],
                        choices=('Продал на этом сайте', 'Продал где-то ещё', 'Другая причина'),
                        default='Продал на этом сайте')
    remove = SubmitField(label='Снять с публикации')

