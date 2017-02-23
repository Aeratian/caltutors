from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from student.models import Student

from django.core.urlresolvers import reverse

from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

import base64, datetime, random, string, time

team_member_id = ['neil', 'michael', 'victor', 'andrew', 'raj', 'bryan',
				  'steven', 'michelle', 'aaron_lopes', 'anirudh_balasubramaniam',
				  'aditya_garg', 'amithab_arumugam', 'sriman_manyam']

team_member_names = {'neil': 'Neil Palleti',
					 'michael': 'Michael Wan',
					 'victor': 'Victor Yin',
					 'andrew': 'Andrew Yeh',
					 'raj': 'Raj Palleti',
					 'bryan': 'Bryan Chen',
					 'steven': 'Steven Liu',
					 'michelle': 'Michelle Kwan',
					 'aaron_lopes': 'Aaron Lopes',
					 'anirudh_balasubramaniam': 'Anirudh Balasubramaniam',
					 'aditya_garg': 'Aditya Garg',
					 'amithab_arumugam': 'Amithab Arumugam',
					 'sriman_manyam': 'Sriman Manyam'
					 }

team_member_title = {'neil': 'Founder & President',
					 'michael': 'Founder & VP',
					 'victor': 'Founder',
					 'andrew': 'Math Tutor',
					 'raj': 'Director of Operations',
					 'aaron_lopes': 'Director of Marketing',
					 'bryan': 'Math & CS Tutor',
					 'steven': 'Chem Tutor',
					 'michelle': 'Math & CS Tutor',
					 'anirudh_balasubramaniam': 'Math Tutor',
					 'aditya_garg': 'Math & CS Tutor',
					 'amithab_arumugam': 'Math Tutor',
					 'sriman_manyam': 'Math & Chem Tutor'
					 }

team_member_description = {'neil': 'Neil is an avid programmer who focuses on a variety of algorithms mainly in Java. He is an officer of ' + 
								   'the Monta Vista Computer Science Club and is in the Gold Division of the online programming contest, USACO' + 
								   '. He is also involved in many physics and math competitions. His hobbies include playing tennis, watching ' + 
								   'Indian movies, and hanging out with friends.',

						   'michael': 'Michael has a strong passion for computer science and mathematics. A competitor in USACO Platinum, Michael' + 
						   			  'spends a lot of his time delving into algorithms and coding. As a result, he is fluent in a multitude of' +
						   			  'languages ranging from C++ to R. He also enjoys mathematics and competes in numerous math competitions. ' + 
						   			  'In his free time, Michael loves to play tennis. He often travels for national tournaments, often out of the state!',

						   'victor': 'Victor is an assiduous programmer. He can code in multiple languages, and excels in Java. Currently, he is in ' + 
						   			 'the Gold Division of the online programming contest, USACO. Victor also passionately studies physics and mathematics. ' + 
						   			 'In his free time, Victor enjoys discovering electronic music, playing volleyball, playing competitive piano, or learning ' + 
						   			 'new instruments and languages.',

						   'andrew': 'Andrew enjoys math and has a penchant for thinking outside of the box. He has won multiple awards and has ' + 
						   			 'qualified for the USA Junior Mathematical Olympiad. Besides math, Andrew has an affinity for computer science ' + 
						   			 'and physics. During his free time, he likes to watch movies, hangout with friends, or play badminton.',

						   'raj': 'Raj is an avid computer programmer who participated in competitions such as AMC 8 and USACO. He plays tennis ' + 
						   		  'competitively on the weekends, and also plays on his school team. In his free time, he enjoys coding, playing ' + 
						   		  'video games, and watching movies.',

						   'bryan': 'Bryan enjoys competitive computer programming and mathematics. He is fluent in C++ and Java, and is in the ' + 
						   			'Platinum division of USACO. He was also invited to attend the Finalist Summer Camp of 2014 & 2016 as one of ' + 
						   			'the top 24 high school competitive coders in the United States of America. Bryan has experience with teaching ' + 
						   			'as he has taught as the instructor of multiple computer science camps. In his free time, he likes to watch ' + 
						   			'television and play badminton and Super Smash Bros. Melee.',

						   'steven': 'Steven has a passion for chemistry. His current goal is to pass the Chemistry Olympiad local exam and become ' + 
						   			 'one of the top twenty high school chemists in the nation. While he has a fondness for chemistry, Steven is ' + 
						   			 'also proficient in calculus and music. During his free time, he likes to immerse himself in Korean culture, ' + 
						   			 'compose music, or play badminton.',

						   'michelle': 'Coming soon!',

						   'aaron_lopes': 'Aaron is mathematics and programming enthusiast, his self-taught skills winning him awards at a variety of ' +
						   				  'hackathons, his most recent being at MenloHacks. His passion for both of the subjects has lead him to pursue ' +
						   				  'freelance web development, as well as participating in a multitude of math competitions. On his free time, ' + 
						   				  'Aaron enjoys long distance running, playing video games, and hanging out with his friends.',

						   'anirudh_balasubramaniam': 'Anirudh Balasubramaniam is an avid programmer and enjoys mathematics. He has taken several ' + 
						   							  'difficult mathematic courses through school and self study. In addition, he knows multiple ' + 
						   							  'programming languages including Java and Python and has won a few hackathons. In his free ' + 
						   							  'time, he likes to play tennis, watch basketball, and watch movies!',

						   'aditya_garg': 'Aditya Garg is a keen programmer who loves to make games and applications. He also loves doing math ' + 
						   				  'problems and has done well on the AMC 10. In addition to Java, he also knows how to program in Ruby ' + 
						   				  'and Python. In his free time, he enjoys playing video games, volunteering, playing basketball, and ' + 
						   				  'watching action movies.',

						   	'amithab_arumugam': 'Amithab Arumugam is a senior at Monta Vista. He loves reading and spends his free time coding. ' + 
						   						'He has tried out many languages and hopes to continue to improve himself in the field. ' + 
						   						'He plays tennis and ultimate frisbee regularly. He loves math, science, and computer science, ' + 
						   						'hoping to take his knowledge of these subjects wherever he goes.',

						   	'sriman_manyam': 'Sriman is a mathematics and chemistry enthusiast. He has participated in AMC 8 and countless math ' +
						   					 'olympiad contests. His interest in mathematics led to him winning a few of these contests.'
						   }

