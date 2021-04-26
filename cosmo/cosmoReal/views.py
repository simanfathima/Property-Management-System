from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from .models import Buy,Rent,Filter,Tenant,Appointment
from .forms import PostForm,SignUpForm,MaintenanceForm,PaymentForm,AppointmentForm,FilterForm
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def myaccount(request):
    return render(request, 'myaccount.html')
        


class HomePageView(TemplateView):
    template_name = 'home.html'

def buy_list(request):
    buys = Buy.objects.filter(posted_date__lte=timezone.now()).order_by('posted_date')
    return render(request, 'buy_list.html', {'buys': buys})

def buy_detail(request,pk):
    buy = get_object_or_404(Buy, pk=pk)
    return render(request, 'buy_detail.html', {'buy': buy})

def rent_list(request):
    rents = Rent.objects.filter(posted_date__lte=timezone.now()).order_by('posted_date')
    return render(request, 'rent_list.html', {'rents': rents})

def rent_detail(request,pk):
    rent = get_object_or_404(Rent, pk=pk)
    return render(request, 'rent_detail.html', {'rent': rent})

def sell_list(request):
    sells = Sell.objects.filter(posted_date__lte=timezone.now()).order_by('posted_date')
    return render(request, 'sell_list.html', {'sells': sells})

def sell_detail(request,pk):
    sell = get_object_or_404(Sell, pk=pk)
    return render(request, 'sell_detail.html', {'sell': sell})

def post_new(request):
     if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            sell = form.save(commit=False)
            sell.posted_date = timezone.now()
            sell.save()
            mail= EmailMultiAlternatives('Selling Request Received','Dear {name}\nYour request for to sell your property at {loc} has been successfully received!'.format(name=sell.seller,loc=sell.location),settings.EMAIL_HOST_USER,[sell.email])
            mail.send()
            return redirect('/')
     else:
        form = PostForm()
     return render(request, 'post_edit.html', {'form': form})


def searchbuy(request):
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(locality__icontains=query) | Q(description__icontains=query) | Q(city__icontains=query) | Q(use__icontains=query) | Q(proptype__icontains=query)

            results= Buy.objects.filter(lookups).distinct()

            context={'results': results,'submitbutton': submitbutton}

            return render(request, 'searchbuy.html', context)

        else:
            return render(request, 'searchbuy.html')

    else:
        return render(request, 'searchbuy.html')

def searchrent(request):
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(locality__icontains=query) | Q(description__icontains=query) | Q(city__icontains=query) | Q(use__icontains=query) | Q(proptype__icontains=query)

            results= Rent.objects.filter(lookups).distinct()

            rentsearch={'results': results,'submitbutton': submitbutton}

            return render(request, 'searchrent.html', rentsearch)

        else:
            return render(request, 'searchrent.html')

    else:
        return render(request, 'searchrent.html')

def tenant_list(request):
        username = None
        if request.user.is_authenticated:
           username = request.user.username

        tenant= Tenant.objects.filter(name__username=username)
        return render(request, 'tenant_list.html', {'tenant': tenant})

def tenant_detail(request,pk):
	tenant = get_object_or_404(Tenant,pk=pk)
	return render(request, 'tenant_detail.html', {'tenant': tenant})

def maintenance(request) :
        if request.user.is_authenticated:
           username = request.user.username
        
        tenant = Tenant.objects.get(name__username=username)
        if(tenant.due!=0):
            return render(request, 'nomaintenance.html')
        else:
            if request.method == "POST":
                form = MaintenanceForm(request.POST,instance=tenant)
                if form.is_valid():   
                   maint=form.save(request.POST)
                   maint.save()
                   mail= EmailMultiAlternatives('Maintenance Request Received','Your maintenance request for {issue} has been successfully received!'.format(issue=maint.issues),settings.EMAIL_HOST_USER,[tenant.email])
                   mail.send()
                   Tenant.objects.filter(name__username=username).update(request='Pending Requests')
                   return redirect('tenant_list')
            else:
                form = MaintenanceForm()
            return render(request, 'maintenance.html', {'form':form})
            

