from django.forms import (Form, CharField, Textarea, ImageField)


class CreateGroupForm(Form):
    name = CharField(max_length=64)
    description = CharField(widget=Textarea, required=False)
    image = ImageField(required=False)
