from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import threading

app = Flask(__name__)

def fetch_data():
    url = "https://www.dadosdemercado.com.br/fluxo"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    table = soup.find("table")
    headers = [header.text.strip() for header in table.find_all("th")]
    rows = table.find_all("tr")[1:]
    
    data = []
    for row in rows[:251]:  # Pegando até 251 linhas
        cols = row.find_all("td")
        entry = {headers[i]: cols[i].text.strip() for i in range(len(cols))}
        data.append(entry)
    
    return data

@app.route("/dados", methods=["GET"])
def get_dados():
    try:
        data = fetch_data()
        return jsonify({
            "status": "Sucesso",
            "total_registros": len(data),  # Adiciona a contagem de registros extraídos
            "dados": data
        })
    except Exception as e:
        return jsonify({
            "status": "Erro",
            "mensagem": str(e)
        })

def run_flask():
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_flask)
    server_thread.start()
