import pickle
import numpy as np
from flask import Flask, request, render_template,redirect, url_for
from utils import img_agents

app = Flask(__name__, static_folder='static')

# Cargar el modelo desde el archivo
with open('modelo_regresion.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        mapa = int(request.form['Mapa'])
        agent = int(request.form['Agent'])
        rnd = int(request.form['Rnd'])
        apr = float(request.form['APR'])
        kpr = float(request.form['KPR'])
        kmax = int(request.form['KMax'])

        X_nuevo = [[mapa,agent,rnd,apr,kpr,kmax]]
        y_pred = model.predict(X_nuevo)
        resultado = y_pred.tolist()

        url_agent_img = img_agents.get(str(agent))
        url_map_img = url_for('static', filename=f'imgs/maps/{mapa}.webp')
        print(f'Imagen: {url_agent_img}')
        return redirect(url_for('predict', resultado=resultado,url_agent_img=url_agent_img, url_map_img=url_map_img))
    
    return render_template('index.html')

@app.route('/predict/<resultado>', methods=['GET'])
def predict(resultado):
    datos_list = eval(resultado)
    url_agent_img = request.args.get('url_agent_img')
    url_map_img = request.args.get('url_map_img')
    return render_template('predict.html',resultado=datos_list,url_agent_img=url_agent_img,url_map_img=url_map_img)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
