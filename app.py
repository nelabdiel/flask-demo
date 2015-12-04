#I Started by looking at the source html file from the example app to see how everything was called.
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
    'Adj. Close': 'red'
}

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        app.vars['ticker'] = request.form['ticker']
        app.vars['features'] = request.form.getlist('features')

        # Pull stock data
        url = 'https://www.quandl.com/api/v3/datasets/WIKI/' + app.vars['ticker'] + '/data.json'
        r = requests.get(url)
        data = r.json()['dataset_data']['data']
        cols = r.json()['dataset_data']['column_names']
        app.vars['data'] = pd.DataFrame(data, columns=cols)
        return redirect('/graph')

@app.route('/graph', methods=['GET'])
def graph():
    df = app.vars['data']

    p = figure(width=650, height=500, x_axis_type="datetime",
                title="Data from Quandle WIKI set")
    for category in app.vars['features']:
        p.line(pd.to_datetime(df['Date']), df[category], color=app.vars['color'][category], line_width=1, legend=app.vars['ticker'] + ": " + category)

    p.legend.orientation = "top_right"

    plot_resources = RESOURCES.render(js_raw=INLINE.js_raw, css_raw=INLINE.css_raw, js_files=INLINE.js_files, css_files=INLINE.css_files)

    script, div = components(p, INLINE)
    html = render_template('graph.html', ticker=app.vars['ticker'], plot_script=script, plot_div=div, plot_resources=plot_resources)
    return encode_utf8(html)

if __name__ == '__main__':
    app.run(port=33507)
