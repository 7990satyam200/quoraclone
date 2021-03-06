from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Board, Topic, Post
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .models import Board, Topic, Post
from .forms import newTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.utils import timezone

# Create your views here.
def home(request):
       boards = Board.objects.all()
       return render(request, 'home.html', {'boards':boards})


# class home(TemplateView):
#     model =Board
#     template_name = 'home.html'


def board_topic(request, pk):
    board = Board.objects.get(pk=pk)
    return render(request, 'topics.html', {'board':board})


# def new_topic(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     if request.method == 'POST':
#         subject = request.POST['subject']
#         message = request.POST['message']
#         user = User.objects.first()
#         topic = Topic.objects.create(subject=subject, board=board, starter=user)
#         post = Post.objects.create(message = message, topic=topic, created_by= user)
#         return redirect('board_topic', pk=board.pk)
#     return render(request, 'new_topic.html', {'board':board})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    # user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = newTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('board_topic', pk=pk)  # TODO: redirect to the created topic page
    else:
        form = newTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply_topic(request, pk, topic_pk):
    board = Board.objects.get(pk=pk)

    topic = get_object_or_404(Topic, board__pk=pk, pk= topic_pk)
    if request.method =='POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post= form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk= topic_pk)

    else:
        form =PostForm()
    return render(request, 'reply_topic.html', {'topic':topic, 'board':board, 'form':form})
