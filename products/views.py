from django.shortcuts import redirect, render
from .models import ItemMain, ItemsImages, ItemRating, ItemsSpecifications, ItemFaq

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

def addReview(request, the_slug):

    if request.method == "POST":
        currentItem = ItemMain.objects.filter(slug = the_slug)[0]
        rating = ItemRating.objects.filter(title=currentItem)[0]
        rating.ratingCount += 1;
        rating.rating += int(request.POST.get('rate', 5))
        rating.feedback = request.POST.get('feeds', "")
        rating.save()

    
    return redirect("/items/"+the_slug)

def faq(request):
    context = {}
    return render(request, 'faq.html', context)

def cart(request):
    context = {}
    return render(request, 'cart.html', context)

def checkout(request):
    context = {}
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
