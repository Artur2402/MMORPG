from django.urls import path
from .views import Index, Search, PostDetail, PostCreate, EditPost, DeletePost, Responses, Respond, response_accept, response_reject
from django.views.generic import TemplateView

urlpatterns = [
    path('index/', Index.as_view(), name='index'),
    path('post/<int:pk>/', PostDetail.as_view(), name='detail'),
    path('search/', Search.as_view(), name='search'),
    path('create/', PostCreate.as_view(), name='create'),
    path('<int:pk>/edit/', EditPost.as_view(), name='edit'),
    path('<int:pk>/delete/', DeletePost.as_view(), name='delete'),
    path('responses', Responses.as_view(), name='responses'),
    path('responses/<int:pk>', Responses.as_view(), name='responses'),
    path('respond/<int:pk>', Respond.as_view(), name='respond'),
    path('response/accept/<int:pk>', response_accept),
    path('response/reject/<int:pk>', response_reject),
    path('contact/', TemplateView.as_view(template_name='contact.html')),
    path('privacy-policy/', TemplateView.as_view(template_name='privacy.html')),
    path('terms/', TemplateView.as_view(template_name='terms.html'))
]
