from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def validate(self, form_data):
        errors =[]
        if len(form_data['name']) == 0:
            errors.append("Name is required.")
        if len(form_data['alias']) == 0:
            errors.append("Alias is required.")
        if len(form_data['email']) == 0:
            errors.append("Email is required.")
        if len(form_data['password']) < 8:
            errors.append("Password is required.")
        if form_data['password'] != form_data['pw_confirm']:
            errors.append("Password confirmation must match password.")

        return errors


    def validate_login(self, form_data):
        errors = []

        if len(form_data['email']) == 0:
            errors.append("Email is required.")
        if len(form_data['password']) < 8:
            errors.append("Password is required.")

        return errors

    def login(self, form_data):
        errors = self.validate_login(form_data)

        if not errors:
            user = User.objects.filter(email=form_data['email']).first()

            if user:
                if str(form_data['password']) == user.password:
                    return user

            errors.append('Invalid input')
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        string_output = "id: {} name: {} alias: {} email:{} password:{}"

        return string_output.format(
            self.id,
            self.name,
            self.alias,
            self.email,
            self.password,
        )
    objects = UserManager()

class Poke(models.Model):
    poker = models.ForeignKey(User, related_name="poked")
    pokee = models.ForeignKey(User, related_name="poked_by")

    def __str__(self):
        return "Poker: {} Pokee: {}".format(
            self.poker.id,
            self.pokee.id,
        )
