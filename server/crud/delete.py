from common import database
import re
from bson.objectid import ObjectId

def coupon(id):
	id=ObjectId(id)
	database.db.coupons.remove( { '_id' : id } )
	return True
def voice(id):
	id=ObjectId(id)
	database.db.voices.remove( { '_id' : id } )
	return True


def style(id):
	id=ObjectId(id)
	database.db.styles.remove( { '_id' : id } )
	return True

def format(id):
	id=ObjectId(id)
	database.db.formats.remove( { '_id' : id } )
	return True

def frequency(id):
	id=ObjectId(id)
	database.db.frequencies.remove( { '_id' : id } )
	return True

def hooktemplate(id):
	id=ObjectId(id)
	database.db.hook_templates.remove( { '_id' : id } )
	return True

def template(id):
	id=ObjectId(id)
	database.db.templates.remove( { '_id' : id } )
	return True

def slogan_length(id):
	id=ObjectId(id)
	database.db.slogan_length.remove( { '_id' : id } )
	return True

def station(id):
	id=ObjectId(id)
	database.db.stations.remove( { '_id' : id } )
	return True


def position(id):
	id=ObjectId(id)
	database.db.postions.remove( { '_id' : id } )
	return True

def hook(id,lid,vid):
	id=ObjectId(id)
	lid=ObjectId(lid)
	vid=ObjectId(vid)
	database.db.new_hooks.remove( { '_id' : id } )
	database.db.hook_lengths.remove( { '_id' : lid } )
	database.db.hook_lengths.remove( { '_id' : vid } )
	return True

def group(id):
	id=ObjectId(id)
	database.db.groups.remove( { '_id' : id } )
	return True



def user(id):
	id=ObjectId(id)
	database.db.users.remove( { '_id' : id } )
	return True