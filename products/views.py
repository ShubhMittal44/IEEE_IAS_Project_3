from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from .models import ItemMain, ItemsImages, ItemRating, ItemsSpecifications, ItemFaq, UserCart,Billing, Bstates, Payment, Shipping
import json
# Create your views here.

def home(request):
    context = {}
    return render(request, 'home.html', context)

def item_list(request):
    
    items = ItemMain.objects.all()
    for i in ItemRating.objects.all():
        print(i.title, i.title_id)
    l = []
    for i in items:
        ll = []
        ll.append(ItemsImages.objects.filter(title=ItemMain.objects.filter(title = i.title)[0])[0].image)
        ll.append(ItemRating.objects.filter(title=ItemMain.objects.filter(title = i.title)[0])[0].ratingValue)
        ll.append(i.price)
        ll.append(i.description)
        ll.append(i.title)
        price = i.price
        offer = i.offers
        newPrice = price - (price * offer)//100
        ll.append(newPrice)
        ll.append(i.slug)
        ll.append(i.offers)
        l.append(ll)
    context = {
        "items": l
    }
    return render(request, "products/item_list.html", context)

def itemView(request, the_slug):
    if request.method == 'GET':
        context = {}
        p = []
        d=[]

        currentItem = ItemMain.objects.filter(slug = the_slug)[0]
        title = currentItem.title
        images = ItemsImages.objects.filter(title=ItemMain.objects.filter(title = title)[0])
        rating = ItemRating.objects.filter(title=ItemMain.objects.filter(title = title)[0])[0]
        descrip = ItemsSpecifications.objects.filter(title=ItemMain.objects.filter(title = title)[0])[0]
        faq = ItemFaq.objects.filter(title=ItemMain.objects.filter(title = title)[0])

        #produect
        price = currentItem.price
        offer = currentItem.offers
        newPrice = price - (price * offer)//100
        p.append(title)
        p.append(price)
        p.append(offer)
        p.append(newPrice)
        p.append(currentItem.availablity)
        p.append(currentItem.shippingCharges)
        p.append(rating.ratingCount)
        p.append(rating.ratingValue)
        p.append(currentItem.plantingAndCare)
        p.append(currentItem.slug)

        #description
        d.append(currentItem.description)
        d.append(descrip.commonName)
        d.append(descrip.plantSpread)
        d.append(descrip.maxHeight)
        d.append(descrip.sunlight)
        d.append(descrip.watering)
        d.append(descrip.soil)
        d.append(descrip.temp)
        d.append(descrip.ferti)
        d.append(descrip.bloomTime)

        context['products'] = p
        context['images'] = images
        context['des'] = d
        context['faq'] = faq

        return render(request, 'products/single_product.html', context)
    else:
        cartItem = json.loads(request.body)
        print(cartItem)
        print(cartItem.get('user', ''))
        print(cartItem.get('item', ''))
        cartModel = UserCart.objects.filter(
            user = User.objects.filter(username = cartItem.get('user', ''))[0],
            title = ItemMain.objects.filter(title=cartItem.get('item', ''))[0],
        )
        print(cartModel)
        if cartModel:
            cartModel[0].total += 1
            cartModel[0].save()
        else:
            cartModel = UserCart(
                user = User.objects.filter(username = cartItem.get('user', ''))[0],
                title = ItemMain.objects.filter(title=cartItem.get('item', ''))[0],
                total = 1
            )
            cartModel.save()


        return redirect('itemView', the_slug=the_slug)


    


def addReview(request, the_slug):

    if request.method == "POST":
        currentItem = ItemMain.objects.filter(slug = the_slug)[0]
        rating = ItemRating.objects.filter(title=currentItem)[0]
        rating.ratingCount += 1
        rating.rating += int(request.POST.get('rate', 5))
        rating.feedback = request.POST.get('feeds', "")
        rating.save()

    
    return redirect("/items/"+the_slug)

def faq(request):
    context = {}
    return render(request, 'faq.html', context)

def cart(request):
    context = {}
    if request.method == "GET":
        print('called')
        user = request.user
        items = UserCart.objects.filter(
            user = User.objects.filter(username = user)[0]
            )
        print(items)
        l = []
        for i in items:
            ll = []
            item =ItemMain.objects.filter(title = i.title)[0]
            ll.append(ItemsImages.objects.filter(title=item)[0].image)
            ll.append(i.title)
            price = item.price
            offer = item.offers
            newPrice = price - (price * offer)//100
            ll.append(newPrice)
            ll.append(i.total)
            l.append(ll)
        print(l)
        context['items'] = l
        
    print(context)
    return render(request, 'cart.html', context)

def checkout(request):
    context = {}
    if request.method == 'POST':
        if request.user.is_authenticated:
            Bfirst_name = request.POST['Bfirst_name']
            Blast_name = request.POST['Blast_name']
            Bcheckout_states = Bstates.objects.get(states = request.POST['Bstates'])
            Bstreet = request.POST['Bstreet']
            Bapartment = request.POST['Bapartment']
            Bcity = request.POST['Bcity']
            Bzip = request.POST['Bzip']
            Bphone = request.POST['Bphone']
            Bemail = request.POST['Bemail']    
            cardno = request.POST['cardno']
            namecard = request.POST['namecard']
            validity = request.POST['validity']
            cvv = request.POST['cvv']
            billing = Billing.objects.create(Bfirst_name=Bfirst_name, Blast_name=Blast_name, Bcheckout_states=Bcheckout_states, Bstreet=Bstreet, Bapartment=Bapartment, Bcity=Bcity, Bzip=float(Bzip), Bphone=float(Bphone), Bemail=Bemail)
            shipping = Shipping.objects.create(Sfirst_name=Bfirst_name, Slast_name=Blast_name, Scheckout_states=Bcheckout_states, Sstreet=Bstreet, Sapartment=Bapartment, Scity=Bcity, Szip=Bzip, Sphone=Bphone, Semail=Bemail)
            payment = Payment.objects.create(cardno=cardno, namecard=namecard, validity=validity, cvv=cvv)
            billing.save()
            payment.save()
            shipping.save()        
            return render(request, 'success')
        else:
            return redirect('login')
    else:
        return render(request, 'checkout.html', context)    

def our_team(request):
    context = {}
    return render(request, 'our_team.html', context)

def success(request):
    context = {}
    return render(request, 'success.html', context)

def order_success(request):
    context = {}
    return render(request, 'order_success.html', context)
