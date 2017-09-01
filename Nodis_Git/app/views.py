"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
##### Sign in modules #####
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from app.forms import SignUpForm, UserCreationForm
from app.tokens import AccountActivationTokenGenerator, account_activation_token
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
###########################

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/imperial_index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def template(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Template Index',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

# Basically this is the same strategy for password reset. Notice that I’m changing the user.is_active to False, 
# so the user can’t log in before confirming the email address. After that, we send the email for the user. 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('app/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            User.email_user(user, subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'app/signup.html', {'form': form})

# Here we do all the magic, checking if the user exists, if the token is valid. 
# If everything checks, we switch the flags is_active and email_confirmed to True and log the user in.
# By changing the value of the email_confirmed field, it will cause the link to be invalidated.
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('Dashboard')
    else:
        return render(request, 'app/account_activation_invalid.html')

def account_activation_sent(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/account_activation_sent.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def dashboard(request):
    """Renders the user dashboard """
    assert isinstance(request, HttpRequest)
    print(request.user)
    if request.user.is_authenticated():
        return render(request, 'app/LoggedIn/Dashboard.html')
    else:
        return render(request, 'app/login.html')

   
def account(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    print(request.user)
    if request.user.is_authenticated():
        return render(request, 'app/LoggedIn/Account.html')
    else:
        return render(request, 'app/login.html')
