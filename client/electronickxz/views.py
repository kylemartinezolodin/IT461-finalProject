from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View

from App.settings import DB_HOST
import requests # for http requests

			
class LoginView(View):
	def get(self, request):
		print(request.session)
		print("qwerty")
		# if hasattr(request, 'sessions'):
		if {'token','userName'} <= request.session.keys(): # equivalent to {'token','userName'} in request.sessions
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
				request.session["userName"] = response.json()["user"]["username"]
				request.session["userFName"] = response.json()["user"]["fname"]
				request.session["userType"] = response.json()["user"]["type"]
				print(request.session)

				if response.json()["user"]["type"] == "standard":
					return redirect('electronickxz:index_view')
				elif response.json()["user"]["type"] == "editor":
					return redirect('electronickxz:editorProduct_view')

			print(response.text)
			if 'user' in response.json():
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

		
		response = requests.post(str(DB_HOST)+'/login', json={"username": "admin","password": "admin"}).json()
		response = requests.post(str(DB_HOST)+'/users/?token='+response["token"],
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
			response = requests.post(str(DB_HOST)+'/login', json={"username": "admin","password": "admin"}).json()
			print("response")
			print(response["token"])
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
			if 'token' in request.session:
				offset = request.GET["offset"] if "offset" in request.GET else 0
				print(offset)
				context = requests.get(str(DB_HOST)+'/items/?fields=&offset='+str(offset)+'&limit=4&token='+request.session["token"]).json()

				data = []
				for item in context["data"]:
					item["link"] = "google.com" #str(DB_HOST) +'/?'
					data.append(item)
				context["data"] = data
				context["user"] = {"id": request.session["userID"], "username": request.session["userFName"], "type": request.session["userType"]}
				print("random")
				print(context)
				return render(request, 'Electronickxz/productseditor.html', context)
			return redirect('electronickxz:login_view')


class EditorProductsRegistrationView(View):
	def get(self, request):
		return render(request, 'Electronickxz/productsregister.html')
	
	def post(self, request):
		name = request.POST.get("name")
		price = request.POST.get("price")
		quantity = request.POST.get("quantity")
		data = {
				"id": 0,
				"name": name,
				"price": float(price),
				"quantity": int(quantity)
				}
		print(data)
		response = requests.post(str(DB_HOST)+'/items/?token='+request.session["token"],json=data)

		if response.status_code == 200: # username exists & correct password
			return redirect('electronickxz:editorProduct_view')

		print(response.text)
		response.status_code = 403 if response.json()["user"]["type"] is'guest' else response.status_code
		print(response.status_code)

		return render(request, 'Electronickxz/productsregister.html', context = {"error": response.status_code if response.status_code is not None else 0})
		
		
class EditorUsersView(View):
	def get(self, request):
		if 'token' in request.session:
			offset = request.GET["offset"] if "offset" in request.GET else 0
			context = requests.get(str(DB_HOST)+'/users/?fields=&offset='+str(offset)+'&limit=4&token='+request.session["token"]).json()
			
			data = []
			for item in context["data"]:
				item["link"] = "google.com" #str(DB_HOST) +'/?'
				data.append(item)
			context["data"] = data
			context["user"] = {"id": request.session["userID"], "username": request.session["userFName"], "type": request.session["userType"]}

			print(context)
			return render(request, 'Electronickxz/userseditor.html', context)
		return redirect('electronickxz:login_view')


class CheckoutView(View):
	def get(self, request):
		if 'token' in request.session:
			offset = request.GET["offset"] if "offset" in request.GET else 0
			user_id = request.session["userID"]
			print(str(DB_HOST)+'/users_cart/'+str(user_id)+'?fields=&offset='+str(offset)+'&limit=4&token=')
			context = requests.get(str(DB_HOST)+'/users_cart/'+str(user_id)+'?fields=&offset='+str(offset)+'&limit=4&token='+request.session["token"]).json()
			
			data = []
			for record in context["data"]:
				item = requests.get(str(DB_HOST)+'/items/'+str(record["item_id"])+'?token='+request.session["token"]).json()
				record["item"] = item
				data.append(record)
			context["data"] = data
			context["user"] = {"id": request.session["userID"], "username": request.session["userFName"], "type": request.session["userType"]}

			print(context)
			return render(request, 'Electronickxz/checkout.html', context)
		return redirect('electronickxz:login_view')

class PaymentView(View):
	def get(self, request):
		return render(request, 'Electronickxz/payment.html')

class SessionVarView(View):
	def get(self, request, *args, **kwargs):
		print(kwargs['key'])
		return HttpResponse(request.session[kwargs['key']])

class LogoutView(View):
	def get(self, request):
		del request.session["token"]
		del request.session["userID"]
		del request.session["userName"]
		del request.session["userFName"]
		del request.session["userType"]
		return redirect('electronickxz:login_view')