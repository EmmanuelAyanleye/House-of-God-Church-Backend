from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Event, EventGallery, GalleryCategory, GalleryImage, MonthlyEvent, MonthlyEventGallery, EventCategory, Sermon
from .forms import EventForm, EventGalleryForm, MonthlyEventForm, MonthlyEventGalleryForm, SermonForm  # Add this line
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from urllib.parse import unquote
from django.db.models.functions import ExtractYear, ExtractMonth, TruncMonth
from django.utils import timezone
from django.db.models import Max, Count
from django.utils.text import slugify
from calendar import month_name
from datetime import datetime
from itertools import groupby
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import random
from .models import Sermon

from django.shortcuts import render
from django.utils import timezone
import pytz
from .models import Message 
from django.contrib import messages as django_messages
# Define the target date (February 1)
WAT = pytz.timezone('Africa/Lagos')

from django.utils import timezone

WAT = timezone.get_fixed_timezone(+1)  # West Africa Time

PROGRAM_BASE_NUMBER = 38  # Base program number for Household

# Function to calculate the next weekday date
def get_next_weekday(target_weekday):
    now = timezone.now().astimezone(WAT)
    days_ahead = (target_weekday - now.weekday()) % 7
    return now + timezone.timedelta(days=days_ahead)

def index(request):
    now = timezone.now().astimezone(WAT)
    target_date = timezone.datetime(now.year, 2, 1, 0, 0, 0, tzinfo=WAT)

    # Adjust for past February (move to next year)
    if now > target_date:
        target_date = timezone.datetime(now.year + 1, 2, 1, 0, 0, 0, tzinfo=WAT)

    # Calculate the program number increment
    program_number = PROGRAM_BASE_NUMBER + (now.year - 2025)

    if now.date() == target_date.date():
        countdown = "It's the day! 🎉"
        is_today = True
    else:
        delta = target_date - now
        countdown = f"{delta.days} days, {delta.seconds // 3600} hours, {(delta.seconds % 3600) // 60} minutes"
        is_today = False

    # Calculate next Wednesday and next Sunday
    next_wednesday = get_next_weekday(2)  # Wednesday is 2 (0 = Monday)
    next_sunday = get_next_weekday(6)  # Sunday is 6

    random_sermons = Sermon.objects.order_by('?')[:4]

    context = {
        'countdown': countdown,
        'is_today': is_today,
        'program_number': program_number,
        'next_wednesday': next_wednesday,
        'next_sunday': next_sunday,
        'random_sermons': random_sermons
    }

    return render(request, 'pages/index.html', context)

def custom_404_view(request, exception):
    return render(request, 'pages/404.html', status=404)

def departments(request):
    department_list = [
        {"name": "Children's Church", "url_name": "children"},
        {"name": "Singles Department", "url_name": "singles"},
        {"name": "Works Department", "url_name": "works"},
        {"name": "Publication Department", "url_name": "publication"},
        {"name": "Evangelism Department", "url_name": "evangelism"},
        {"name": "Holy Police", "url_name": "holy"},
        {"name": "Technical Crew", "url_name": "technical"},
        {"name": "Villa Sanitation", "url_name": "villa"},
        {"name": "Pastoral Care", "url_name": "pastoral"},
        {"name": "Missions Department", "url_name": "missions"},
        {"name": "Protocol Department", "url_name": "protocol"},
        {"name": "Benevolence Department", "url_name": "benevolence"},
    ]

    context = {
        "departments": department_list
    }
    return render(request, "pages/department.html", context)


def our_church(request):
    page = int(request.GET.get('page', 1))
    
    # Define the content for each page
    page_content = {
        1: """The young ministry had its inaugural Sunday morning service on the 1st of February, 1987 in his living room, then in the Ikeja area of Lagos state. As membership of the young but peculiar church grew into the hundreds and thousands, the surrounding grounds of his house became sitting area for the overspill from the living room. 
            <br><br>
            The ministry of the church and the person of Reverend Chris Okotie as a minister of the gospel became nationally recognized when the Lord Jesus Christ inspired the inauguration of the GRACE PROGRAMME and the television ministry, APOKALUPSIS.""",
        2: """The charity driven GRACE programme was instituted in 1990 and has become a major benevolence channel of the ministry on an annual basis. The objective of the programme as directed by the Lord Jesus is to extend the arm of care and sharing to the less privileged in the society through recognized non governmental organizations who deal directly with such people. 
            <br><br>
            In 1996 the KARIS AWARD, yet another inspiration by the Lord Jesus, which is aimed at appreciating Nigerians who have positively impacted the nation but have not been recognized by the government, was instituted and subsumed into the GRACE programme."""
    }

    context = {
        'current_page': page,
        'total_pages': len(page_content),
        'content': page_content.get(page, ''),
        'has_next': page < len(page_content),
        'has_previous': page > 1,
        'next_page': page + 1 if page < len(page_content) else None,
        'prev_page': page - 1 if page > 1 else None,
    }
    
    return render(request, 'pages/aboutchurch.html', context)

