import commands
from django.conf import settings
from django.shortcuts import redirect

class GatedContent(object):
	"""
	Prevents specific content directories and types 
	from being exposed to non-authenticated users
	"""

	def process_request(self, request):
		path = request.path
		user = request.user # out of the box auth, YMMV

		is_gated = False
		for gated in settings.GATED_CONTENT:
			if path.startswith(gated) or path.endswith(gated):
				 is_gated = True
				 break

		a = ""
		a += str(path)
		a += (", " + str(is_gated) + ", " + str(user.is_authenticated()))
		commands.getoutput('echo "%s" >> log' % a)

		# Validate the user is an authenticated/valid user
		if is_gated and not user.is_authenticated():
			return redirect('https://cupertutors.org')