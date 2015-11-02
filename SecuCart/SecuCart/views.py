from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.forms.models import model_to_dict
from django.forms.utils import ErrorList
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File

from carton.cart import Cart
from models import Item

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def render_template(request, template, context):
    template = loader.get_template(template)
    context = RequestContext(request, context)
    return template.render(context)

def home(request):
    return HttpResponse(render_template(request, 'SecuCart/home.html', {}))

@csrf_exempt
def inventory(request):
    if request.method == 'GET':
        i = Item.objects.all()
        items = []
        for item in i:
            print item.name, item.description
            items.append(item)
        return HttpResponse(render_template(request, 'SecuCart/inventory.html', { 'items': items }))

    elif request.method == 'POST':
        print 'item_number:', request.POST.get('item_number')
        for i in request.POST:
            if i != 'item_number':
                item = Item.objects.get(name=i)
                print 'item:', i, item.name, item.quantity, item.price
                item.quantity = item.quantity - int(request.POST.get('item_number'))
                item.save()
                cart = Cart(request.session)
                cart.add(item, price=1.0, quantity=request.POST.get('item_number'))           
                return HttpResponse(render_template(request, 'SecuCart/shopping_cart.html', {}))


def shopping_cart(request):
    cart = Cart(request.session)
    return HttpResponse(render_template(request, 'SecuCart/shopping_cart.html', {'cart': cart}))





def login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if user:
            if user.is_active:
                login(request, user)
                messages.success(
                    request, 'User: ' + request.POST['username'] + ' successfully loged in')
                return HttpResponseRedirect(request.POST.get('next'))
            else:
                messages.error(
                    request, 'User: ' + request.POST['username'] + ' is a disactivated account')
                return HttpResponseRedirect('login')
        else:
            messages.error(request, "Username or password incorrect")
            return HttpResponseRedirect('login')
    else:
        if 'next' in request.GET:
            redirect = request.GET.get('next')

        else:
            redirect = ''
        response = HttpResponse(
            render_template(request, "SecuCart/login.html", {"next": redirect}))
        return response
