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
        grafica, animales_imagenes = graficar(df, municipio, subscription_key, search_url)
        show = 1
        return render_template("index.html", municipios=municipios, form=munForm, show=show, municipio = munForm.municipio.data, grafica = grafica, animales_imagenes = animales_imagenes)
        #return redirect(url_for('analisis', municipio=munForm.municipio.data))

    return render_template("index.html", municipios=municipios, form = munForm)

@app.route('/analisis/<municipio>')
def analisis(municipio):
    print(municipio)
    grafica, animales_imagenes = graficar(df,municipio,subscription_key,search_url)
    return render_template("graficas.html", grafica = grafica, municipio = municipio, animales_imagenes = animales_imagenes)

if __name__ == '__main__':
    app.run()
