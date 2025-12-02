from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Usamos um contador global para gerar IDs de forma segura
# para evitar IDs duplicados após uma exclusão.
next_task_id = 3 

tarefas = [
    {"id": 1, "titulo": "Lavar roupa", "descricao": "Lavar roupa", "concluida": False},
    {"id": 2, "titulo": "Passar roupa", "descricao": "Passar roupa", "concluida": False}
]

@app.route("/tasks", methods=["GET"])
def get_tasks():
    # Retorno 200 OK é o padrão do Flask para GET
    return jsonify({"tarefas": tarefas, "total": len(tarefas)})

@app.route("/tasks/<int:id>", methods=["GET"])
def get_task_by_id(id):
    # Usando list comprehension para encontrar a tarefa de forma mais limpa
    tarefa_encontrada = next((t for t in tarefas if t["id"] == id), None)

    if tarefa_encontrada:
        return jsonify({"mensagem": "Tarefa encontrada!", "tarefa": tarefa_encontrada})
    else:
        # Aborta com um erro 404
        abort(404, description="Tarefa não encontrada!")

@app.route("/tasks", methods=["POST"])
def add_task():
    global next_task_id

    # 1. Validação básica da entrada JSON
    if not request.is_json or 'titulo' not in request.json:
        # Aborta com erro 400 Bad Request
        abort(400, description="Dados inválidos: 'titulo' é obrigatório e o formato deve ser JSON.")
    
    nova_tarefa_dados = request.json

    # 2. Atribui um ID único usando o contador global
    nova_tarefa = {
        "id": next_task_id,
        "titulo": nova_tarefa_dados["titulo"],
        "descricao": nova_tarefa_dados.get("descricao", ""), # Usa .get() para valor padrão se não existir
        "concluida": nova_tarefa_dados.get("concluida", False) 
    }
    
    next_task_id += 1 # Incrementa o contador

    tarefas.append(nova_tarefa)
    # Retorna 201 Created para indicar criação bem-sucedida
    return jsonify({"mensagem": "Tarefa cadastrada!", "tarefa": nova_tarefa}), 201

@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    dados = request.json
    tarefa_encontrada = next((t for t in tarefas if t["id"] == id), None)

    if not tarefa_encontrada:
        abort(404, description="Tarefa não encontrada!")

    if not request.is_json:
         abort(400, description="Requisição deve ser JSON")

    # Atualiza apenas os campos fornecidos na requisição
    tarefa_encontrada.update(dados)
    
    return jsonify({"mensagem": "Tarefa atualizada!"})

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    global tarefas

    tarefa_encontrada = next((t for t in tarefas if t["id"] == id), None)
    
    if not tarefa_encontrada:
        abort(404, description="Tarefa não encontrada!")
    
    # Maneira segura de remover o item da lista enquanto itera
    tarefas.remove(tarefa_encontrada)
    
    return jsonify({"mensagem": "Tarefa apagada!"})


if __name__ == "__main__":
    # Roda o servidor Flask localmente
    app.run(debug=True)

