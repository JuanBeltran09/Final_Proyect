from flask import Flask, render_template, request, redirect, url_for

import forms
from Grafica import graficar
import Filtro_Df as fil


df = fil.filtro()
subscription_key = 'b281266792354b04a9743d3a43ed24b7'
search_url = 'https://api.bing.microsoft.com/v7.0/images/search'


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    municipios = df['municipality'].drop_duplicates().tolist()
    munForm = forms.munForm(request.form)

    if request.method == 'POST':
        municipio = request.form.get('municipio')
        munForm.municipio.data = municipio
        animal_info = graficar(df, municipio, subscription_key, search_url)
        show = 1
        return render_template("index.html",
                               municipios=municipios,
                               form=munForm,
                               show=show,
                               municipio = munForm.municipio.data,
                               animal_info = animal_info)

    return render_template("index.html", municipios=municipios, form = munForm)

if __name__ == '__main__':
    app.run()
