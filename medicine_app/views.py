from django.shortcuts import render, redirect
from medicine_app.forms import *
from medicine_app.models import *
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timedelta
from medicine_app.serializers import *
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response

def contraindications(request):
    return render(request, 'protivopokazaniya.html')

def index(request):
    blood_groups = BloodGroup.objects.all()
    if request.user.is_staff and request.method == 'POST':
        form = BloodGroupForm(request.POST)
        if form.is_valid():
            group = form.cleaned_data['group']
            is_active = form.cleaned_data['is_active']
            BloodGroup.objects.filter(group=group).update(is_active=is_active)
            return redirect('/')
    else:
        form = BloodGroupForm()
    context = {
        'blood_groups': blood_groups,
        'form': form if request.user.is_staff else None,
    }
    return render(request, 'index.html', context)



def planned_donations(request):
    return render(request, 'planned-donations.html')

def about(request):
    return render(request, 'o_nas.html')

def donors(request):
    return render(request, 'kak_stat_donorom.html')

def logining(request):
    return render(request, 'login.html')

@login_required
def profile(request):
    username = request.user.username
    filtered_data = Plan.objects.filter(username=username)
    filtered_data2 = CreateUser.objects.filter(username=username)
    return render(request, 'profile.html', {'filtered_data': filtered_data, 'filtered_data2': filtered_data2})

class PlanView(View):
    def get(self, request):
        form = Appointment()
        return render(request, 'planirovanie.html', context={
            'form': form,
        })

    def post(self, request):
        if request.method == 'POST':
            form = Appointment(request.POST)
            if form.is_valid():
                username = request.user.username
                blood_date = form.save(commit=False)
                blood_date.username = username
                try:
                    blood_date.save()
                except:
                    model = Plan.objects.get(username=username)
                    model.weight = blood_date.weight
                    model.height = blood_date.height
                    model.age = blood_date.age
                    model.group_of_blood = blood_date.group_of_blood
                    model.save()
                return redirect('schedule_donation')
        else:
            form = Appointment()
        return render(request, 'planirovanie.html', {'form': form})

class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'register.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                user.save()
                return HttpResponseRedirect('/')
        return render(request, 'register.html', context={
            'form': form,
        })

class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'login.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                form.add_error(None, "Неправильный пароль или указанная учётная запись не существует!")
                return render(request, "login.html", {"form": form})
        return render(request, 'login.html', context={
            'form': form,
        })

@login_required
def schedule_donation(request):
    if request.method == 'POST':
        donation_date = request.POST.get('donation_date')
        donation_time = request.POST.get('donation_time')
        
        if donation_date and donation_time:
     
            donation_datetime = datetime.strptime(f"{donation_date} {donation_time}", "%Y-%m-%d %H:%M")
            
           
            if donation_datetime.weekday() != 6:
       
                messages.success(request, '')
                return redirect('index')
            else:
                messages.error(request, 'Донации не проводятся по воскресеньям')
        else:
            messages.error(request, 'Пожалуйста, выберите дату и время донации')
    
    today_date = datetime.now().strftime('%Y-%m-%d')
    

    time_slots = []
    start_time = datetime.strptime("08:30", "%H:%M")
    end_time = datetime.strptime("16:30", "%H:%M")
    
    while start_time <= end_time:
        time_slots.append(start_time.strftime("%H:%M"))
        start_time += timedelta(minutes=40)
    
    return render(request, 'schedule_donation.html', {
        'today_date': today_date,
        'time_slots': time_slots
    })

@login_required
def check_donor_info(request):
    username = request.user.username
    donor_info = Plan.objects.filter(username=username).first()
    if donor_info:
        return redirect('schedule_donation')
    else:
        return redirect('planing_donor')

@login_required
def update_donor_info(request):
    if request.method == 'POST':
        form = Appointment(request.POST)
        if form.is_valid():
            username = request.user.username
            try:
                model = Plan.objects.get(username=username)
                model.weight = form.cleaned_data['weight']
                model.height = form.cleaned_data['height']
                model.age = form.cleaned_data['age']
                model.group_of_blood = form.cleaned_data['group_of_blood']
                model.save()
                messages.success(request, '')
            except Plan.DoesNotExist:
                blood_date = form.save(commit=False)
                blood_date.username = username
                blood_date.save()
                messages.success(request, '')
            
            # Проверяем источник запроса
            if request.POST.get('source') == 'profile':
                return redirect('profile')
            else:
                return redirect('schedule_donation')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
            return render(request, 'planirovanie.html', {'form': form})
    return redirect('planing_donor')

class PlanView(View):
    def get(self, request):
        form = Appointment()
        source = request.GET.get('source', '')
        return render(request, 'planirovanie.html', context={
            'form': form,
            'source': source,
        })

    def post(self, request):
        if request.method == 'POST':
            form = Appointment(request.POST)
            if form.is_valid():
                username = request.user.username
                blood_date = form.save(commit=False)
                blood_date.username = username
                try:
                    blood_date.save()
                except:
                    model = Plan.objects.get(username=username)
                    model.weight = blood_date.weight
                    model.height = blood_date.height
                    model.age = blood_date.age
                    model.group_of_blood = blood_date.group_of_blood
                    model.save()
                
                # Проверяем источник запроса
                if request.POST.get('source') == 'profile':
                    return redirect('profile')
                else:
                    return redirect('schedule_donation')
        else:
            form = Appointment()
        return render(request, 'planirovanie.html', {'form': form})

class NewData(APIView):
    def post(self, request):
        username = request.data.get('username')

        try:
            plan = Plan.objects.get(username=username)
        except Plan.DoesNotExist:
            return Response({"error": "Plan not found"}, status=status.HTTP_400_BAD_REQUEST)

        request.data["username"] = plan

        date, created = Data.objects.update_or_create(
            username=plan,
            defaults=request.data
        )

        serializer = DataSerializer(date)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
class GetData(APIView):
    def get(self, request):
         users = Plan.objects.select_related('data').all()
         print(users)
         serializer = PlannedSerializer(users, many=True)
         return Response(serializer.data)

class DataDeleteView(generics.DestroyAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

class IsStaff(APIView):
    def post(self, request):
        username = request.data.get('username')
        is_staff = CreateUser.objects.get(username=username)
        serializer = IsStaffSerializer(is_staff)
        print(serializer.data)
        return Response(serializer.data)
