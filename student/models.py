from __future__ import unicode_literals

import json
import string
import unicodedata
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	classes = models.CharField(max_length=1000)
	firstname = models.CharField(max_length=100)
	lastname = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	school = models.CharField(max_length=100)

	saved_answers = models.CharField(max_length=1000)
	num_tries = models.CharField(max_length=1000)
	
	amc_8_scores = models.CharField(max_length=500)
	amc_8_locks  = models.CharField(max_length=500)
	
	amc_10_scores = models.CharField(max_length=500)
	amc_10_locks = models.CharField(max_length=500)

	usaco_bronze_scores = models.CharField(max_length=500)
	usaco_bronze_locks  = models.CharField(max_length=500)

	def __str__(self):
		return "Student (%s, %s) with classes %s" % (self.firstname, self.lastname, self.classes)
	
	def setClasses(self, x):
		self.classes = ','.join(x)

	def getClasses(self):
		# self.classes = ''
		ls = self.classes.split(',')
		newls = []

		old_names = ["AMC 8", "AMC 10", "Algebra 2", "Geometry", "Chemistry"]
		changed = False

		for i in ls:
			if i in old_names:
				changed = True
			if i not in old_names:
				newls.append(i)
		
		newls = sorted(newls)
		if changed:
			self.setClasses(newls)
			
		return newls

	def removeClasses(self, classname):
		l = self.classes.split(',')
		newl = []
		for a in l:
			if a != classname:
				newl.append(a)
		self.classes = ','.join(newl)

	def setSavedAnswers(self, dictval):
		s = repr(dictval)
		self.saved_answers = s

	def getSavedAnswers(self):
		return eval(self.saved_answers)

	def setNumTries(self, dictval):
		s = repr(dictval)
		self.num_tries = s

	def getNumTries(self):
		return eval(self.num_tries)

	#Helper method
	def get_ith_occurence(self, str, sub, i):
		ret = -1
		if i > 0:
			ret = str.find(sub)
			while ret >= 0 and i > 1:
				ret = str.find(sub, ret + len(sub))
				i -= 1
			if ret == -1:
				ret = str.__len__()
		return ret

	def get_score(self, class_name, i, j): # i = topic, #j = easy / medium / hard (0, 1, 2)
		if class_name == "amc_8":
			s = self.amc_8_scores.encode('ascii','replace')[self.get_ith_occurence(self.amc_8_scores, ';', i)+1:self.get_ith_occurence(self.amc_8_scores, ';', i+1)]
			return s[self.get_ith_occurence(s, ',', j)+1: self.get_ith_occurence(s, ',', j+1)]
		elif class_name == "amc_10":
			s = self.amc_10_scores.encode('ascii','replace')[self.get_ith_occurence(self.amc_10_scores, ';', i)+1:self.get_ith_occurence(self.amc_10_scores, ';', i+1)]
			return s[self.get_ith_occurence(s, ',', j)+1: self.get_ith_occurence(s, ',', j+1)]

	#Example: class_name: amc_8,
	#		 topic_id: 0 (algebra),
	#		 problem_type: 0 (0: easy, 1: medium, 2: hard)
	#		 problems_correct: 5
	#		 problems_total: 24
	def set_score(self, class_name, topic_id, problem_type_id, problems_correct, problems_total): 
		if class_name == "amc_8":
			semi_colon_index = self.get_ith_occurence(self.amc_8_scores, ';', topic_id) + 1
			comma_index = self.amc_8_scores[:semi_colon_index].__len__() + self.get_ith_occurence(self.amc_8_scores[semi_colon_index:], ',', problem_type_id)
			a = self.amc_8_scores.find(',', comma_index+1)
			if a == -1:
				a = self.amc_8_scores.__len__()
			b = self.amc_8_scores.find(';', comma_index+1)
			if b == -1:
				b = self.amc_8_scores.__len__()
			end_index = min(a, b)
			new_score = self.amc_8_scores[:comma_index+1] + str(problems_correct) + '/' + str(problems_total) + self.amc_8_scores[end_index:]
			# print "Old Score String: " + self.amc_8_scores
			# print "New Score String: " + self.amc_8_scores[:comma_index+1] + str(problems_correct) + '/' + str(problems_total) + self.amc_8_scores[end_index:]
			self.amc_8_scores = new_score

		elif class_name == "amc_10":
			semi_colon_index = self.get_ith_occurence(self.amc_10_scores, ';', topic_id) + 1
			comma_index = self.amc_10_scores[:semi_colon_index].__len__() + self.get_ith_occurence(self.amc_10_scores[semi_colon_index:], ',', problem_type_id)
			a = self.amc_10_scores.find(',', comma_index+1)
			if a == -1:
				a = self.amc_10_scores.__len__()
			b = self.amc_10_scores.find(';', comma_index+1)
			if b == -1:
				b = self.amc_10_scores.__len__()
			end_index = min(a, b)
			new_score = self.amc_10_scores[:comma_index+1] + str(problems_correct) + '/' + str(problems_total) + self.amc_10_scores[end_index:]
			# print "Old Score String: " + self.amc_10_scores
			# print "New Score String: " + self.amc_10_scores[:comma_index+1] + str(problems_correct) + '/' + str(problems_total) + self.amc_10_scores[end_index:]
			self.amc_10_scores = new_score
			

	def get_lock(self, class_name, topic_id):
		if class_name == "amc_8":
			start = self.get_ith_occurence(self.amc_8_locks, ';', topic_id) + 1
			end = self.get_ith_occurence(self.amc_8_locks, ';', topic_id+1)
			return self.amc_8_locks[start:end]
		elif class_name == "amc_10":
			start = self.get_ith_occurence(self.amc_10_locks, ';', topic_id) + 1
			end = self.get_ith_occurence(self.amc_10_locks, ';', topic_id+1)
			return self.amc_10_locks[start:end]

	def set_lock(self, class_name, topic_id, val):
		if class_name == "amc_8":
			start = self.get_ith_occurence(self.amc_8_locks, ';', topic_id) + 1
			end = self.get_ith_occurence(self.amc_8_locks, ';', topic_id+1)
			s = self.amc_8_locks[0:start] + val + self.amc_8_locks[end:]
			self.amc_8_locks = s
			# print s
		elif class_name == "amc_10":
			start = self.get_ith_occurence(self.amc_10_locks, ';', topic_id) + 1
			end = self.get_ith_occurence(self.amc_10_locks, ';', topic_id+1)
			s = self.amc_10_locks[0:start] + val + self.amc_10_locks[end:]
			self.amc_10_locks = s
			# print s