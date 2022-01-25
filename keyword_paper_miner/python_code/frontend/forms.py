from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class EnterSettingsForm(FlaskForm):
    keywords = StringField(validators=[DataRequired(), Length(min=2)])
    website = SelectField(label='Queried website', choices=['Google Scholar', 'PubMed'])
    output_amount = SelectField(label='How many papers do you want?', choices=range(1, 101))
    evaluation = [
        "",
        "K-Score",
        "Citations",
        "Year"
    ]
    rating = SelectField(label='Rate by:', choices=evaluation)
    preferences = SelectField(label="K-Score preferences", choices=["", "year", "author", "citations"])
    search = SubmitField('Start the search')

