from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL

import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Google Map URL', validators=[DataRequired(), URL(require_tld=True)])
    open = StringField('Open Time', validators=[DataRequired()])
    close = StringField('Close Time', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"],
                                validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Rating', choices=["💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪", "✘"],
                              validators=[DataRequired()])
    power_rating = SelectField('Power Outlet Rating', choices=["🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌", "✘"],
                               validators=[DataRequired()])
    submit = SubmitField('Submit')


# Exercise:
# use a validator to check that the URL field has a URL entered.

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            with open('cafe-data.csv', mode='a', encoding='utf-8') as csv_file:
                csv_file.write(f'\n{form.cafe.data}, '
                               f'{form.location.data}, '
                               f'{form.open.data}, '
                               f'{form.close.data}, '
                               f'{form.coffee_rating.data}, '
                               f'{form.wifi_rating.data}, '
                               f'{form.power_rating.data}')
                return "success"
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        cafes_length = len(list_of_rows)
        for row in csv_data:
            list_of_rows.append(row)
    print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows, cafes_count=cafes_length)


if __name__ == '__main__':
    app.run(debug=True)
