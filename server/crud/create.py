from common import database
import re

def voice(voice):
	voice['uid']=database.db.voices.find().sort("uid",-1).limit(1)[0]['uid']+1
	database.db.voices.insert(voice)
	return True

def template(template):
	template['length'] = float(template['length'])
	database.db.templates.insert(template)
	return True

def hooktemplate(template):
	database.db.hook_templates.insert(template)
	return True

def format(format):
	format['uid']=database.db.formats.find().sort("uid",-1).limit(1)[0]['uid']+1
	database.db.formats.insert(format)
	return True

def position(pos):
	pos['words']=len(re.findall(r'\w+', pos['name']))
	database.db.postions.insert(pos)
	return True

def station(station):
	station['words']=len(re.findall(r'\w+', station['name']))
	database.db.stations.insert(station)
	return True

def frequency(frequency):
	database.db.frequencies.insert(frequency)
	return True

def style(style):
	style['uid']=database.db.styles.find().sort("uid",-1).limit(1)[0]['uid']+1
	database.db.styles.insert(style)
	return True

def template(template):
	if template['name'] is not None:
		database.db.templates.insert(template)
		return True
	else:
		return False
	
def hooktemplate(template):
	if template['name'] is not None:
		database.db.hook_templates.insert(template)
		return True
	else:
		return False

def hook(hook):
	if hook['hook'] is not None:
		database.db.new_hooks.insert({
			'hook':hook['hook'],
			'format':hook['format'],
			'category':hook['category'],
			'song':hook['song'],
			'artist':hook['artist'],
			'album_art':hook['album_art']			
		})
		if hook['length'] is not None:
			database.db.hook_lengths.insert({
				'file':hook['hook'],
				'length':hook['length']				
			})
		if hook['volength'] is not None:
			database.db.hook_lengths.insert({
				'file':hook['hook']+"_VO",
				'length':hook['volength'],				
			})
		return True
	else:
		return False
	
def slogan_length(slogan):
	if slogan['length'] is not None:
		database.db.slogan_length.insert(slogan)
		return True
	else:
		return False
	
def coupon(c):
	if c['code'] is not None:
		database.db.coupons.insert(c)
		return True
	else:
		return False

def group(group):
	if group['name'] is not None:
		database.db.groups.insert(group)
		return True
	else:
		return False
