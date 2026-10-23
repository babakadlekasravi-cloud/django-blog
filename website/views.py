from django.shortcuts import render,redirect
from website.forms import TicketForm
from django.contrib import messages

# Create your views here.
def index_view(request):
    return render(request,"website/index.html")

def contact_view(request):
    if request.method=="POST":
        form=TicketForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,"sucees")
            return redirect('website:contact')
        else:
            messages.add_message(request,messages.ERROR,'error')
    else:
        form=TicketForm()

    return render(request,"website/contact.html",{'form':form})

def about_view(request):
    return render(request,"website/about.html")
