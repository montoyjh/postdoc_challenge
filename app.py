import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State

from distribution import Distribution, parse_file

from flask_caching import Cache
import logging

logger = logging.getLogger(__name__)


# standard Dash css, fork this for a custom theme
# we real web devs now
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        #'https://codepen.io/mikesmith1611/pen/QOKgpG.css'
                        ]

app = dash.Dash(external_stylesheets=external_stylesheets)
server = app.server
# app.scripts.config.serve_locally = True
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
                               html.Span(id='{}_summary'.format(name)),
                               html.Span(
                                   ['Drag and Drop or ',
                                    html.A('Select File')],
                                   id='{}_upload_label'.format(name)),
                               help_layout("Upload a text file representing a list of"
                                           "{} and sizes.".format(name))
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
    children=[html.Div([html.H3(app.title), html.Br()],
                       style={'textAlign': 'center'}),
              uploaders,
              button,
              html.Div(id='plot-content')],
    style={'marginLeft': 200, 'marginRight': 200, 'marginTop': 30})



@app.callback(Output('plot-content', 'children'),
              [Input('generate_plot', 'n_clicks')],
              [State('files_upload_data', 'filename'),
               State('nodes_upload_data', 'filename')])
def plot_distribution(n_clicks, nodes_file, files_file):
    """Plots the distribution"""
    logger.info("Using nodes file %s and files file %s",
                (nodes_file, files_file))
    distribution = Distribution.from_filenames(nodes_file, files_file)
    fig = distribution.get_plotly(output_file=False)
    component = dcc.Graph(id="distribution_chart", figure=fig)
    return component


@app.callback(Output('nodes_summary', 'children'),
              [Input('nodes_upload_data', 'filename')])
def node_summary(nodes_file):
    logger.info("Parsing nodes file %s", nodes_file)
    return get_file_summary(nodes_file, 'nodes')


@app.callback(Output('files_summary', 'children'),
              [Input('files_upload_data', 'filename')])
def node_summary(nodes_file):
    logger.info("Parsing nodes file %s", nodes_file)
    return get_file_summary(nodes_file, 'files')


def get_file_summary(filename, name):
    try:
        data = parse_file(filename)
        size_list = list(zip(*data))[1]
        minmax = min(size_list), max(size_list)
        msg = "{} contains {} {}, sizes {}-{}".format(
            filename, name, len(size_list), minmax[0], minmax[1])
        color='green'
    except:
        logger.info("Error parsing file")
        msg = "Error parsing {}".format(filename)
        color = 'red'
    return html.P(msg, style={'color': color})


if __name__ == '__main__':
    app.run_server(debug=False)
