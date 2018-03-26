from __future__ import unicode_literals

from django.db import models

from ..main.models import Comment


# the "re" module will let us perform some regular expression operations
import re
# Check for Valid Email format
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# NAME_REGEX Check letters only, at least 2 characters /^[a-zA-Z]{2,}$/
NAME_REGEX = re.compile(r'^[a-zA-Z]{2,}$')
# PASSWORD_REGEX at least 8 characters /^.{8,}$/
PASSWORD_REGEX = re.compile(r'^.{8,}$')

# Bcrypt hashing
import bcrypt

class UserManager(models.Manager):
    def reg_validator(self, postData):

        errors = {}

        #validate first name
        if len(postData['first_name']) < 1:
            errors["first name reg"] = "You must enter your first name"
        elif not NAME_REGEX.match(postData['first_name']):
            errors["first name reg"] = "Invalid characters or not at least 2 characters in first name"

        #validate last name
        if len(postData['last_name']) < 1:
            errors["last name reg"] = "You must enter your last name"
        elif not NAME_REGEX.match(postData['last_name']):
            errors["last name reg"] = "Invalid characters or not at least 2 characters in last name"

        #validate email
        if len(postData['email']) < 1:
            errors["email reg"] = "You must enter an email address"
        elif not EMAIL_REGEX.match(postData['email']):
            errors["email reg"] = "Invalid email address"
        elif self.filter(email = postData['email']):
            errors["email reg"] = "Email address already in use"

        #validate password
        if len(postData['password']) < 1:
            errors["password reg"] = "You must enter a password"
        elif not PASSWORD_REGEX.match(postData['password']):
             errors["password reg"] = "Passwords must be 8 characters or more"

        #validate confirm_password
        if len(postData['confirm_password']) < 1:
            errors["confirm password reg"] = "You must confirm password"
        elif postData['confirm_password'] != postData['password']:
            errors["confirm password reg"] = "Password and Confirm Password must match"
   
        return errors

    #login form validator
    def login_validator(self, postData):

        errors = {}

        #validate email
        if len(postData['email']) < 1:
            errors["email login"] = "You must enter an email address"
            return errors
        if not self.filter(email = postData['email']):
            errors["email login"] = "Email address does not exist"
            return errors

        #validate password
        if len(postData['password']) < 1:
            errors["password login"] = "You must enter your password"
        elif not bcrypt.checkpw(postData['password'].encode(), self.get(email = postData['email']).password.encode()):
             errors["password login"] = "Incorrect email/password combination"

        return errors

    # create a user 
    def create_user(self, clean_data):
        hashed_pw = bcrypt.hashpw(clean_data["password"].encode(), bcrypt.gensalt())
 
        level = 1
        admin_set = User.objects.filter(user_level=9)
        if len(admin_set) < 1:
            level = 9

        return self.create(
            first_name=clean_data["first_name"], 
            last_name=clean_data["last_name"], 
            email=clean_data["email"], 
            password=hashed_pw,
            user_level=level,
            description=""
        )
    def update_names_validator(self, postData, id):

        u =  User.objects.get(pk=id)

        errors = {}

        if u.first_name <> postData["first_name"]:
            if len(postData['first_name']) < 1:
                errors["first name upd"] = "First name cannot be empty"
            elif not NAME_REGEX.match(postData['first_name']):
                errors["first name upd"] = "Invalid characters or not at least 2 characters in first name"
            else:
                print "update_validation: first_name changed and passes validation -- saving ", postData["first_name"]
                u.first_name = postData["first_name"]
                u.save()

        if u.last_name <> postData["last_name"]:
            if len(postData['last_name']) < 1:
                errors["last name upd"] = "Last name cannot be empty"
            elif not NAME_REGEX.match(postData['last_name']):
                errors["last name upd"] = "Invalid characters or not at least 2 characters in first name"
            else:
                print "update_validation: last_name changed and passes validation -- saving ", postData["last_name"]
                u.last_name = postData["last_name"]
                u.save()

        if u.email <> postData["email"]:
            if len(postData['email']) < 1:
                errors["email upd"] = "Email address cannot be empty"
            elif not EMAIL_REGEX.match(postData['email']):
                errors["email upd"] = "Email needs to have valid email address format"
            elif User.objects.filter(email=postData['email']).exists():
                errors["email upd"] = "Email address already exists"
            else:
                print "update_validation: email changed and passes validation -- saving ", postData["email"]
                u.email = postData["email"]
                u.save()

        return errors

    def update_pwd_validator(self, postData, id):

        u =  User.objects.get(pk=id)

        errors = {}

        #update password if one supplied regardless of whether it has changed
        if len(postData['password']) > 0:
            if not PASSWORD_REGEX.match(postData['password']):
                errors["password upd"] = "Passwords must be 8 characters or more"
            elif postData['confirm_password'] != postData['password']:
                errors["confirm password upd"] = "Password and Confirm Password must match"
            else:
                print "update_validation: password passes validation -- saving ", postData["password"]
                hashed_pw = bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt())
                u.password = hashed_pw
                u.save()
        
        return errors
    
    def update_desc_validator(self, postData, id):

        u =  User.objects.get(pk=id)

        errors = {}

        #update description if something supplied
        if len(postData['description']) < 1:
            errors["desc upd"] = "No description was supplied"

        else:
            print "update_validation: description supplied -- saving ", postData["description"]
            u.description = postData["description"]
            u.save()
        
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    user_level = models.IntegerField(default=1)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # *************************

    # Connect an instance of UserManager to our User model overwriting the old hidden objects key with a new one with extra properties
    objects = UserManager()
    # *************************
    def __str__(self):
        return '%s %s %s %s' % (self.first_name, self.last_name, self.email, self.description)
