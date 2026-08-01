from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalogo.models import Product
from .models import BrowsingHistory, Wishlist


class AccountLoginView(LoginView):
    template_name = 'accounts/login.html'


class AccountLogoutView(LogoutView):
    pass


def signup(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile(request):
    wishlist = Wishlist.objects.filter(user=request.user).select_related('product')
    history = BrowsingHistory.objects.filter(user=request.user).select_related('product')[:20]

    context = {
        'wishlist': wishlist,
        'history': history,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
@require_POST
def toggle_wishlist(request):
    slug = request.POST.get('slug')
    product = get_object_or_404(Product, slug=slug)

    item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.delete()

    return JsonResponse({'active': created})
