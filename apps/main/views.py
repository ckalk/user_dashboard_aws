from django.shortcuts import render, HttpResponse, redirect

# import object Class(es) from models.py
from ..users.models import *

# import messages to use flask error messaging
from django.contrib import messages

# Inside your app's views.py file
from django.core.urlresolvers import reverse


# ************************

# / - display main index page (home page)
def index(request):

    return render(request, 'main/index.html')

# ************************

# /signin - display a signin form 
def signin(request):
    
    #clear session just to make sure only one person is logged in
    request.session.clear()
    
    return render(request, 'main/signin.html')


# /login - process data from signin form
def login(request):
    print "***** in login route: request.POST = ", request.POST

    # Use validation performed in models.py
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        # return to signin page with errors
        return redirect(reverse('main:my_signin'))

    else:
        user = User.objects.get(email=request.POST["email"])
        request.session['id'] = user.id
        request.session['user_level'] = user.user_level
        messages.success(request, "Thank you {} {} for logging in".format(user.first_name, user.last_name))

        #if user_level=9 send to admin dashboard
        if request.session['user_level']==9:
            return redirect(reverse('dashboard:my_admin_dashboard'))

        # else go to normal user dashboard
        return redirect(reverse('dashboard:my_dashboard')) 

# ************************

# /logoff -  log current user off and return to main index page
def logoff(request):
    # clean session and return to main index page
    request.session.clear()
    return redirect(reverse('main:my_index')) 

# ************************

# /register - display a registration form 
def register(request):

  return render(request, 'main/register.html')


# /create_user - process data from registration form 
def create_user (request):
    print "***** in create_user route: request.POST = ", request.POST

    # Use validation performed in models.py
    errors = User.objects.reg_validator(request.POST)

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
         # return to register form page with errors

        return redirect(reverse('main:my_register')) 

    else:
        new_user = User.objects.create_user(request.POST)
        request.session['id'] = new_user.id
        request.session['user_level'] = new_user.user_level
        messages.success(request, "Thank you {} {} for registering".format(new_user.first_name, new_user.last_name))
        #if user_level=9 send to admin dashboard
        if request.session['user_level']==9:
            return redirect(reverse('dashboard:my_admin_dashboard'))

        # else go to normal user dashboard
        return redirect(reverse('dashboard:my_dashboard')) 

