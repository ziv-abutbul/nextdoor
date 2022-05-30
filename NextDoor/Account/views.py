from itertools import chain

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from .form import CustomUserCreationForm, UserProfileForm, RequestForm, MessageForm, CommentForm, SupportTicketForm,\
    RequestChangeForm, CommentChangeForm,RemoveBanForm,UserTicketForm
from .models import CustomUser, UserProfile, RequestModel, MessageModel, CommentModel, UserTicketModel, SupportTicketModel
from django.db.models.signals import post_save
from django.contrib.auth import authenticate
from django.contrib import messages
from django.conf import settings
from operator import attrgetter


class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'Account/signup.html'
    def post(self, request, *args, **kwargs):
        pass
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            UserProfile.objects.create(user=user)
            return redirect('login')
        else:
            return render(request, self.template_name, {'form' : form })


@user_passes_test(lambda u: u.is_superuser,login_url='home')
def Make_user_to_support(request,pk_test):
    user = CustomUser.objects.get(username=pk_test)#get the user we want to make him support
    group=Group.objects.get(name='support')#get the group of support
    user.groups.add(group)#add to user the group
    user.save()#save in DB user after update
    return render(request, 'home/HomePage.html')


@user_passes_test(lambda u: u.is_superuser,login_url='home')
def Remove_user_to_support(request,pk_test):
    user = CustomUser.objects.get(username=pk_test)#get the user we want to remove him from group
    group=Group.objects.get(name='support')#get the group of support
    user.groups.remove(group)#remove to user the group
    user.save()#save in DB user after update
    return render(request, 'home/HomePage.html')

def user_profile(request,pk_test):
    get_user = CustomUser.objects.get(username=pk_test) #get the user we want to show profile
    if get_user.is_active: #check if the user is not in ban
        profile = UserProfile.objects.get(user=get_user) #get model profile of user
        posts = RequestModel.objects.filter(user=get_user).order_by('-created_at') #get all post of user to show in feed
        if posts:
            last_request = posts.last().created_at #show the lest request in page
        else:
            last_request = None

        return render(request, "Account/user_profile.html",{'get_user': get_user, 'profile': profile, 'posts':posts, 'last_request':last_request})
    else:
        messages.success(request, 'User profile in Ban')
        return render(request, 'home/HomePage.html')

@login_required(login_url='home')
def edit_profile(request,pk_test):
    if request.user.username==pk_test or request.user.groups.filter(name='support').exists(): #check if the user how login or support to edit profile
        get_user = CustomUser.objects.get(username=pk_test) #get the user we want to change
        profile = UserProfile.objects.get(user=get_user) #get the profile of user we want to change
        form = UserProfileForm(request.POST or None, instance=profile)
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                address = request.POST.get('location', False) #enter all args
                city = request.POST.get('locality', False)
                country = request.POST.get('country', False)
                apt = request.POST.get('apt', False)
                lat = request.POST.get('lat', False)
                lng = request.POST.get('lng', False)
                instance = form.save(commit=False) #add to user all args
                instance.address = address
                instance.city = city
                instance.country = country
                instance.postal_code = apt
                instance.latitude = lat
                instance.longitude = lng
                form.save() #save in DB after update
                messages.success(request,'Your Profile has been changed successfully!')
                return redirect('user_profile', pk_test)
        return render(request, "Account/edit_profile.html",{'get_user': get_user, 'profile': profile , 'form': form})
    else:
        messages.success(request, 'You do not have permission to edit a profile that is not you!')
        return render(request, 'home/HomePage.html')

@login_required(login_url='home')
def edit_request(request,pk_test,pk):
    if request.user.username==pk_test or request.user.groups.filter(name='support').exists(): #check if the user who login or support to edit request
        get_user = CustomUser.objects.get(username=pk_test) #get the user of request
        profile = UserProfile.objects.get(user=get_user) #get profile of user
        posts = RequestModel.objects.get(id=pk) #get the post we want to edit
        form = RequestChangeForm(request.POST or None, instance=posts) #call function edit in form
        if request.method == 'POST':
            form = RequestChangeForm(request.POST, request.FILES, instance=posts)
            if form.is_valid():
                form.save() # save in DB after update
                messages.success(request,'Your request has been changed successfully!')
                return redirect('user_profile', pk_test)
        return render(request, "Account/edit_request.html",{'get_user': get_user, 'profile': profile , 'form': form})
    else:
        messages.success(request, 'You do not have permission to edit a profile that is not you!')
        return render(request, 'home/HomePage.html')