def our_pastor(request):
    page = int(request.GET.get('page', 1))
    
    # Define content for each page
    page_content = {
        1: {
            'text': """Reverend Chris Okotie was born on the 16th of June, 1958 to the family of Francis Idje and Cecilia Okotie in Ethiope West Local Government area of Delta State, South-South Nigeria. He had his primary education between 1964 and 1970 at Kirikiri Primary School, Lagos, as his father, who was a civil servant, was stationed in Lagos at the time. He proceeded to Edo College in Benin for his secondary education between 1971 and 1977. 
            <br><br>
            He had his 'A' Level certificate in 1978 and went on to study law at the University of Nigeria, Nsukka, in the former Anambra but now Enugu state. His multi-talented nature was evident from his childhood and became more apparent when he became the lead singer of the Edo College school band.
            <br><br>
            His exploits in music blossomed and while he was studying law at the University of Nigeria, Nsukka, he eventually rose to become the most celebrated Nigerian pop music star in 1980 when he released his first album, 'I Need Someone.'""",
            'image': 'pastor.jpg'
        },
        2: {
            'text': """At the peak of his young musical career and to the bewilderment of the show business world and the general public in 1984, he decided to abandon his musical career and return to the university to complete his study of law. It was in this period that he had his conversion experience and became a born again Christian, having experienced the saving grace of the Lord Jesus Christ. 
            <br><br>
            He was eventually awarded a Bachelor's degree in Law at his graduation in 1984, thereafter moving to the Nigerian Law School in Lagos. In 1985, in obedience to a divine call from the Lord Jesus Christ, he left the shores of Nigeria and proceeded to bible school in Tulsa, Oklahoma in the United States of America to prepare for a life of Christian ministry.
            <br><br>
            He returned to Nigeria in 1986, and after being commissioned by the Lord Jesus Christ, launched into the pastoral ministry with the inauguration of the HOUSEHOLD OF GOD FELLOWSHIP in 1987, and which later became THE HOUSEHOLD OF GOD INTERNATIONAL MINISTRIES.""",
            'image': 'pastor2.jpg'
        },
        3: {
            'text': """The young ministry had its inaugural Sunday morning service on the 1st of February, 1987 in his living room, then in the Ikeja area of Lagos state. As membership of the young but peculiar church grew into the hundreds and thousands, the surrounding grounds of his house became sitting area for the overspill from the living room. 
            <br><br>
            The ministry of the church and the person of Reverend Chris Okotie as a minister of the gospel became nationally recognized when the Lord Jesus Christ inspired the inauguration of the GRACE PROGRAMME and the television ministry, APOKALUPSIS.
            <br><br>
            The charity driven GRACE programme was instituted in 1990 and has become a major benevolence channel of the ministry on an annual basis. The objective of the programme as directed by the Lord Jesus is to extend the arm of care and sharing to the less privileged in the society through recognized non governmental organizations who deal directly with such people.""",
            'image': 'pastor3.jpg'
        },
        4: {
            'text': """In 1996 the KARIS AWARD, yet another inspiration by the Lord Jesus, which is aimed at appreciating Nigerians who have positively impacted the nation but have not been recognized by the government, was instituted and subsumed into the GRACE programme.
            <br><br>
            The KARIS award has been given over the years to distinguished Nigerians like Mallam Aminu Kano, Tai Solarin, Hajia Gambo Sawaba, Gen. Murtala Mohammed (posthumous), DIG Chris Omeben, Mr. Taiwo Akinkunmi, Mrs. Margaret Ekpo, Chief Michael Imuodu and many others.
            <br><br>
            The year 2010 KARIS award recipient was Chief Gani Fawehinmi, SAN, who was so honoured, though posthumously, for his contributions to the practice of law and the fight for good governance and human rights in Nigeria.""",
            'image': 'pastor4.jpg'
        },
        5: {
            'text': """It is worthy of note that some of the awardees of the programme have been subsequently recognized by government at various levels. The GRACE programme has several beneficiaries, charity organizations who have become traditional recipients of the charitable disposition of Reverend Chris Okotie and the members of the Household of God Church on an annual basis. 
            <br><br>
            They include the Sunshine Foundation, the Pacelli School for the Blind and Partially Sighted, The Little Saints’ Orphanage and The Spinal Cord Injuries Association of Nigeria. Each of these organizations receives five hundred thousand naira from the ministry.
            <br><br>
            The Lord Jesus Christ again inspired the television ministry of the Household of God Church, known popularly as Apokalupsis, which was instituted in 1999 to carry the message of the grace of God presented with a balanced biblical perspective beyond the walls of the local assembly to a larger audience both locally and more recently, internationally.""",
            'image': 'pastor5.jpg'
        },
        6: {
            'text': """The international audience can download messages online, and the live streaming of church services is also in the works.
            <br><br>
            The television ministry has received many awards including that from the Nigerian Television Authority network in the year 2002. By 1990, the location of the church in Reverend Chris Okotie’s house could no longer be sustained as membership had grown to several thousands, though two services were being held each Sunday morning.
            <br><br>
            The need for the ministry to move to a permanent location had become clear for all to see. After a prolonged search and by divine direction, a run down factory in the Oregun area of Ikeja in Lagos was found and a lease agreement entered into with the owner. The ministry moved in and held its first Sunday service at the newly renovated auditorium on the 19th of December, 1992. The date coincided with the day of GRACE 1992.""",
            'image': 'pastor6.jpg'
        },
        7: {
            'text': """This site and all the surrounding land in the immediate vicinity thus became a target of faith for Reverend Chris Okotie and the church members and indeed the ministry now owns a vast expanse of land in the area by the grace of the Lord Jesus Christ. 
            <br><br>
            In the year 1999, Reverend Chris Okotie once again, with instructions from the Lord Jesus, left Nigeria on a retreat during which he wrote the manuscript of the iconic best selling novel, THE LAST OUTCAST.
            <br><br>
            The manuscript was subjected to intense review over a period of time and the finished book was eventually published in 2002 and received rave reviews from all quarters. The novel thus exposed another aspect of Reverend Chris Okotie’s talent and the hand of the Lord Jesus upon him to the general public.""",
            'image': 'pastor7.png'
        },
        8: {
            'text': """By the grace and provident disposition of the Lord Jesus Christ, the ministry right now is in the process of building a new seven-storey facility to house the Children’s Church, which will be moved out of its present location as soon as the SILVER CITADEL is completed. 
            <br><br>
            In November 2005, on receiving a word from the Lord Jesus, the joint celebration of birthdays by members of the church born in the same month of the year was instituted by Reverend Chris Okotie as a means of creating yet another forum for fellowship among members, aside from the several departments in the ministry, which are more administratively based.
            <br><br>
            These celebrations have brought out the creativity in the people of the Household of God Church and indeed made the church a lot livelier.""",
            'image': 'pastor8.jpg'
        },
        9: {
            'text': """These celebrations have brought out the creativity in the people of the Household of God Church and indeed made the church a lot livelier.In the year 2006, the Queen Esther beauty pageant was also created by Reverend Chris Okotie based on an inspiration from the Lord, to project biblical character values for women and to correct the global wrong estimation and perception of feminine beauty as that which is from the outward appearance. 
            <br><br>
            The pageant involves ladies who are members of the church dressed as different female characters from the bible, and who are then judged on their representation of such biblical characters and the creativity displayed in their costumes. The pageant has broadened in its conceptualization with each passing year since its inception. The pageant is subsumed in the annual GRACE Programme.
            <br><br>
            The KARIS award now carries a cash prize of two million naira.""",
            'image': 'pastor9.jpg'
        },
    }
    
    total_pages = len(page_content)
    current_content = page_content.get(page, page_content[1])
    
    context = {
        'current_page': page,
        'total_pages': total_pages,
        'content': current_content['text'],
        'image': current_content['image'],
        'has_next': page < total_pages,
        'has_previous': page > 1,
        'next_page': page + 1 if page < total_pages else None,
        'prev_page': page - 1 if page > 1 else None,
    }
    
    return render(request, 'pages/aboutpastor.html', context)

