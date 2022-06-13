from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View

from App.settings import DB_HOST
import requests # for http requests

			
class LoginView(View):
	def get(self, request):
		return render(request, 'Electronickxz/login.html')
	def post(self, request):
		username = request.POST.get("username")
		password = request.POST.get("password")
		if 'btnLogin' in request.POST:
			print(username)
			print(password)
			return redirect('electronickxz:index_view')
				
class RegistrationView(View):
	def get(self, request):
		return render(request, 'Electronickxz/register.html')
	def post(self, request):
		fname = request.POST.get("firstname")
		lname = request.POST.get("lastname")
		username = request.POST.get("username")
		password = request.POST.get("password")

		print(fname)
		print(lname)
		print(username)
		return redirect('electronickxz:index_view')
		
class IndexClientView(View):
	def get(self, request):
		if 'token' not in request.GET.keys():
			context = requests.get(str(DB_HOST)+'/items/?fields=&offset=0&limit=4&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWQiOjEsImV4cCI6MTY1NTE4NzgzM30.MDrl8nkh-iD73wqm8OgdVYQZrCoIuG5x8vpo8UvwPBY').json()
			data = []
			for item in context["data"]:
				item["link"] = "google.com" #str(DB_HOST) +'/?'
				data.append(item)
			context["data"] = data
			context["user"] = {"id": 69, "username": "Mongo", "type": "Standard"}
			print(context)
		else:
			context = requests.get(str(DB_HOST)+'/items/?fields=&offset='+request.GET["offset"]+'&limit=4&token='+request.GET["token"]).json()
			data = []
			for item in context["data"]:
				item["link"] = "google.com" #str(DB_HOST) +'/?'
				data.append(item)
			context["data"] = data
			context["user"] = {"id": 69, "username": "Mongo", "type": "Standard"}
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