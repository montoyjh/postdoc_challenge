from os import environ
from uuid import uuid4
from base64 import b64decode

import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State

from distribution import Distribution, parse_string

from flask_caching import Cache
import logging

logger = logging.getLogger(__name__)


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
#                         'https://codepen.io/mikesmith1611/pen/QOKgpG.css']
app = dash.Dash()

app.server.secret_key = environ.get('FLASK_SECRET_KEY', str(uuid4()))
server = app.server
app.scripts.config.serve_locally = True
app.title = "File distributor"
route = dcc.Location(id='url', refresh=False)

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem', 'CACHE_DIR': '.tmp'
})


def help_layout(help_message):
    html.Span([" ", html.Span(help_message, className="tooltiptext")],
              className="tooltip")


def get_upload_div(name):
    return html.Div([
                html.Label('Load a {} config (e. g. {}.txt):'.format(name, name)),
                dcc.Upload(id='{}_upload_data'.format(name),
                           children=html.Div([
                               html.Span(
                                   ['Drag and Drop or ',
                                    html.A('Select File')],
                                   id='{}_upload_label'.format(name)),
                           ]),
                           style={
                               'width': '100%',
                               'height': '100px',
                               'lineHeight': '60px',
                               'borderWidth': '1px',
                               'borderStyle': 'dashed',
                               'borderRadius': '5px',
                               'textAlign': 'center',
                           },
                           ),
            ])

uploaders = html.Div([html.Br(), get_upload_div('files'), get_upload_div('nodes')])
button = html.Button('Generate plot', id='generate_plot')

app.layout = html.Div(
    children=[route,
              html.Div([html.H3(app.title), html.Br()],
                       style={'textAlign': 'center'}),
              uploaders,
              button,
              html.Div(id='plot-content')],
    style={'marginLeft': 200, 'marginRight': 200, 'marginTop': 30})

app.css.append_css(
    {"external_url": 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
app.css.append_css(
    {"external_url": 'https://codepen.io/mkhorton/pen/zPgJJw.css'})
app.css.append_css(
    {"external_url": 'https://codepen.io/mikesmith1611/pen/QOKgpG.css'})



@app.callback(Output('plot-content', 'children'),
              [Input('generate_plot', 'n_clicks')],
              [State('files_upload_data', 'contents'),
               State('nodes_upload_data', 'contents')])
def plot_distribution(n_clicks, files_content, nodes_content):
    """Plots the distribution"""
    if files_content is not None and nodes_content is not None:
        filestring = stringify_contents(files_content)
        nodestring = stringify_contents(nodes_content)
        print(nodestring)
        distribution = Distribution.from_strings(nodestring, filestring)
        fig = distribution.get_plotly(output_file=False)
        component = dcc.Graph(id="distribution_chart", figure=fig)
        return component


@app.callback(Output('nodes_upload_label', 'children'),
              [Input('nodes_upload_data', 'filename'),
               Input('nodes_upload_data', 'contents')])
def node_summary(fname, contents):
    if fname is not None:
        logger.info("Parsing nodes file %s", fname)
        return get_file_summary(fname, contents, 'nodes')
    else:
        return ['Drag and Drop or ', html.A('Select File')]


@app.callback(Output('files_upload_label', 'children'),
              [Input('files_upload_data', 'filename'),
               Input('files_upload_data', 'contents')])
def node_summary(fname, contents):
    if fname is not None:
        logger.info("Parsing nodes file %s", fname)
        return get_file_summary(fname, contents, 'files')
    else:
        return ['Drag and Drop or ', html.A('Select File')]


def stringify_contents(contents):
    content_type, contents = contents.split(',')
    return b64decode(contents).decode('utf-8')


def get_file_summary(filename, contents, name):
    if contents is not None:
        try:
            decoded = stringify_contents(contents)
            data = parse_string(decoded)
            size_list = list(zip(*data))[1]
            minmax = min(size_list), max(size_list)
            msg = "{} contains {} {}, sizes {}-{}".format(
                filename, name, len(size_list), minmax[0], minmax[1])
            color='green'
        except Exception as e:
            logger.debug("Error parsing file {}".format(e))
            msg = "Error parsing {}".format(filename)
            color = 'red'
        return html.P(msg, style={'color': color})


if __name__ == '__main__':
    app.run_server(debug=False)
