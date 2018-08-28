from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views import View
from django.views import generic
from django.contrib.auth.models import User, Group

from . import models
from .forms import CreateGroupForm
from .models import Group, GroupMember


class CreateGroup(LoginRequiredMixin, View):
    def get(self, request):
        form = CreateGroupForm()
        ctx = {'form': form}

        return render(request,
                      template_name='groups/create_group.html',
                      context=ctx)

    def post(self, request):
        form = CreateGroupForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            image = form.cleaned_data['image']

            if Group.objects.filter(name=name).exists():
                return HttpResponseRedirect('/object_already_exist')

            Group.objects.create(name=name,
                                 description=description,
                                 image=image)
            return HttpResponseRedirect(reverse('groups:all'))
        return HttpResponseRedirect('/wrong_value')


class SingleGroup(generic.DetailView):
    model = Group


class ListGroups(generic.ListView):
    model = Group


class ListUserGroups(generic.ListView):
    model = Group
    # for group in groups:
    #     print(group.members)
    # groups = User.groups
    # for group in groups:
    #     print(group.name)

    # queryset = Group.objects.filter(members__user__username=User.username)
    # print(queryset)
    # template_name = 'groups/user_group_list.html'


class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get("slug"))

        try:
            GroupMember.objects.create(user=self.request.user, group=group)

        except IntegrityError:
            messages.warning(self.request, ("Warning, already a member of {}".format(group.name)))

        else:
            messages.success(self.request, "You are now a member of the {} group.".format(group.name))

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)