@login_required(login_url='home')
def edit_comment(request,pk_test,pk):
    if request.user.username==pk_test or request.user.groups.filter(name='support').exists(): #check if user who login or support
        get_user = CustomUser.objects.get(username=pk_test) #get the user we want to edit comment
        profile = UserProfile.objects.get(user=get_user) #get to profile user
        comments = CommentModel.objects.get(id=pk) #get the comment we want to change
        form = CommentChangeForm(request.POST or None, instance=comments) # call function edit in form
        if request.method == 'POST':
            form = CommentChangeForm(request.POST, request.FILES, instance=comments)
            if form.is_valid():
                form.save() #save in DB after update
                messages.success(request,'Your comments has been changed successfully!')
                pk=comments.request.id #get the request id to back page request
                return redirect('view_request', pk_test,pk)
        return render(request, "Account/edit_comment.html",{'get_user': get_user, 'profile': profile , 'form': form})
    else:
        messages.success(request, 'You do not have permission to edit a profile that is not you!')
        return render(request, 'home/HomePage.html')

def Rulse(request):
    return render(request, 'Account/Rulse.html')


# Allow the user to create a request
@login_required(login_url='home')
def create_request(request,pk_test):
    if request.user.username==pk_test or request.user.groups.filter(name='Support').exists(): #check if the user who login to open request of user
        get_user = CustomUser.objects.get(username=pk_test) #get the user
        profile = UserProfile.objects.get(user=get_user) #get the user profile
        if request.method == 'POST':
            form = RequestForm(request.POST) # call function create request in form
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save() # save in DB after create
                messages.success(request,'Your request has been sent successfully!')
                return redirect('user_profile', pk_test)
        else:
            form = RequestForm()
        return render(request, "Account/create_request.html",{'get_user': get_user, 'profile': profile , 'form': form})
    else:
        messages.success(request, 'You do not have permission to create a request!')
        return render(request, 'home/HomePage.html')


# Display the requests that the user has made
@login_required(login_url='home')
def requests(request,pk_test):
    get_user = CustomUser.objects.get(username=pk_test) #get user we want to show all request
    profile = UserProfile.objects.get(user=get_user) #get to profile to show img
    requests = RequestModel.objects.filter(user=get_user).order_by('created_at') #get all request of user by date of create
    return render(request, "Account/requests.html",{'get_user': get_user, 'profile': profile , 'requests': requests})

@login_required(login_url='home')
def close_request(request,pk_test,pk):
    if request.user.username == pk_test or request.user.groups.filter(name='support').exists(): #check if the user who login is the user who click to close request
        get_user = CustomUser.objects.get(username=pk_test)
        profile = UserProfile.objects.get(user=get_user)
        user_request = RequestModel.objects.get(pk=pk) #get the request we want to close
        user_request.close = True #change the request to close
        user_request.save() #save in DB after upadate
        messages.success(request, 'The request closed successfully!')
        return redirect('user_profile', pk_test)
    else:
        messages.success(request, 'You can not close another users request!')
        return render(request, 'home/HomePage.html')

@login_required(login_url='home')
def messaging(request,pk_test):
    if request.user.username != pk_test or request.user.groups.filter(name='Support').exists(): #check user dont send mess dont him self
        get_user = CustomUser.objects.get(username=request.user.username) #get user who send the mess
        get_receiver = CustomUser.objects.get(username=pk_test) #get user who receiv the mess
        profilerec = UserProfile.objects.get(user=get_receiver)
        profile = UserProfile.objects.get(user=get_user)
        Historysender = MessageModel.objects.filter(sender=request.user,receiver=get_receiver).order_by('created_at') #get all history mess from sender
        Historyreciver = MessageModel.objects.filter(sender=get_receiver, receiver=request.user).order_by('created_at') #get all history mess from reciver
        History = sorted(chain(Historysender, Historyreciver), key=attrgetter('created_at')) #create chain by date and time to show list mess
        if request.method == 'POST':
            form = MessageForm(request.POST) #call function to create new mess
            if form.is_valid():
                instance = form.save(commit=False)
                instance.sender = request.user #set who send new mess
                instance.receiver = CustomUser.objects.get(username=pk_test) #set who reciver the new mess
                #instance.receiver = CustomUser.objects.get(username=form.cleaned_data['receiver'])
                instance.save()
                messages.success(request,'Your message has been sent successfully! to- '+ profilerec.first_name)
                return redirect('messaging', pk_test)
        else:
            form = MessageForm()
        return render(request, "Account/messaging.html",{'get_user': get_user, 'profile': profile , 'form': form,'get_receiver':get_receiver,'History':History})
    else:
        messages.success(request, 'You do not have permission to send a message to a user that is not you!')
        return render(request, 'home/HomePage.html')


