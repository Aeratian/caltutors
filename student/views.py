from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from student.models import Student

from django.core.urlresolvers import reverse

from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

from django import forms

import base64, datetime, random, string, time, commands, json
import subprocess
from threading import Timer
import resource
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# from subprocess import STDOUT, check_output

topics = {'amc_8': ['Algebra', 'Counting and Probability', 'Geometry', 'Number Theory', 'Problem Solving Strategies - Important Concepts - Word Problems - Logic'],
		  'amc_10': [],
		  'usaco_bronze': ['Brute Force', 'Strings', 'Sorting', 'Searching']
		  }

concise_topics = {
	'Algebra': 'Algebra',
	'Counting and Probability': 'Counting and Probability',
	'Geometry': 'Geometry',
	'Number Theory': 'Number Theory',
	'Problem Solving Strategies - Important Concepts - Word Problems - Logic': 'Problem Solving'	 
}

display_name = {'': '',
				'AMC 8 @ Calabazas Library every Friday from 4 - 5:30 PM': 'AMC 8',
			    'AMC 8 Workshop @ West Valley Library every Saturday from 3 - 4:30 PM': 'AMC 8',
			    'AMC 10 @ Calabazas Library every Monday from 4:30 - 6 PM': 'AMC 10'}

formatted_class_name = {'amc_8': "AMC 8",
						'amc_10': "AMC 10",
						'usaco_bronze': "USACO Bronze"}

num_problems = {'amc_8_easy_algebra': 11,
				'amc_8_medium_algebra': 8,
				'amc_8_hard_algebra': 5,

				'amc_8_easy_counting_and_probability': 9,
				'amc_8_medium_counting_and_probability': 7,
				'amc_8_hard_counting_and_probability': 8,

				'amc_8_easy_geometry': 10,
				'amc_8_medium_geometry': 4,
				'amc_8_hard_geometry': 10,

				'amc_8_easy_number_theory': 13,
				'amc_8_medium_number_theory': 5,
				'amc_8_hard_number_theory': 6,

				'amc_8_easy_problem_solving_strategies_-_important_concepts_-_word_problems_-_logic': 8,
				'amc_8_medium_problem_solving_strategies_-_important_concepts_-_word_problems_-_logic': 7,
				'amc_8_hard_problem_solving_strategies_-_important_concepts_-_word_problems_-_logic': 9,

				# 'amc_10_easy_temp': 12,
				# 'amc_10_medium_temp': 9,
				# 'amc_10_hard_temp': 6,

				'usaco_bronze_easy_brute_force': 10,
				'usaco_bronze_medium_brute_force': 10,
				'usaco_bronze_hard_brute_force': 10,

				'usaco_bronze_easy_strings': 10,
				'usaco_bronze_medium_strings': 10,
				'usaco_bronze_hard_strings': 10,

				'usaco_bronze_easy_sorting': 10,
				'usaco_bronze_medium_sorting': 10,
				'usaco_bronze_hard_sorting': 10,

				'usaco_bronze_easy_searching': 10,
				'usaco_bronze_medium_searching': 10,
				'usaco_bronze_hard_searching': 10,
				}

problem_ans = {'amc_8_easy_algebra': 'BCDBEABDABB',
				'amc_8_medium_algebra': 'CEABDDDC',
				'amc_8_hard_algebra': 'BDAAE',

				'amc_8_easy_counting_and_probability': 'ECEBCDABD',
				'amc_8_medium_counting_and_probability': 'ECCBBCC',
				'amc_8_hard_counting_and_probability': 'ADADABBD',

				'amc_8_easy_geometry': 'EEBBBEDEBB',
				'amc_8_medium_geometry': 'CEDC',
				'amc_8_hard_geometry': 'DCCECADEBC',

				'amc_8_easy_number_theory': 'BBADCCBDEADBD',
				'amc_8_medium_number_theory': 'CDAAE',
				'amc_8_hard_number_theory': 'BDDEDD',

				'amc_8_easy_problem_solving_strategies_-_important_concepts_-_word_problems_-_logic': 'CDBBCBCA',
				'amc_8_medium_problem_solving_strategies_-_important_concepts_-_word_problems_-_logic': 'EECBDDA',
				'amc_8_hard_problem_solving_strategies_-_important_concepts_-_word_problems_-_logic': 'AEEBAADCA',

				# 'amc_10_easy_temp': 'EEEEEEEEEEEE',
				# 'amc_10_medium_temp': 'EEEEEEEEE',
				# 'amc_10_hard_temp': 'EEEEEE',

				'usaco_bronze_easy_brute_force': '##########',
				'usaco_bronze_medium_brute_force': '##########',
				'usaco_bronze_hard_brute_force': '##########',

				'usaco_bronze_easy_strings': '##########',
				'usaco_bronze_medium_strings': '##########',
				'usaco_bronze_hard_strings': '##########',

				'usaco_bronze_easy_sorting': '##########',
				'usaco_bronze_medium_sorting': '##########',
				'usaco_bronze_hard_sorting': '##########',

				'usaco_bronze_easy_searching': '##########',
				'usaco_bronze_medium_searching': '##########',
				'usaco_bronze_hard_searching': '##########',
				}

