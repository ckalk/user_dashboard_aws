from __future__ import unicode_literals

from django.db import models



class MessageManager(models.Manager):
    def msg_validator(self, postData):

        errors = {}
        #validate message
        if len(postData['message']) < 1:
            errors["message msg"] = "Message is empty"

        return errors

    # create a message
    def create_message(self, clean_data):
        msg_by = users.User.objects.get(id=clean_data["msg_by"])
        msg_to = users.User.objects.get(id=clean_data["msg_to"])
        this_msg = clean_data["message"]
        return self.create(
            message=this_msg, msg_from=msg_from, msg_to=msg_to
        )


class Message(models.Model):
    message = models.TextField()
    msg_by = models.ForeignKey('users.User', related_name="posts")
    msg_to = models.ForeignKey('users.User', related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # *************************

    # Connect an instance of MessageManager to our Message model
    objects = MessageManager()
    # *************************
    def __str__(self):
        return '%s %s %s' % (self.msg_by, self.msg_to, self.message)



class CommentManager(models.Manager):
    def cmt_validator(self, postData):

        errors = {}
        #validate comment
        if len(postData['comment']) < 1:
            errors["comment msg"] = "Comment is empty"

        return errors

    # create a comment
    def create_comment(self, clean_data):
        cmt_by = users.User.objects.get(id=clean_data["cmt_by"])
        this_cmt = clean_data["comment"]
        return self.create(
            message=this_msg, msg_author=this_user
        )

class Comment(models.Model):
    comment = models.TextField()
    message = models.ForeignKey(Message, related_name="comments")
    cmt_by = models.ForeignKey('users.User', related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # *************************

    # Connect an instance of CommentManager to our Comment model
    objects = CommentManager()
    # *************************
    def __str__(self):
        return '%s %s %s' % (self.comment, self.message, self.cmt_by)