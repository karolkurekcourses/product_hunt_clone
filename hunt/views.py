from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from datetime import datetime, timezone


def homepage(request):
    products = Product.objects.all()
    return render(request, 'hunt/home.html', context={'products': products})


@login_required(login_url='account:login')
def create(request):
    if request.method == "POST":
        input_set = {'image', 'csrfmiddlewaretoken', 'icon', 'short_body', 'url', 'body', 'title'}
        if set(dict(request.POST).keys()) | set(dict(request.FILES).keys()) == input_set:
            product = Product(title=request.POST['title'], body=request.POST['body'])
            if request.POST['url'].replace('https://', 'http://').startswith('http://'):
                product.url = request.POST['url']
            else:
                product.url = 'https://' + request.URL['url']
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pub_datetime = datetime.now(timezone.utc)
            product.creator = request.user
            product.short_body = request.POST['short_body']
            product.save()
            return redirect(f'/product/{product.pk}/')
        else:
            return render(request, 'hunt/create.html', context={'error': "You need to fill all data!"})
    return render(request, 'hunt/create.html')


def details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'hunt/product_details.html', context={'product': product})


def about(request):
    return render(request, 'hunt/about.html')


@login_required(login_url='account:login')
def esteem(request, product_id):
    def decide_where_to_redirect(request):
        if 'product' in request.META['HTTP_REFERER']:
            return redirect(f'/product/{product_id}/')
        return redirect(request.META['HTTP_REFERER'])

    if request.method == 'POST':
        user = request.user
        product = get_object_or_404(Product, id=product_id)
        vote_ids = [int(x) for x in product.vote_users.split(',') if x != '']
        if user == product.creator or int(user.id) in vote_ids:
            return decide_where_to_redirect(request)
        product.votes += 1
        vote_ids.append(int(user.id))
        product.vote_users = ','.join([str(x) for x in vote_ids])
        product.save()
        return decide_where_to_redirect(request)