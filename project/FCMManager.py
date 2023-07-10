from django.http import JsonResponse
import firebase_admin
from firebase_admin import credentials,messaging
cred = credentials.Certificate("C:/Users/ASUS/.vscode/django/assignment test/project/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
app = firebase_admin.get_app()

def send_push(request,FCMtoken):
    
    # registration_token = request.GET.get['token']
    print(FCMtoken)
    message = messaging.Message(
        notification=messaging.Notification(
            title='New message',
            body='Hello, world!'
        ),
        token=FCMtoken
    )
    response = messaging.send(message, app=app)
    return response