def singles(request):
    return render(request, 'pages/singles.html')

def children(request):
    page = int(request.GET.get('page', 1))
    
    page_content = {
        1: """Jesus spoke these words when His disciples tried to turn back children who had been 
            brought by their parents to be blessed by Him. Jesus gathered the children to Himself and used their simple trust to demonstrate what pleases God the Father. Jesus loves them and we want them to love and know Him. 
            <br><br>
            In The Household of God Church, Jesus is our foundation. Our children's church is therefore not a place where children are kept while adults attend service. Neither is it a place where the children learn a couple of songs and listen to bible stories to keep them busy. Our children's church is a place where our children are taught and instructed in the word of God so they can grow up to know Him and learn how they can live to please Him.
            <br><br>
            The gospel is the same no matter the age group. Therefore, our children learn the same bible truths as the adults but in smaller bits and pieces and in simpler language. """,
        2: """It's a complete service, going from opening prayer to praise and worship, to the word, to offering up to closing prayer and grace. The department is headed by Sis. Bolanle Body-Lawson and accommodates children from birth to fifteen (15) years. The teachers are all volunteers, and are committed members of the Household of God Church. They are people who are born again, speak in tongues, are consistent in church and have sat under the teaching of Rev. Chris Okotie for at least six (6) months. 
            <br><br>
            Our children's church is helping to shape the character of our children for the future, and for us teachers, it's a great honour to be working with these children.
            <br><br>
            We count ourselves blessed and are thankful to be a part of their lives. CHILDREN'S CHURCH DEPARTMENT was formed in February 1987. We have Approximately 140 members (teachers). We meet every First Saturday of the month"""
    }

    context = {
        'current_page': page,
        'total_pages': len(page_content),
        'content': page_content.get(page, page_content[1]),
        'has_next': page < len(page_content),
        'has_previous': page > 1,
        'next_page': page + 1 if page < len(page_content) else None,
        'prev_page': page - 1 if page > 1 else None,
    }
    
    return render(request, 'pages/children.html', context)