# Display the messages that the user received
@login_required(login_url='home')
def inbox(request,pk_test):
    if request.user.username==pk_test or request.user.groups.filter(name='support').exists(): #get the user inbox who login
        get_user = CustomUser.objects.get(username=pk_test) #get the user
        profile = UserProfile.objects.get(user=get_user) #get the profile
        allprofile = UserProfile.objects.all()
        messagess = MessageModel.objects.filter(receiver=request.user).order_by('created_at') #get all mess of user
        return render(request, "Account/inbox.html",{'get_user': get_user, 'profile': profile , 'messages': messagess,'allprofile':allprofile})
    else:
        messages.success(request, 'You do not have permission to view this inbox!')
        return render(request, 'home/HomePage.html')

@login_required(login_url='home')
def messaging_read(request,pk_test,pk):
    if request.user.username == pk_test or request.user.groups.filter(name='Support').exists():
        get_user = CustomUser.objects.get(username=pk_test)
        profile = UserProfile.objects.get(user=get_user)
        messagess = MessageModel.objects.get(id=pk) #get the mess we want to change status
        messagess.read =True #change the status to read
        messagess.save() # save in DB after upadte
        messagess = MessageModel.objects.filter(receiver=request.user).order_by('created_at')
        messages.success(request, 'You inbox is update successfully!')
        return render(request, "Account/inbox.html",{'get_user': get_user, 'profile': profile , 'messages': messagess})

@login_required(login_url='home')
def messaging_delete(request,pk_test,pk):
    if request.user.username == pk_test or request.user.groups.filter(name='Support').exists():
            get_user = CustomUser.objects.get(username=pk_test)
            profile = UserProfile.objects.get(user=get_user)
            messagess = MessageModel.objects.get(id=pk) #get the mess we want to delete
            MessageModel.delete(messagess) # delete mess
            messagess = MessageModel.objects.filter(receiver=request.user).order_by('created_at') #back all mess after delete
    return render(request, "Account/inbox.html",{'get_user': get_user, 'profile': profile , 'messages': messagess})

@login_required(login_url='home')
def view_request(request,pk_test,pk):
    get_user = CustomUser.objects.get(username=pk_test) #get the user we want to show request
    allprofile = UserProfile.objects.all() #get all profile to show img
    profile = UserProfile.objects.get(user=get_user)
    user_request = RequestModel.objects.get(pk=pk) #get the request we want to show
    comments = CommentModel.objects.filter(request=user_request).order_by('created_at') #get all comment of this request
    # Allow a user to comment on a request
    if request.method == 'POST':
        form = CommentForm(request.POST) #call function to create new comment in form
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.request = user_request
            instance.save() # save the new comment in DB
            messages.success(request,'Your comment has been sent successfully!')
            return redirect('view_request', pk_test,pk)
    else:
        form = CommentForm()

    return render(request, "Account/view_request.html",{'get_user': get_user, 'profile': profile , 'user_request': user_request, 'comments': comments, 'form': form, 'allprofile': allprofile})

@user_passes_test(lambda u: u.is_superuser,login_url='home')
def delete_user(request,pk_test):
    get_user = CustomUser.objects.get(username=pk_test) #get user to delete
    profile = UserProfile.objects.get(user=get_user) #get profile to delete
    CustomUser.delete(get_user) #delete from DB
    UserProfile.delete(profile) #delete from DB
    messages.success(request, 'You Delete user successfully!')
    return render(request, 'home/HomePage.html')

