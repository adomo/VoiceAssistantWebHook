
from assistanthandlerwithauth import AssistantHandlerWithAuth
import urllib
import json
import requests
import authutils
from abc import ABCMeta, abstractmethod

class AssistantHandlerWithAuthCode(AssistantHandlerWithAuth):
	__metaclass__ = ABCMeta

	def __init__(self, action, apiName):
		AssistantHandlerWithAuth.__init__(self,action, apiName)
	
	def handle(self, parameters):
		resultjson = None
		if self.shouldCallUrl(parameters):
			url = self.getUrl(parameters)
			print "calling url " + url
			accessToken = authutils.getAccessToken(self.apiName)   
			if accessToken is None:
				raise ValueError(self.getApiName() + ' is not authorized. Please visit /static/auth.html to authorize')
			headers = {"Authorization": "Bearer " + accessToken}
			postData = self.getPostData(parameters)
			if postData is None:
				result = requests.get(url, headers = headers)
			else:
				postData = json.dumps(postData, indent=4)
				headers['content-type'] = 'application/json'
				print "postData: " + postData
				result = requests.post(url, data = postData, headers = headers)
			print("Result:")
			print result
			resultjson = result.json()
		return self.getResponse(self.getSpeech(parameters, resultjson))

	@abstractmethod
	def getAuthUrl(self):
		pass

	@abstractmethod
	def getTokenUrl(self):
		pass

	@abstractmethod
	def getScopes(self):
		pass 