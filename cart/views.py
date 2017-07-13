from django.shortcuts import render, get_object_or_404, redirect, reverse

# Create your views here.
from .models import CartItem
from django.contrib.auth.decorators import login_required
from products.models import Product
from payments.forms import MakePaymentForm
from django.template.context_processors import csrf
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
import stripe

stripe.api_key = settings.STRIPE_SECRET

@login_required(login_url="/accounts/login")
def user_cart(request):
    cartItems = CartItem.objects.filter(user=request.user)
    total = 0
    for item in cartItems:
        total += item.quantity * item.product.price

        if request.method == 'POST':
            form = MakePaymentForm(request.POST)
            if form.is_valid():
                try:
                    customer = stripe.Charge.create(
                    amount=int(total * 100),
                    currency="EUR",
                    description=request.user.email,
                    card=form.cleaned_data['stripe_id'],
                )
                except (stripe.error.CardError, e):
                    messages.error(request, "Your card was declined!")

                if customer.paid:
                    messages.success(request, "You have successfully paid")
                    CartItem.objects.filter(user=request.user).delete()
                    return redirect(reverse('products'))
            else:
                messages.error(request, "Unable to take payment")
        else:
            messages.error(request, "We were unable to take a payment with that card!")
    else:
        if len(cartItems) == 0:
            return render(request, 'empty_cart.html')

        form = MakePaymentForm()

    args = {'form': form,
            'items': cartItems,
            'total': total,
            'publishable': settings.STRIPE_PUBLISHABLE}
    args.update(csrf(request))

    return render(request, 'cart.html', args)

@login_required(login_url="/accounts/login")
def add_to_cart(request, id):
    product = get_object_or_404(Product, pk=id)
    

    try:
        cartItem = CartItem.objects.get(user=request.user, product=product)
        cartItem.quantity += 1
    except CartItem.DoesNotExist:
        cartItem = CartItem(
            user=request.user,
            product=product,
            quantity=1
        )

    cartItem.save()
    return redirect(reverse('cart'))

def adjust_cart(request, id):
    quantity = request.POST['quantity']
    cartItem = CartItem.objects.get(id=id)
    if int(quantity) > 0:
        cartItem.quantity = quantity
        cartItem.save()
    else:
        cartItem.delete()
    return redirect(reverse('cart'))