def works(request):
    return render(request, 'pages/works.html')

def publication(request):
    return render(request, 'pages/publication.html')

def evangelism(request):
    return render(request, 'pages/evangelism.html')

def holy(request):
    return render(request, 'pages/holy.html')

def technical(request):
    page = int(request.GET.get('page', 1))
    
    page_content = {
        1: """The Technical Crew as it's fondly called was one of the first few departments to be established shortly after the founding of the Church in 1987. The department was established in 1988 for the purpose of installing and maintaining light fittings as well as other electrical and electronic fittings like Air-conditioners, musical equipment, generators, etc in the church. 
            <br><br>
            At the turn of the millennium in year 2000, the functions of the department was further expanded to include the church annual Christmas decorations involving wholesale lighting decoration of all trees in and around the church premises, the fence and the entire street of the Household of God Church.
            <br><br> 
            This annual church event serves to physically demonstrate to the world, that Jesus Christ is the Light of the World.The department presently has 35 members who meet every second Saturday at 1.00pm to pray, worship and join faith with members on personal issues of life.""",
        2: """They also meet regularly to carry out maintenance works in the church as the need arises. The annual Christmas lighting and decorations which commence by the first of October every year practically take all of the time of members as we have to be in church all day, every day to ensure the December first deadline for 'lights-on' is met.
        <br><br>
        Pat Otuechere-Obakude as the head of department (HOD), has led the department since 2011 with grace, purposeful leadership and great understanding of member's individuality that pulls together to deliver on the goals and objectives for which the department was established for.We pray for the Lord's divine enablement, strength and wisdom to do that which He has called us to do in his vineyard. 
        <br><br>
        As we light up and decorate His house, He will decorate and help our lives to shine for the world to see and glorify His Name. He promised, He will not forget our labour of Love"""
    }

    context = {
        'current_page': page,
        'total_pages': len(page_content),
        'content': page_content.get(page, page_content[1]),
        'has_next': page < len(page_content),
        'has_previous': page > 1,
        'next_page': page + 1 if page < len(page_content) else None,
        'prev_page': page - 1 if page > 1 else None,
    }
    
    return render(request, 'pages/technical.html', context)

def villa(request):
    return render(request, 'pages/villa.html')

def pastoral(request):
    page = int(request.GET.get('page', 1))
    
    page_content = {
        1: """The Pastoral Care Department was set up in 1998 from the various Church units that had closely worked with the Pastor. It is structured to meet the needs of the brethren and ensure the proper organization of the specific arms of the ministry. It comes directly under the office of the Pastor of the Church, Rev. Chris Okotie.
              <br>
              There are 4 core units which make up the department: <br>
              <strong>VISITATION</strong> <br>
              Visitation section is simply VISITATION: To establish PERSONAL CONTACT with members of the local Church. The team relies on requests from needy members and information offered by friends and family who need the attention of the team for fellowship encouragement and prayer support, through the 'I Care' cards.
              <br><br>
              <strong>PRAISE & WORSHIP TEAM</strong><br>
              This section leads the congregation in Praise and Worship to God and our Lord Jesus Christ during services (Sundays and Wednesdays), and during functions like weddings and the Church's annual GRACE Programme.
              <br>""",
        2: """<strong>AUDIO/VIDEO CREW SECTION</strong><br>
              The Audio-Visual Section comprises of the audio-visual crew and the tape ministry. It is responsible for the recording of the Church's sermons on both audio and video and Church's audio and video equipment's for ensuring audibility of the sermon, praise and worship as well as the visual display of activities and lyrics of songs.
              <br><br>
              <strong>CHRISTIAN PARENTING CLASS</strong><br>
              The Christian Parenting Class ministers Biblical principles of good parenting and child upbringing to married couples either believing God for the fruit of the womb or already expectant parents. It also offers physical fitness regimen to help ensure that expectant mothers are fit and strong throughout the duration of their pregnancy.
              The department which has over 50 listed members meets twice a month: first and third Saturdays, from 12 noon on the Church premises
              The administrative Head of Department is Miss Ogorchukwu Ogweh. She joined The Household of God International Church on February 1, 1988. She has been a volunteer Church worker for 27 years, out of which time she has led the Pastoral Care Department for 16 years."""
    }

    context = {
        'current_page': page,
        'total_pages': len(page_content),
        'content': page_content.get(page, page_content[1]),
        'has_next': page < len(page_content),
        'has_previous': page > 1,
        'next_page': page + 1 if page < len(page_content) else None,
        'prev_page': page - 1 if page > 1 else None,
    }
    
    return render(request, 'pages/pastoral.html', context)

def missions(request):
    return render(request, 'pages/missions.html')

def protocol(request):
    return render(request, 'pages/protocol.html')

def benevolence(request):
    return render(request, 'pages/benevolence.html')

def esther16(request):
    return render(request, 'pages/esther16.html')

def january(request):
    return render(request, 'pages/january.html')

def is_staff(user):
    return user.is_staff

