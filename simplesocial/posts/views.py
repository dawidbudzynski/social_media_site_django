from braces.views import SelectRelatedMixin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views import View, generic

from .forms import PostForm
from .models import Post

User = get_user_model()


class PostList(SelectRelatedMixin, generic.ListView):
    model = Post
    select_related = ("user", "group")


class UserPosts(generic.ListView):
    model = Post
    template_name = "posts/user_post_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = Post
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreatePost(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        ctx = {'form': form}

        return render(request,
                      template_name='posts/create_post.html',
                      context=ctx)

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.cleaned_data['group']
            message = form.cleaned_data['message']
            image = form.cleaned_data['image']
            user = self.request.user

            if Post.objects.filter(message=message).exists():
                return HttpResponseRedirect('/object_already_exist')

            Post.objects.create(group=group,
                                message=message,
                                user=user,
                                image=image)
            return HttpResponseRedirect(reverse('groups:all'))
        return HttpResponseRedirect('/wrong_value')


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = Post
    select_related = ("user", "group")
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)
