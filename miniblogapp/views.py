from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.core.serializers import serialize, json
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.views.decorators.csrf import csrf_exempt

from .models import Post, Comment, Profile
from .forms import CommentForm, UpdateForm, ProfileUpdateForm, PostForm


# Create your views here.

class IndexView(generic.ListView):
    model = Post
    template_name = 'miniblogapp/index.html'
    context_object_name = 'index_list'

    def get_queryset(self):
        return Post.post_objects.all().order_by('-date_created')[:2]


class PostListView(generic.ListView):
    model = Post
    queryset = Post.post_objects.all().order_by('-date_created')


class AuthorDetailView(generic.DetailView):
    model = User
    template_name = 'miniblogapp/user_detail.html'
    context_object_name = 'user_detail'

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context['comment'] = Comment.objects.filter(post__author=self.kwargs['pk']).count()

        if self.request.user.id == self.kwargs['pk']:
            context['update_form'] = UpdateForm(instance=context['user_detail'])
            context['profile_update_form'] = ProfileUpdateForm(instance=context['user_detail'].profile)
            context['all_author_post'] = Post.objects.filter(author_id=self.kwargs['pk'])
        else:
            context['all_author_post'] = Post.post_objects.filter(author_id=self.kwargs['pk'])
            context['update_form'] = None
            context['profile_update_form'] = None
        return context


@login_required
def post_user_form(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UpdateForm(request.POST, instance=user)
    profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)

    if form.is_valid() and profile_update_form.is_valid():
        form.save()
        profile_update_form.save()

        return HttpResponseRedirect(reverse('author-detail', args=[pk]))
    context = {
        "update_form": form,
        "'profile_update_form": profile_update_form,
    }

    return render(request, "miniblogapp/user_detail.html", context=context)


class AuthorListView(generic.ListView):
    model = User
    template_name = 'miniblogapp/user_list.html'


class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['current_user'] = self.request.user

        if self.request.user.id != context['post'].author.id:
            comment = Comment.comment_objects.filter(post__slug=self.kwargs.get('slug')).order_by('-date')
        else:
            comment = Comment.objects.filter(post__slug=self.kwargs.get('slug')).order_by('-date')

        context['comment'] = comment
        return context


@login_required
def post_comment_form(request, slug):
    pst = Post.objects.get(slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = pst.id
            comment.email = request.user.email
            comment.firstname = request.user.first_name
            comment.lastname = request.user.last_name
            comment.save()
            data = serialize('json', [comment, ])
            return JsonResponse({"data": data}, status=200)
        return JsonResponse({"data": form.errors}, status=400)

        # context = {
        #     "comment_form": form,
        # }
        # return render(request, "miniblogapp/post_detail.html", context=context)


class ChangePasswordView(PasswordChangeView):
    template_name = 'miniblogapp/password_change_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        self.request.session.flush()
        logout(self.request)
        return super(ChangePasswordView, self).form_valid(form)


class UpdatePost(UserPassesTestMixin, generic.UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(UpdatePost, self).form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class HideUnhiddenComment(View):
    def post(self, request, slug, pk):
        comment = Comment.objects.get(id=pk)

        # if comment.is_hidden:
        #     comment.is_hidden = False
        # elif not comment.is_hidden:
        #     comment.is_hidden = True
        comment.is_hidden = not comment.is_hidden

        comment.save()
        return HttpResponseRedirect(reverse('post-detail', args=[slug]))
