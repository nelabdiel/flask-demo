from flask import Flask, render_template, request, redirect
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.templates import RESOURCES
from bokeh.util.string import encode_utf8

import requests
import pandas as pd

app = Flask(__name__)

app.vars = {}

app.vars['color'] = {
    'Close': 'navy',
    'Adj. Close': 'orange',
    'Volume': 'green'
}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        app.vars['ticker'] = request.form['ticker']
        app.vars['features'] = request.form.getlist('features')

        if app.vars['ticker'].strip() == '':
            return redirect('/error-quandle')

        # Pull stock data
        url = 'https://www.quandl.com/api/v3/datasets/WIKI/' + app.vars['ticker'] + '/data.json'
        r = requests.get(url)
        if r.status_code == 404:
            return redirect('/error-quandle')
        else:
            data = r.json()['dataset_data']['data']
            cols = r.json()['dataset_data']['column_names']
            app.vars['data'] = pd.DataFrame(data, columns=cols)
            #app.vars['data'] = df[['Date'] + app.vars['features']].head(5)
            return redirect('/graph')

if __name__ == '__main__':
  app.run(port=33507)
