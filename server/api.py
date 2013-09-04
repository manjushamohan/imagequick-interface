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
from crud import create,edit
import  time
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



@app.route('/get/styles/', methods=['GET'])
@crossdomain(origin='*', headers='authorization,Content-Type')
def get_styles():
    return jsonify({'styles':ui_core.get_style_list()})



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
            if data['hook'] and data['format'] and data['category'] and data['volength'] and data['length']:
                data['volength'] = float(data['volength'])
                data['length'] = float(data['length'])
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
            
                data['length'] = float(data['length'])
                create.template(data)
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
            if data['hook'] and data['format'] and data['category'] and data['volength'] and data['length']:
                
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
            
                edit.station(data)
                return jsonify({'status':'success','data':data}) # Pick this data using Angular
            else:
                return jsonify({'status':'fail','message':'Missing data for some field'})
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





#This is after all functions
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")