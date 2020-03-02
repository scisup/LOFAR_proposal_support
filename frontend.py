"""Main file"""

__author__ = "Sarrvesh S. Sridhar"
__email__ = "sarrvesh@astron.nl"

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Output, State, Input
from gui import layout
import flask
import DegSupIndicator_v1_1 as d

# Initialize the dash app
server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN], \
                server=server, url_base_pathname='/support_estimator/')
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

#######################################
# Setup the layout of the web interface
#######################################
app.layout = layout
app.title = 'LOFAR Project Support Estimator'

#######################################
# What should the Calculate button do?
#######################################
def str2bool(var):
    if var == 'True':
        return True
    else:
        return False

@app.callback(
    Output('deg_support', 'value'),
    [Input('calculate','n_clicks')],
    [State('prop_type_drop', 'value'),
     State('obs_type_drop', 'value'),
     State('nObsHours', 'value'),
     State('obs_strategy_drop', 'value'),
     State('nObsRuns', 'value'),
     State('nSAP', 'value'),
     State('nPipe', 'value'),
     State('para_obs_drop', 'value'),
     State('array_req_drop', 'value'),
     State('rt_drop', 'value'),
     State('change_target_drop', 'value'),
     State('dynspec_drop', 'value')
    ]
)
def on_calculate_click(n, prop_type, obs_type, n_hours_total, \
                       obs_strategy, n_runs, n_sap, n_pipe, para_obs, \
                       array_req, rt, change_tar, dynspec):
    if n is None:
        # The page has just loaded
        return ''
    else:
        # User has clicked on the button
        output_str = d.main(
            Projtype = prop_type,
            Tobsreq  = n_hours_total,
            Obsmode = obs_type,
            Obsstrategytype = obs_strategy,
            Parallelobs = str2bool(para_obs),
            Nruns = n_runs,
            Nsap = n_sap,
            Arrconstr = str2bool(array_req),
            Schedconstr = False,
            Resptel = str2bool(rt),
            Targlistupd = str2bool(change_tar),
            Npipxobs = n_pipe,
            Dynsp = str2bool(dynspec)
        )
        return output_str

if __name__ == '__main__':
    #app.run_server(debug=True, host='0.0.0.0', port=8052)
    app.run_server(debug=False, host='0.0.0.0', port=8052, \
                  dev_tools_ui=False, dev_tools_props_check=False)
