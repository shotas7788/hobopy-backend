from chalice import Chalice
from chalicelib import database
from chalice import BadRequestError, Chalice, NotFoundError

app = Chalice(app_name='hobopy-backend')

# ①　すべてのTodoを取得する
@app.route('/todos', methods=['GET'], cors=True)
def get_all_todos():
    return database.get_all_todos()

# ②　指定されたIDのToDoを取得する
@app.route('/todos/{todo_id}', methods=['GET'], cors=True)
def get_todo(todo_id):
    todo = database.get_todo(todo_id)
    if todo:
        return todo
    else:
        raise NotFoundError('Todo not found.')

@app.route('/todos', methods=['POST'], cors=True)
def create_todo():
    # １．リクエストメッセージボディを取得する
    todo = app.current_request.json_body

    # ２．必須項目をチェックする
    for key in ['title', 'memo', 'priority']:
        if key not in todo:
            raise BadRequestError(f"{key} is required.")

    # ３．データを登録する
    return database.create_todo(todo)

@app.route('/todos/{todo_id}', methods=['PUT'], cors=True)
def update_todo(todo_id):
    changes = app.current_request.json_body

    # １．データを更新する
    return database.update_todo(todo_id, changes)

@app.route('/todos/{todo_id}', methods=['DELETE'], cors=True)
def delete_todo(todo_id):
    
    # １．データを削除する
    return database.delete_todo(todo_id)

# @app.route('/')
# def index():
#     return {'hello': 'world'}


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
