import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import numpy as np
from datetime import datetime
import re

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Compression"),
    dcc.Input(
        id="input_number",
        type="number",
        placeholder="input type number",
    ),
    html.Div(id="input_data"),

    html.H3("Input Length"),
    html.Div(id="input_length"),

    html.H3("Compressed Output"),
    html.Div(id="output_data"),

    html.H3("Output Length"),
    html.Div(id="output_length"),

    html.H3("De-Compressed Output"),
    html.Div(id="decompressed_data"),

    html.H3("De-Compressed Output Length"),
    html.Div(id="decompressed_length")
])


# Produce Input String
@app.callback(
    Output("input_data", "children"),
    Input("input_number", "value")
)
def produce_input(value):
    d = datetime.now().strftime("%H:%M:%S")
    s = str(d)
    for i in range(value):
        val = np.random.randint(-255, 255, size=(3,))
        for i in val:
            s = f"{s},{i}"
    return s


# Input String Length
@app.callback(
    Output("input_length", "children"),
    Input("input_data", "children")
)
def input_length_fn(value):
    return len(value)


# Compression Algorithm
@app.callback(
    Output("output_data", "children"),
    Input("input_data", "children")
)
def compressed_output(value):
    # dissolve timestamp H,M,S
    # rest:
    def f(output_string):
        output_string = output_string + 255
        a = output_string % 94
        a = chr(a+33)
        b = output_string // 94
        b = chr(b+33)
        # return n*"?" and f(n//94)+chr(n % 94+33)
        return b+a
    s = [int(i) for i in re.split(":|,", value)]
    compressed_value = ""
    for i in s:
        compressed_value = compressed_value + f(i)
    return compressed_value


# Compressed Output Length
@app.callback(
    Output("output_length", "children"),
    Input("output_data", "children")
)
def output_length_fn(value):
    return len(value)


# De-Compression Algorithm
@app.callback(
    Output("decompressed_data", "children"),
    Input("output_data", "children")
)
def decompressed_output(compressed_data):
    def g(compressed_characters):
        b = compressed_characters[0]
        b = ord(b) - 33
        a = compressed_characters[1]
        a = ord(a) - 33
        result = (b*94)+a - 255
        result = str(result)
        return result

    decompressed_value = ""
    counter = 4
    while (len(compressed_data)//2 > 0):
        counter = counter - 1
        if(counter > 0 and counter == 3):
            decompressed_value = decompressed_value + g(compressed_data[:2])
        elif(counter > 0):
            decompressed_value = decompressed_value + \
                ":" + g(compressed_data[:2])
        else:
            decompressed_value = decompressed_value + \
                "," + g(compressed_data[:2])

        compressed_data = compressed_data[2:]
    return decompressed_value


# De-Compressed Output Length
@app.callback(
    Output("decompressed_length", "children"),
    Input("decompressed_data", "children")
)
def decompressed_output_length_fn(value):
    return len(value)


if __name__ == "__main__":
    app.run_server()