def index_view(request):
	data = {}
	data['login'] = "0"
	data['message'] = "-" #default value
	# type = request.GET.get('id', 'default')
	# if type == "1":
	# 	data['message'] = "Your password has been updated! Please sign in again"
	if request.user.is_authenticated():
		try:
			request.user.student
			data['login'] = "1"
		except ObjectDoesNotExist:
			print "*** Error: Student DNE"
	return render(request, 'pages/index.html', data)

def team_view(request):
	data = {}
	data['login'] = "0"
	data['message'] = "-" #default value
	if request.user.is_authenticated():
		try:
			request.user.student
			data['login'] = "1"
		except ObjectDoesNotExist:
			print "*** Error: Student DNE"
	return render(request, 'pages/team.html', data)

def team_member_view(request):
	data = {}
	data['login'] = "0"
	data['message'] = "-" #default value
	type = request.GET.get('name', 'default')
	if type in team_member_id:
		if request.user.is_authenticated():
			try:
				request.user.student
				data['login'] = "1"
			except ObjectDoesNotExist:
				print "*** Error: Student DNE"
		data['name'] = team_member_names[type]
		data['picture'] = type
		data['title'] = team_member_title[type]
		data['text'] = team_member_description[type]
		return render(request, 'pages/team_member.html', data)
	else:
		return redirect('pages:team')

def classes_view(request):
	data = {}
	data['login'] = "0"
	data['message'] = "-" #default value
	if request.user.is_authenticated():
		try:
			request.user.student
			data['login'] = "1"
		except ObjectDoesNotExist:
			print "*** Error: Student DNE"
	return render(request, 'pages/classes.html', data)

def tutors_view(request):
	data = {}
	data['login'] = "0"
	data['message'] = "-" #default value
	if request.user.is_authenticated():
		try:
			request.user.student
			data['login'] = "1"
		except ObjectDoesNotExist:
			print "*** Error: Student DNE"
	return render(request, 'pages/tutors.html', data)

def photo_view(request):
	data = {}
	data['login'] = "0"
	data['message'] = "-" #default value
	if request.user.is_authenticated():
		try:
			request.user.student
			data['login'] = "1"
		except ObjectDoesNotExist:
			print "*** Error: Student DNE"
	return render(request, 'pages/photo.html', data)

def contact_view(request):
	data = {}
	data['login'] = "0"
	data['message'] = "-" #default value
	if request.user.is_authenticated():
		try:
			request.user.student
			data['login'] = "1"
		except ObjectDoesNotExist:
			print "*** Error: Student DNE"
	return render(request, 'pages/contact.html', data)

def contact_submit_view(request):
	data = {}
	return render(request, 'pages/thanks.html', data)