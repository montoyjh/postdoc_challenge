import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State

from distribution import Distribution

from flask_caching import Cache
import logging

log = logging.getLogger(__name__)

# TODO: Fix math rendering

app = dash.Dash()
server = app.server
# app.config.supress_callback_exceptions = True  # TODO: remove this?
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
                html.Label('Load a {} config (e. g. {}.txt):'.format(name)),
                dcc.Upload(id='{}_upload_data'.format(name),
                           children=html.Div([
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
                           multiple=True)
            ])

uploaders = html.Div([html.Br(), get_upload_div('files'), get_upload_div('nodes')])
button = html.Button('Generate plot', id='generate_plots')

app.layout = html.Div(
    children=[html.Div([html.H3(app.title), html.Br()],
                       style={'textAlign': 'center'}),
              uploaders,
              html.Div(id='plot-content')],
    style={'marginLeft': 200, 'marginRight': 200, 'marginTop': 30})

# standard Dash css, fork this for a custom theme
# we real web devs now
app.css.append_css(
    {'external_url': 'https://codepen.io/mikesmith1611/pen/QOKgpG.css'})


@app.callback(Output('', 'children'),
              [Input('generate_plot', 'n_clicks')],
              [State('files_upload_data', 'filename'),
               State('nodes_upload_data', 'filename')])
def plot_distribution(nodes_file, files_file):
    """Plots the distribution"""
    distribution = Distribution.from_filenames(nodes_file, files_file)
    return distribution.get_plotly()


if __name__ == '__main__':
    app.run_server(debug=True)
