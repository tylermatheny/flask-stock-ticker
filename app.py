from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
import pandas as pd
import urllib
import datetime as dt
import requests
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components


app = Flask(__name__)
import os

stock = {}


# Index page
@app.route('/')
def home():
	return redirect('/input')

@app.route('/input', methods = ['GET', 'POST'])
def index():
	return render_template('input.html')

@app.route('/plotting', methods = ['GET','POST'])
def make_plot():
	stock['ticker'] = request.form['ticker']
	API_key = '_KWGA1mS7JAaZmohsVj6'
	start_date = request.form['start_year'] + '-' + request.form['start_month'] + '-' + '01'
	end_date = request.form['end_year'] + '-' + request.form['end_month'] +  '-' + '30'
	api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/' + stock['ticker']+ '.json?api_key=' + API_key
	metric = request.form['metric']
	data = requests.get(api_url)
	new = data.json()
	df = pd.DataFrame(new['data'], columns = new['column_names'])
	df['Date'] = pd.to_datetime(df['Date'])
	mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
	df = df[mask] 


	# create a new plot with a datetime axis type
	plot = figure(plot_width=1000, plot_height=600, x_axis_type='datetime')
	plot.xaxis.axis_label = 'Date'
	plot.xaxis.axis_label_text_font_style = 'normal'
	plot.xaxis.major_label_text_font_size = '14pt'
	plot.xaxis.axis_label_text_font_size = "18pt"
	plot.yaxis.axis_label = 'Price (USD)'
	plot.yaxis.major_label_text_font_size = '14pt'
	plot.yaxis.axis_label_text_font_size = "18pt"
	plot.yaxis.axis_label_text_font_style = 'normal'


	plot.line( x = df.Date, y = df[metric], line_color="#f46d43", line_width=6, line_alpha=0.6, legend = stock['ticker'] + ' price')
	plot.legend.location = "top_left"
	#plot.title.text = request.form['']
	components(plot)
	script, div = components(plot)

	
	return render_template('plot.html', script = script, div =div)

# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
	app.run(port=5000, debug=True)


