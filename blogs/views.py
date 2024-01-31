from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from blogs.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'body', 'image',)
    context_object_name = 'objects_list'
    success_url = reverse_lazy('blogs:list')

    def get_initial(self):
        return {'user': self.request.user}

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog
    context_object_name = 'objects_list'

    def get_queryset(self):
        """Метод получения данных всех постов"""
        queryset = super().get_queryset()
        queryset = queryset.filter()
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'body')
    success_url = reverse_lazy('blogs:list')


class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blogs/blog_confirm_delete.html'
    success_url = reverse_lazy('blogs:list')
