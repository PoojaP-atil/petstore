from django.shortcuts import render, redirect
from django.views.generic import ListView,DetailView, CreateView
from petapp.models import pet,register,cart,order,orderdetails,payment
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse
from petapp.forms import form
from django.contrib.auth.hashers import make_password,check_password
from datetime import date

# Create your views here.
class PetListView(ListView):
    model = pet
    template_name = 'petlist.html'
    context_object_name = 'petobj'

class PetDetailView(DetailView):
    model = pet
    template_name = 'petdetail.html'
    context_object_name = 'petdetail'

class PetListViewCM(ListView): 
    queryset = pet.pets.get_pet_age()   
    template_name = 'petlist.html'
    context_object_name = 'petobj'

def searchbox(request):
    if request.method == "POST":
        sq= request.POST.get('search_query')
        result = pet.pets.filter(Q(Species__icontains= sq) | Q(Breed__icontains= sq) | Q(Name__icontains= sq) | Q(Age__iexact = sq) |Q(Gender__iexact= sq) |Q(Height__iexact= sq) |Q(Weight__iexact= sq) |Q(Price__iexact= sq))
        return render(request, 'petlist.html', {'petobj':result})

def registration(request):
    if request.method=="GET":
        return render(request,"register.html")
    elif request.method=="POST":
        name = request.POST.get("name")
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        address = request.POST.get("address")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        phoneno = request.POST.get("phone")
        email =request.POST.get("email")
        password= request.POST.get("pass")
        passw = make_password(password)
        regobj = register(Name=name,Gender=gender,Age=age,Address=address,State=state,Pincode=pincode,PhoneNo=phoneno,Email=email,Password=passw)
        regobj.save()

        return HttpResponse("Customer registered Successfully")

def services(request):
    return render(request, 'services.html')

def login(request):
    if request.method=="GET":
        return render(request,"login.html")
    elif request.method=="POST":
        reg = register.objects.filter(Email = request.POST.get("email"))

        if reg:
            regobj = register.objects.get(Email=request.POST.get("email"))
            passfe = request.POST.get("pass")
            flag = check_password(passfe,regobj.Password)

            if True:
                request.session['email'] = request.POST.get('email')
                return redirect("../petlist/")

            else:
                return HttpResponse("Wrong username or password")  

def logout(request):
    request.session['email'] = ''
    return redirect('../login/')  
    # user = request.session['username']
    # user.delete()
    # return redirect('../login/')

def addcart(request):
    productid = request.POST['pid']
    petobj = pet.pets.get(id=productid)
    user = request.session['email']
    custobj = register.objects.get(Email =user)
    flag = cart.objects.filter(customerid = custobj.id,productid = petobj.id)
    if flag:
        cobj = cart.objects.get(customerid = custobj.id,productid = petobj.id)
        cobj.quantity = cobj.quantity + 1;
        cobj.totalamount = cobj.quantity * petobj.Price;
        cobj.save()
    else: 
        cobj = cart(quantity=1, totalamount= petobj.Price, customerid = custobj, productid = petobj)
        cobj.save()

    cartobjdisplay = cart.objects.filter(customerid = custobj.id)
    return render(request,'petlist.html',{'session': user,'petobj':pet.pets.all()})

def viewcart(request):
    user = request.session['email']
    custobj = register.objects.get(Email =user)
    cartobjdisplay = cart.objects.filter(customerid = custobj.id)
    return render(request,'cart.html',{'session': user,'petobj':cartobjdisplay})
    
def quantity(request): 
    user = request.session['email']
    custobj = register.objects.get(Email=user)
    pid = request.POST.get("pid") 
    petobj = pet.pets.get(id=pid)
    bq = request.POST['buttonquantity']
    if bq =='-': 
        cartobj = cart.objects.get(customerid = custobj.id,productid = pid)
        cartobj.quantity = cartobj.quantity - 1
        cartobj.totalamount = petobj.Price * cartobj.quantity
        cartobj.save()
        if cartobj.quantity == 0:
            cartobj.delete()
    else: 
        cartobj = cart.objects.get(customerid = custobj.id,productid = pid)
        cartobj.quantity = cartobj.quantity + 1
        cartobj.totalamount = petobj.Price * cartobj.quantity
        cartobj.save()
    cartobjdisplay = cart.objects.filter(customerid = custobj.id)
    return render(request,'cart.html',{'session': user,'petobj':cartobjdisplay})

def summarypage(request):
    user = request.session['email']
    cobj = register.objects.get(Email =user)
    cartobj = cart.objects.filter(customerid = cobj.id)
    totalbill = 0

    for i in cartobj:
        totalbill = i.totalamount + totalbill
    return render(request,'summary.html',{'session': user,'petobj':cartobj,'totalbill':totalbill})

def paymentpage(request):
    user = request.session['email']
    cobj = register.objects.get(Email=user)
    name = request.POST.get('name')
    address= request.POST.get('address')
    phoneno = int(request.POST.get('phoneno'))
    city = request.POST.get('city')
    state = request.POST.get('state')
    pincode = int(request.POST.get('pincode'))
    Totalbillamount = request.POST.get('totalbillamount')
    bill = float(Totalbillamount)
   
    orderobj = order(Name= name, City = city, State=state, Address = address, PhoneNo = phoneno, Pincode = pincode, totalbillamount = bill)
  
    cartobj = cart.objects.filter(customerid = cobj.id)
    totalbill = 0

    for i in cartobj:
        dateobj = date.today()
        datedata = str(dateobj).replace('-','')
        orderno = str(orderobj.id) + datedata
        totalbill = i.totalamount + totalbill
        orderobj.ordernumber = orderno
        orderobj.save()

    return render(request,'payment.html',{'orderobj':orderobj,'session': user,'petobj':cartobj,'totalbill':totalbill})

def orderplaced(request,tid,orderid):
    user = request.session['email']
    cobj = register.objects.get(Email=user)
    cartobj = cart.objects.filter(customerid = cobj.id)
    totalbill = i.totalamount + totalbill

    orderobj = orderdetails.objects.get(orderno = orderid)
    paymentobj = payment(transactionid = tid, paymentstatus='paid',customerid=cobj,orderid = orderobj)
    paymentobj.save()
    
    for i in cartobj:
        orderdetailobj = orderdetails(paymentid = paymentobj,ordernumber = orderid, productid = i.productid,customerid = i.customerid,quantity = i.quantity,totalprice = i.totalamount)
        orderdetailobj.save()
        i.delete()
    return render(request,'order_placed.html',{'session': user,'orderno' : orderobj ,'totalbill' : totalbill})

def orderplaced1(request, tid, orderid):
    print("Order Placed View Reached")
    user = request.session['email']
    cobj = register.objects.get(Email=user)
    cartobj = cart.objects.filter(customerid=cobj.id)
    totalbill = 0
    for i in cartobj:
            totalbill = totalbill + i.totalamount
    orderobj = orderdetails.objects.get(orderno=orderid)
    paymentobj = payment(transactionid=tid, paymentstatus='paid', customerid=cobj, orderid=orderobj, paymentmode = 'Paypal')
    paymentobj.save()

    for i in cartobj:
        orderdetailobj = orderdetails(paymentid=paymentobj, ordernumber=orderid, productid=i.productid, customerid=i.customerid, quantity=i.quantity, totalprice=i.totalamount)
        orderdetailobj.save()

    cartobj.delete()
    return render(request, 'order_placed.html')