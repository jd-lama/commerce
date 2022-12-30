from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User

from django.contrib.auth.decorators import login_required

class newListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title','description','startingBid','category']

class newPictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = ['picture','alt_text']

class newBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['offer']

class newCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.TextInput(attrs={
                'class': "form-control",
                "placeholder":"place your comments here"
            })
        }



#login required
def newListing(request):
    PictureFormSet = modelformset_factory(Picture,form=newPictureForm,extra = 4)

    if request.method == "POST":
        form = newListingForm(request.POST,request.FILES)
        imagesForm = PictureFormSet(request.POST,request.FIELS,
                                    queryset=Picture.objects.none())
        if form.is_valid() and imagesFOrm.is_valid():
            newListing = form.save(commit = False)
            newListing.creator = request.user
            newListing.save()

            for form in imagesForm.cleaned_data:
                if form:
                    picture = form["picture"]
                    text = form['alt_text']
                    newPicture = Picture(listing = newListing,picture = picture,alt_text = text)
                    newPicture.save()

            return render(request,"actions/newListing.html",{
                "form": newListingForm(),
                "imageForm": PictureFormSet(queryset = Picture.objects.move())
                "success": True
        })
        else:
            return render(request,"auctions/newListing.html",{
                "form": newListingForm(),
                "imageForm": PictureFormSet(queryset=Picture.objects.none())
            })
    else:
        return render(request,"actions/newListing.html",{
            "form": newListingForm()
            "imageForm": PictureFormSet(querySet = Picture.objects.none())
        })
def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