def payment(request) :
        if request.user.is_authenticated:
                username = request.user.username

        tenant = Tenant.objects.get(name__username=username)
        if(tenant.due==0):
                return render(request, 'nopayment.html')
        else:
                if request.method == "POST":
                   
                   form = PaymentForm(request.POST)
                   if form.is_valid():
                     pay = form.save(commit=False)
                     if(pay.due != tenant.due):
                         return redirect('paymentfailed')
                     else:
                         mail= EmailMultiAlternatives('Rent Payment Successful','You have Successfully Paid Your Rent Amount : {amt}'.format(amt=pay.due),settings.EMAIL_HOST_USER,[tenant.email])
                         mail.send()
                         Tenant.objects.filter(name__username=username).update(due=0)
                         return redirect('tenant_list')
                
                else:
                    form = PaymentForm()
                    
                return render(request, 'payment.html', {'form':form})
def paymentfailed(request):
      return render(request,'paymentfailed.html')

def bookappointment(request):
     if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.posted_date = timezone.now()
            app.save()
            mail= EmailMultiAlternatives('Booking Successful','You have Successfully Booked an Appointment with co$mo Real Properties on {date}'.format(date=app.date),settings.EMAIL_HOST_USER,[app.email])
            mail.send()
            return redirect('success')
     else:
        form = AppointmentForm()
     return render(request, 'book.html', {'form': form})

def success(request):
        return render(request,'success.html')

def sortrent(request):
        rents = Rent.objects.filter(posted_date__lte=timezone.now()).order_by('price')
        return render(request,'rent_list.html',{'rents':rents})

def sortrentde(request):
        rents = Rent.objects.filter(posted_date__lte=timezone.now()).order_by('-price')
        return render(request,'rent_list.html',{'rents':rents})

def sortbuy(request):
        buys = Buy.objects.filter(posted_date__lte=timezone.now()).order_by('price')
        return render(request,'buy_list.html',{'buys':buys})

def sortbuyde(request):
        buys = Buy.objects.filter(posted_date__lte=timezone.now()).order_by('-price')
        return render(request,'buy_list.html',{'buys':buys})

def buyfilter(request):
     if request.method == "POST":
        form = FilterForm(request.POST)
        if form.is_valid():
            fil = form.save(commit=False)
            fil.save()

            if(fil.city == None):
                if(fil.proptype == None):
                    if(fil.use == None):
                      lookups= posted_date__lte=timezone.now()
                    else:
                      lookups = Q(use__icontains=fil.use)
                else:
                    if(fil.use == None):
                      lookups= Q(proptype__icontains=fil.proptype)
                    else:
                      lookups = Q(proptype__icontains=fil.proptype) & Q(use__icontains=fil.use)

            elif(fil.proptype == None):
                if(fil.city == None):
                    if(fil.use == None):
                      lookups= posted_date__lte=timezone.now()
                    else:
                      lookups = Q(use__icontains=fil.use)
                else:
                    if(fil.use == None):
                      lookups= Q(city__icontains=fil.city)
                    else:
                      lookups = Q(city__icontains=fil.city) & Q(use__icontains=fil.use)
            
            elif(fil.use == None):
                if(fil.city == None):
                    if(fil.proptype == None):
                      lookups= posted_date__lte=timezone.now()
                    else:
                      lookups = Q(proptype__icontains=fil.proptype)
                else:
                    if(fil.proptype == None):
                      lookups= Q(city__icontains=fil.city)
                    else:
                      lookups = Q(city__icontains=fil.city) & Q(proptype__icontains=fil.proptype) 
 
            elif(fil.city != None):
                if(fil.proptype == None):
                    if(fil.use == None):
                      lookups= Q(city__icontains=fil.city)
                    else:
                      lookups = Q(city__icontains=fil.city) & Q(use__icontains=fil.use)
                else:
                    if(fil.use == None):
                      lookups= Q(city__icontains=fil.city) & Q(proptype__icontains=fil.proptype)
                    else:
                      lookups = Q(proptype__icontains=fil.proptype) & Q(use__icontains=fil.use) & Q(proptype__icontains=fil.proptype)
            
            elif(fil.proptype != None):
                if(fil.city == None):
                    if(fil.use == None):
                      lookups= Q(proptype__icontains=fil.proptype)
                    else:
                      lookups = Q(proptype__icontains=fil.proptype) & Q(use__icontains=fil.use)
                else:
                    if(fil.use == None):
                      lookups= Q(city__icontains=fil.city) & Q(proptype__icontains=fil.proptype)
                    else:
                      lookups = Q(proptype__icontains=fil.proptype) & Q(use__icontains=fil.use) & Q(proptype__icontains=fil.proptype)

            elif(fil.use != None):
                if(fil.city == None):
                    if(fil.proptype == None):
                      lookups= Q(use__icontains=fil.use)
                    else:
                      lookups = Q(proptype__icontains=fil.proptype) & Q(use__icontains=fil.use)
                else:
                    if(fil.use == None):
                      lookups= Q(city__icontains=fil.city) & Q(use__icontains=fil.use)
                    else:
                      lookups = Q(proptype__icontains=fil.proptype) & Q(use__icontains=fil.use) & Q(proptype__icontains=fil.proptype)
            

            results= Buy.objects.filter(lookups)
            return render(request,'buy_list.html',{'buys':results})
     else:
        form = FilterForm()
     return render(request, 'filter.html', {'form': form})

