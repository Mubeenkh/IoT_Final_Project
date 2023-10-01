import RPi.GPIO as GPIO
from time import sleep

# Import packages
from dash import Dash, html, Input, Output, State, callback, dcc

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

LED = 26

GPIO.setup(LED,GPIO.OUT,initial=0)

# Initialize the app
app = Dash(__name__)

# switch_turn_on_style = {'color': 'rgb(209, 231, 42)'}
img_light_on = 'assets/images/light_on.png'
style_img_light_on = {
    'height': '40%',
    'width':'40%',
    '-webkit-filter': 'drop-shadow(1px 1px 20px rgba(255, 255, 0, 1))',
    'filter': 'drop-shadow(1px 1px 20px rgba(255, 255, 0, 1))',
}

# switch_turn_off_style = {'color': 'rgb(154, 154, 154)'}
img_light_off = 'assets/images/light_off.png'
style_img_light_off = {
    'height': '40%',
    'width':'40%',
}



# App layout
app.layout = html.Div(
    children=[
        # html.Div(children='Hello World')
        html.Div([
            html.H2('Phase 1:'),
            html.Div([
                html.Div([
                    html.Img(src=img_light_off,id='light-img',style={})
                ],style={}),
                html.Div([
                    html.Button('Turn On', id='light-switch', n_clicks=0,style={})
                ],style={})
                
            ],id='light-container',style={}),
            # 'width': '50%' or 'display':'inline-block'
            # 'justify':'center','align':'center', 

        ])
    ]
    ,style={}
)

@callback(
    [Output('light-switch', 'children'),
    #  Output('light-switch', 'style'),
     Output('light-switch', 'title'),
     Output('light-img', 'src'),
     Output('light-img', 'style'),],
    Input('light-switch', 'n_clicks')
)

def update_button(n_clicks):
    bool_disabled = n_clicks % 2
    if bool_disabled:
        GPIO.output(LED,1)
        return 'Turn Off', 'Too bright', img_light_on, style_img_light_on
    else: 
        GPIO.output(LED,0)
        return 'Turn On','Too dark', img_light_off, style_img_light_off

# Run the app
if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True)
    app.run(debug=True)