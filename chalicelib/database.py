import uuid
import os
import boto3
from boto3.dynamodb.conditions import Key

# １．DynamoDBへの接続を許可する
def _get_database():
    endpoint = os.environ.get('DB_ENDPOINT')
    if endpoint:
        return boto3.resource('dynamodb', endpoint_url=endpoint)
    else:
        return boto3.resource('dynamodb')

# ２．すべてのレコードを取得する
def get_all_todos():
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])
    response = table.scan()
    return response['Items']

# ３．指定されたIDのレコードを取得する
def get_todo(todo_id):
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])
    response = table.query(
        KeyConditionExpression=Key('id').eq(todo_id)
    )
    items = response['Items']
    return items[0] if items else None

def create_todo(todo):
    # １．登録内容を作成する
    item = {
        'id': uuid.uuid4().hex,
        'title': todo['title'],
        'memo': todo['memo'],
        'priority': todo['priority'],
        'completed': False,
    }

    # ２．DynamoDBにデータを登録する
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])
    table.put_item(Item=item)
    return item

def update_todo(todo_id, changes):
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])

    # １．クエリを構築する
    update_expression = []
    expression_attribute_values = {}
    for key in ['title', 'memo', 'priority', 'completed']:
        if key in changes:
            update_expression.append(f"{key} = :{key[0:1]}")
            expression_attribute_values[f":{key[0:1]}"] = changes[key]
    
    # ２．DynamoDBのデータを更新する
    result = table.update_item(
        Key={
            'id': todo_id,
        },
        UpdateExpression='set ' + ','.join(update_expression),
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues='ALL_NEW'
    )
    return result['Attributes']

def delete_todo(todo_id):
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])

    # １．DynamoDBのデータを削除する
    result = table.delete_item(
        Key={
            'id': todo_id,
        },
        ReturnValues='ALL_OLD'
    )
    return result['Attributes']


# ①　疑似データベースを定義する
# BLUE_THREE = [
#     {
#         'id': 'L5',
#         'title': '夢の舞台へ駆け上がる',
#         'memo': 'TONOSAKI',
#         'priority': 3,
#         'completed': False,
#     },
#     {
#         'id': 'L6',
#         'title': '今ここで魅せる',
#         'memo': 'GENDA',
#         'priority': 2,
#         'completed': False,
#     },
#     {
#         'id': 'L8',
#         'title': 'その瞬間を掴む',
#         'memo': 'KANEKO',
#         'priority': 1,
#         'completed': False,
#     }
# ]

# ②　すべてのレコードを取得する

# def get_all_todos():
#     return BLUE_THREE

# ③　指定されたIDのレコードを取得する

# def get_todo(todo_id):
#     for todo in BLUE_THREE:
#         if todo['id'] == todo_id:
#             return todo
#     return None
