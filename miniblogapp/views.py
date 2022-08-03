from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic, View
from .models import Post, Comment, Profile
from .forms import CommentForm, UpdateForm, ProfileUpdateForm


# Create your views here.

class IndexView(generic.ListView):
    model = Post
    template_name = 'miniblogapp/index.html'
    context_object_name = 'index_list'

    def get_queryset(self):
        return Post.objects.all().order_by('-date_created')[:2]


class PostListView(generic.ListView):
    model = Post
    queryset = Post.objects.all().order_by('-date_created')


class AuthorDetailView(View):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Http404

    def get(self, request, pk):
        user_detail = self.get_object(pk)
        comment = Comment.objects.filter(post__author=self.kwargs['pk']).count()
        update_form = UpdateForm(instance=user_detail)
        profile_update_form = ProfileUpdateForm(instance=user_detail.profile)
        context = {
            'user_detail': user_detail,
            "comment": comment,
            "update_form": update_form,
            'profile_update_form': profile_update_form,
        }
        return render(request, 'miniblogapp/user_detail.html', context)

    @method_decorator(login_required)
    def post(self, request, pk):
        user = self.get_object(pk=pk)
        profile = Profile.objects.get(author_id=pk)
        form = UpdateForm(request.POST, instance=user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if form.is_valid() and profile_update_form.is_valid():
            form.save()
            profile_update_form.save()

            return HttpResponseRedirect(reverse('author-detail', args=[pk]))
        context = {
            "update_form": form,
            "'profile_update_form": profile_update_form,
        }

        return render(request, "miniblogapp/user_detail.html", context=context)

    # model = User
    # template_name = 'miniblogapp/user_detail.html'
    # context_object_name = 'user_detail'
    #
    # def get_context_data(self, **kwargs):
    #     context = super(AuthorDetailView, self).get_context_data(**kwargs)
    #     context['comment'] = Comment.objects.filter(post__author=self.kwargs['pk']).count()
    #     return context


class AuthorListView(generic.ListView):
    model = User
    template_name = 'miniblogapp/user_list.html'


class PostDetailView(View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        comment_form = CommentForm()
        context = {
            'post': post,
            "comment_form": comment_form,
            # "session_date": request.session.get("blog")
        }
        return render(request, 'miniblogapp/post_detail.html', context)

    @method_decorator(login_required)
    def post(self, request, slug):
        form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        # if self.request.user and not AnonymousUser:
        if form.is_valid():
            comment = form.save(commit=False)
            comment.patch = post.id
            comment.email = self.request.user.email
            comment.firstname = self.request.user.first_name
            comment.lastname = self.request.user.last_name
            comment.save()
            return HttpResponseRedirect(reverse('post-detail', args=[slug]))
        # else:
        #     blog = request.session.get("blog")
        #     if blog is None:
        #         blog = request.POST["text"]
        #     request.session["blog"] = blog
        #     return redirect('login')

        context = {
            "comment_form": form,
        }

        return render(request, "miniblogapp/post_detail.html", context=context)

    # def get_queryset(self):
    #     return Comment.objects.all().order_by('-date')

# class post_detail(request, slug):
#     """View function for renewing a specific BookInstance by librarian."""
#     post = get_object_or_404(Post, slug=slug)
#
#     # If this is a POST request then process the Form data
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#
#             # redirect to a new URL:
#             return HttpResponseRedirect(reverse('post-detail', args=(post.slug,)))
#
#     # If this is a GET (or any other method) create the default form.
#     else:
#         form = CommentForm(request.POST)
#         post = post
#
#     context = {
#         'form': form,
#         'post': post
#     }

# return render(request, 'miniblogapp/post_detail.html', context)