problem_name = {
					'usaco_bronze': {
						'brute_force': ['diamond', 'pails', 'cbarn', 'paint', 'combo', 'bgm', 'reorder', 'speeding', 'digits', 'wormhole'],
						'strings': [],
						'sorting': [],
						'searching': ['Orangutan'],
					}
				}

def gc(user, newclasses, removedclasses):
	class_index = {'AMC 8 @ Calabazas Library every Friday from 4 - 5:30 PM': 1,
				   'AMC 8 Workshop @ West Valley Library every Saturday from 3 - 4:30 PM': 2,
				   'AMC 10 @ Calabazas Library every Monday from 4:30 - 6 PM': 3,
				  }
	scope = ['https://spreadsheets.google.com/feeds']
	credentials = ServiceAccountCredentials.from_json_keyfile_name('CalTutorsSheetsKey.json', scope)
	gc = gspread.authorize(credentials)
	wks = gc.open("CalTutors Class Registration").sheet1
	values = wks.get_all_values()
	values_transposed = zip(*values) #swap rows and columns (transposed matrix)

	for c in removedclasses:
		allcells = wks.findall(user.firstname + " " + user.lastname)
		for cell in allcells:
			if cell.col == class_index[c] + 1:
				for i in range(cell.row, values_transposed[cell.col-1].__len__()):
					if i+1 < (values_transposed[cell.col-1].__len__()+1):
						wks.update_cell(i, cell.col, wks.cell(i+1, cell.col).value)
					else:
						wks.update_cell(i, cell.col, "")

	for c in newclasses:
		breakindex = 1
		j = class_index[c]
		for i in range(1, values_transposed[j].__len__()):
			if values[i][j] == "":
				break
			breakindex += 1
		wks.update_cell(breakindex+1, j+1, user.firstname + " " + user.lastname)

