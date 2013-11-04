from common import database
import calendar
from bson.objectid import ObjectId
def get_voice_list():
	voicelist = []
	for voice in database.db.voices.find():
		v={
			"uid":voice['uid'],
			"name":voice['name']
		}
		voicelist.append(v)
	return voicelist
def get_voices():
	voicelist = []
	for voice in database.db.voices.find():
		voicelist.append(voice)
	return voicelist
def get_voice(id):
	voice=database.db.voices.find_one({'uid':id})
	return voice


def get_style_list():
	stylelist = []
	for style in database.db.styles.find():
		s={
			"uid":style['uid'],
			"name":style['name']
		}
		stylelist.append(s)
	return stylelist
def get_hooktemplate_list():
	hooktemplatelist = []
	for hooktemplate in database.db.hook_templates.find():
		s={
			"_id":hooktemplate['_id'],
			"name":hooktemplate['name'],
			"formatids":hooktemplate['formatids']
		}
		hooktemplatelist.append(s)
	return hooktemplatelist
def get_template_list():
	templatelist = []
	for template in database.db.templates.find():
		s={
			"_id":template['_id'],
			"name":template['name'],
			"formatids":template['formatids']
		}
		templatelist.append(s)
	return templatelist

def get_slogan_list():
	sloganlist = []
	for slogan in database.db.postions.find():
		sloganlist.append(slogan['name'])
	return sloganlist

def get_station_list():
	stationlist = []
	for station in database.db.stations.find():
		stationlist.append(station['name'])
	return stationlist

def get_frequency_list():
	frequencylist = []
	for frequency in database.db.frequencies.find():
		frequencylist.append(frequency['frequency'])
	return frequencylist
def get_group_list():
	grouplist = []
	for group in database.db.groups.find():
		grouplist.append(group['name'])
	return grouplist


def get_hook_list():
	hooks = []
	for hook in database.db.hooks.find():
		hooks.append(hook['hook'])
	return hooks

def get_producer_list():
	producer_list = []
	for template in database.db.templates.find():
		producer_list.append(template['producer'])
	return list(set(producer_list))

def get_format_list():
	formatlist = []
	for format in database.db.formats.find():
		f={
			"uid":format['uid'],
			"name":format['name']
		}
		formatlist.append(f)
	return formatlist

def get_category_list():
	list = ['current','recurrent','gold','special']
	return list

def get_format_ids(formats):
	idlist = []
	for format in formats:
		idlist.append(str(database.db.formats.find_one({'name':format})['uid']))
	return idlist

def get_voice_ids(formats):
	idlist = []
	for format in formats:
		idlist.append(str(database.db.voices.find_one({'name':format})['uid']))
	return idlist

def get_style_ids(styles):
	idlist = []
	for style in styles:
		idlist.append(str(database.db.styles.find_one({'name':style})['uid']))
	return idlist

def get_months():
	months = []
	for month in calendar.month_name:
		months.append(month)
	return months

def get_month_number(month):
	months = get_months()
	number = str(months.index(month))
	return number.zfill(2)



def get_coupons():
	couponlist = []
	for coupon in database.db.coupons.find():
		couponlist.append(coupon)
	return couponlist
def get_coupon(id):
	id=ObjectId(id)
	coupon=database.db.coupons.find_one({'_id':id})
	return coupon

def get_styles():
	stylelist = []
	for style in database.db.styles.find():
		stylelist.append(style)
	return stylelist
def get_style(id):
	style=database.db.styles.find_one({'uid':id})
	return style

def get_slogans():
	sloganlist = []
	for slogan in database.db.slogan_length.find():
		sloganlist.append(slogan)
	return sloganlist
def get_slogan(id):
	id=ObjectId(id)
	slogan=database.db.slogan_length.find_one({'_id':id})
	return slogan

def get_formats():
	formatlist = []
	for format in database.db.formats.find():
		formatlist.append(format)
	return formatlist
def get_format(id):
	format=database.db.formats.find_one({'uid':id})
	format['voiceIds']=[int(x) for x in format['voiceIds']]
	return format

def get_frequencies():
	frequencylist = []
	for frequency in database.db.frequencies.find():
		frequencylist.append(frequency)
	return frequencylist
def get_frequency(id):
	id=ObjectId(id)
	frequency=database.db.frequencies.find_one({'_id':id})
	return frequency

def get_hooks():
	hooklist = []
	for hook in database.db.hooks.find():
		hooklist.append(hook)
	return hooklist
def get_hook(id):
	id=ObjectId(id)
	hook=database.db.hooks.find_one({'_id':id})
	hook['length']=database.db.hook_lengths.find_one({'file':hook['hook']})
	hook['volength']=database.db.hook_lengths.find_one({'file':hook['hook']+"_VO"})
	return hook

def get_positions():
	positionlist = []
	for position in database.db.postions.find():
		positionlist.append(position)
	return positionlist
def get_position(id):
	id=ObjectId(id)
	position=database.db.postions.find_one({'_id':id})
	position['formatIds']=[int(x) for x in position['formatIds']]
	return position

def get_stations():
	stationlist = []
	for station in database.db.stations.find():
		stationlist.append(station)
	return stationlist
def get_station(id):
	id=ObjectId(id)
	station=database.db.stations.find_one({'_id':id})
	station['formatIds']=[int(x) for x in station['formatIds']]
	return station

def get_hooktemps():
	hooktemplist = []
	for hooktemp in database.db.hook_templates.find():
		hooktemplist.append(hooktemp)
	return hooktemplist

def get_hooktemp(id):
	id=ObjectId(id)
	hooktemp=database.db.hook_templates.find_one({'_id':id})
	hooktemp['formatids']=[int(x) for x in hooktemp['formatids']]
	hooktemp['posVoiceids']=[int(x) for x in hooktemp['posVoiceids']]
	hooktemp['posStyleids']=[int(x) for x in hooktemp['posStyleids']]
	hooktemp['statVoiceids']=[int(x) for x in hooktemp['statVoiceids']]
	hooktemp['statStyleids']=[int(x) for x in hooktemp['statStyleids']]
	hooktemp['freVoiceids']=[int(x) for x in hooktemp['freVoiceids']]
	hooktemp['freStyleids']=[int(x) for x in hooktemp['freStyleids']]
	return hooktemp

def get_templates():
	templatelist = []
	for template in database.db.templates.find():
		templatelist.append(template)
	return templatelist

def get_template(id):
	id=ObjectId(id)
	template=database.db.templates.find_one({'_id':id})
	template['formatids']=[int(x) for x in template['formatids']]
	template['posVoiceids']=[int(x) for x in template['posVoiceids']]
	template['posStyleids']=[int(x) for x in template['posStyleids']]
	template['statVoiceids']=[int(x) for x in template['statVoiceids']]
	template['statStyleids']=[int(x) for x in template['statStyleids']]
	template['freVoiceids']=[int(x) for x in template['freVoiceids']]
	template['freStyleids']=[int(x) for x in template['freStyleids']]
	return template


def get_groups():
	grouplist = []
	for group in database.db.groups.find():
		grouplist.append(group)
	return grouplist
def get_group(id):
	id=ObjectId(id)
	group=database.db.groups.find_one({'_id':id})
	
	return group

def get_users():
	userlist=[]
	for user in database.db.users.find():
		userlist.append(user)
	return userlist
def get_user(id):
	id=ObjectId(id)
	user=database.db.users.find_one({'_id':id})
	return user
