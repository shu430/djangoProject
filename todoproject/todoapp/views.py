from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from todoapp.models import Task

# Create your views here.
#タスク一覧に関するclass
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name =  "tasks"

    #タスクの所有者=ログインユーザのみ表示させる
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tasks = context["tasks"].filter(user=self.request.user)
        
        searchInputText = self.request.GET.get("search", "")
        if searchInputText:
            #前方一致検索
            tasks = context["tasks"].filter(title__startswith=searchInputText)

        #context辞書に以下を設定
        context["tasks"] = tasks
        context["search"] = searchInputText
        return context

#タスク詳細に関するclass
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"

#タスク追加に関するclass
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    #fields = "__all__" #['uesr', 'title',...]
    fields = ['title', 'completed', 'description']
    success_url = reverse_lazy("tasks")

    #タスク作成時、作成者が所有者になるよう設定
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
        
#タスク更新に関するclass
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = "__all__" #['uesr', 'title',...]
    success_url = reverse_lazy("tasks")

#タスク削除に関するclass
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    fields = "__all__" #['uesr', 'title',...]
    success_url = reverse_lazy("tasks")

class TaskListLoginView(LoginView):
    fields = "__all__"
    template_name= "todoapp/login.html"
    
    def get_success_url(self):
        return reverse_lazy("tasks")

#画面からユーザ追加をする設定
class RegisterTodoapp(FormView):
    template_name = "todoapp/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("tasks")
    
    #ユーザ追加時に保存する処理
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)