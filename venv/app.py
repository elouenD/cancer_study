# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import base64

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

def readCancerFile(path): 
    file = list()
    with open(path) as f:
        for line in f:
            file.append(line.replace('\n', ''))
    file.pop(0)
    return file

patients = readCancerFile("dataSet/Overall_Survival_(Months).txt")
ar = readCancerFile("dataSet/AR_Cleaned.txt")
foxA1 = readCancerFile("dataSet/FOXA1_Cleaned.txt")
tp53 = readCancerFile("dataSet/TP53_Cleaned.txt")

def stringToFloat(tab):
    for i in range(len(tab)):
        tab[i] = round(float(tab[i]))

def countSurvivalOneList(tab):
    monthCount= {}
    for i in range(len(tab)):
        monthCount[tab[i]] = tab.count(tab[i])
    return monthCount

def triBulle(tab):
    n = len(tab)
    # Traverser tous les éléments du tableau
    for i in range(n):
        for j in range(0, n-i-1):
            # échanger si l'élément trouvé est plus grand que le suivant
            if tab[j] > tab[j+1] :
                tab[j], tab[j+1] = tab[j+1], tab[j]

def getValues(data):
    stringToFloat(data)
    triBulle(data)
    monthCount = countSurvivalOneList(data)
    return [list(monthCount.keys()), list(monthCount.values())]

image_filename = './images/metastatic-cancer.jpg' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
patientsValues = getValues(patients)
tp53Values = getValues(tp53)
arValues = getValues(ar)
foxA1Values = getValues(foxA1)    
    
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=tp53Values[0],
    y= tp53Values[1],
    name = 'TP53', # Style name/legend entry with html tags
    connectgaps=True # override default to connect the gaps
))
fig.add_trace(go.Scatter(
    x=arValues[0],
    y=arValues[1],
    name='AR',
))
fig.add_trace(go.Scatter(
    x=foxA1Values[0],
    y=foxA1Values[1],
    name='FOXA1',
))


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Metastatic Prostate Adenocarcinoma study',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div([
        html.Div('    If your prostate cancer spreads to other parts of your body, your doctor may tell you that it\'s "metastatic" or' +
                 'that your cancer has "metastasized." Most often, prostate cancer spreads to the bones or lymph nodes. It\'s also common ' +
                 'for it to spread to the liver or lungs. It\'s rarer for it to move to other organs, such as the brain.' +
    'It\'s still prostate cancer, even when it spreads. For example, metastatic prostate cancer in a bone in your hip is not bone cancer. ' +
       'It has the same prostate cancer cells the original tumor had. Metastatic prostate cancer is an advanced form of cancer. There\'s no cure, ' +
       'but you can treat it and control it. Most men with advanced prostate cancer live a normal life for many years.' +
                'The scheme in the right show us the cancer prostate location and where the prostate cancer can be spread',
    style={'fontSize': 14, 'margin': 10, 'width': '50%', 'display': 'inline-block', 'margin-right': 110}),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image), style={'with': 40})
    ], style={'marginBottom': 50, 'marginTop': 25, 'display': 'inline-block'}),
    dcc.Graph(
        id='example-graph-3',
        figure={
            'data': [
                {'x': patientsValues[0], 'y': patientsValues[1], 'type': 'bar', 'name': 'overall for all genes'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),
    dcc.Graph(
        id='example-graph-1',
        figure={
            'data': [
                {'x': tp53Values[0], 'y': tp53Values[1], 'type': 'bar', 'name': 'TP53'},
                {'x': arValues[0], 'y': arValues[1], 'type': 'bar', 'name': 'AR'},
                {'x': foxA1Values[0], 'y': foxA1Values[1], 'type': 'bar', 'name': 'FOXA1'},

            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),
    dcc.Graph(
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

