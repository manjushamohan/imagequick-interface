from flask import Flask, Response, render_template
from functools import wraps
from bson.objectid import ObjectId
#from flask import jsonify
import json
from datetime import timedelta, datetime
from flask import make_response, request, current_app
from functools import update_wrapper
import hashlib
from calendar import month_name
from time import sleep
from urllib import urlencode
from sqlite3 import connect, Error as sqerr
from urllib2 import urlopen, Request
from werkzeug.datastructures import ImmutableOrderedMultiDict
from common import ui_core
from common import database
from batch import voicetotemplate
from analytics import analytics
from crud import create,edit,delete
import  time
from werkzeug.datastructures import ImmutableOrderedMultiDict
from werkzeug import secure_filename
import os 
import urllib
#Overriding JSONIFY for MongoIDs
try: 
    import json 
    import datetime
except ImportError: 
    import simplejson as json 
 
try: 
    from bson.objectid import ObjectId 
except: 
    pass 
 

class APIEncoder(json.JSONEncoder): 
    def default(self, obj): 
        if isinstance(obj, (datetime.datetime, datetime.date)): 
            return obj.ctime() 
        elif isinstance(obj, datetime.time): 
            return obj.isoformat() 
        elif isinstance(obj, ObjectId): 
            return str(obj) 
        return json.JSONEncoder.default(self, obj)

def jsonify(data): 
    return Response(json.dumps(data, cls=APIEncoder),mimetype='application/json') 

app = Flask(__name__)
UPLOAD_FOLDER = '/var/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'json', 'csv', 'jpg', 'jpeg', 'gif','pdf'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def create_user(username, password, email):
    if database.db.users.find_one({'username': username}) is not None:
        return {
            'status': 'fail',
            'message': "Username already exists! Please use a diffrent username"
        }
    elif database.db.users.find_one({'email': email}) is not None:
        return {
            'status': 'fail',
            'message': "Email already registered! Please reset you password if you can't access your account"
        }
    else:
        #todo: Station, Frequecy and Slogan, zipcode ( Possibly ids)
        user = {
            'username': username,
            'email': email,
            'password': hashlib.sha1(password).hexdigest(),
            'groups': [],
            'tracks': [],
            'affiliate': {
                'station': '',
                'slogan': '',
                'frequency': '',
                'remaining': 10
            }
        }
        database.db.users.insert(user)
        return {
            'status': 'success',
            'message': None
        }


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
#Write all function to get data here: 

