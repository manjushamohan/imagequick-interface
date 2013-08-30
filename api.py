from flask import Flask, Response, render_template
from functools import wraps
from bson.objectid import ObjectId
from flask import jsonify
import json
from datetime import timedelta, datetime
from flask import make_response, request, current_app
from functools import update_wrapper
import hashlib
from produce import *
from time import sleep
from urllib import urlencode
from sqlite3 import connect, Error as sqerr
from urllib2 import urlopen, Request
from werkzeug.datastructures import ImmutableOrderedMultiDict
from common import ui_core
from common import database
from batch import voicetotemplate
from analytics import analytics
from crud import create

app = Flask(__name__)


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp
            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            #h['Access-Control-Allow-Headers'] = 'authorization'
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        f.required_methods = ['OPTIONS']
        return update_wrapper(wrapped_function, f)

    return decorator


def jsonp(func):
    """Wraps JSONified output for JSONP requests."""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)

    return decorated_function


def check_auth(username, password):
    res = db.users.find_one({'username': str(username), 'password': hashlib.sha1(password).hexdigest()})
    if res:
        return True


@crossdomain(origin='*', headers='authorization')
def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    #resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        user = db.users.find_one({'username': str(auth.username), 'password': hashlib.sha1(auth.password).hexdigest()})
        user['_id'] = str(user['_id'])
        return f(user=user, *args, **kwargs)

    return decorated

# @Manju Add functions here. This one is an Example for the code below
'''
class AddSlo(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'Add Slogan Length',size=(400,300))
        wx.Frame.CentreOnScreen(self)
        inp=wx.Panel(self,-1,(-1,-1),(-1,-1))
        wx.StaticText(inp,-1,"Slogan",pos=(40,40))
        self.sl=wx.TextCtrl(inp,-1,"",pos=(120,35),size=(200,30))
        wx.StaticText(inp,-1,"Length",pos=(40,80))
        self.le=wx.TextCtrl(inp,-1,"",pos=(120,75),size=(200,30))
        but=wx.Button(inp,label='Add',pos=(150,130),size=(65,-1)).Bind(wx.EVT_BUTTON,self.butact)

    def butact(self,event):
        slog = {
                'slogan':self.sl.GetValue(),
                'length':float(self.le.GetValue()),
        }
        create.slogan_length(slog)
        self.Close()
'''

@app.route('/add/slogan_length', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def add_slogan_length():
    if request.method == 'POST':
        """
        Sample Data Received here: 
        {
                slogan:'Eighties Nineties and Now',
                length:23.5,
        }
        You get all this data in JSON from AngularJS
    
        """
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        if data['length'] and data['slogan']:
            data['length'] = float(data['length'])
            create.slogan_length(data) 
            return jsonify({'status':'success','data':data}) # Pick this data using Angular
        else:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass



#This is after all functions
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")