from django.contrib import messages
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth,User
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.base import View

from myapp.models import Profile, Products
from myapp.tokens import account_activation_token
from PayTm import Checksum
MERCHANT_KEY = "i4Qc9KFWqeLapGSz"



def Index(request):

    return render(request,"myapp/index.html")

def Thanks(request):
    return render(request,"myapp/Thanks.html")

def Login(request):
    if request.method == 'POST':
        un = request.POST['uname']
        pass1 = request.POST['pass']

        user = auth.authenticate(username=un,password=pass1)
        if user is not None:
            auth.login(request,user)
            request.session['username'] = un
            request.session['pk']=user.pk
            request.session.set_expiry(300)
            return render(request,'myapp/index.html',{"data":un,"Flag":True})
        else:
            messages.info(request,'Invalid credentials')
            return render(request,'myapp/login.html',{"status":"Invalid credentials"})
    else:
        return render(request,'myapp/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/Thanks')


def Register(request):
    if request.method == 'POST':
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        em = request.POST['email']
        un = request.POST['uname']
        pass1 = request.POST['pass']
        pass2 = request.POST['pass2']
        country = request.POST['country']

        if pass1 == pass2:

            if User.objects.filter(username=un).exists():
                messages.info(request, 'Username already Taken')
                # print("Username Taken")
                return redirect('/Register')
            elif User.objects.filter(email=em).exists():
                messages.info(request, "Email Taken")
                # print("Username Taken")
                return redirect('/Register')
            else:
                user = User.objects.create_user(username=un, email=em, password=pass1, first_name=fn, last_name=ln)
                user.is_active = False  # Deactivate account till it is confirmed
                user.save()


                # print('user created !')

                current_site = get_current_site(request)
                subject = 'Activate Your MySite Account'
                message = render_to_string('myapp/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                #user.email_user(subject, message)
                # send_mail(
                #     "Hello User",
                #     "Welcome to Email Confirmation",
                #     "corejavabtes@gmail.com",
                #     [em],
                #     fail_silently=False,
                # )
                send_mail(
                        subject,
                        message,
                        'corejavabtes@gmail.com',
                        [em],
                        fail_silently=False,
                    )

                messages.success(request, ('Please Confirm your email to complete registration.'))
                return redirect('/Login')

                # return render(request,'index.html')

        else:
            print('password not matched !')
            messages.info(request, 'register')

        return redirect('/Register')

    else:

        return render(request,"myapp/register.html")

def UserProfile(request):
    pkk = None
    unn = None
    if request.method == 'POST':
        hob = request.POST['hobby']
        IA = request.POST['IA']
        loc = request.POST['loc']
        FA = request.POST['FA']
        if request.session.has_key('pk'):
            pkk = request.session['pk']
            unn = request.session['username']
            p = User.objects.get(pk=pkk)
            obj = Profile(hobby=hob, interst_area=IA, Puser =p,location=loc, fav_author=FA)
            obj.save()
            return render(request, "myapp/Thanks.html",{"data":unn,"Flag":True})
        else:
            return render(request,"myapp/Profile.html",{"data":"Login Required"})

    else:

        return render(request,"myapp/Profile.html",{"data":unn,"Flag":True})

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            #uid = force_text(urlsafe_base64_decode(uidb64))
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profilee.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            print("confirmed",user.is_active)
            return render(request,'myapp/index.html',{"data":user.first_name,"Flag":True})
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('/Thanks')


def paymentMode(request):
    param_dict = {
        "MID": "Zjfrqs35148164910675",
        "ORDER_ID": "1012",
        "CUST_ID": "809",
        "TXN_AMOUNT": "2",
        "CHANNEL_ID": "WEB",
        "INDUSTRY_TYPE_ID": "Retail",
        "WEBSITE": "WEBSTAGING",
        #"CALLBACK_URL": "http/127.0.0.1:8000/handleRequest/",
        "CALLBACK_URL":"https://merchant.com/callback/"

    }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)

    return render(request,'myapp/paytm.html',{'params':param_dict})

@csrf_exempt
def handlerequest(request):
    #paytm will send you post request here
    return redirect('/Thanks')


from .Model_Class import Model
import requests
import json
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImJ0ZXNzdHVkZW50c0BnbWFpbC5jb20iLCJyb2xlIjoiVXNlciIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL3NpZCI6IjQxNjEiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3ZlcnNpb24iOiIxMDkiLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL2xpbWl0IjoiMTAwIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9tZW1iZXJzaGlwIjoiQmFzaWMiLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL2xhbmd1YWdlIjoiZW4tZ2IiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiIyMDk5LTEyLTMxIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9tZW1iZXJzaGlwc3RhcnQiOiIyMDIwLTA0LTE1IiwiaXNzIjoiaHR0cHM6Ly9hdXRoc2VydmljZS5wcmlhaWQuY2giLCJhdWQiOiJodHRwczovL2hlYWx0aHNlcnZpY2UucHJpYWlkLmNoIiwiZXhwIjoxNTg3OTc4MzY5LCJuYmYiOjE1ODc5NzExNjl9.0XFksvKli00uxxNiReq3pLTO5s--oImtzUQfDa73Drk&format=json&language=en-gb"
dict = {}
def MedicApi(request):
    list = []

    url = "https://healthservice.priaid.ch/symptoms?token="+token

    response = requests.get(url)
    # source_path = Path("https://jsonplaceholder.typicode.com/todos")
    document = json.loads(response.text)
    for x in document:
        id = x['ID']
        name = x['Name']
        #list.append(name)
        dict.update({name:id})
       # print("......",dict)
    return render(request, "myapp/medicapi.html", {"dict":dict})

def Diagnosis(request):

    listt = []
    print("working")
    if request.method == 'POST':
        sympId = request.POST['symid']
        age = request.POST['age']
        gen = request.POST['gender']
        url1 = "https://healthservice.priaid.ch/diagnosis?symptoms=["+sympId+"]&gender="+gen+"&year_of_birth="+age+"&token=" + token
        response = requests.get(url1)
        document = json.loads(response.text)
        for x in document:
            issue = x['Issue']
            id = issue['ID']
            name = issue['Name']
            icd = issue['IcdName']
            pname = issue['ProfName']

            obj = Model(name,icd,pname)  #Object Creation
            listt.append(obj)
            #specialization = x['Specialisation']


    return render(request, "myapp/medicapi.html",{"issue":listt,"dict":dict})

def pproducts(request):
    result = Products.objects.all()
    #print(result)
    return render(request,'myapp/Productss.html',{'result':result})

def display(request,pk):

    print(pk)
    result = Products.objects.filter(pk=pk)

    return render(request,'myapp/Cart.html',{'result':result})