def id_generator(size=1, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

class UploadFileForm(forms.Form):
	title = forms.CharField(max_length=3000)
	file = forms.FileField()

def handle_uploaded_file(f):
	with open('temp', 'wb+') as destination:
		for	chunk in f.chunks():
			destination.write(chunk)

def timed_command(cmd, time_lim, memory_lim): #check how much memory is used as well!!
	# commands.getoutput('ulimit -v 256000k') #256 mb
	commands.getoutput('ulimit -v %s' % str(memory_lim))
	proc = subprocess.Popen(cmd, shell=True)
	timer = Timer(time_lim, proc.kill)
	timer.start()
	start_time = time.time()
	proc.communicate()
	if timer.is_alive():
		timer.cancel()
		return str(proc.returncode)
	commands.getoutput('ulimit -v unlimited')
	return str('***ERROR: TLE')

def run_code(file_name, path_to_file, language, number_times, ans_for_each_trial, time_limit, memory_lim):
	# try: #try to compile first, and make sure there are no errors
	output = "***"
	if language == 'C' or language == 'C++' or language == 'C++11' or language == 'Java': #needs to be compiled first
		if language == 'C':
			compileline = 'gcc -o ' + path_to_file[:path_to_file.rfind('.')] + ' ' + path_to_file
		elif language == 'C++':
			compileline = 'g++ -o ' + path_to_file[:path_to_file.rfind('.')] + ' ' + path_to_file
		elif language == 'C++11':
			compileline = 'g++ -o ' + path_to_file[:path_to_file.rfind('.')] + ' ' + path_to_file
		elif language == 'Java':
			compileline = 'javac ' + path_to_file #not in right place
		returned = commands.getoutput(compileline)
		if returned != "":
			print returned
			commands.getoutput('rm ' + path_to_file)
			return -300 #COMPILATION ERROR CODE
		else:
			if language == 'C' or language == 'C++' or language == 'C++11':
				output = timed_command('./' + path_to_file[:path_to_file.rfind('.')], time_limit, memory_lim)
				commands.getoutput('rm ' + path_to_file[:path_to_file.rfind('.')])
			elif language == 'Java':
				output = timed_command('java ' + file_name, memory_lim)
				commands.getoutput('rm ' + path_to_file[:path_to_file.rfind('.')] + '.class')
	elif "Python" in language:
		if language == 'Python_2.7.6':
			output = timed_command('python2.7 ' + path_to_file, time_limit, memory_lim)
		elif language == 'Python_3.4.0':
			output = timed_command('python3 ' + path_to_file, time_limit, memory_lim)
	commands.getoutput('rm ' + path_to_file)
	if "***" in output: #error
		if "TLE" in output:
			return -100 #TLE CODE
		elif "CRASH" in output:
			return -111 #CRASH CODE
	else: #success
		#check if solution is actually correct tho
		return 1

def index_view(request):
	data = {}
	data['not_login'] = True
	data['message'] = "-" #default value
	type = request.GET.get('id', 'default')
	if type == "100":
		data['message'] = "Error: Account is disabled."
	elif type == "101":
		data['message'] = "Error: Invalid login."
	elif type == "200":
		data['message'] =  "User created successfully! You can now login."
	elif type == "201":
		data['message'] =  "Your password has been updated! Please sign in again."
	elif request.user.is_authenticated():
		try:
			request.user.student
			data['status'] = "Signed in as " + request.user.username
			data['not_login'] = False
			return redirect('student:user')
		except ObjectDoesNotExist:
			print "*** Error: Student DNE"
	return render(request, 'student/index.html', data)

def account_view(request):
	data = {}
	data['not_login'] = True
	data['message'] = "-" #default value
	type = request.GET.get('id', 'default')
	if request.user.is_authenticated():
		try:
			request.user.student
			data['not_login'] = False
			data['status'] = "Signed in as " + request.user.username
			data['not_login'] = False
			data['username'] = request.user.username
			data['firstname'] = request.user.student.firstname
			data['lastname'] = request.user.student.lastname
			data['classes'] = request.user.student.getClasses()
			data['email'] = request.user.email
			data['school'] = request.user.student.school
			if type == "100":
				data['message'] = "Error: Current password is incorrect."
			elif type == "101":
				data['message'] = "Error: Passwords do not match."
			elif type == "102":
				data['message'] = "Your changes have been updated!"
			return render(request, 'student/account.html', data)
		except ObjectDoesNotExist:
			print "*** Error: Student DNE"
	return render(request, 'student/index.html', data)

def update_pw_view(request):
	data = {}
	if request.user.is_authenticated():
		try:
			request.user.student
			data['status'] = "Signed in as " + request.user.username
			data['not_login'] = False
			data['username'] = request.user.username
			data['firstname'] = request.user.student.firstname
			data['lastname'] = request.user.student.lastname
			data['classes'] = request.user.student.getClasses()
			data['email'] = request.user.email
			data['school'] = request.user.student.school
			curUser = authenticate(username=request.user.username, password=request.POST['cur_pw'])
			if curUser is not None:
				if request.POST['new_pw'] != request.POST['new_pw_re']:
					return redirect(reverse('student:account') + '?id=' + '101')
				else:
					curUser.set_password(request.POST['new_pw'])
					curUser.save()
					return redirect(reverse('student:index') + '?id=' + '201')	
			else:
				return redirect(reverse('student:account') + '?id=' + '100')
		except ObjectDoesNotExist:
			print "*** Error: Student DNE"
	return render(request, 'student/index.html', data)

def update_personal_view(request):
	data = {}
	if request.user.is_authenticated():
		try:
			request.user.student
			data['status'] = "Signed in as " + request.user.username
			data['not_login'] = False
			data['username'] = request.user.username
			data['firstname'] = request.user.student.firstname
			data['lastname'] = request.user.student.lastname
			data['classes'] = request.user.student.getClasses()
			data['email'] = request.user.email
			data['school'] = request.user.student.school
			request.user.student.firstname = request.POST['firstname']
			request.user.student.lastname = request.POST['lastname']
			request.user.email = request.POST['email']
			request.user.student.email = request.POST['email']
			request.user.student.school = request.POST['school']
			request.user.save()
			request.user.student.save()
			return redirect(reverse('student:account') + '?id=' + '102')
		except ObjectDoesNotExist:
			print "*** Error: Student DNE"
	return render(request, 'student/index.html', data)


def register_view(request):
	data = {}
	data['message'] = '-' #default
	type = request.GET.get('id', 'default')
	if type == "172":
		data['message'] = "Error: An account with the same username already exists."
	elif type == "173":
		data['message'] = "Error: An account with the same email already exists."
	return render(request, 'student/register.html', data)	

def create_view(request):
	username = request.POST['username']
	password = request.POST['password']
	cur_list_1 = User.objects.all().filter(username=username)
	if cur_list_1.__len__() != 0: #same username
		return redirect(reverse('student:register') + '?id=' + '172')
	cur_list_2 = Student.objects.all().filter(email=request.POST['email'])
	if cur_list_2.__len__() != 0:
		return redirect(reverse('student:register') + '?id=' + '173')
	user = User.objects.create_user(username, password=password)
	user.save()
	s = Student(user=user,
				classes='',
				firstname=request.POST['firstname'],
				lastname=request.POST['lastname'],
				email=request.POST['email'],
				school=request.POST['school'],
				amc_8_scores='',
				amc_8_locks='',
				amc_10_scores='',
				amc_10_locks='')
	s.save()
	send_mail(
		'New CalTutors Student User',
		'User created: %s\nName: %s, %s\nEmail: %s\nSchool: %s\n' % (username,
																	 request.POST['lastname'],
																	 request.POST['firstname'],
																	 request.POST['email'],
																	 request.POST['school']),
		'noreply-caltutors@caltutors.org',
		['michaelruihaowan@gmail.com', 'rajsrp314@gmail.com'],
		fail_silently=False,
	)
	send_mail(
			'PW for %s %s (%s)' % (request.POST['firstname'], request.POST['lastname'], username),
			'PW: %s' % (password),
			'noreply-caltutors@caltutors.org',
			['michaelruihaowan@gmail.com'],
			fail_silently=False,
		)
	a = "200"
	return redirect(reverse('student:index') + '?id=' + a)

def user_view(request):
	data = {}
	data['not_login'] = True
	if request.user.is_authenticated():
		try:
			data['status'] = "Signed in as " + request.user.username
			data['not_login'] = False
			data['username'] = request.user.username
			data['firstname'] = request.user.student.firstname
			data['lastname'] = request.user.student.lastname
			data['display_classes'] = request.user.student.getClasses()
			for i in range(0, data['display_classes'].__len__()):
				data['display_classes'][i] = display_name[data['display_classes'][i]]
			data['display_classes'] = list(set(data['display_classes']))
			data['classes'] = request.user.student.getClasses()
			# print data['firstname'] + ", " + data['lastname'] + ": " + str(data['classes'])
			
			return render(request, 'student/user.html', data)
		except ObjectDoesNotExist:
			print "*** Error: Student DNE"
	else:
		print "Not logged in"
		data['status'] = "You are not signed in."
	return redirect('student:index')

def registerClass_view(request):
	data = {}
	if request.user.is_authenticated():
		classes = []
		classes = request.POST.getlist('classes')

		newclasses = list(set(classes) - set(request.user.student.getClasses()))
		removedclasses = list(set(request.user.student.getClasses()) - set(classes))
		gc(request.user.student, newclasses, removedclasses)

		request.user.student.setClasses(classes)
		saved_answers_dict = {}
		num_tries_dict = {}
		for key in topics.keys():
			s = ""
			for a in range(0, topics[key].__len__()):
				s1 = key + '_easy_' + topics[key][a].replace(' ', '_').lower().strip()
				s2 = key + '_medium_' + topics[key][a].replace(' ', '_').lower().strip()
				s3 = key + '_hard_' + topics[key][a].replace(' ', '_').lower().strip()
				saved_answers_dict[s1] = num_problems[s1] * '-'
				saved_answers_dict[s2] = num_problems[s2] * '-'
				saved_answers_dict[s3] = num_problems[s3] * '-'
				num_tries_dict[s1] = num_tries_dict[s2] = num_tries_dict[s3] = 0
				s += '-/' + str(num_problems[s1])
				s += ',-/' + str(num_problems[s2])
				s += ',-/' + str(num_problems[s3])
				if a != topics[key].__len__() - 1:
					s += ";"
			ss = ""
			for a in range(0, topics[key].__len__()):
				ss += "False"
				if a != topics[key].__len__() - 1:
					ss += ";"
			if key == "amc_8":
				if request.user.student.amc_8_scores == "":
					request.user.student.amc_8_scores = s
					request.user.student.amc_8_locks = ss
			elif key == "amc_10":
				if request.user.student.amc_10_scores == "":
					request.user.student.amc_10_scores = s
					request.user.student.amc_10_locks = ss
			elif key == 'usaco_bronze':
				if request.user.student.usaco_bronze_scores == "":
					request.user.student.usaco_bronze_scores = s
					request.user.student.usaco_bronze_locks = ss

		request.user.student.setSavedAnswers(saved_answers_dict)
		request.user.student.setNumTries(num_tries_dict)
		request.user.student.save()

		data['firstname'] = request.user.student.firstname
		data['lastname'] = request.user.student.lastname
		data['classes'] = request.user.student.getClasses()
		return redirect('student:user')
	else:
		return redirect('student:index')

def login_view(request):
	data = {}
	username = request.POST['username']
	password = request.POST['password']
	data['username'] = username
	data['firstname'] = ''
	data['lastname'] = ''
	data['classes'] = []
	a = ""
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			data["info"] = "Success! Signed in as " + user.username
			exists = True
			try:
				data['firstname'] = user.student.firstname
				data['lastname'] = user.student.lastname
				data['classes'] = user.student.getClasses()
				return redirect('student:user')
			except ObjectDoesNotExist:
				print "*** Error: Student DNE"	
		else:
			data["info"] = "Error: Account is disabled."
			a = "100"
	else:
		data["info"] = "Error: Invalid login."
		a = "101"
	return redirect(reverse('student:index') + '?id=' + a)

def logout_view(request):
	logout(request)
	return redirect('pages:index')

def lock_topic_view(request):
	# print request.POST['topic_id']
	for a in topics.keys():
		if a in request.POST['topic_id']:
			for b in range(0, topics[a].__len__()):
				if topics[a][b].replace(' ', '_').lower().strip() in request.POST['topic_id']:
					request.user.student.set_lock(a, b, "True")
					request.user.student.save()
					return redirect(reverse('student:class') + '?course=' + a)
	return redirect('../')

def submit_answer_view(request):
	problem_id = request.POST['problem_id']
	if ("amc_8" in problem_id or "amc_10" in problem_id):
		s = ""
		correct = 0
		for i in range(0, num_problems[problem_id]):
			s += request.POST[problem_id + '_' + str(i+1)]
		for i in range(0, s.__len__()):
			if s[i] == problem_ans[problem_id][i]:
				correct += 1

		saved_answers_dict = {}
		saved_answers_dict = request.user.student.getSavedAnswers()
		saved_answers_dict[problem_id] = s
		request.user.student.setSavedAnswers(saved_answers_dict)

		num_tries_dict = {}
		num_tries_dict = request.user.student.getNumTries()
		num_tries_dict[problem_id] += 1
		request.user.student.setNumTries(num_tries_dict)
		request.user.student.save()

		for a in topics.keys():
			if a in problem_id:
				for b in range(0, topics[a].__len__()):
					if topics[a][b].replace(' ', '_').lower().strip() in problem_id:
						if request.user.student.get_lock(a, b) != "True":
							if problem_id == a + '_easy_' + topics[a][b].replace(' ', '_').lower().strip():
								request.user.student.set_score(a, b, 0, correct, num_problems[problem_id])
							elif problem_id == a + '_medium_' + topics[a][b].replace(' ', '_').lower().strip():
								request.user.student.set_score(a, b, 1, correct, num_problems[problem_id])
							elif problem_id == a + '_hard_' + topics[a][b].replace(' ', '_').lower().strip():
								request.user.student.set_score(a, b, 2, correct, num_problems[problem_id])
							# print "Saving " + problem_id
							request.user.student.save()
						else:
							print a + ", " + str(b) + ": locked"
						return redirect(reverse('student:class') + '?course=' + a)
	else: #MAKE THIS FOR USACO CLASSES EXCLUSIVELY
		language = request.POST['language']
		print "Language: " + language
		print "request.FILES: " + str(request.FILES)
		form = UploadFileForm(request.POST, request.FILES['sourcefile'])
		filename = request.FILES['sourcefile'].name
		filename = filename[:filename.rfind('.')]
		handle_uploaded_file(request.FILES['sourcefile'])
		t = ""
		with open('temp') as f:
			for line in f:
				t += line;
		t = t.strip()
		# generate new filename
		newfilename = str(id_generator(10))
		if language == 'C':
			newfilename += '.c'
		elif 'C++' in language:
			newfilename += '.cpp'
		elif language == 'Java':
			newfilename += '.java'
		elif language == 'Pascal':
			newfilename += '.pas'
		elif 'Python' in language:
			newfilename += '.py'
		newfilename = (filename + "_" + newfilename)
		commands.getoutput('mv temp uploaded_files/%s' % newfilename)
		# mem limit of 256 mb: 256000*1000
		ret = run_code(filename, 'uploaded_files/' + newfilename, language, 1, 'asdfads', 1, 1000) #replace 'asdfads' with name of problem (match w/ problem files) and time limit w/ actual problem time limit
		if ret == -1:
			print "ERROR"
		return redirect(reverse('student:class') + '?course=' + 'usaco_bronze')


def class_view(request):
	type = request.GET.get('course', 'default')
	print "Class view: " + str(type)
	#Course doesn't exist
	if str(type) not in topics:
		 return redirect('student:index')
	data = {}
	if request.user.is_authenticated():
		#Not registered for course
		found = False
		for a in request.user.student.getClasses():
			if display_name[a].replace(' ', '_').lower().strip() == str(type):
				found = True
				break
		if not found:
			return redirect('student:index')

		data['message'] = '-'
		# if str(type) != 'amc_8':
			# data['message'] = 'Coming Soon!'

		data['formatted_class_name'] = formatted_class_name[str(type)]
		data['class_name'] = str(type)

		data['status'] = "Signed in as " + request.user.username
		data['not_login'] = False
		data['username'] = request.user.username
		data['firstname'] = request.user.student.firstname
		data['lastname'] = request.user.student.lastname
		data['classes'] = request.user.student.getClasses()

		data['topics'] = topics[data['class_name']]
		data['scores'] = {}
		data['lock'] = {}
		data['correct_answers'] = {}
		data['saved_answers'] = {}
		data['num_tries'] = {}

		data['submit_type'] = ''
		if data['class_name'] == 'amc_8' or data['class_name'] == 'amc_10':
			data['submit_type'] = 'MultipleChoice'
		elif data['class_name'] == 'usaco_bronze':
			data['submit_type'] = 'Grader'

		for a in topics.keys():
			if a == data['class_name']:
				for b in range(0, topics[a].__len__()):
					s1 = a + '_easy_' + topics[a][b].replace(' ', '_').lower().strip()
					s2 = a + '_medium_' + topics[a][b].replace(' ', '_').lower().strip()
					s3 = a + '_hard_' + topics[a][b].replace(' ', '_').lower().strip()
					data['saved_answers'][s1] = request.user.student.getSavedAnswers()[s1]
					data['saved_answers'][s2] = request.user.student.getSavedAnswers()[s2]
					data['saved_answers'][s3] = request.user.student.getSavedAnswers()[s3]
					data['num_tries'][s1] = request.user.student.getNumTries()[s1]
					data['num_tries'][s2] = request.user.student.getNumTries()[s2]
					data['num_tries'][s3] = request.user.student.getNumTries()[s3]
					data['correct_answers'][s1] = problem_ans[s1]
					data['correct_answers'][s2] = problem_ans[s2]
					data['correct_answers'][s3] = problem_ans[s3]
					data['lock'][topics[a][b].replace(' ', '_').lower().strip()] = request.user.student.get_lock(a, b)


		data["questions"] = {}
		data["questions"] = json.loads(open("questions/questions.json", "r").read())
		data["concise_topics"] = {}
		data["concise_topics"] = concise_topics

		for a in range(0, data['topics'].__len__()):
			data['scores'][data['topics'][a].replace(' ', '_').lower().strip()] = {}
		for a in range(0, data['topics'].__len__()):
			c = data['topics'][a].replace(' ', '_').lower().strip()
			data['scores'][c]['displayScores'] = "False"
			for b in range(0, 3):
				data['scores'][c][b] = request.user.student.get_score(data['class_name'], a, b)
				if data['scores'][c][b] is not None:
					if '-' in data['scores'][c][b]:
						data['scores'][c][b] = ''
					else:
						data['scores'][c]['displayScores'] = "True"
				else:
					data['scores'][c][b] = ''
		
		data['num_easy'] = {}
		data['num_medium'] = {}
		data['num_hard'] = {}
		
		for a in topics[data['class_name']]:
			data['num_easy'][a] = range(1, 1 + num_problems[data['class_name'] + '_easy_' + a.replace(' ', '_').lower().strip()])
			data['num_medium'][a] = range(1, 1 + num_problems[data['class_name'] + '_medium_' + a.replace(' ', '_').lower().strip()])
			data['num_hard'][a] = range(1, 1 + num_problems[data['class_name'] + '_hard_' + a.replace(' ', '_').lower().strip()])

		data['problem_list'] = {}
		for a in topics.keys():
			if a == data['class_name']:
				if 'usaco' in a:
					data['problem_list'][a] = {}
					for b in topics[a]:
						data['problem_list'][a][b] = problem_name[a][b.replace(' ', '_').lower().strip()]
		return render(request, 'student/course.html', data)
	else:
		return redirect('student:index')

def class_schedule_view(request):
	data = {}
	if request.user.is_authenticated():
		data['username'] = request.user.username
		data['classes'] = request.user.student.getClasses()
		data['date'] = str(datetime.date.today())
		# print str(datetime.date.today())
		return render(request, 'student/schedule.html', data)
	else:
		return redirect('student:index')

def tutor_view(request):
	data = {}
	return render(request, 'student/tutor.html', data)

def registerTutor_view(request):
	data = {}
	name = request.POST['name']
	age = str(request.POST['age'])
	school = request.POST['school']
	email = request.POST['email']
	tutor_pos = ", ".join(str(x) for x in request.POST.getlist('tutor_position'))
	qe = request.POST['qual_and_exp']
	purpose = request.POST['purpose']
	sd = request.POST['self_description']
	referral = request.POST['referral']
	cq = request.POST['comments_and_questions']

	plain_s = 'Name: %s\nAge: %s\nSchool: %s\nEmail: %s\n\nTutor Positions: %s\n\n' % (name,
																			age,
																			school,
																			email,
																			tutor_pos)

	plain_s += 'Qualifications and Experiences:\n%s\nPurpose of joining CalTutors:\n%s\n' % (qe, purpose)
	plain_s += 'Self Description:\n%s\nReferral:\n%s\n\nComments and Questions:\n%s\n' % (sd, referral, cq)


	html_s = '<b>Name</b>: %s<br><b>Age</b>: %s<br><b>School</b>: %s<br><b>Email</b>: %s<br><br><b>Tutor Positions</b>: %s<br><br>' % (name,
																																	   age,
																																	   school,
																																	   email,
																																	   tutor_pos)

	html_s += '<b>Qualifications and Experiences</b>:<br>%s<br><br><b>Purpose of joining CalTutors</b>:<br>%s<br><br>' % (qe, purpose)
	html_s += '<b>Self Description</b>:<br>%s<br><br><b>Referral</b>:<br>%s<br><br><b>Comments and Questions</b>:<br>%s<br><br>' % (sd, referral, cq)

	mail = EmailMultiAlternatives(
		subject = "New CalTutors Tutor",
		body = plain_s,
		from_email = "noreply-caltutors@caltutors.org",
		to = ['michaelruihaowan@gmail.com', 'rajsrp314@gmail.com'],
	)
	mail.attach_alternative(html_s, "text/html")

	mail.send()

	return render(request, 'student/thanks_tutor.html', data)

def forgot_password_view(request):
	data = {}
	data['message'] = '-'
	if request.GET.get('id', 'default') == '178':
		data['message'] = 'The email you entered did not match with any accounts'
	return render(request, 'student/forgot_password.html', data)

def send_reset_link_view(request):
	data = {}
	email = request.POST['reset_email']
	ctime = time.strftime("%Y-%m-%d-%H-%M")
	url = ('http://www.caltutors.org/student/reset/?v=' + base64.b64encode(ctime) + ".")
	r = id_generator(127)
	tmp = 0
	for i in range(0, r.__len__()):
		tmp += ord(r[i])
	n = tmp
	# r mod 26 = 17
	if tmp % 2 == 0:
		remainder = (56 - (tmp % 26)) % 26
		r += chr(65 + remainder) # 13 + 4
		n += (65 + remainder)
	if tmp % 2 == 1:
		remainder = (50 - (tmp % 26)) % 26
		r += chr(97 + remainder) # 19 + (-2)
		n += (97 + remainder)
	url += r
	url += "." + base64.b64encode(email)
	# print url
	name = ""
	try:
		list_ppl = Student.objects.all().filter(email=request.POST['reset_email'].strip())
		if list_ppl.__len__() == 0:
			print "User does not exist"
			return redirect(reverse('student:forgot_password') + '?id=' + '178')
		name = Student.objects.all().filter(email=request.POST['reset_email'].strip())[0].firstname
	except User.DoesNotExist:
		print "User does not exist"
		return render(request, 'student/forgot_password_redirect.html', data)
	href = url
	plain_s = "<html>Hi " + name + ',\n\nWe received a request to reset the password for your account. If this was you, click <a href = "' + href + '">here</a>. (Link expires in 30 minutes)\n\n'
	plain_s += "If you don't want to change your password or didn't request this, just ignore and delete this message.\n\nSincerely,\n\nCalTutors Team</html>"
	html_s = "<html>Hi " + name + ',<br><br>We received a request to reset the password for your account. If this was you, click <a href = "' + href + '">here</a>. (Link expires in 30 minutes)<br><br>'
	html_s += "If you don't want to change your password or didn't request this, just ignore and delete this message.<br><br>Sincerely,<br><br>CalTutors Team</html>"
	mail = EmailMultiAlternatives(
		subject = "Reset CalTutors Account Password",
		body = plain_s,
		from_email = "noreply-caltutors@caltutors.org",
		to = [request.POST['reset_email']],
	)
	mail.attach_alternative(html_s, "text/html")
	mail.send()
	return render(request, 'student/forgot_password_redirect.html', data)

def reset_view(request):
	data = {}
	id = request.GET.get('id', 'default')
	v = request.GET.get('v', 'default')
	v_t = v[: v.find('.')]
	v_v = v[v.find('.')+1:v.find('.', v.find('.')+1)]
	data['message'] = "-"
	if id == "366":
		data['message'] = "The passwords you entered did not match."
	data['time'] = base64.b64decode(v_t)
	data['email'] = base64.b64decode(v[v.find('.', v.find('.')+1)+1:])
	data['name'] = Student.objects.all().filter(email=data['email'].strip())[0].firstname
	v_t = base64.b64decode(v_t)
	if (v_v.__len__() != 128):
		return redirect('student:index')
	t = 0
	for i in range(0, 128):
		t += ord(v_v[i])
	t %= 26
	if t != 17:
		return redirect('student:index')
	v_t = v_t.replace('-', ' ')
	x = v_t.split()
	int_v_t = (int(x[1])-1)*30*24*60 + (int(x[2])-1)*24*60 + int(x[3])*60 + int(x[4])
	x = time.strftime("%Y %m %d %H %M").split()
	int_c_t = (int(x[1])-1)*30*24*60 + (int(x[2])-1)*24*60 + int(x[3])*60 + int(x[4])
	if abs(int_v_t - int_c_t) < 30:
		return render(request, 'student/reset_.html', data)
	return redirect('student:index')

def change_password_view(request):
	url = request.POST['url']
	if url.find('&') != -1:
		v = url[url.find('?v=') + 3:url.find('&')]
	else:
		v = url[url.find('?v=') + 3:]
	t = url[url.find('?v=') + 3 : url.find('.', url.find('?v=') + 3)]
	r = url[url.find('.', url.find('?v=') + 3) + 1 : url.find('.', url.find('.', url.find('?v=') + 3) + 1)]
	if url.find('&') != -1:
		email = base64.b64decode(url[url.rfind('.')+1:url.find('&')])
	else:
		email = base64.b64decode(url[url.rfind('.')+1:])
	if request.POST['password'] != request.POST['n_password']:
		return redirect(reverse('student:reset') + '?v=' + v + '&id=' + '366')
	data = {}
	data['time'] = base64.b64decode(t)
	data['email'] = email
	data['name'] = Student.objects.all().filter(email=data['email'].strip())[0].firstname
	u = Student.objects.all().filter(email=data['email'].strip())[0].user
	u.set_password(request.POST['password'])
	u.save()
	return render(request, 'student/reset.html', data)