@app.route('/get/voices/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def get_voices():
    return jsonify({'voices':ui_core.get_voice_list()})


@app.route('/get/slogans/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def get_slogans():
    return jsonify({'slogans':ui_core.get_slogan_list()})

@app.route('/get/stations/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def get_stations():
    return jsonify({'stations':ui_core.get_station_list()})

@app.route('/get/frequency/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def get_frequency():
    return jsonify({'frequencies':ui_core.get_frequency_list()})

@app.route('/get/groups/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def get_groups():
    return jsonify({'groups':ui_core.get_group_list()})



@app.route('/get/styles/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def get_styles():
    return jsonify({'styles':ui_core.get_style_list()})

@app.route('/get/hooktemplates/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def get_hooktemplates():
    return jsonify({'hooktemplates':ui_core.get_hooktemplate_list()})


@app.route('/get/templates/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def get_templates():
    return jsonify({'templates':ui_core.get_template_list()})

@app.route('/get/hooks/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def get_hooks():
    return jsonify({'hooks':ui_core.get_hook_list()})


@app.route('/get/producers/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def get_producers():
    return jsonify({'producers':ui_core.get_producer_list()})
@app.route('/get/formatsname/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def get_formatsname():
    return jsonify({'formats':ui_core.get_formatname_list()})

@app.route('/get/formats/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def get_formats():
    return jsonify({'formats':ui_core.get_format_list()})

@app.route('/get/category/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def get_category():
    return jsonify({'category':ui_core.get_category_list()})


@app.route('/get/formatids/<formats>', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def get_formatids(formats):
    return jsonify({'formatids':ui_core.get_format_ids(formats)})

@app.route('/get/voiceids/<formats>', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def get_voiceids(formats):
    return jsonify({'voiceids':ui_core.get_voice_ids(formats)})


@app.route('/get/styleids/<styles>', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def get_styleids(styles):
    return jsonify({'styleids':ui_core.get_style_ids(styles)})


@app.route('/get/months/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def get_month():
    return jsonify({'hooks':ui_core.get_months()})


@app.route('/get/months/<month>', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def get_months(month):
    return jsonify({'hooks':ui_core.get_month_number(month)})

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
        try:
            if data['length'] and data['slogan']:
                data['length'] = float(data['length'])
                create.slogan_length(data) 
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})  
    else:
        pass


@app.route('/add/style', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def add_style():
    if request.method == 'POST':
       
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['name']:
                
                create.style(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})  
    else:
        pass



@app.route('/add/group', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def add_group():
    if request.method == 'POST':
       
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['name'] and data['voices'] and data['format'] and data['templates']:
                
                data['format'] = int(data['format'])
                create.group(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})  
    else:
        pass






@app.route('/add/coupon', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def add_coupon():
    if request.method == 'POST':
       
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['code'] and data['remaininguses'] and data['maxtracks']:
                data['remaininguses'] = int(data['remaininguses'])
                data['maxtracks'] = int(data['maxtracks'])
                create.coupon(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})  
    else:
        pass



@app.route('/add/hook', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def add_hook():
    if request.method == 'POST':
        
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['hook'] and data['format'] and data['category'] and data['volength'] and data['length'] and data['song'] and data['artist'] and data['album_art']:
                data['volength'] = float(data['volength'])
                data['length'] = float(data['length'])
                data['album_art']=urllib.quote_plus(data['album_art'], ':/+')
                create.hook(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})  
    else:
        pass

@app.route('/add/voice', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def add_voice():
    if request.method == 'POST':
       
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['name'] and data['description']:
                
                create.voice(data) 
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass




@app.route('/add/frequency', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def add_frequency():
    if request.method == 'POST':
       
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['frequency'] and data['filename']:
            
                create.frequency(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass




@app.route('/add/station', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def add_station():
    if request.method == 'POST':
       
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['name'] and data['formatIds']:

                data['formatIds']=[str(x) for x in data['formatIds']]
                create.station(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass




@app.route('/add/position', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def add_position():
    if request.method == 'POST':
       
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['name'] and data['formatIds']:
                data['formatIds']=[str(x) for x in data['formatIds']]
                create.position(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass



@app.route('/add/format', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def add_format():
    if request.method == 'POST':
       
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['name'] and data['realName'] and data['voiceIds']:
                data['voiceIds'] = [str(x) for x in data['voiceIds']]
                create.format(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass




@app.route('/add/hooktemplate', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def add_hooktemplate():
    if request.method == 'POST':
        
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['name'] and data['filename1'] and data['filename2'] and data['producer'] and data['formatids'] and data['posCue'] and data['posVoiceids'] and data['posStyleids'] and data['statWords'] and data['statCue1'] and data['statCue2'] and data['statVoiceids'] and data['statStyleids'] and data['freCue1'] and data['freCue2'] and data['freVoiceids'] and data['freStyleids'] and data['price']:
                data['formatids'] = [str(x) for x in data['formatids']]
                data['posVoiceids'] = [str(x) for x in data['posVoiceids']]
                data['posStyleids'] = [str(x) for x in data['posStyleids']]
                data['statVoiceids'] = [str(x) for x in data['statVoiceids']]
                data['statStyleids'] = [str(x) for x in data['statStyleids']]
                data['freVoiceids'] = [str(x) for x in data['freVoiceids']]
                data['freStyleids'] = [str(x) for x in data['freStyleids']]
                data['show']=True
                create.hooktemplate(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass




@app.route('/add/template', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def add_template():
    if request.method == 'POST':
        
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['statCue'] and data['name'] and data['producer'] and data['posCue'] and data['price'] and data['statWords'] and data['filename'] and data['freCue'] and data['length'] and data['formatids'] and data['freStyleids'] and data['freVoiceids'] and data['statStyleids'] and data['posVoiceids'] and data['posStyleids'] and data['statVoiceids'] and data['posWords'] :
                data['formatids'] = [str(x) for x in data['formatids']]
                data['posVoiceids'] = [str(x) for x in data['posVoiceids']]
                data['posStyleids'] = [str(x) for x in data['posStyleids']]
                data['statVoiceids'] = [str(x) for x in data['statVoiceids']]
                data['statStyleids'] = [str(x) for x in data['statStyleids']]
                data['freVoiceids'] = [str(x) for x in data['freVoiceids']]
                data['freStyleids'] = [str(x) for x in data['freStyleids']]
                data['length'] = float(data['length'])
                data['show']=True
                create.template(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass



#All View Functions Goes in here 
@app.route('/all/users/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def users():
    return jsonify({'users':ui_core.get_users()})

@app.route('/gets/user/<id>', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def user(id):
    return jsonify({'user':ui_core.get_user(id)})

@app.route('/edit/user', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def edit_user():
    if request.method == 'POST':
       
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['username'] and data['email']:
                
                edit.user(data) 
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass




@app.route('/all/voices/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def voices():
    return jsonify({'voices':ui_core.get_voices()})

@app.route('/gets/voice/<int:id>', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def voice(id):
    return jsonify({'voice':ui_core.get_voice(id)})


@app.route('/edit/voice', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def edit_voice():
    if request.method == 'POST':
       
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['name'] and data['description']:
                
                edit.voice(data) 
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass



@app.route('/all/coupons/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def coupons():
    return jsonify({'coupons':ui_core.get_coupons()})

@app.route('/gets/coupon/<id>', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def coupon(id):
    return jsonify({'coupon':ui_core.get_coupon(id)})


@app.route('/edit/coupon', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def edit_coupon():
    if request.method == 'POST':
       
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['code'] and data['remaininguses'] and data['maxtracks']:
                data['remaininguses'] = int(data['remaininguses'])
                data['maxtracks'] = int(data['maxtracks'])
                edit.coupon(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})  
    else:
        pass





@app.route('/all/styles/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def styles():
    return jsonify({'styles':ui_core.get_styles()})

@app.route('/gets/style/<int:id>', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def style(id):
    return jsonify({'style':ui_core.get_style(id)})

@app.route('/edit/style', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def edit_style():
    if request.method == 'POST':
       
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['name']:
                
                edit.style(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})  
    else:
        pass


@app.route('/all/slogans/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def slogans():
    return jsonify({'slogans':ui_core.get_slogans()})

@app.route('/gets/slogan/<id>', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def slogan(id):
    return jsonify({'slogan':ui_core.get_slogan(id)})

@app.route('/edit/slogan_length', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def edit_slogan_length():
    if request.method == 'POST':
       
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['length'] and data['slogan']:
                data['length'] = float(data['length'])
                edit.slogan_length(data) 
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})  
    else:
        pass



@app.route('/all/formats/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def formats():
    return jsonify({'formats':ui_core.get_formats()})

@app.route('/gets/format/<int:id>', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def format(id):
    return jsonify({'format':ui_core.get_format(id)})

@app.route('/edit/format', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def edit_format():
    if request.method == 'POST':
       
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['name'] and data['realName'] and data['voiceIds']:
                data['voiceIds'] = [str(x) for x in data['voiceIds']]
                edit.format(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass





@app.route('/all/frequencies/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def frequencies():
    return jsonify({'frequencies':ui_core.get_frequencies()})

@app.route('/gets/frequency/<id>', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def frequency(id):
    return jsonify({'frequency':ui_core.get_frequency(id)})

@app.route('/edit/frequency', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def edit_frequency():
    if request.method == 'POST':
       
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['frequency'] and data['filename']:
            
                edit.frequency(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass


@app.route('/all/hooks/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def hooks():
    return jsonify({'hooks':ui_core.get_hooks()})

@app.route('/gets/hook/<id>', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def hook(id):
    return jsonify({'hook':ui_core.get_hook(id)})

@app.route('/edit/hook', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def edit_hook():
    if request.method == 'POST':
        
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['hook'] and data['format'] and data['category'] and data['volength'] and data['length'] and data['song'] and data['artist'] and data['album_art']:
                
                data['album_art']=urllib.quote_plus(data['album_art'], ':/+%')
                edit.hook(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})  
    else:
        pass


@app.route('/all/positions/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def positions():
    return jsonify({'positions':ui_core.get_positions()})

@app.route('/gets/position/<id>', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def position(id):
    return jsonify({'position':ui_core.get_position(id)})


@app.route('/edit/position', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def edit_position():
    if request.method == 'POST':
       
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['name'] and data['formatIds']:
                data['formatIds']=[str(x) for x in data['formatIds']]
                edit.position(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass



@app.route('/all/stations/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def stations():
    return jsonify({'stations':ui_core.get_stations()})

@app.route('/gets/station/<id>', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def station(id):
    return jsonify({'station':ui_core.get_station(id)})


@app.route('/edit/station', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def edit_station():
    if request.method == 'POST':
       
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['name'] and data['formatIds']:
                data['formatIds']=[str(x) for x in data['formatIds']]
                edit.station(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass

@app.route('/all/hooktemps/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def hooktemps():
    return jsonify({'hooktemps':ui_core.get_hooktemps()})

@app.route('/gets/hooktemp/<id>', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def hooktemp(id):
    return jsonify({'hooktemp':ui_core.get_hooktemp(id)})

@app.route('/edit/hooktemp', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def edit_hooktemp():
    if request.method == 'POST':
        
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['name'] and data['filename1'] and data['filename2'] and data['producer'] and data['formatids'] and data['posCue'] and data['posVoiceids'] and data['posStyleids'] and data['statWords'] and data['statCue1'] and data['statCue2'] and data['statVoiceids'] and data['statStyleids'] and data['freCue1'] and data['freCue2'] and data['freVoiceids'] and data['freStyleids'] and data['price']:
                data['formatids'] = [str(x) for x in data['formatids']]
                data['posVoiceids'] = [str(x) for x in data['posVoiceids']]
                data['posStyleids'] = [str(x) for x in data['posStyleids']]
                data['statVoiceids'] = [str(x) for x in data['statVoiceids']]
                data['statStyleids'] = [str(x) for x in data['statStyleids']]
                data['freVoiceids'] = [str(x) for x in data['freVoiceids']]
                data['freStyleids'] = [str(x) for x in data['freStyleids']]
                edit.hooktemp(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass


@app.route('/all/templates/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def templates():
    return jsonify({'templates':ui_core.get_templates()})

@app.route('/gets/template/<id>', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def template(id):
    return jsonify({'template':ui_core.get_template(id)})

@app.route('/edit/template', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def edit_template():
    if request.method == 'POST':
        
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['statCue'] and data['name'] and data['producer'] and data['posCue'] and data['price'] and data['statWords'] and data['filename'] and data['freCue'] and data['length'] and data['formatids'] and data['freStyleids'] and data['freVoiceids'] and data['statStyleids'] and data['posVoiceids'] and data['posStyleids'] and data['statVoiceids'] and data['posWords'] :
                data['formatids'] = [str(x) for x in data['formatids']]
                data['posVoiceids'] = [str(x) for x in data['posVoiceids']]
                data['posStyleids'] = [str(x) for x in data['posStyleids']]
                data['statVoiceids'] = [str(x) for x in data['statVoiceids']]
                data['statStyleids'] = [str(x) for x in data['statStyleids']]
                data['freVoiceids'] = [str(x) for x in data['freVoiceids']]
                data['freStyleids'] = [str(x) for x in data['freStyleids']]
                data['length'] = float(data['length'])
                edit.template(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass



@app.route('/all/groups/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def groups():
    return jsonify({'groups':ui_core.get_groups()})

@app.route('/gets/group/<id>', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def group(id):
    return jsonify({'group':ui_core.get_group(id)})


@app.route('/edit/group', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def edit_group():
    if request.method == 'POST':
       
        data = request.json # This gets all json data posted here ,ie the data on top
        #Do some double checking verifications
        try:
            if data['name'] and data['voices'] and data['format'] and data['templates']:
                
                data['format'] = int(data['format'])
                
                edit.group(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})  
    else:
        pass




#All Update Functions Goes in here 

@app.route('/update/sfp', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def update_sfp():
    if request.method == 'POST':
       
        data = request.json 
        try:
            if data['format'] and data['voice']:
                
                voicetotemplate.station_frequency_position(data['format'],data['voice'])
                return jsonify({'status':'success'}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass

@app.route('/update/sf', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def update_sf():
    if request.method == 'POST':
       
        data = request.json 
        try:
            if data['format'] and data['voice']:
                
                voicetotemplate.station_frequency(data['format'],data['voice'])
                return jsonify({'status':'success'}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass

@app.route('/update/station', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def update_station():
    if request.method == 'POST':
       
        data = request.json 
        try:
            if data['format'] and data['voice']:
                
                voicetotemplate.station(data['format'],data['voice'])
                return jsonify({'status':'success'}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass

@app.route('/update/frequency', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def update_frequency():
    if request.method == 'POST':
       
        data = request.json 
        try:
            if data['format'] and data['voice']:
                
                voicetotemplate.frequency(data['format'],data['voice'])
                return jsonify({'status':'success'}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass

@app.route('/update/position', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def update_position():
    if request.method == 'POST':
       
        data = request.json 
        try:
            if data['format'] and data['voice']:
                
                voicetotemplate.position(data['format'],data['voice'])
                return jsonify({'status':'success'}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
    else:
        pass


#All Delete Functions Goes in here 

@app.route('/delete/user', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def delete_user():
    if request.method == 'POST':
        try:
            data=request.data
            delete.user(data)
            return jsonify({'status':'success'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
           
    else:
        pass

@app.route('/delete/group', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def delete_group():
    if request.method == 'POST':
        try:
            data=request.data
            delete.group(data)
            return jsonify({'status':'success'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
           
    else:
        pass

@app.route('/delete/coupon', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def delete_coupon():
    if request.method == 'POST':
        try:
            data=request.data
            delete.coupon(data)
            return jsonify({'status':'success'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
           
    else:
        pass

@app.route('/delete/style', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def delete_style():
    if request.method == 'POST':
        try:
            data=request.data
            delete.style(data)
            return jsonify({'status':'success'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
           
    else:
        pass

@app.route('/delete/format', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def delete_format():
    if request.method == 'POST':
        try:
            data=request.data
            delete.format(data)
            return jsonify({'status':'success'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
           
    else:
        pass

@app.route('/delete/frequency', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def delete_frequency():
    if request.method == 'POST':
        try:
            data=request.data
            delete.frequency(data)
            return jsonify({'status':'success'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
           
    else:
        pass

@app.route('/delete/hooktemplate', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def delete_hooktemplate():
    if request.method == 'POST':
        try:
            data=request.data
            delete.hooktemplate(data)
            return jsonify({'status':'success'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
           
    else:
        pass

@app.route('/delete/template', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def delete_template():
    if request.method == 'POST':
        try:
            data=request.data
            delete.template(data)
            return jsonify({'status':'success'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
           
    else:
        pass

@app.route('/delete/slogan_length', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def delete_slogan_length():
    if request.method == 'POST':
        try:
            data=request.data
            delete.slogan_length(data)
            return jsonify({'status':'success'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
           
    else:
        pass

@app.route('/delete/station', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def delete_station():
    if request.method == 'POST':
        try:
            data=request.data
            delete.station(data)
            return jsonify({'status':'success'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
           
    else:
        pass

@app.route('/delete/voice', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def delete_voice():
    if request.method == 'POST':
        try:
            data=request.data
            delete.voice(data)
            return jsonify({'status':'success'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
           
    else:
        pass

@app.route('/delete/position', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def delete_position():
    if request.method == 'POST':
        try:
            data=request.data
            delete.position(data)
            return jsonify({'status':'success'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
           
    else:
        pass 

@app.route('/delete/hook', methods=['POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def delete_hook():
    if request.method == 'POST':
        try:
            data=request.json
            id=data['_id']
            lid=data['length']['_id']
            vid=data['volength']['_id']
            delete.hook(id,lid,vid)
            return jsonify({'status':'success'})
        except:
            return jsonify({'status':'fail','message':'Missing data for some field'})
           
    else:
        pass     









#All analyitics goes here 

@app.route('/analytics/voice/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def analytics_voice_chart():
    chart = analytics.chart_voices()
    chart = chart.fillna(0)
    c_data = {
        'labels':chart.index.tolist(),
        'buy':chart.buy.tolist(),
        'play':chart.play.tolist(),
        'b2p':chart.b2p_percent.tolist()
    }
    return jsonify({'chart':c_data})

@app.route('/analytics/voice/monthly/<int:count>/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def analytics_voice_monthly(count):
    x = count
    now = time.localtime()
    comb = [time.localtime(time.mktime([now.tm_year, now.tm_mon - n, 1, 0, 0, 0, 0, 0, 0]))[:2] for n in range(x)]
    months = []
    for i in comb:
        chart = analytics.monthly_voice(i[0],i[1])
        chart = chart.fillna(0)
        c_data = {
            'month':month_name[i[1]],
            'labels':chart.index.tolist(),
            'buy':chart.buy.tolist(),
            'play':chart.play.tolist(),
        }
        months.append(c_data)
    return jsonify({'charts':months})




#All View Functions Goes in here 
@app.route('/view/templates/imaging', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def view_tempaltes_imaging():
    t = []
    templates = database.db.templates.find()
    for template in templates:
        t.append(template)
    return jsonify({'templates':t})



@app.route('/utilities/import/hooks/lengths',methods=['GET','POST'])
def import_hook_lengths():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #import_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            #command = ['mongoimport', '-h', db_ip, '-d', 'imagequick_dev', '-c', 'hook_lengths', '--type', 'csv', '--fields', 'file,length', '--drop',import_file]
            #out = check_output(command)
            #print " ".join(command)
            #print out
            #return str(out)
            return "Success"
    return '''
    <!doctype html>
    <title>Upload CSV file to import HOOK LENGTHS</title>
    <h1>Upload CSV for Hook Lengths</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/utilities/import/hooks/titles',methods=['GET','POST'])
def import_hooks():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #import_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            #command = ['mongoimport', '-h', db_ip, '-d', 'imagequick_dev', '-c', 'hooks', '--type', 'csv', '--fields', 'hook,format,category', '--drop',import_file]
            #out = check_output(command)
            #print " ".join(command)
            #print out
            #return str(out)
            return "Success"
    return '''
    <!doctype html>
    <title>Upload CSV file to import Hook Titles</title>
    <h1>Upload CSV for Hook Titles</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/backend/create_user', methods=['GET', 'POST'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def add_user():
        if request.method == 'POST':
            data = request.json
            a=create_user(data['username'], data['password'], data['email'])
            print a
            if a['status'] == 'success':
                user = database.db.users.find_one({'email': data['email']})
                user['affiliate']['station'] = data['station']
                user['affiliate']['slogan'] = data['slogan']
                user['affiliate']['frequency'] = data['frequency']
                user['affiliate']['remaining'] = int(data['remaining'])
                user['groups'].append(data['groups'])
                database.db.users.save(user)
                return jsonify({'status':'success'})
            else:
                return Response('Username/Email Already Found')
            return render_template('affliateconfirmation.html', data=data)
        



#This is after all functions
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")