def admin_login(request):
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            # Get the next URL, but sanitize it
            next_url = request.GET.get('next', '')
            if next_url:
                next_url = unquote(next_url)
                # Prevent infinite loops by checking for multiple login occurrences
                if next_url.count('login') > 1:
                    return redirect('admin_dashboard')
            return redirect(next_url or 'admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'admin/login.html')

@login_required
def admin_dashboard(request):
    events = Event.objects.all()
    monthly_events = MonthlyEvent.objects.annotate(
        gallery_count=Count('gallery')
    ).order_by('-year', 'month')
    
    # Group events by year
    years_data = []
    current_year = None
    year_events = []
    
    for event in monthly_events:
        if current_year != event.year:
            if current_year is not None:
                years_data.append({
                    'event_year': current_year,
                    'events': year_events
                })
            current_year = event.year
            year_events = []
        year_events.append(event)
    
    if year_events:  # Add the last year
        years_data.append({
            'event_year': current_year,
            'events': year_events
        })

    context = {
        'events': events,
        'years': years_data,
    }
    return render(request, 'admin/dashboard.html', context)

def admin_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('admin_login')

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        gallery_files = request.FILES.getlist('gallery_images')
        
        if form.is_valid():
            event = form.save()
            
            # Handle multiple gallery images
            for image in gallery_files:
                EventGallery.objects.create(
                    event=event,
                    image=image
                )
            
            messages.success(request, 'Event created successfully!')
            return redirect('admin_event_detail', slug=event.slug)
    else:
        form = EventForm()
    return render(request, 'admin/event_form.html', {'form': form})

@login_required
def delete_gallery_image(request, image_id):
    # Get the gallery image
    gallery_image = get_object_or_404(MonthlyEventGallery, id=image_id)
    event = gallery_image.event  # Save the event reference before deletion
    
    if request.method == 'POST':
        # Delete the image
        gallery_image.delete()
        messages.success(request, 'Image deleted successfully.')
        
        # Redirect back to the event detail page
        return redirect('monthly_event_detail', slug=event.slug)
    
    # If not POST, redirect back
    return redirect('monthly_event_detail', slug=event.slug)

@login_required
def edit_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save()
            
            # Handle new gallery images
            gallery_files = request.FILES.getlist('gallery_images')
            for image in gallery_files:
                EventGallery.objects.create(
                    event=event,
                    image=image
                )
            
            messages.success(request, 'Event updated successfully!')
            return redirect('admin_event_detail', slug=event.slug)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'admin/event_form.html', {
        'form': form,
        'event': event
    })

@login_required
def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    gallery = event.gallery.all()
    return render(request, 'admin/event_detail.html', {
        'event': event,
        'gallery': gallery
    })

