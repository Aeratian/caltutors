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
				  'aditya_garg', 'amithab_arumugam', 'sriman_manyam', 'kevin_tan',
				  'michael_wu', 'william_zhang', 'tom_zhang', 'tae_kyu',
				  'saumya_tawakley', 'parth_asawa', 'maya_abiram', 'brandon_guo']

team_member_names = {
	'neil': 'Neil Palleti',
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
	'sriman_manyam': 'Sriman Manyam',
	'kevin_tan': 'Kevin Tan',
	'michael_wu': 'Michael Wu',
	'william_zhang': 'William Zhang',
	'tom_zhang': 'Tom Zhang',
	'tae_kyu_kim': 'Tae Kyu Kim',
	'saumya_tawakley': 'Saumya Tawakley',
	'parth_asawa': 'Parth Asawa',
	'maya_abiram': 'Maya Abiram',
	'brandon_guo': 'Brandon Guo'
}

team_member_title = {
	'neil': 'Founder',
	'michael': 'Founder & President',
	'victor': 'Founder',
	'andrew': 'Math Tutor',
	'raj': 'Vice President',
	'aaron_lopes': 'Director of Marketing',
	'bryan': 'Math & CS Tutor',
	'steven': 'Chem Tutor',
	'michelle': 'Math & CS Tutor',
	'anirudh_balasubramaniam': 'Math Tutor',
	'aditya_garg': 'Math & CS Tutor',
	'amithab_arumugam': 'Math Tutor',
	'sriman_manyam': 'Math & Chem Tutor',
	'kevin_tan': 'Private Tutor',
	'michael_wu': 'Private Tutor',
	'william_zhang': 'Math Tutor',
	'tom_zhang': 'Math & CS Tutor',
	'tae_kyu_kim': 'Math & CS Tutor',
	'saumya_tawakley': 'Math & CS Tutor',
	'parth_asawa': 'Math Tutor',
	'maya_abiram': 'Math & CS Tutor',
	'brandon_guo': 'Math Tutor',
}