def rentfilter(request):
     if request.method == "POST":
        form = FilterForm(request.POST)
        if form.is_valid():
            fil = form.save(commit=False)
            fil.save()

            if(fil.city == None):
                if(fil.proptype == None):
                    if(fil.use == None):
                      lookups= posted_date__lte=timezone.now()
                    else:
                      lookups = Q(use__icontains=fil.use)
                else:
                    if(fil.use == None):
                      lookups= Q(proptype__icontains=fil.proptype)
                    else:
                      lookups = Q(proptype__icontains=fil.proptype) & Q(use__icontains=fil.use)

            elif(fil.proptype == None):
                if(fil.city == None):
                    if(fil.use == None):
                      lookups= posted_date__lte=timezone.now()
                    else:
                      lookups = Q(use__icontains=fil.use)
                else:
                    if(fil.use == None):
                      lookups= Q(city__icontains=fil.city)
                    else:
                      lookups = Q(city__icontains=fil.city) & Q(use__icontains=fil.use)
            
            elif(fil.use == None):
                if(fil.city == None):
                    if(fil.proptype == None):
                      lookups= posted_date__lte=timezone.now()
                    else:
                      lookups = Q(proptype__icontains=fil.proptype)
                else:
                    if(fil.proptype == None):
                      lookups= Q(city__icontains=fil.city)
                    else:
                      lookups = Q(city__icontains=fil.city) & Q(proptype__icontains=fil.proptype) 
 
            elif(fil.city != None):
                if(fil.proptype == None):
                    if(fil.use == None):
                      lookups= Q(city__icontains=fil.city)
                    else:
                      lookups = Q(city__icontains=fil.city) & Q(use__icontains=fil.use)
                else:
                    if(fil.use == None):
                      lookups= Q(city__icontains=fil.city) & Q(proptype__icontains=fil.proptype)
                    else:
                      lookups = Q(proptype__icontains=fil.proptype) & Q(use__icontains=fil.use) & Q(proptype__icontains=fil.proptype)
            
            elif(fil.proptype != None):
                if(fil.city == None):
                    if(fil.use == None):
                      lookups= Q(proptype__icontains=fil.proptype)
                    else:
                      lookups = Q(proptype__icontains=fil.proptype) & Q(use__icontains=fil.use)
                else:
                    if(fil.use == None):
                      lookups= Q(city__icontains=fil.city) & Q(proptype__icontains=fil.proptype)
                    else:
                      lookups = Q(proptype__icontains=fil.proptype) & Q(use__icontains=fil.use) & Q(proptype__icontains=fil.proptype)

            elif(fil.use != None):
                if(fil.city == None):
                    if(fil.proptype == None):
                      lookups= Q(use__icontains=fil.use)
                    else:
                      lookups = Q(proptype__icontains=fil.proptype) & Q(use__icontains=fil.use)
                else:
                    if(fil.use == None):
                      lookups= Q(city__icontains=fil.city) & Q(use__icontains=fil.use)
                    else:
                      lookups = Q(proptype__icontains=fil.proptype) & Q(use__icontains=fil.use) & Q(proptype__icontains=fil.proptype)
            

            results= Rent.objects.filter(lookups)
            return render(request,'rent_list.html',{'rents':results})
     else:
        form = FilterForm()
     return render(request, 'filter.html', {'form': form})
        
def rent_recommend(request,pk):
    result_list = []
    rent = get_object_or_404(Rent, pk=pk)
    rents = Rent.objects.filter(posted_date__lte=timezone.now()).order_by('posted_date')
    for i in rents:
       if(i.price-rent.price <= 6000 and i.propid!=rent.propid):
           result_list.append(i.propid)
    results= Rent.objects.filter(propid__in=result_list)
    return render(request, 'rent_list.html', {'rents': results})








