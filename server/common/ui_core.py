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

def get_template_list():
	templatelist = []
	for template in database.db.templates.find():
		templatelist.append(template['name'])
	return templatelist

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
	return position

def get_stations():
	stationlist = []
	for station in database.db.stations.find():
		stationlist.append(station)
	return stationlist
def get_station(id):
	id=ObjectId(id)
	station=database.db.stations.find_one({'_id':id})
	return station