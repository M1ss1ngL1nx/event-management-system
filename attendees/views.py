from django.shortcuts import render
from .models import Event, EventAttendee, Attendee
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.utils.text import slug, slugify
from django.contrib import messages

# Create your views here.
def Attendees(request):
    attendees = Attendee.objects.all()
    category = request.GET.get('category')
    attendee_type = request.GET.get("event_type_choices")
    attendee_status = request.GET.get('is_active')
    if category:
        attendees = Attendee.objects.filter(category = category)
        
    if attendee_type: 
        attendees = Attendee.objects.filter(attendee_type= attendee_type)
    if attendee_status:
        attendees = Attendee.objects.filter(attendee_status = attendee_status)
        
    context = {
        "category" : Attendee.job_title,
        "attendee_type" : Event.event_type_choices,
        "attendee_status" : Attendee.is_active,
    }
    
    return render(request, 'attendees/attendees.html', context)


def AttendeeDetail(request, slug):
    attendee_detail = get_object_or_404(Attendee, slug=slug)
    
    attendees = EventAttendee.object.filter(event = event)
    Capacity = Event.max_attendees
    
    context = {
        "attendee_detail": attendee_detail,
        "attendees": attendees,
        "Capacity": Capacity,
    }
    
    return render(request, 'attendees/attendeeDetail.html', context)

def addAttendee(request):
    if request.method == 'POST':
        form = AttendeeForm(request.POST)
        
        if form.is_valid():
            attendee = form.save(commit=False)
            id = form.save(attendee.attendee_id)
            attendee_name = form.save(attendee.get_full_name)
            attendee.save()
            
            return redirect("attendee_detail", slug= attendee.slug)
        
        else: 
            form = AttendeeForm()
            
        context = {
            "form": form,
        }
        
        return render(request, "attendees/addAttendee.html", context)
    
def edit_attendee(request):
    attendee = get_object_or_404(Attendee)
    
    if attendee.date_registered <= timezone.now():
        messages.error(request,"You cannot change attendee's details during ongoing event.")
        return redirect("attendee_detail", details= AttendeeDetail)
    
    form = Attendee(request.POST or None, instance= attendee)
    
    if request.method == "POST":
        if form.is_valid():
            updated_attendee = form.save(commit= False)
            
            updated_attendee.save()
            
            return redirect("attendeedetail", details= attendee.slug)
        
        context = {
            "form": form,
            "attendee": attendee
        }
        
        return render(request, "attendees/editAttendee.html", context)
    
    