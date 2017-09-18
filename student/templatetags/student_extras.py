from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def lower(value):
	return value.lower()

@register.filter
@stringfilter
def trim(value):
	return value.strip()

@register.filter
@stringfilter
def replaceSpaceWithUnderScore(value):
	ret = ""
	for c in range(0, value.__len__()):
		if value[c] != ' ':
			ret += value[c]
		else:
			ret += "_"
	return ret

def key(d, key_name):
	return d[key_name]
key = register.filter('key', key)

@register.filter
def index(List, i):
    return List[int(i)]

@register.filter
def get_range(value):
	return range(value)

def charAt(string, index):
	return string[index]
charAt = register.filter('charAt', charAt)

@register.filter(name='file_exists')
def file_exists(filepath):
    if default_storage.exists(filepath):
        return filepath
    else:
        index = filepath.rfind('/')
        new_filepath = filepath[:index] + '/image.png'
        return new_filepath