# Import packages
from dash import Dash, html, Input, Output, State, callback, dcc
# Initialize the app
app = Dash(__name__)

switch_turn_on_style = {'font-size':'20px','color': 'black','height': '50px','width': '200px', 'border-radius':'20px'}
img_light_on = 'assets/images/light_on.png'

switch_turn_off_style = {'font-size':'20px','color': 'black','height': '50px','width': '200px', 'border-radius':'20px'}
img_light_off = 'assets/images/light_off.png'

# App layout
app.layout = html.Div([
    # html.Div(children='Hello World')
    html.Div([
        html.H2('Phase 1:'),
        html.Div([
            html.Div([
                html.Img(src=img_light_off,id='light-img',style={'height':'40%','width':'40%'})
            ],style={}),
            html.Div([
                html.Button('Turn On', id='light-switch', n_clicks=0,style={'font-size':'30px'})
            ],style={})
            
        ],style={'border':'2px black solid','border-radius':'20px','display':'inline-block','textAlign': 'center','padding':'20px'}),
        # 'width': '50%' or 'display':'inline-block'
        # 'justify':'center','align':'center', 

    ])
])

@callback(
    [Output('light-switch', 'children'),
     Output('light-switch', 'style'),
     Output('light-switch', 'title'),
     Output('light-img', 'src')],
    Input('light-switch', 'n_clicks')
)

def update_button(n_clicks):
    bool_disabled = n_clicks % 2
    if bool_disabled:
        return 'Turn On', switch_turn_on_style, 'Too dark', img_light_off
    else:
        return 'Turn Off', switch_turn_off_style, 'Too bright', img_light_on

# Run the app
if __name__ == '__main__':
    app.run(debug=True)