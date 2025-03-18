"""
URL configuration for medicineProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from medicine_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about_us/', views.about, name='about'),
    path('how_to_be_donors/', views.donors, name='donors'),
    path('planing_donor/', views.PlanView.as_view(), name='planing_donor'),
    path('login/', views.SignInView.as_view(), name='login'),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('schedule_donation/', views.schedule_donation, name='schedule_donation'),
    path('update_donor_info/', views.update_donor_info, name='update_donor_info'),
    path('check_donor_info/', views.check_donor_info, name='check_donor_info'),
    path('protivopokazaniya/', views.contraindications, name='contraindications'),
    path('planned_donations/', views.planned_donations, name='planned_donations'),
    path('api/add_data/', views.NewData.as_view(), name='add_data'),
    path('api/delete_data/<int:pk>/', views.DataDeleteView.as_view(), name='delete_data'),
    path('api/planned-donations/', views.GetData.as_view(), name='get_data'),
    path('api/is_staff/',views.IsStaff.as_view(), name='is_staff')
] 
