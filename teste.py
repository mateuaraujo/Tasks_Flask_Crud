import pytest
import requests

#CRUD de tarefas
Base_URL = "http://127.0.0.1:5000"
tasks = []
#Criação de tarefas(Create):
def test_create_task():
    new_task_data = { "title": "Tarefa de teste", "description": "Descrição da tarefa de teste" }
    response = requests.post(f"{Base_URL}/tasks", json=new_task_data)
    assert response.status_code == 201
    response_json = response.json()
    assert "message" in response_json
    assert "id" in response_json
    tasks.append(response_json["id"])

#Retorno de todas as tarefas(Read):
def test_get_tasks():
    response = requests.get(f"{Base_URL}/tasks")
    assert response.status_code == 200
    response_json = response.json()
    assert "tasks" in response_json
    assert "total_tasks" in response_json

#Retorno Tarefa específica
def test_get_task():
    if tasks:
        task_id = tasks[0]
        response = requests.get(f"{Base_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert task_id == response_json['id']

# Atualização de tarefas(Update):
def test_update_task():
    if tasks:
        task_id = tasks[0]
        payload = {
            "completed": True,
            "description": "Nova descrição",
            "title": "Título atualizado"
        }
        response = requests.put(f"{Base_URL}/tasks/{task_id}", json=payload)
        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json

        # Nova requisição a tarefa especifica
        response = requests.get(f"{Base_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["title"] == payload["title"]
        assert response_json["description"] == payload["description"]
        assert response_json["completed"] == payload["completed"]

#Delete de tarefas(Delete):

def test_delete_task():
    if tasks:
        task_id = tasks[0]
        response = requests.delete(f"{Base_URL}/tasks/{task_id}")
        assert response.status_code == 200

        response = requests.get(f"{Base_URL}/tasks/{task_id}")
        assert response.status_code == 404