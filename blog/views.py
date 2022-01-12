from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value
from django.conf import settings
from itertools import chain
from . import forms,models
from authentication.models import User
from django.db import IntegrityError

# Create your views here.
@login_required

def abonnements(request):
    form = forms.FollowForm()
    context={"form":form}
    followed_users = get_followed_users(request.user)
    following_users = get_following_users(request.user)
    context.update(following_users)
    context.update(followed_users)

    # Chercher pour suivre un utilisateur
    if request.method == "POST":
        form = forms.FollowForm(request.POST)
        if form.is_valid():
            find_user = form.cleaned_data.get("username")
            if find_user == request.user.username:
                error = f"Vous ne pouvez pas vous suivre vous-même"
                context.update({"error":error})
                return render(request,'abonnements.html',context)
            try:
                found_user = User.objects.get(username=find_user)
            except User.DoesNotExist:
                error = f"{find_user} n'existe pas ! "
                context.update({"error":error})
                return render(request,'abonnements.html',context)

            try:
                instance = models.UserFollows(user=request.user,followed_user=found_user)
                instance.save()
                followed_users = get_followed_users(request.user)
                return redirect("abonnements")

            except IntegrityError:
                error = f"Vous avez déjà suivi {find_user}"
                context.update({"error":error})
                return render(request,'abonnements.html',context)

    return render(request,'abonnements.html',context)

def get_following_users(user):
    context={}
    try:
        clean_followings = models.UserFollows.objects.filter(user=user)
    except models.UserFollows.DoesNotExist:
        clean_followings = None

    if clean_followings is not None:
        following_users = []
        for userfollows in clean_followings:
            followed_user = userfollows.followed_user
            following_users.append(followed_user)
        context.update({"following_users":following_users})
    return context

def get_followed_users(user):
    context={}
    try:
        clean_followed = models.UserFollows.objects.filter(followed_user_id=user)
    except models.UserFollows.DoesNotExist:
        clean_followed = None
    
    if clean_followed is not None:
        followed_users = []
        for userfollows in clean_followed:
            followed_user = userfollows.user
            followed_users.append(followed_user)
        context.update({"followed_users":followed_users})
    return context
    
def unfollow(request,pk):
    unfollow = models.UserFollows.objects.filter(followed_user_id=pk)
    unfollow.delete()
    return redirect("abonnements")


def posts(request):
    user = request.user
    tickets = get_user_viewable_tickets(user)
    reviews = get_user_viewable_reviews(user)

    if reviews is not None and tickets is not None:
        posts = sorted(
        chain(reviews, tickets), 
        key=lambda post: post.time_created, 
        reverse=True
        )
    elif reviews is not None:
        posts = reviews
    else:
        posts = tickets
    context={"posts":posts,"media_url":settings.MEDIA_URL}
    return render(request,"posts.html",context)


def edit(request,pk,content_type):
    if content_type == "TICKET":
        return edit_ticket(request,pk,content_type)
    elif content_type == "REVIEW":
        return edit_review(request,pk,content_type)


def delete(request,pk,content_type):
    if content_type == "TICKET":
        post = models.Ticket.objects.get(id=pk)
    elif content_type == "REVIEW":
        post = models.Review.objects.get(id=pk)
    post.delete()
    return redirect("posts")


def edit_ticket(request,pk,content_type=None):
    ticket = models.Ticket.objects.get(id=pk)
    form = forms.TicketForm(instance=ticket)
    if request.method == "POST":
            form = forms.TicketForm(request.POST,request.FILES,instance=ticket)
            if form.is_valid():
                form.save()
                return redirect('flux')
    return render(request,"edit.html",context={"form":form})


def edit_review(request,pk,content_type=None):
    review = models.Review.objects.get(id=pk)
    form = forms.ReviewForm(instance=review)
    if request.method=="POST":
        form = forms.ReviewForm(request.POST,request.FILES,instance=review)
        if form.is_valid():
            form.save()
            return redirect('flux')
    return render(request,"edit.html",context={"form":form})


def get_user_viewable_tickets(user):
    userID = user.id
    tickets = models.Ticket.objects.filter(user_id=userID)
    if len(tickets) >= 1:
        return tickets
    else:
        return None


def get_user_viewable_reviews(user):
    userID = user.id
    reviews = models.Review.objects.filter(user_id=userID)
    if len(reviews) >= 1:
        return reviews
    else:
        return None


def create_ticket(request,is_from_review=False,form=None):
        if form == None:
            form=forms.TicketForm(request.FILES)
        else:
            form = form
        if request.method == "POST":
            form = forms.TicketForm(request.POST,request.FILES)
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.user = request.user
                form.save()
            if is_from_review==False:
                return redirect('flux')
            else:
                return ticket
        return render(request,"create_ticket.html",context={"form":form})


def ticket(request,pk):
    ticket = models.Ticket.objects.get(id=pk)
    return render(request,"ticket.html/",context={"ticket":ticket,"media_url":settings.MEDIA_URL})


def create_review(request,form=None,pk=None,ticket_review=False):
    if pk is not None:
        ticket = models.Ticket.objects.get(id=pk)
    if form is None:
        form = forms.ReviewForm()
    else:
        form = form
    if request.method =="POST":
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.ticket = ticket
            instance.save()
            instance.ticket.review = instance
            instance.ticket.save()
            if ticket_review is True:
                return instance
            else:
                return redirect("flux")
    context={"review_form":form,"post":ticket,"media_url":settings.MEDIA_URL}
    if ticket_review is False: 
        context["clean_tickets"] = True
    return render(request,"create_review.html",context)


def ticket_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method =="POST":
        ticket = create_ticket(request,True,ticket_form)
        create_review(request,review_form,pk=ticket.id,ticket_review=True)
        return redirect('flux')
    return render(request,"ticket_review.html",context={"review_form":review_form,"ticket_form":ticket_form})


def flux(request):

    reviews = get_user_viewable_reviews(request.user)
    tickets = get_user_viewable_tickets(request.user)
    following_users = get_following_users(request.user)

    for following_user in following_users["following_users"]:
        f_reviews = get_user_viewable_reviews(following_user)
        f_tickets = get_user_viewable_tickets(following_user)

        if f_reviews is not None and reviews is None:
            reviews = f_reviews
            
        if f_tickets is not None and tickets is None:
            tickets = f_tickets

        if f_reviews is not None and reviews is not None:
            reviews = reviews | f_reviews

        if f_tickets is not None and tickets is not None:
            tickets = tickets | f_tickets

    if reviews is not None and tickets is not None:
        posts = sorted(
            chain(reviews, tickets), 
            key=lambda post: post.time_created, 
            reverse=True
        )
    else:
        posts = tickets
    context={'posts': posts,"media_url":settings.MEDIA_URL,"user":request.user,"clean_tickets":False}
    return render(request,'flux.html',context)
