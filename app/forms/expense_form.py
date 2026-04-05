from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired

class ExpenseForm(FlaskForm):
    amount = DecimalField("Amount", validators=[DataRequired()])
    
    category = SelectField(
        "Category",
        choices=[
            ("Food", "Food"),
            ("Travel", "Travel"),
            ("Shopping", "Shopping"),
            ("Bills", "Bills"),
            ("Other", "Other")
        ],
        validators=[DataRequired()]
    )

    description = StringField("Description")
    
    submit = SubmitField("Add Expense")