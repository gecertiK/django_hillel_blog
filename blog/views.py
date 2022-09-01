from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_page

from .forms import RegisterForm, ContactUsForm
from .models import Comment, Post, User


def index(request):
    num_posts = Post.objects.count()
    num_comments = Comment.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(
        request,
        'blog/index.html',
        context={'num_posts': num_posts, 'num_comments': num_comments,
                 'num_visits': num_visits},
    )


class RegisterFormView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()

        username = self.request.POST['username']
        password = self.request.POST['password1']

        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class UserEditView(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    template_name = 'blog/update_user.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class PostListView(generic.ListView):
    model = Post
    paginate_by = 20
    template_name = 'blog/post_list.html'


@method_decorator(cache_page(30), name='dispatch')
class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class CreatePost(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Post
    success_message = 'Author was created'
    template_name = "blog/create_post.html"
    fields = ('title', 'brief_description', 'full_description', 'image', 'posted')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        send_mail(
            'Post',
            'Create new post',
            'david@example.com',
            ['admin@example.com'],
            fail_silently=False,
        )

        return super(CreatePost, self).form_valid(form)


class MyCommentView(LoginRequiredMixin, generic.ListView):
    model = Comment
    template_name = 'blog/my_comments.html'
    paginate_by = 10

    def get_queryset(self):
        return Comment.objects.filter(username=self.request.user).filter(posted_com=True)


class CommentCreateView(SuccessMessageMixin, generic.CreateView):
    template_name = 'blog/create_comment.html'
    model = Comment
    fields = ('username', "text", 'post')
    success_message = 'Comment was created'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})

    def get_initial(self):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        return {
            'post': post
        }

    def form_valid(self, form):
        send_mail(
            'Comment',
            'Create new comment',
            'david@example.com',
            ['admin@example.com'],
            fail_silently=False,
        )
        return super(CommentCreateView, self).form_valid(form)


class ProfileInfo(generic.DetailView):
    model = User
    template_name = "blog/profile_info.html"

    def get_context_data(self, **kwargs):
        if self.request.user == self.get_object():
            object_list = Post.objects.filter(author=self.get_object())
            context = super(ProfileInfo, self).get_context_data(object_list=object_list, **kwargs)
        else:
            object_list = Post.objects.filter(author=self.get_object())
            context = super(ProfileInfo, self).get_context_data(object_list=object_list, **kwargs)
        return context


@method_decorator(cache_page(30), name='dispatch')
class ProfileList(generic.ListView):
    queryset = User.objects.all()
    template_name = "blog/profile_list.html"


class MessageAdmin(SuccessMessageMixin, generic.FormView):
    form_class = ContactUsForm
    success_message = 'Message was send'
    success_url = reverse_lazy('index')
    template_name = 'blog/contact_us.html'

    def form_valid(self, form):
        data = form.cleaned_data
        send_mail('MESSAGE',
                  data['text'],
                  'admin@gmail.com',
                  ['example@gmail.com'],
                  fail_silently=False,
                  )
        return super(MessageAdmin, self).form_valid(form)


class BloggerPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    success_message = 'Password successfully changed'
    template_name = 'registration/password_reset_confirm.html'

    def get_success_url(self):
        return reverse('index')