team_member_description = {
	'neil': 'Neil is an avid programmer who focuses on a variety of algorithms mainly in Java. He is an officer of the Monta Vista Computer Science Club and is in the Gold Division of the online programming contest, USACO. He is also involved in many physics and math competitions. His hobbies include playing tennis, watching Indian movies, and hanging out with friends.',
	'michael': 'Michael has a strong passion for computer science and mathematics. A competitor in USACO Platinum, Michael spends a lot of his time delving into algorithms and coding. As a result, he is fluent in a multitude oflanguages ranging from C++ to R. He also enjoys mathematics and competes in numerous math competitions.  In his free time, Michael loves to play tennis. He often travels for national tournaments, often out of the state!',
	'victor': 'Victor is an assiduous programmer. He can code in multiple languages, and excels in Java. Currently, he is in the Gold Division of the online programming contest, USACO. Victor also passionately studies physics and mathematics. In his free time, Victor enjoys discovering electronic music, playing volleyball, playing competitive piano, or learning new instruments and languages.',
	'andrew': 'Andrew enjoys math and has a penchant for thinking outside of the box. He has won multiple awards and has qualified for the USA Junior Mathematical Olympiad. Besides math, Andrew has an affinity for computer science and physics. During his free time, he likes to watch movies, hangout with friends, or play badminton.',
	'raj': 'Raj is an avid computer programmer who participated in competitions such as AMC 8 and USACO. He plays tennis competitively on the weekends, and also plays on his school team. In his free time, he enjoys coding, playing video games, and watching movies.',
	'bryan': 'Bryan enjoys competitive computer programming and mathematics. He is fluent in C++ and Java, and is in the Platinum division of USACO. He was also invited to attend the Finalist Summer Camp of 2014 & 2016 as one of the top 24 high school competitive coders in the United States of America. Bryan has experience with teaching as he has taught as the instructor of multiple computer science camps. In his free time, he likes to watch television and play badminton and Super Smash Bros. Melee.',
	'steven': 'Steven has a passion for chemistry. His current goal is to pass the Chemistry Olympiad local exam and become one of the top twenty high school chemists in the nation. While he has a fondness for chemistry, Steven is also proficient in calculus and music. During his free time, he likes to immerse himself in Korean culture, compose music, or play badminton.',
	'michelle': 'Coming soon!',
	'aaron_lopes': 'Aaron is mathematics and programming enthusiast, his self-taught skills winning him awards at a variety of hackathons, his most recent being at MenloHacks. His passion for both of the subjects has lead him to pursue freelance web development, as well as participating in a multitude of math competitions. On his free time,  Aaron enjoys long distance running, playing video games, and hanging out with his friends.',
	'anirudh_balasubramaniam': 'Anirudh Balasubramaniam is an avid programmer and enjoys mathematics. He has taken several difficult mathematic courses through school and self study. In addition, he knows multiple programming languages including Java and Python and has won a few hackathons. In his free time, he likes to play tennis, watch basketball, and watch movies!',
	'aditya_garg': 'Aditya Garg is a keen programmer who loves to make games and applications. He also loves doing math problems and has done well on the AMC 10. In addition to Java, he also knows how to program in Ruby and Python. In his free time, he enjoys playing video games, volunteering, playing basketball, and watching action movies.',
	'amithab_arumugam': 'Amithab Arumugam is a senior at Monta Vista. He loves reading and spends his free time coding. He has tried out many languages and hopes to continue to improve himself in the field. He plays tennis and ultimate frisbee regularly. He loves math, science, and computer science, hoping to take his knowledge of these subjects wherever he goes.',
	'sriman_manyam': 'Sriman is a mathematics and chemistry enthusiast. He has participated in AMC 8 and countless math olympiad contests. His interest in mathematics led to him winning a few of these contests.',
	'kevin_tan': '[Coming soon!]',
	'michael_wu': '[Coming soon!]',
	'william_zhang': 'William is active in competitive mathematics and coding. He is fluent in Java, C++, and Python and is also in the Gold division of the online programming contest USACO. He is a three time AIME qualifier and scored a 144 on the 2017 AMC 10B. He has experience teaching as a Kennedy Middle School Mathcounts coach, and has previously represented Kennedy in the competition itself.  He enjoys watching TV shows and running in his free time.',
	'tom_zhang': 'Tom is an avid programmer who is in the Gold division of the USACO contest. In addition to algorithmic coding, Tom participates in hackathons, most recently winning second place at Firebird Hacks. He spends the rest of his time playing baseball for his high school team, participating in school clubs like Debate, and playing video games.',
	'tae_kyu_kim': 'Tae Kyu Kim is a freshman at Monta Vista High School. He has participated in the AMC competitions since middle school, perfecting the AMC 8 and qualifying for AIME in eighth grade. In addition, he studies C++ and is in the Gold division for USACO. In his free time, he enjoys playing rhythm games and the cello.',
	'saumya_tawakley': 'Saumya has a strong passion for science and has participated in many science olympiad competitions. She enjoys computer science and has also become a writer in her school’s science and technology magazine. Her hobbies include hanging out with friends and volunteering at various events around the city.',
	'parth_asawa': 'Parth is an avid mathlete who is a freshman at Monta Vista. In particular, he enjoys working on geometry problems and has qualified for the American Invitational Mathematics Examination as well as scoring a perfect score on the AMC 8. During his free time, he enjoys playing the piano and working on physics problems.',
	'maya_abiram': 'Maya is passionate about mathematics and computer science. She is a past AIME Qualifier and has participated in numerous math competitions. One of her goals is to conduct mathematics based research. While she in deeply interested in STEM, she also enjoys Model United Nations, playing tennis, watching Netflix, and loves music.',
	'brandon_guo': 'Brandon enjoys both learning and teaching math. He has qualified for late rounds in both the Berkeley and MATHCOUNTS competition and has experience with competitions like the AIME. During his free time, he likes to play soccer and study physics.'
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