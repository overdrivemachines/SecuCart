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

def inventory(request):
    i = Item.objects.all()
    items = []
    for item in i:
        items.append(item)
    print items
    return HttpResponse(render_template(request, 'SecuCart/inventory.html', {'items': items}))

def shopping_cart(request):
    return HttpResponse(render_template(request, 'SecuCart/shopping_cart.html', {'items': items}))

def add(request):
    cart = Cart(request.session)
    item = Item.objects.get(id=request.GET.get('item_id'))
    cart.add(item, price=item.price)
    return HttpResponse("Added")



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
