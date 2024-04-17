from django.forms import ModelForm, EmailField, CharField
from .models import Room, Profile
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ["host", "participants"]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ["avatar", "bio"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"] = CharField(initial=self.instance.user.username)
        self.fields["email"] = EmailField(initial=self.instance.user.email)
        self.order_fields(field_order=["avatar", "username", "email", "bio"])

    def save(self, commit=True):
        user = User.objects.get(id=self.instance.user.id)
        user.username = self["username"].value()
        user.email = self["email"].value()
        user.save()
        return super(ProfileForm, self).save(commit=commit)
