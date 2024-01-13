from django.shortcuts import render, redirect
from django.views.generic import ListView,DetailView, CreateView
from petapp.models import pet,register,cart
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

def paymentpage2(request):
    user = request.session['email']
    cobj = register.objects.get(Email=user)
    Name = request.POST.get('name')
    Address= request.POST.get('address')
    Phoneno = int(request.POST.get('phoneno'))
    City = request.POST.get('city')
    State = request.POST.get('state')
    Pincode = int(request.POST.get('pincode'))
    Totalbillamount = float(request.POST.get('totalbillamount'))
    orderobj = order(name= Name, city = City, state=State, address = Address, phoneno = Phoneno, pincode = Pincode, totalbillamount = Totalbillamount)
    orderobj.save()

    dateobj = date.today()

    print(dateobj)
    datedata = str(dateobj).replace('-','')

    orderno = str(orderobj.id) + datedata
    orderobj.ordernumber = orderno
    orderobj.save()

    cartobj = cart.objects.filter(customerid = cobj.id)

    for i in cartobj:
        orderdetailobj = orderdetail(ordernumber = orderno, productid = i.productid,customerid = i.customerid,quantity = i.quantity,totalprice = i.totalamount)
        orderdetailobj.save()
        i.delete()

    orderdetialobjectdisplay = orderdetail.objects.filter()
    return render(request,'payment.html',{'orderobj':orderobj})


def paymentpage1(request):
        user = request.session['email']
        cobj = register.objects.get(Email =user)
        cartobj = cart.objects.filter(customerid = cobj.id)
        totalbill = 0
        for i in cartobj:
            totalbill = i.totalamount + totalbill
            return render(request,'payment.html',{'session': user,'petobj':cartobj,'totalbill':totalbill})

from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date
from .models import register, order, cart, orderdetails  # Import your models



def paymentpage(request):
    user = request.session['email']
    cobj = register.objects.get(Email=user)

    name = request.POST.get('name')
    address = request.POST.get('address')
    phoneno = int(request.POST.get('phoneno'))
    city = request.POST.get('city')
    state = request.POST.get('state')
    pincode = int(request.POST.get('pincode'))
    totalbillamount_str = request.POST.get('totalbillamount')
    if totalbillamount_str is not None:
        Totalbillamount = float(totalbillamount_str)
    else:
        # Handle the case where 'totalbillamount' is not present
        Totalbillamount = 0.0 

    # Create and save the order object
    orderobj = order(Name=name, City=city, State=state, Address=address, PhoneNo=phoneno, Pincode=pincode, totalbillamount=Totalbillamount)
    orderobj.save()

   
    # Generate the order number
    dateobj = date.today()
    datedata = str(dateobj).replace('-', '')
    orderno = str(orderobj.id) + datedata
    orderobj.ordernumber = orderno
    orderobj.save()

    # Retrieve items from the cart
    cartobj = cart.objects.filter(customerid=cobj.id)

    # Save order details and delete items from the cart
    for i in cartobj:
        orderdetailobj = orderdetails(ordernumber=orderno, productid=i.productid, customerid=i.customerid, quantity=i.quantity, totalprice=i.totalamount)
        orderdetailobj.save()
        i.delete()

    # Display a success message using Django's messages framework
    messages.success(request, f'Order placed successfully! Your order number is {orderno}. ')

    # Redirect to a thank you page or any other appropriate page
    return redirect('../petlist/')
