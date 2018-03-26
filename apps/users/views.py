from django.shortcuts import render, HttpResponse, redirect

# import object Class(es) from models.py
from .models import *

# import messages to use flask error messaging
from django.contrib import messages

# Inside your app's views.py file
from django.core.urlresolvers import reverse


# /users/new - display form for an admin to add a new user (similar to self registration form)
def new(request):
    print "*** got to users new"
    return render(request, 'users/new.html')


#POST to /users/create - if no errors, calls the create_user method to insert a new user record into database. 
def create(request):
    print "*** got to users create"
    # add check here to make sure logged in user is an admin; if not, print error and send to logout route

    print "in users create route: request.POST = ", request.POST

    # Use validation performed in models.py
    errors = User.objects.reg_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect(reverse('users:my_new')) 

    else:
        print "*** users create -- creating new user"
        new_user = User.objects.create_user(request.POST)
        messages.success(request, "User {} {} successfully added".format(new_user.first_name, new_user.last_name))
        #send back to admin dashboard
        return redirect(reverse('dashboard:my_admin_dashboard'))


# *************************

# /users/edit - display form for an admin to edit a user 
def profile(request):
    print "*** got to users edit (with no id) ==> editing own profile"
    id = request.session['id']
    context = {
        "user": User.objects.get(id=id)
        }
    return render(request, 'users/edit.html', context)


# /users/edit - display form for an admin to edit a user 
def edit(request, id):
    print "*** got to users edit"
    context = {
        "user": User.objects.get(id=id)
        }
    return render(request, 'users/edit.html', context)


# /users/edit/(?P<id>\d+) - process the edit
def update(request, id):
    print "*** got to users update"
    print "request=", request.POST
    print "id = ", id

    # Use validation and update performed in models.py

    #test if the email and names form was submitted
    if "first_name" in request.POST:
        errors = User.objects.update_names_validator(request.POST, id)
        print "in users update names/email route, returned from validator with errors=", errors
        # if errors in updated values found, return to edit view and display errors
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            if id <> request.session['id'] or request.session['user_level']<9 :
                return redirect(reverse('users:my_edit', args=(id,)))
            else:
                return redirect(reverse('users:my_profile'))
        
        # if no errors in updated values found update was successful and show updated record
        else:
            messages.success(request, "Name and/or email of User ID {} successfully updated".format(id))
            print "*** users update name/email -- no errors, displaying show template"
            return redirect(reverse('users:my_show', args=(id,)))

    #test if the password change form was submitted
    if "password" in request.POST:
        errors = User.objects.update_pwd_validator(request.POST, id)
        print "in users update password route, returned from validator with errors=", errors
        # if errors in updated values found, return to edit view and display errors
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect(reverse('users:my_edit', args=(id,)))
        
        # if no errors in updated values found update was successful and show updated record
        else:
            messages.success(request, "Password of User ID {} successfully updated".format(id))
            print "*** users update password route-- no errors, displaying show template"
            return redirect(reverse('users:my_show', args=(id,)))

    #test if the description form was submitted
    if "description" in request.POST:
        errors = User.objects.update_desc_validator(request.POST, id)
        print "in users update description route, returned from validator with errors=", errors
        # if errors in updated values found, return to edit view and display errors
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect(reverse('users:my_edit', args=(id,)))
        
        # if no errors in updated values found update was successful and show updated record
        else:
            messages.success(request, "Description of User ID {} successfully updated".format(id))
            print "*** users update description -- no errors, displaying show template"
            return redirect(reverse('users:my_show', args=(id,)))
# *************************

# /users/show/(?P<id>\d+) - display a specific user's data
def show(request, id):
    print "*** got to users show"
    context = {
        "user": User.objects.get(id=id)
        }
    return render(request, 'users/show.html', context)


# *************************

# GET /users/destroy/<id> - calls the destroy method to remove a particular user with the given id.
def destroy(request, id):
    print "*** got to users destroy, with id=", id
    u = User.objects.get(id=id)
    u.delete()
    return redirect(reverse('dashboard:my_admin_dashboard')) 
