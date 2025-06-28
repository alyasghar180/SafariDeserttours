from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from decimal import Decimal

from .models import Booking, BookingAddon
from .forms import BookingForm, BookingAddonForm
from packages.models import Package, PackageAddon
from .utils import send_booking_confirmation_email, send_booking_notification_to_admin


class BookingCreateView(FormView):
    """
    View for creating a new booking.
    """
    template_name = 'bookings/booking_form.html'
    form_class = BookingForm
    
    def dispatch(self, request, *args, **kwargs):
        # Get the package being booked
        self.package = get_object_or_404(Package, slug=self.kwargs['package_slug'], is_active=True)
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['package'] = self.package
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['package'] = self.package
        
        # Get available addons for this package
        addon_relations = self.package.addon_relations.filter(addon__is_active=True)
        context['addon_relations'] = addon_relations
        
        # Create addon forms
        addon_forms = []
        for relation in addon_relations:
            form = BookingAddonForm(addon=relation.addon, prefix=f'addon_{relation.addon.id}')
            addon_forms.append({
                'form': form,
                'relation': relation,
            })
        context['addon_forms'] = addon_forms
        
        return context
    
    def form_valid(self, form):
        """Process the booking form."""
        with transaction.atomic():
            try:
                # Get form data
                package = self.package
                booking_date = form.cleaned_data.get('booking_date')
                full_name = form.cleaned_data.get('full_name')
                email = form.cleaned_data.get('email')
                phone = form.cleaned_data.get('phone')
                nationality = form.cleaned_data.get('nationality', '')
                adults = form.cleaned_data.get('adults', 1)
                children = form.cleaned_data.get('children', 0)
                emirate = form.cleaned_data.get('emirate')
                pickup_location = form.cleaned_data.get('pickup_location')
                pickup_location_text = form.cleaned_data.get('pickup_location_text', '')
                hotel_name = form.cleaned_data.get('hotel_name', '')
                hotel_room = form.cleaned_data.get('hotel_room', '')
                address_details = form.cleaned_data.get('address_details', '')
                special_requests = form.cleaned_data.get('special_requests', '')
                payment_method = form.cleaned_data.get('payment_method', 'credit_card')
                
                # Calculate base price
                base_price = package.price * adults
                if package.child_price and children > 0:
                    base_price += package.child_price * children
                else:
                    # If no specific child price, use adult price with 30% discount
                    from decimal import Decimal
                    base_price += (package.price * Decimal('0.7')) * children
                
                # Add pickup location cost if applicable
                if pickup_location and pickup_location.additional_cost:
                    # Apply pickup cost per person
                    pickup_cost = pickup_location.additional_cost * (adults + children)
                    base_price += pickup_cost
                
                # CRITICAL FIX: Create a default pickup location if none is selected
                # This is essential to prevent the IntegrityError
                from locations.models import PickupLocation, Emirate
                
                # Get or create a default emirate
                default_emirate, _ = Emirate.objects.get_or_create(
                    name="Default",
                    defaults={
                        "is_active": True,
                        "display_order": 999
                    }
                )
                
                # Get or create a default pickup location
                default_pickup, _ = PickupLocation.objects.get_or_create(
                    name="Default Location",
                    emirate=default_emirate,
                    defaults={
                        "is_active": True,
                        "display_order": 999,
                        "additional_cost": 0
                    }
                )
                
                # CRITICAL FIX: Always use the default pickup location if none is selected
                if not pickup_location:
                    pickup_location = default_pickup
                
                # Create the booking directly with all required fields
                booking = Booking(
                    package=package,
                    booking_date=booking_date,
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    nationality=nationality,
                    adults=adults,
                    children=children,
                    emirate=emirate,
                    pickup_location=pickup_location,  # This is the critical field that was causing the error
                    pickup_location_text=pickup_location_text,
                    hotel_name=hotel_name,
                    hotel_room=hotel_room,
                    address_details=address_details,
                    special_requests=special_requests,
                    payment_method=payment_method,
                    total_price=base_price
                )
                
                # Set user if logged in
                if self.request.user.is_authenticated:
                    booking.user = self.request.user
                
                # Save the booking with all fields properly set
                booking.save()
            except Exception as e:
                # Log the error for debugging
                print(f"Error creating booking: {str(e)}")
                # Re-raise the exception to trigger form_invalid
                raise
            
            # Process addon forms
            addon_relations = self.package.addon_relations.filter(addon__is_active=True)
            addon_total = 0
            
            for relation in addon_relations:
                addon_form = BookingAddonForm(
                    self.request.POST,
                    addon=relation.addon,
                    prefix=f'addon_{relation.addon.id}'
                )
                
                if addon_form.is_valid():
                    quantity = addon_form.cleaned_data['quantity']
                    if quantity > 0:
                        # Get the price (special price if available, otherwise default price)
                        price = relation.get_price()
                        
                        # Create booking addon
                        booking_addon = BookingAddon.objects.create(
                            booking=booking,
                            addon=relation.addon,
                            quantity=quantity,
                            price=price
                        )
                        
                        # Calculate addon price
                        if relation.addon.is_per_person:
                            addon_price = price * quantity * (adults + children)
                        else:
                            addon_price = price * quantity
                        
                        addon_total += addon_price
            
            # Update total price with addons
            booking.total_price += addon_total
            booking.save()
            
            # Store booking ID in session for confirmation page
            self.request.session['booking_id'] = booking.booking_id
            
            # Send notification emails
            try:
                send_booking_confirmation_email(booking)
                send_booking_notification_to_admin(booking)
            except Exception as e:
                # Log the error but don't stop the booking process
                print(f'Error sending email notifications: {str(e)}')
            
            from django.utils.translation import gettext_lazy
            messages.success(
                self.request,
                gettext_lazy('Your booking has been created successfully! Booking reference: {0}').format(booking.booking_id)
            )
            
            return redirect('booking_confirmation')
    
    def form_invalid(self, form):
        from django.utils.translation import gettext_lazy
        messages.error(
            self.request,
            gettext_lazy('There was an error with your booking. Please check the form and try again.')
        )
        return super().form_invalid(form)


