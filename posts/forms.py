from django.forms import (Form, CharField, Textarea, ModelChoiceField, ImageField, Select)
from groups.models import Group
from posts import models


class PostForm(Form):
    group = ModelChoiceField(queryset=Group.objects.all(), widget=Select)
    message = CharField(widget=Textarea, required=False)
    image = ImageField(required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["group"].queryset = (
                models.Group.objects.filter(
                    pk__in=user.groups.values_list("group__pk")
                )
            )
