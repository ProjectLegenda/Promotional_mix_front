from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
def v_login(request):
   if request.method == 'POST':
       username = request.POST.get('username')
       password = request.POST.get('password')
       # Authenticate the user
       user = authenticate(request, username=username, password=password)
       if user is not None:
           # Log the user in
           login(request, user)
           return redirect('get_groups')  # Redirect to a home page or another page after login
       else:
           # If authentication fails
           messages.error(request, 'Invalid username or password')
   return render(request, 'api/templates/login.html')