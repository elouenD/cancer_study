# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#F1ECEB',
    'text': '#111111'
}

patients = list()
with open("dataSet/Overall_Survival_(Months).txt") as f:
    for line in f:
        patients.append(line.replace('\n', ''))

patients.pop(0)
print(patients)

def stringToFloat(tab):
    for i in range(len(patients)):
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

stringToFloat(patients)
triBulle(patients)
monthCount = countSurvivalOneList(patients)
nbByMonth = list(monthCount.keys())
nbAlive = list(monthCount.values())


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

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
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
            id='example-graph-3',
            figure={
                'data': [
                    {'x': nbByMonth, 'y': nbAlive, 'type': 'bar', 'name': 'overall for all genes'},
                    {'x': nbByMonth, 'y': nbAlive, 'type': 'bar', 'name': ''},
                ],
                'layout': {
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    }
                }
            }
    )


])

if __name__ == '__main__':
    app.run_server(debug=True)