@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='support').exists(),login_url='home')
def delete_request(request,pk_test,pk):
    user_request = RequestModel.objects.get(pk=pk) #get request we want to delete
    RequestModel.delete(user_request) # delete request
    messages.success(request, 'You Delete Request successfully!')
    return render(request, 'home/HomePage.html')

@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='support').exists(),login_url='home')
def request_to_delete(request):
    requestlist = RequestModel.objects.all().order_by('-created_at') #get all request to list
    return render(request, 'Account/request_to_delete.html',{'requestlist':requestlist})


@login_required(login_url='home')
def support_ticket(request):
    get_user = CustomUser.objects.get(username=request.user.username)
    profile = UserProfile.objects.get(user=get_user)
    # check if user is in support group
    if request.method == 'POST' and request.user.groups.filter(name='support').exists(): #check if user is support
        form = SupportTicketForm(request.POST) #call function to create new ticket in form
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save() #save in DB
            messages.success(request,'Your support ticket has been sent successfully!')
            return render(request, 'home/HomePage.html')
    else:
        form = SupportTicketForm()
    return render(request, "Account/support_ticket.html",{'get_user': get_user, 'profile': profile , 'form': form})

@login_required(login_url='home')
def user_ticket(request,pk_test):
    get_user = CustomUser.objects.get(username=pk_test)
    profile = UserProfile.objects.get(user=get_user)
    if request.method == 'POST':
        form = UserTicketForm(request.POST) #call function to create ticket by user
        if form.is_valid():
            instance = form.save(commit=False)
            instance.request_user = profile #Bring the user being reported
            instance.user = request.user #Bring the user who reports it
            instance.save()
            messages.success(request,'Your user ticket has been sent successfully!')
            return render(request, 'home/HomePage.html')
    else:
        form = UserTicketForm()
    return render(request, "Account/user_ticket.html",{'form': form})

def RemoveBan(request):
    form = RemoveBanForm(request.POST)
    if request.method == 'POST':
        form = RemoveBanForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request,'Your Request for remove ban has been sent successfully!')
            return render(request, 'home/HomePage.html')
    return render(request, "Account/RemoveBan.html",{'form': form})


@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='support').exists(),login_url='home')
def Open_support_tickets(request):
    requestlist = UserTicketModel.objects.filter(status="open")
    return render(request, 'Account/open_support_tickets.html',{'requestlist':requestlist})


@user_passes_test(lambda u: u.is_superuser,login_url='home')
def Banned_list(request):
    requestlist = CustomUser.objects.filter(is_active = False)
    return render(request, 'Account/banned_list.html',{'requestlist':requestlist})

@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='support').exists(),login_url='home')
def change_status_ticket(request,pk):
    user_request = UserTicketModel.objects.get(pk=pk)
    user_request.status=True
    user_request.save()
    messages.success(request, 'You Ticket change to close!')
    return render(request, 'home/HomePage.html')

@user_passes_test(lambda u: u.is_superuser,login_url='home')
def change_user_to_Active(request,pk):
    user = CustomUser.objects.get(username=pk)
    user.is_active = True
    user.save()
    messages.success(request, 'The user unbanned')
    return render(request, 'home/HomePage.html')

@user_passes_test(lambda u: u.is_superuser,login_url='home')
def change_user_to_not_Active(request,pk):
    user = CustomUser.objects.get(username=pk)
    user.is_active = False
    user.save()
    messages.success(request, 'The user banned')
    return render(request, 'home/HomePage.html')


# support view to see tickets and status (close or open)
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='support').exists(),login_url='home')
def support_view(request):
    request_list = SupportTicketModel.objects.all().order_by('-status')
    if request.user.groups.filter(name='support').exists():
        request_list = SupportTicketModel.objects.filter(user=request.user).order_by('-status')

    return render(request, 'Account/support_view.html',{'request_list':request_list})


# Admin function to display amount of users
@user_passes_test(lambda u: u.is_superuser,login_url='home')
def user_count(request):
    get_user = CustomUser.objects.get(username=request.user.username)
    profile = UserProfile.objects.get(user=get_user)
    users = CustomUser.objects.all()
    user_c = users.count()
    return render(request, "Account/user_count.html",{'get_user': get_user, 'profile': profile , 'user_c': user_c})