class BookingConfirmationView(TemplateView):
    """
    View for displaying booking confirmation.
    """
    template_name = 'bookings/booking_confirmation.html'
    
    def get(self, request, *args, **kwargs):
        # Get booking ID from session
        booking_id = request.session.get('booking_id')
        if not booking_id:
            messages.error(request, _('No booking information found.'))
            return redirect('home')
        
        # Get booking object
        booking = get_object_or_404(Booking, booking_id=booking_id)
        
        # Clear session
        if 'booking_id' in request.session:
            del request.session['booking_id']
        
        return render(request, self.template_name, {'booking': booking})


class BookingDetailView(DetailView):
    """
    View for displaying booking details.
    """
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'
    
    def get_object(self, queryset=None):
        return get_object_or_404(Booking, booking_id=self.kwargs['booking_id'])


class BookingHistoryView(LoginRequiredMixin, ListView):
    """
    View for displaying booking history for logged-in users.
    """
    model = Booking
    template_name = 'bookings/booking_history.html'
    context_object_name = 'bookings'
    paginate_by = 10
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')


class BookingCancelView(LoginRequiredMixin, DetailView):
    """
    View for cancelling a booking.
    """
    model = Booking
    template_name = 'bookings/booking_cancel.html'
    context_object_name = 'booking'
    
    def get_object(self, queryset=None):
        booking = get_object_or_404(
            Booking, 
            booking_id=self.kwargs['booking_id'],
            status__in=['pending', 'confirmed']  # Only allow cancellation of pending or confirmed bookings
        )
        
        # Check if the booking belongs to the current user
        if booking.user and booking.user != self.request.user:
            raise PermissionDenied()
            
        return booking
    
    def post(self, request, *args, **kwargs):
        booking = self.get_object()
        cancellation_reason = request.POST.get('cancellation_reason', '')
        
        # Update booking status to cancelled
        booking.status = 'cancelled'
        booking.cancellation_reason = cancellation_reason
        booking.cancelled_at = timezone.now()
        booking.save()
        
        # Send cancellation email notification
        try:
            from .utils import send_booking_cancellation_email
            send_booking_cancellation_email(booking)
        except Exception as e:
            print(f'Error sending cancellation email: {str(e)}')
        
        messages.success(
            request,
            _('Your booking has been cancelled successfully. Booking reference: {0}').format(booking.booking_id)
        )
        
        return redirect('booking_history')


