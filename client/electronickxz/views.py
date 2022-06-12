from django.shortcuts import render
from django.views.generic import View

			
class LoginView(View):
	def get(self, request):
		return render(request, 'Electronickxz/login.html')

class RegistrationView(View):
	def get(self, request):
		return render(request, 'Electronickxz/register.html')
		

class IndexClientView(View):
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
		return render(request, 'Electronickxz/clientdashboard.html', context)

		
class EditorProductsView(View):
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
					"curr":"http://google.com",
					"next":"http://google.com",
					"prev":"http://google.com",
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