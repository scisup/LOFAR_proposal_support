import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

header = html.Div([
            html.H1('LOFAR Project Support Estimator'),
         ])

labelWidth = 6
inpWidth = 4
dropWidth = 4

# PROPOSAL TYPE
single_cycle_only = [ {'label':'Single cycle', 'value':'LC'} ]
long_term_cycle   = [
                        {'label':'Long term', 'value':'LT'},
                        {'label':'Single cycle', 'value':'LC'}
                    ]
prop_type = dbc.FormGroup([
                dbc.Label('Proposal type', width=labelWidth),
                dbc.Col(
                    dcc.Dropdown(
                        options=single_cycle_only, value='LC', 
                        searchable=False, clearable=False, 
                        id='prop_type_drop'
                    ), width=dropWidth
                )
            ], row=True)

# Observation type
obs_type = dbc.FormGroup([
                dbc.Label('Observation type', width=labelWidth),
                dbc.Col(
                    dcc.Dropdown(
                        options=[
                            {'label':'IF (interferometric)', 'value':'IF'},
                            {'label':'BF (beamformed)', 'value':'BF'},
                            {'label':'IF+BF', 'value':'IF+BF'},
                            {'label':'TBB', 'value':'TBB'}
                        ], value='IF', 
                        searchable=False, clearable=False, 
                        id='obs_type_drop'
                    ), width=dropWidth
                )
            ], row=True)

# Total observing hours
obs_hours_total = dbc.FormGroup([
                dbc.Label('Total observing hours in the proposal', width=labelWidth),
                dbc.Col(
                    dbc.Input(type='number',
                              id='nObsHours',
                              value=1,
                              min=0
                    ), width=inpWidth
                )
            ], row=True)

# Observing strategy
obs_strategy = dbc.FormGroup([
                dbc.Label('Observation strategy', width=labelWidth),
                dbc.Col(
                    dcc.Dropdown(
                        options=[
                          {'label':'bookended', 'value':'bookended'},
                          {'label':'interleaved', 'value':'interleaved'},
                          {'label':'no-LST-constraint', 'value':'noLST-constraint'},
                          {'label':'single-run', 'value':'single-run'},
                          {'label':'lucky-imaging', 'value':'lucky-imaging'}
                        ], value='noLST-constraint', 
                        searchable=False, clearable=False, 
                        id='obs_strategy_drop'
                    ), width=dropWidth
                )
            ], row=True)

# No. of individual runs
runs = dbc.FormGroup([
                dbc.Label('Number of observing runs', width=labelWidth),
                dbc.Col(
                    dbc.Input(type='number',
                              id='nObsRuns',
                              value=1,
                              min=1
                    ), width=inpWidth
                )
            ], row=True)

# No. of subbands per observation
nsap = dbc.FormGroup([
                dbc.Label('Number of SAPs per observation (0-8)', width=labelWidth),
                dbc.Col(
                    dbc.Input(type='number',
                              id='nSAP',
                              value=1,
                              min=1,
                              max=8
                    ), width=inpWidth
                )
            ], row=True)

# No. of subbands per observation
npipe = dbc.FormGroup([
                dbc.Label('Number of pipelines per observation', width=labelWidth),
                dbc.Col(
                    dbc.Input(type='number',
                              id='nPipe',
                              value=1,
                              min=0
                    ), width=inpWidth
                )
            ], row=True)

# Observing strategy
para_obs = dbc.FormGroup([
                dbc.Label('Are parallel observations needed?', width=labelWidth),
                dbc.Col(
                    dcc.Dropdown(
                        options=[
                          {'label':'False', 'value':'False'},
                          {'label':'True', 'value':'True'}
                        ], value='False', 
                        searchable=False, clearable=False, 
                        id='para_obs_drop'
                    ), width=dropWidth
                )
            ], row=True)

# Observing strategy
array_req = dbc.FormGroup([
                dbc.Label('Do you need special array configuration? (e.g. any stations not to be missed)', width=labelWidth),
                dbc.Col(
                    dcc.Dropdown(
                        options=[
                          {'label':'False', 'value':'False'},
                          {'label':'True', 'value':'True'}
                        ], value='False', 
                        searchable=False, clearable=False, 
                        id='array_req_drop'
                    ), width=dropWidth
                )
            ], row=True)

# Observing strategy
rt = dbc.FormGroup([
                dbc.Label('Do you want to use responsive telescope?', width=labelWidth),
                dbc.Col(
                    dcc.Dropdown(
                        options=[
                          {'label':'False', 'value':'False'},
                          {'label':'True', 'value':'True'}
                        ], value='False', 
                        searchable=False, clearable=False, 
                        id='rt_drop'
                    ), width=dropWidth
                )
            ], row=True)

# 
change_target = dbc.FormGroup([
                dbc.Label('Will you change the target list during the cycle(s)?', width=labelWidth),
                dbc.Col(
                    dcc.Dropdown(
                        options=[
                          {'label':'False', 'value':'False'},
                          {'label':'True', 'value':'True'}
                        ], value='False', 
                        searchable=False, clearable=False, 
                        id='change_target_drop'
                    ), width=dropWidth
                )
            ], row=True)

# Dynamic spectrum pipeline
dynspec = dbc.FormGroup([
                dbc.Label('Do you want to use the DynSpec pipeline?', width=labelWidth),
                dbc.Col(
                    dcc.Dropdown(
                        options=[
                          {'label':'False', 'value':'False'},
                          {'label':'True', 'value':'True'}
                        ], value='False', 
                        searchable=False, clearable=False, 
                        id='dynspec_drop'
                    ), width=dropWidth
                )
            ], row=True)
# Button
buttons = dbc.FormGroup([
                dbc.Label('', width=labelWidth),
                dbc.Col(dbc.Button('Calculate', id='calculate', color='dark'))
            ], row=True)

form = dbc.Form([prop_type, obs_type, obs_hours_total, \
                 obs_strategy, runs, nsap, npipe, \
                 para_obs, array_req, rt, change_target, \
                 dynspec, buttons])

# Label to show output
output = dbc.FormGroup([
                dbc.Label('Required degree of support', width=labelWidth),
                dbc.Col(
                    dbc.Input(type='text',
                              id='deg_support',
                              value='',
                              disabled=True
                    ), width=inpWidth
                )
            ], row=True)

layout = html.Div([
            dbc.Row(dbc.Col(header)),
            html.Hr(),
            dbc.Row(dbc.Col(form)),
            dbc.Row(dbc.Col(output))
         ], style={'width':'45%', 'padding':'20px'})