@login_required
def add_gallery_images(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.method == 'POST':
        form = EventGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            gallery = form.save(commit=False)
            gallery.event = event
            gallery.save()
            messages.success(request, 'Image added to gallery!')
            return redirect('admin_event_detail', slug=event.slug)
    else:
        form = EventGalleryForm()
    return render(request, 'admin/gallery_form.html', {'form': form, 'event': event})

def event_public_view(request, slug):
    event = get_object_or_404(Event, slug=slug)
    
    # Handle description pagination
    description = event.description
    page = int(request.GET.get('page', 1))
    chunk_size = 1300  # Match monthly_event page break size
    total_pages = (len(description) + chunk_size - 1) // chunk_size
    
    # Get the current chunk of text
    start = (page - 1) * chunk_size
    end = start + chunk_size
    current_description = description[start:end]
    
    context = {
        'event': event,
        'gallery': event.gallery.all(),
        'current_description': current_description,
        'current_page': page,
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_previous': page > 1,
        'next_page': page + 1 if page < total_pages else None,
        'prev_page': page - 1 if page > 1 else None,
    }
    
    return render(request, 'pages/event_detail.html', context)

def get_event_categories(request):
    queen_esther_events = Event.objects.filter(
        category__name='Queen Esther'
    ).order_by('-year')
    
    grace_events = Event.objects.filter(
        category__name='G.R.A.C.E'
    ).order_by('-year')
    
    return {
        'queen_esther_events': queen_esther_events,
        'grace_events': grace_events
    }

@login_required
def monthly_event_dashboard(request):
    categories = MonthlyEventCategory.objects.all()
    events = MonthlyEvent.objects.all().order_by('-year', 'month')
    return render(request, 'admin/monthly_events/dashboard.html', {
        'categories': categories,
        'events': events
    })

@login_required
def admin_sermon_list(request):
    sermons = Sermon.objects.all().order_by('-date_posted')
    return render(request, 'admin/sermons/list.html', {'sermons': sermons})

@login_required
def edit_sermon(request, pk):
    sermon = get_object_or_404(Sermon, pk=pk)
    if request.method == 'POST':
        form = SermonForm(request.POST, instance=sermon)
        if form.is_valid():
            form.save()
            messages.success(request, "Sermon updated successfully!")
            return redirect('admin_sermon_list')
    else:
        form = SermonForm(instance=sermon)
    return render(request, 'admin/sermons/form.html', {'form': form, 'sermon': sermon})

@login_required
def delete_sermon(request, pk):
    sermon = get_object_or_404(Sermon, pk=pk)
    if request.method == 'POST':
        sermon.delete()
        messages.success(request, "Sermon deleted successfully!")
        return redirect('admin_sermon_list')
    return render(request, 'admin/sermons/confirm_delete.html', {'sermon': sermon})

@login_required
def create_monthly_event(request):
    if request.method == 'POST':
        form = MonthlyEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('monthly_event_detail', slug=event.slug)
    else:
        form = MonthlyEventForm()
    return render(request, 'admin/monthly_events/event_form.html', {'form': form})

@login_required
def monthly_event_detail(request, slug):
    event = get_object_or_404(MonthlyEvent, slug=slug)
    
    # Get all galleries and group them by year
    galleries = MonthlyEventGallery.objects.filter(event=event)\
        .order_by('-year', '-date_added')
    
    # Group images by year
    gallery_by_year = []
    for year, images in groupby(galleries, key=lambda x: x.year):
        gallery_by_year.append({
            'grouper': year,
            'list': list(images)
        })
    
    context = {
        'event': event,
        'gallery_by_year': gallery_by_year,
    }
    return render(request, 'admin/monthly_events/event_detail.html', context)

@login_required
def edit_monthly_event(request, pk):
    event = get_object_or_404(MonthlyEvent, pk=pk)
    if request.method == 'POST':
        form = MonthlyEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('monthly_event_detail', slug=event.slug)
    else:
        form = MonthlyEventForm(instance=event)
    return render(request, 'admin/monthly_events/event_form.html', {'form': form, 'event': event})

@login_required
def delete_monthly_event(request, pk):
    event = get_object_or_404(MonthlyEvent, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('admin_dashboard')
    return render(request, 'admin/monthly_events/confirm_delete.html', {'event': event})

@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('events_list')
    return render(request, 'admin/events/confirm_delete.html', {'event': event})

@login_required
def events_list(request):
    events = Event.objects.all().order_by('-year')
    categories = EventCategory.objects.all()
    
    # Filter by category if requested
    category_id = request.GET.get('category')
    if category_id:
        events = events.filter(category_id=category_id)
    
    context = {
        'events': events,
        'categories': categories,
        'selected_category': category_id
    }
    return render(request, 'admin/events/events_list.html', context)

@login_required
def monthly_events_list(request):
    events = MonthlyEvent.objects.all().order_by('-date')
    
    # Filter by event type if requested
    event_type = request.GET.get('type')
    if event_type:
        events = events.filter(event_type=event_type)
    
    context = {
        'events': events,
        'event_types': MonthlyEvent.EVENT_TYPES,
        'selected_type': event_type
    }
    return render(request, 'admin/monthly_events/events_list.html', context)

def monthly_event_public_view(request, category, month, year):
    event = get_object_or_404(MonthlyEvent, 
                            category__name=category,
                            month=month,
                            year=year)
    years = MonthlyEvent.objects.filter(
        category__name=category,
        month=month
    ).values_list('year', flat=True).distinct().order_by('-year')
    
    return render(request, 'pages/monthly_event.html', {
        'event': event,
        'years': years,
        'current_year': year,
        'current_month': month
    })

def monthly_event_month(request, event_type, month):
    event_type_display = event_type.replace('-', ' ').title()
    month_name = dict(MonthlyEvent.MONTHS)[month]
    
    # Get all years that have content for this event type and month
    available_years = MonthlyEvent.objects.filter(
        event_type=event_type_display,
        month=month
    ).values_list('year', flat=True).distinct().order_by('-year')
    
    selected_year = request.GET.get('year')
    gallery = []
    
    if selected_year:
        try:
            event = MonthlyEvent.objects.get(
                event_type=event_type_display,
                month=month,
                year=selected_year
            )
            gallery = event.gallery.all()
        except MonthlyEvent.DoesNotExist:
            pass
    
    context = {
        'event_type': event_type_display,
        'month_name': month_name,
        'available_years': available_years,
        'selected_year': int(selected_year) if selected_year else None,
        'gallery': gallery
    }
    
    template_name = f'monthly_events/{month_name.lower()}.html'
    return render(request, template_name, context)

def monthly_event_view(request, event_type, month):
    # Convert month name to number
    month_names = {m.lower(): i for i, m in enumerate(month_name) if m}
    month_num = month_names.get(month.lower())
    
    if not month_num:
        raise Http404("Month not found")
    
    current_year = timezone.now().year
    
    years = MonthlyEvent.objects.filter(
        event_type=event_type,
        month=month_num
    ).values_list('year', flat=True).distinct().order_by('-year')
    
    selected_year = request.GET.get('year', years.first() or current_year)
    
    try:
        event = MonthlyEvent.objects.get(
            event_type=event_type,
            month=month_num,
            year=selected_year
        )
        gallery = event.gallery.all().order_by('-date_added')
        
        # Handle description pagination (now word-based)
        description = event.description
        page = int(request.GET.get('page', 1))
        words_per_page = 193  
        words = description.split()
        total_pages = (len(words) + words_per_page - 1) // words_per_page
        
        # Get the current chunk of text
        start = (page - 1) * words_per_page
        end = start + words_per_page
        current_description = ' '.join(words[start:end])
        
    except MonthlyEvent.DoesNotExist:
        event = None
        gallery = []
        current_description = ""
        total_pages = 1
        page = 1
    
    context = {
        'event': event,
        'gallery': gallery,
        'available_years': years,
        'selected_year': int(selected_year),
        'month_name': month_name[month_num],
        'event_type': event_type,
        'no_event': event is None,
        'current_description': current_description,
        'current_page': page,
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_previous': page > 1,
        'next_page': page + 1 if page < total_pages else None,
        'prev_page': page - 1 if page > 1 else None,
    }
    
    return render(request, 'pages/monthly_event.html', context)

@login_required
def add_monthly_event_gallery(request, event_id):
    event = get_object_or_404(MonthlyEvent, id=event_id)
    initial_year = request.GET.get('year', timezone.now().year)
    
    if request.method == 'POST':
        if not request.FILES.getlist('images'):
            messages.error(request, 'Please select at least one image to upload.')
            return redirect('add_monthly_event_gallery', event_id=event_id)

        year = request.POST.get('year', timezone.now().year)
        files = request.FILES.getlist('images')
        
        created_images = []
        for f in files:
            gallery_image = MonthlyEventGallery.objects.create(
                event=event,
                image=f,
                year=year
            )
            created_images.append(gallery_image)
        
        if created_images:
            messages.success(request, f'{len(created_images)} images uploaded successfully!')
            return redirect('monthly_event_detail', slug=event.slug)
        else:
            messages.error(request, 'No images were uploaded. Please try again.')
    else:
        form = MonthlyEventGalleryForm(initial={'year': initial_year})
    
    context = {
        'form': form,
        'event': event,
        'gallery': event.gallery.all().order_by('-year', '-date_added')
    }
    return render(request, 'admin/monthly_events/add_gallery.html', context)

def weddings(request):
    page = request.GET.get('page', 1)
    images = GalleryImage.objects.filter(category__slug='weddings').order_by('-date_added')
    
    paginator = Paginator(images, 28)  # Show 28 images per page
    try:
        gallery_images = paginator.page(page)
    except PageNotAnInteger:
        gallery_images = paginator.page(1)
    except EmptyPage:
        gallery_images = paginator.page(paginator.num_pages)
    
    context = {
        'gallery_images': gallery_images,
        'category_name': 'WEDDINGS'
    }
    return render(request, 'pages/weddings.html', context)

def baby_dedication(request):
    page = request.GET.get('page', 1)
    images = GalleryImage.objects.filter(category__slug='baby-dedication').order_by('-date_added')
    
    paginator = Paginator(images, 28)
    try:
        gallery_images = paginator.page(page)
    except PageNotAnInteger:
        gallery_images = paginator.page(1)
    except EmptyPage:
        gallery_images = paginator.page(paginator.num_pages)
    
    context = {
        'gallery_images': gallery_images,
        'category_name': 'BABY DEDICATION'
    }
    return render(request, 'pages/baby_dedication.html', context)

def christmas(request):
    page = request.GET.get('page', 1)
    images = GalleryImage.objects.filter(category__slug='christmas-light').order_by('-date_added')
    
    paginator = Paginator(images, 28)
    try:
        gallery_images = paginator.page(page)
    except PageNotAnInteger:
        gallery_images = paginator.page(1)
    except EmptyPage:
        gallery_images = paginator.page(paginator.num_pages)
    
    context = {
        'gallery_images': gallery_images,
        'category_name': 'HOG CHRISTMAS LIGHT EDITION'
    }
    return render(request, 'pages/christmas.html', context)

def church_gallery(request):
    page = request.GET.get('page', 1)
    images = GalleryImage.objects.filter(category__slug='church-gallery').order_by('-date_added')
    
    paginator = Paginator(images, 28)
    try:
        gallery_images = paginator.page(page)
    except PageNotAnInteger:
        gallery_images = paginator.page(1)
    except EmptyPage:
        gallery_images = paginator.page(paginator.num_pages)
    
    context = {
        'gallery_images': gallery_images,
        'category_name': 'CHURCH GALLERY'
    }
    return render(request, 'pages/church_gallery.html', context)

def pastor_gallery(request):
    page = request.GET.get('page', 1)
    images = GalleryImage.objects.filter(category__slug='pastors-gallery').order_by('-date_added')
    
    paginator = Paginator(images, 28)
    try:
        gallery_images = paginator.page(page)
    except PageNotAnInteger:
        gallery_images = paginator.page(1)
    except EmptyPage:
        gallery_images = paginator.page(paginator.num_pages)
    
    context = {
        'gallery_images': gallery_images,
        'category_name': "PASTOR'S GALLERY"
    }
    return render(request, 'pages/pastor_gallery.html', context)

@login_required
def gallery_dashboard(request, category_slug):
    category = get_object_or_404(GalleryCategory, slug=category_slug)
    page = request.GET.get('page', 1)
    images = category.images.all()
    
    # Pagination - 28 images per page
    paginator = Paginator(images, 28)
    try:
        gallery_images = paginator.page(page)
    except PageNotAnInteger:
        gallery_images = paginator.page(1)
    except EmptyPage:
        gallery_images = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'images': gallery_images,
    }
    return render(request, 'admin/gallery/dashboard.html', context)

@login_required
def add_gallery_images(request, category_slug):
    category = get_object_or_404(GalleryCategory, slug=category_slug)
    
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        for image in images:
            GalleryImage.objects.create(
                category=category,
                image=image
            )
        messages.success(request, 'Images uploaded successfully')
        return redirect('admin_gallery', category_slug=category_slug)
    
    return render(request, 'admin/gallery/upload.html', {'category': category})

@login_required
def delete_gallery_image(request, image_id):
    gallery_image = get_object_or_404(MonthlyEventGallery, id=image_id)
    event = gallery_image.event  # Save the event reference before deletion

    if request.method == 'POST':
        gallery_image.delete()
        messages.success(request, 'Image deleted successfully.')
    return redirect('monthly_event_detail', slug=event.slug)

def add_sermon(request):
    if request.method == 'POST':
        form = SermonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sermon added successfully!")
            return redirect('add_sermon')  # Redirects to the same page
        else:
            messages.error(request, "There was an error adding the sermon.")
    else:
        form = SermonForm()
        
    return render(request, 'admin/add_sermon.html', {'form': form})

def watch(request):
    # Get all sermons
    all_sermons = list(Sermon.objects.all())
    
    if not all_sermons:
        # Handle case when no sermons exist
        return render(request, 'pages/watch.html', {
            'sermon': None,
            'more_sermons': [],
            'error_message': 'No sermons available'
        })

    # Get specific sermon or random one
    sermon_id = request.GET.get('id')
    if sermon_id:
        sermon = get_object_or_404(Sermon, id=sermon_id)
    else:
        sermon = random.choice(all_sermons)

    # Get other sermons for "Watch More" section
    other_sermons = [s for s in all_sermons if s.id != sermon.id]
    random.shuffle(other_sermons)

    # Paginate other sermons
    paginator = Paginator(other_sermons, 8)  # Show 8 sermons per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'sermon': sermon,
        'more_sermons': page_obj,
    }
    
    return render(request, 'pages/watch.html', context)

