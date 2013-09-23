from common import database
import re
from bson.objectid import ObjectId

def voice(voice):
	voice['_id']=ObjectId(voice['_id'])
	database.db.voices.save(voice)
	return True


def style(style):
	style['_id']=ObjectId(style['_id'])

	database.db.styles.save(style)
	return True

def coupon(coupon):
	coupon['_id']=ObjectId(coupon['_id'])
	database.db.coupons.save(coupon)
	return True	

def slogan_length(slogan):
	slogan['_id']=ObjectId(slogan['_id'])
	database.db.slogan_length.save(slogan)
	return True	

def frequency(frequency):
	frequency['_id']=ObjectId(frequency['_id'])
	database.db.frequencies.save(frequency)
	return True

def format(format):
	format['_id']=ObjectId(format['_id'])
	database.db.formats.save(format)
	return True
def hook(hook):
	hook['_id']=ObjectId(hook['_id'])
	if hook['hook'] is not None:

		database.db.hooks.save({
			'_id':hook['_id'],
			'hook':hook['hook'],
			'format':hook['format'],
			'category':hook['category']			
		})
		if hook['length'] is not None:
			length=hook['length']
			length['_id']=ObjectId(length['_id'])
			length['length']=float(length['length'])
			database.db.hook_lengths.save({
				'_id':length['_id'],
				'file':hook['hook'],
				'length':length['length']				
			})
		if hook['volength'] is not None:
			length=hook['volength']
			length['_id']=ObjectId(length['_id'])
			length['length']=float(length['length'])
			database.db.hook_lengths.save({
				'_id':length['_id'],
				'file':hook['hook']+"_VO",
				'length':length['length']				
			})
		return True
	else:
		return False
	
		
def frequency(frequency):
	frequency['_id']=ObjectId(frequency['_id'])
	database.db.frequencies.save(frequency)
	return True

def position(position):
	position['_id']=ObjectId(position['_id'])
	database.db.postions.save(position)
	return True
def station(station):
	station['_id']=ObjectId(station['_id'])
	database.db.stations.save(station)
	return True

def hooktemp(hooktemp):
	hooktemp['_id']=ObjectId(hooktemp['_id'])
	database.db.hook_templates.save(hooktemp)
	return True

def template(template):
	template['_id']=ObjectId(template['_id'])
	database.db.templates.save(template)
	return True

def group(group):
	group['_id']=ObjectId(group['_id'])
	database.db.groups.save(group)
	return True

def user(user):
	user['_id']=ObjectId(user['_id'])
	database.db.users.save(user)
	return True