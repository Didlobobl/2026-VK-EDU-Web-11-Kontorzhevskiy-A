from django.shortcuts import render


def login(request):
    return render(request, 'core/login.html')

def signup(request):
    return render(request, 'core/signup.html')

def profile(request):
    user_data = {
        'username': 'dr_house',
        'email': 'house@pup.com',
        'nickname': 'Gregory'
    }
    return render(request, 'core/profile.html', {'user': user_data})
