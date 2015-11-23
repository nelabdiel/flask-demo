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
    'Adj. Close': 'orange'
}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(port=33507)