class BookingUpdateView(LoginRequiredMixin, FormView):
    """
    View for updating an existing booking.
    """
    template_name = 'bookings/booking_update.html'
    form_class = BookingForm
    
    def dispatch(self, request, *args, **kwargs):
        # Get the booking to update
        self.booking = get_object_or_404(
            Booking, 
            booking_id=self.kwargs['booking_id'],
            status__in=['pending', 'confirmed']  # Only allow modification of pending or confirmed bookings
        )
        
        # Check if the booking belongs to the current user
        if self.booking.user and self.booking.user != self.request.user:
            raise PermissionDenied()
        
        # Get the package associated with the booking
        self.package = self.booking.package
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['package'] = self.package
        kwargs['instance'] = self.booking
        return kwargs
    
    def get_initial(self):
        # Pre-fill the form with existing booking data
        initial = {
            'booking_date': self.booking.booking_date,
            'adults': self.booking.adults,
            'children': self.booking.children,
            'full_name': self.booking.full_name,
            'email': self.booking.email,
            'phone': self.booking.phone,
            'nationality': self.booking.nationality,
            'pickup_location': self.booking.pickup_location,
            'hotel_name': self.booking.hotel_name,
            'hotel_room': self.booking.hotel_room,
            'special_requests': self.booking.special_requests,
            'payment_method': self.booking.payment_method,
        }
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking'] = self.booking
        context['package'] = self.package
        
        # Get available addons for this package
        addon_relations = self.package.addon_relations.filter(addon__is_active=True)
        context['addon_relations'] = addon_relations
        
        # Create addon forms with initial data from existing booking addons
        addon_forms = []
        for relation in addon_relations:
            # Check if this addon is already in the booking
            try:
                booking_addon = BookingAddon.objects.get(booking=self.booking, addon=relation.addon)
                initial_quantity = booking_addon.quantity
            except BookingAddon.DoesNotExist:
                initial_quantity = 0
                
            form = BookingAddonForm(
                addon=relation.addon, 
                prefix=f'addon_{relation.addon.id}',
                initial={'quantity': initial_quantity}
            )
            addon_forms.append({
                'form': form,
                'relation': relation,
                'initial_quantity': initial_quantity
            })
        context['addon_forms'] = addon_forms
        
        return context
    
    def form_valid(self, form):
        with transaction.atomic():
            # Update booking object
            booking = form.save(commit=False)
            
            # Calculate initial total price (without addons)
            adults = form.cleaned_data['adults']
            children = form.cleaned_data['children']
            
            base_price = self.package.price * adults
            if self.package.child_price and children > 0:
                base_price += self.package.child_price * children
            else:
                # If no specific child price, use adult price with 30% discount
                base_price += (self.package.price * Decimal('0.7')) * children
            
            booking.total_price = base_price
            booking.save()
            
            # Delete existing addons and recreate them
            BookingAddon.objects.filter(booking=booking).delete()
            
            # Process addon forms
            addon_relations = self.package.addon_relations.filter(addon__is_active=True)
            addon_total = 0
            
            for relation in addon_relations:
                addon_form = BookingAddonForm(
                    self.request.POST,
                    addon=relation.addon,
                    prefix=f'addon_{relation.addon.id}'
                )
                
                if addon_form.is_valid():
                    quantity = addon_form.cleaned_data['quantity']
                    if quantity > 0:
                        # Get the price (special price if available, otherwise default price)
                        price = relation.get_price()
                        
                        # Create booking addon
                        booking_addon = BookingAddon.objects.create(
                            booking=booking,
                            addon=relation.addon,
                            quantity=quantity,
                            price=price
                        )
                        
                        # Calculate addon price
                        if relation.addon.is_per_person:
                            addon_price = price * quantity * (adults + children)
                        else:
                            addon_price = price * quantity
                        
                        addon_total += addon_price
            
            # Update total price with addons
            booking.total_price += addon_total
            booking.save()
            
            # Send update notification emails
            try:
                from .utils import send_booking_update_email
                send_booking_update_email(booking)
            except Exception as e:
                print(f'Error sending update email: {str(e)}')
            
            messages.success(
                self.request,
                _('Your booking has been updated successfully! Booking reference: {0}').format(booking.booking_id)
            )
            
            return redirect('booking_detail', booking_id=booking.booking_id)
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            _('There was an error updating your booking. Please check the form and try again.')
        )
        return super().form_invalid(form)