def sermon_action(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=401)
        
    sermon_id = request.POST.get('sermon_id')
    action_type = request.POST.get('type')
    
    sermon = get_object_or_404(Sermon, id=sermon_id)
    
    if action_type == 'like':
        if request.user in sermon.dislikes.all():
            sermon.dislikes.remove(request.user)
        if request.user in sermon.likes.all():
            sermon.likes.remove(request.user)
        else:
            sermon.likes.add(request.user)
    elif action_type == 'dislike':
        if request.user in sermon.likes.all():
            sermon.likes.remove(request.user)
        if request.user in sermon.dislikes.all():
            sermon.dislikes.remove(request.user)
        else:
            sermon.dislikes.add(request.user)
            
    return JsonResponse({
        'likes': sermon.total_likes(),
        'dislikes': sermon.total_dislikes(),
        'user_action': action_type if request.user in (sermon.likes.all() if action_type == 'like' else sermon.dislikes.all()) else None
    })

def sermon_like(request, sermon_id):
    sermon = get_object_or_404(Sermon, id=sermon_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        session_key = f'sermon_{sermon_id}_voted'
        if not request.session.get(session_key):
            if action == 'like':
                sermon.likes += 1
            elif action == 'dislike':
                sermon.dislikes += 1
            sermon.save()
            request.session[session_key] = True
        return JsonResponse({'likes': sermon.likes, 'dislikes': sermon.dislikes})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# contact view 
 # Make sure to import the Message model

def contact_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # Save the message to the database
        Message.objects.create(
            full_name=full_name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect("index")  # Redirect to the homepage after submission

    return render(request, "pages/index.html")






# admin conatct us 
@login_required
def admin_messages_view(request):
    messages = Message.objects.all().order_by('-created_at')
    unread_count = Message.objects.filter(is_read=False).count()
    return render(request, 'admin/contact_us.html', {
        'messages': messages,
        'unread_count': unread_count
    })

@login_required
def mark_message_as_read(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        if not message.is_read:
            message.is_read = True
            message.save()
            django_messages.success(request, 'Message marked as read.')
        return redirect('admin_messages')  # Make sure this matches your URL name
    
    # If not POST, redirect anyway
    return redirect('admin_messages')
    
# admin message detail and delete view
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    return render(request, 'hog/message_detail.html', {'message': message})

# admin message delete view
def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        message.delete()
        django_messages.success(request, 'Message deleted successfully.')
        return redirect('/custom-admin/messages/?deleted=true')  # Using query param for toast trigger
    
    return render(request, 'hog/message_confirm_delete.html', {'message': message})