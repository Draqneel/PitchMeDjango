from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from core.forms import FilterForm
from core.models import Event, UserFilter, City, Notification


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'core/index.html'
    queryset = Event.objects.all()
    context_object_name = 'events'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)
        ctx['form'] = FilterForm()
        ctx['notifications'] = self.request.user.notifications.filter(is_read=False)
        return ctx


class EventDetail(LoginRequiredMixin, DetailView):
    template_name = 'core/event_detail_template.html'
    model = Event
    context_object_name = 'event'


class SearchListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'core/index.html'
    context_object_name = 'events'

    def get_queryset(self):
        city = self.request.GET.get('city')
        start = self.request.GET.get('start_bound')
        end = self.request.GET.get('end_bound')
        themes = self.request.GET.getlist('themes')
        if 'save' in self.request.GET:
            item = UserFilter.objects.create(
                user=self.request.user,
                city=City.objects.get(pk=city),
                dt_start=start,
                dt_end=end,
            )
            item.themes.set(themes)
            item.save()
        query_set = self.model.objects.filter(
            Q(city__pk=city) &
            Q(dt_start__gte=start) &
            Q(dt_start__lte=end) &
            Q(themes__in=themes)
        ).distinct()

        return query_set

    def clean(self):
        if 'save' in self.request.GET:
            user_id = self.request.GET.get('pk')
            city = self.request.GET.get('city')
            start = self.request.GET.get('start_bound')
            end = self.request.GET.get('end_bound')
            themes = self.request.GET.getlist('themes')
            item = UserFilter(
                user=User.objects.get(pk=user_id),
                city=City.objects.get(pk=city),
                dt_start=start,
                dt_end=end,
                themes=themes
            )
            item.save()

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(SearchListView, self).get_context_data(**kwargs)
        ctx['form'] = FilterForm()
        return ctx


class CreateUserFilterView(LoginRequiredMixin, CreateView):
    model = UserFilter


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    context_object_name = 'notifications'
    template_name = 'core/notifications_list_template.html'

    def get_queryset(self):
        query_set = self.request.user.notifications.filter(is_read=False)
        return query_set


class NotificationDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'core/notifications_list_template.html'
    model = Notification
    success_url = reverse_lazy('core:notifications')
