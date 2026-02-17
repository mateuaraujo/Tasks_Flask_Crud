from flask import Flask, request, jsonify
from sqlalchemy import true
from models.task import Task

app = Flask(__name__)

"""@app.route("/")
def hello_world():
  return "Hello world!"

@app.route("/about")
def about():
  return "Página sobre"""

#CRUD de tarefas
#Create, Read, Update, Delete
#Criação de tarefas(Create):
tasks = []
task_id_control = 1

@app.route("/tasks", methods=["POST"])
def create_task():
  global task_id_control
  data = request.get_json()
  new_task = Task(id=task_id_control, title=data["title"], description=data["description"])
  task_id_control += 1
  tasks.append(new_task)
  print(tasks)
#  print(data)
  return jsonify({"message": "Tarefa criada com sucesso!"}), 201

#  Leitura de tarefas(Read):
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks_list = [task.to_dict() for task in tasks]
    """  for task in tasks:
    tasks_list.append(task.to_dict())   """
    output = {
        "tasks": tasks_list,
        "total_tasks": len(tasks_list)
    }
    return jsonify(output)

#  return jsonify([task.to_dict() for task in tasks])

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    for task in tasks:
        if task.id == task_id:
            return jsonify(task.to_dict())
    return jsonify({"message": "Tarefa não encontrada!"}), 404

# Atualização de tarefas(Update):
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    if task == None:
        return jsonify({"message": "Tarefa não encontrada!"}), 404
    
    data = request.get_json()
    task.title = data["title"]
    task.description = data["description"]
    task.completed = data["completed"]
    return jsonify({"message": "Tarefa atualizada com sucesso!"}) 

# Exclusão de tarefas(Delete):
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
        
    if task == None:
        return jsonify({"message": "Tarefa não encontrada!"}), 404
    
    tasks.remove(task)
    return jsonify({"message": "Tarefa excluída com sucesso!"})

if __name__ == "__main__":
  app.run(debug=True)
