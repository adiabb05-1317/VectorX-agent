from flask import g,request, current_app



def sample():
    current_app.config['PORT']
    return "Hello World"