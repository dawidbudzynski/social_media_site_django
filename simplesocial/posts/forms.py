from django import forms
from django.forms import (Form, CharField, ChoiceField, Textarea, ModelChoiceField, ImageField, ModelMultipleChoiceField,
                          CheckboxSelectMultiple, Select,
                          NullBooleanField)

from posts import models
from groups.models import Group


# class PostForm(forms.ModelForm):
#     class Meta:
#         fields = ("message", "group")
#         model = models.Post

class PostForm(Form):
    group = ModelChoiceField(queryset=Group.objects.all(), widget=Select)
    message = CharField(widget=Textarea, required=False)
    image = ImageField()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["group"].queryset = (
                models.Group.objects.filter(
                    pk__in=user.groups.values_list("group__pk")
                )
            )
