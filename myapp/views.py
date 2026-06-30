from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Item
from .forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
import logging # built-in Python library for tracking system events and errors
from django.shortcuts import get_object_or_404 #Django helper to fetch data or auto-trigger a 404 
from django.utils import timezone




#  creating a logger instance after the current file for targeted debugging
logger = logging.getLogger(__name__)


# Creating function based views here.(listview)
# @login_required
# @cache_page(60 * 15) # implementing caching
# @vary_on_headers("User-Agent") #caching by headers
def index(request):
    # Getting items from the database
    logger.info("Fetching all items from the database")
    logger.info(f"User : {request.user} , time:[{timezone.now().isoformat()}] requested item list from {request.META.get('REMOTE_ADDR')}")
    item_list = Item.objects.all()
    logger.debug(f"Found {item_list.count()} items")

    # pagination 
    paginator = Paginator(item_list,5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    # Creating context
    context = {
        'page_obj' : page_obj
    }
    # Passing the context object to the render method along with the template
    return render(request,"myapp/index.html",context)

# class based view (listview) - Gets all items from the model
class IndexClassView(ListView):
    model = Item
    template_name = "myapp/index.html"
    context_object_name = 'item_list'

# Function based view
def detail(request,id):
    logger.info(f"Fetching an item with id:{id}")
    try:
        # trying to find the item by ID, or trigger a 404 error if missing
        item = get_object_or_404(Item,pk=id)
        # Log the item details for developer troubleshooting
        logger.debug(f"Item found {item.item_name} (${item.item_price})")
    except Exception as e:
        # Record the specific error and the target ID in the system logs
        logger.error("Error fetching the item with id %s: %s", id,e)
        # Forward the 404 or 500 error so Django can show the correct error
        raise

    context ={
        'item' : item
    }
    return render(request,'myapp/detail.html',context)

# # class based detail view - When you want to render one item from the database
# # Then in the url.py I have changed from id to pk(primary key)
# class FoodDetail(DetailView):
#     model = Item 
#     template_name = 'myapp/detail.html'
#     context_object_name = 'item'


# Creating form
def create_item(request):
    form = ItemForm(request.POST or None)
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myapp:index')
        else:
            print(form.errors['item_price'])
        

    context ={
        'form' : form 
    }
    return render(request,'myapp/item-form.html',context)

# class based item create view 
class ItemCreateView(CreateView):
    # item_form.html
    model = Item
    form_class = ItemForm
    def form_valid(self,form):
       form.instance.user_name = self.request.user
       return super().form_valid(form)




def update_item(request,id):
    item = Item.objects.get(id=id)
    form = ItemForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('myapp:index')
    context ={
        'form' : form 
    }
    return render(request,'myapp/item-form.html',context)

# class based view - Update view
class ItemUpdateView(UpdateView):
    model = Item 
    fields = ['item_name','item_desc','item_price','item_image']
    template_name_suffix = "_update_form"
    
    # updating the based on the logged user and not anyone can override it
    def get_queryset(self):
        return Item.objects.filter(user_name=self.request.user)



def delete_item(request,id):
    item = Item.objects.get(id=id)
    if request.method == "POST":
        item.delete()
        return redirect('myapp:index')
    
    return render(request,'myapp/item-delete.html')

class ItemDelete(DeleteView):
    model = Item 
    success_url = reverse_lazy('myapp:index')

def get_objects(request):
    for item in Item.objects.all():
        print(item.item_name)

def get_objects_optimized(request):
    items = Item.objects.all('item_name')
    for item in items:
        print(item.item_name)


