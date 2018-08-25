from django.forms import (Form, CharField, ChoiceField, Textarea, ModelChoiceField, ImageField, ModelMultipleChoiceField,
                          CheckboxSelectMultiple, Select,
                          NullBooleanField)


class CreateGroupForm(Form):
    name = CharField(max_length=64)
    description = CharField(widget=Textarea, required=False)
    image = ImageField()
