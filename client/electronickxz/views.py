from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View

from App.settings import DB_HOST
import requests # for http requests

			
class LoginView(View):
	def get(self, request):
		print("qwerty")
		if hasattr(request, 'sessions'):
			if {'token','userName'} <= request.sessions: # equivalent to {'token','userName'} in request.sessions
				return redirect('electronickxz:index_view')
		return render(request, 'Electronickxz/login.html')

	def post(self, request):
		username = request.POST.get("username")
		password = request.POST.get("password")
	
		if 'btnLogin' in request.POST:
			response = requests.post(str(DB_HOST)+'/login', json={"username": username,"password": password})
			
			# 200 means username exists & correct password and do not allow guest type user to login
			if response.status_code == 200 and response.json()["user"]["type"] is not 'guest': 
				request.session["token"] = response.json()["token"]
				request.session["userID"] = response.json()["user"]["id"]
				request.session["userFName"] = response.json()["user"]["fname"]
				request.session["userType"] = response.json()["user"]["type"]
				print(request.session)
				return redirect('electronickxz:index_view')

			print(response.text)
			response.status_code = 403 if response.json()["user"]["type"] is'guest' else response.status_code
			print(response.status_code)

		return render(request, 'Electronickxz/login.html', context = {"error": response.status_code if response.status_code is not None else 0})
			
				
class RegistrationView(View):
	def get(self, request):
		return render(request, 'Electronickxz/register.html')
	def post(self, request):
		fname = request.POST.get("firstname")
		lname = request.POST.get("lastname")
		username = request.POST.get("username")
		password = request.POST.get("password")

		response = requests.post(str(DB_HOST)+'/users/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWQiOjEsImV4cCI6MTY1NTIwMDI0Mn0.ZyO9v0O8oKijXGDrX5YMFVr2snfzYSVd_2lL8roQlPE',
			json={
				"id": 0,
				"username": username,
				"password": password,
				"fname": fname,
				"lname": lname,
				"type": "standard"
				}
		)

		if response.status_code == 200: # username exists & correct password
			return redirect('electronickxz:login_view')

		print(response.text)
		print(response.status_code)
		return render(request, 'Electronickxz/register.html', context = {"error": response.status_code if response.status_code is not None else None})
		
class IndexClientView(View):
	def get(self, request):
		if 'token' not in request.session:
			response = requests.post(str(DB_HOST)+'/login', json={"username": "guest","password": "guest"}).json()
			context = requests.get(str(DB_HOST)+'/items/?fields=&offset=0&limit=4&token='+response["token"]).json()
		else:
			offset = request.GET["offset"] if "offset" in request.GET else 0
			context = requests.get(str(DB_HOST)+'/items/?fields=&offset='+str(offset)+'&limit=4&token='+request.session["token"]).json()
		
		data = []
		for item in context["data"]:
			item["link"] = "google.com" #str(DB_HOST) +'/?'
			data.append(item)
		context["data"] = data
		context["user"] = None
		if 'userID' in request.session:
			context["user"] = {"id": request.session["userID"], "username": request.session["userFName"], "type": request.session["userType"]}

		print(context)
		return render(request, 'Electronickxz/clientdashboard.html', context)
	
	def post(self, request):
		return redirect('electronickxz:checkout_view')

		
class EditorProductsView(View):
	def get(self, request):
		context={
			'data' : [
				{
				"id": 420,
				"name": "kong",
				"price": 69.69,
				"link": "google.com"
				},
				{
				"id": 421,
				"name": "Jong",
				"price": 69.69,
				"link": "youtube.com"
				},
				{
				"id": 422,
				"name": "Bong",
				"price": 69.69,
				"link": "facebook.com"
				},
			],
			"metadata":{
				"links":{
					"curr":"google.com",
					"next":"google.com",
					"prev":"google.com",
				}
			},
			'user' : {"id": 69, "username": "Mongo", "type": "Standard"},
		}
		return render(request, 'Electronickxz/productseditor.html', context)


class EditorProductsRegistrationView(View):
	def get(self, request):
		return render(request, 'Electronickxz/productsregister.html')
		
		
class EditorUsersView(View):
	def get(self, request):
		context={
			'data' : [
				{"id": 1,"name": "Kiko"},
				{"id": 2,"name": "Mereno"},
				{"id": 3,"name": "Jojo"},
				{"id": 4,"name": "Binay"},
			],
			"metadata":{
				"links":{
					"curr":"google.com",
					"next":"google.com",
					"prev":"google.com",
				}
			},
			'user' : {"id": 69, "username": "Mongo", "type": "Standard"},
		}
		return render(request, 'Electronickxz/userseditor.html', context)


class CheckoutView(View):
	def get(self, request):
		context={
			'data' : [
				{
				"id": 420,
				"name": "kong",
				"price": 69.69
				},
				{
				"id": 421,
				"name": "Jong",
				"price": 69.69
				},
				{
				"id": 422,
				"name": "Bong",
				"price": 69.69
				},
			],
			"metadata":{
			},
			'user' : {"id": 69, "username": "Mongo", "type": "Standard"},
		}
		return render(request, 'Electronickxz/checkout.html', context)

class PaymentView(View):
	def get(self, request):
		return render(request, 'Electronickxz/payment.html')

class SessionVarView(View):
	def get(self, request, *args, **kwargs):
		print(kwargs['key'])
		return HttpResponse(request.session[kwargs['key']])