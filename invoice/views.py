from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required , user_passes_test
from .models import *
from .forms import *
from uuid import uuid4
from .views import *
from django.conf import settings
from decimal import Decimal



@login_required(login_url='signIn')
def invoiceList(request):
    try:
        # Retrieve the vendor linked with the logged-in user
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        # If no vendor is associated with the user, show an error or empty list
        messages.error(request, "No vendor associated with your account.")
        return render(request, 'invoice/invoice.html', {'invoices': []})

    # Fetch only the invoices associated with the vendor
    invoices = Invoice.objects.filter(vendor=vendor)
    invoice_data = []

    for invoice in invoices:
        # Ensure all financial calculations use Decimal
        sub_total = Decimal(invoice.sub_total or 0)
        other_fee_amount = Decimal(invoice.other_fees_amount or 0)

        # Calculate the total for each invoice
        invoice_total = sub_total + other_fee_amount

        invoice_data.append({
            'invoice': invoice,
            'invoice_total': invoice_total,
        })

    context = {
        'invoices': invoice_data,
    }

    return render(request, 'invoice/invoice.html', context)

@login_required(login_url='signIn')
def createInvoice(request):
    # Ensure that the logged-in user has an associated Vendor
    try:
        vendor = Vendor.objects.get(user=request.user)  # Adjust according to your Vendor model
    except Vendor.DoesNotExist:
        messages.error(request, "You must have a vendor account to create an invoice.")
        return redirect('some_redirect_url')  # Redirect to an appropriate page

    # Create a blank invoice
    number = 'INV-' + str(uuid4()).split('-')[1]
    new_invoice = Invoice.objects.create(number=number, vendor=vendor)  # Use the Vendor instance
    new_invoice.save()

    inv = Invoice.objects.get(number=number)

    Invoice.delete_blank_invoices()

    return redirect('create-build-invoice', slug=inv.slug)


@login_required(login_url='signIn')
def createBuildInvoice(request, slug):
    # Retrieve the invoice or show an error message
    try:
        invoice = Invoice.objects.get(slug=slug)
        pass
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoiceList')

    # Check if the vendor is associated with the invoice
    if not invoice.vendor:
        messages.error(request, "No vendor associated with the invoice.")
        return redirect('invoiceList')  # Adjust to your appropriate redirect 

    # Calculate totals and populate context data
    #fetch all the products - related to this invoice
    other_fee_name = invoice.other_fees_name
    other_fee_amount = invoice.other_fees_amount or 0 
    total = (invoice.sub_total or 0) + other_fee_amount 

    context = {}
    context['invoice'] = invoice
    context['other_fee_name'] = other_fee_name
    context['other_fee_amount'] = other_fee_amount
    context['total'] = total


    if request.method == 'GET':
        prod_form  = ItemForm(vendor=invoice.vendor)
        other_fee_form = otherFeeForm(instance=invoice)
        inv_form = invoiceForm(instance=invoice)
        item_selection_form = ItemSelectionForm(vendor=invoice.vendor)


        context['item_selection_form'] = item_selection_form
        context['prod_form'] = prod_form
        context['inv_form'] = inv_form
        context['other_fee_form'] = other_fee_form
        context['invoice'] = invoice
        return render(request, 'invoice/create.html', context)
    
    if request.method == 'POST':
        prod_form  = ItemForm(request.POST, vendor=invoice.vendor)
        inv_form = invoiceForm(request.POST, instance=invoice)
        other_fee_form = otherFeeForm(request.POST, instance=invoice)
        item_selection_form = ItemSelectionForm(request.POST , vendor=invoice.vendor)
        
        if item_selection_form.is_valid() and 'quantity' in request.POST:
            selected_item = item_selection_form.cleaned_data['selected_item']
            quantity = item_selection_form.cleaned_data['quantity']

            if invoice.sub_total is None:
                invoice.sub_total = 0.0

            item_instance = Product.objects.get(pk=selected_item.pk)

            # Check if an InvoiceItem for the selected item already exists for this invoice
            existing_invoice_item = InvoiceItem.objects.filter(invoice=invoice, item=item_instance).first()

            if existing_invoice_item:
                # Update the existing InvoiceItem
                existing_invoice_item.quantity += quantity
                existing_invoice_item.sub_total += item_instance.discounted_price * quantity
                existing_invoice_item.save()
            else:
                # Create a new InvoiceItem
                invoice_item = InvoiceItem.objects.create(
                    invoice=invoice,
                    item=item_instance,
                    unit_type=item_instance.unit_type,
                    quantity=quantity,
                    unit_price=item_instance.discounted_price,
                    sub_total=item_instance.discounted_price * quantity
                )
                invoice.products.add(item_instance)

            # Update subtotal
            invoice.sub_total += item_instance.discounted_price * quantity

            invoice.save()
            messages.success(request, "Item added to the invoice successfully")
            return redirect('create-build-invoice', slug=slug)
      
        
        elif inv_form.is_valid() and 'status' in request.POST:
            invoice_instance = inv_form.save(commit=False)  # Don't save immediately
            if not invoice_instance.number:  # Ensure number is generated if not present
                latest_invoice = Invoice.objects.order_by('id').last()
                next_number = f"INV-{(latest_invoice.id if latest_invoice else 0) + 1}"
                invoice_instance.number = next_number

            invoice_instance.save()  # Now save the instance
            messages.success(request, "Invoice updated successfully")
            return redirect('InvoiceList')
                
        
        
        elif other_fee_form.is_valid() and 'other_fees_amount' in request.POST:
                other_fees_name = other_fee_form.cleaned_data['other_fees_name']
                other_fees_amount = other_fee_form.cleaned_data['other_fees_amount']
                
                if other_fees_amount < 0:
                    messages.warning(request, "Other fees amount cannot be less than 0.")
                else:
                    other_fee_form.save()
                    messages.success(request, "Other fees updated successfully")
                
                return redirect('create-build-invoice', slug=slug)
        else:
            context['prod_form'] = prod_form
            context['inv_form'] = inv_form
            context['other_fee_form'] = other_fee_form
            context['item_selection_form'] = item_selection_form
            messages.error(request,"Problem processing your request")
            return render(request, 'invoice/create.html', context)
        
    return render(request, 'invoice/create.html', context)



    




@login_required(login_url='login')
def delete_invoice_product(request, slug, product_id):
    invoice = get_object_or_404(Invoice, slug=slug)
    product = get_object_or_404(Product, id=product_id)
    invoice_item = InvoiceItem.objects.filter(invoice=invoice, item=product).first()

    invoice.products.remove(product)

    if invoice_item:
        invoice.sub_total -= invoice_item.sub_total
        invoice_item.delete()

    if not invoice.products.exists():
        invoice.discount_amount = 0
        invoice.tax_amount = 0
        invoice.other_fees_amount = 0

    invoice.save()
    messages.success(request, 'Item removed successfully!')
    return redirect('create-build-invoice', slug=slug)

@login_required(login_url='login')
def viewPrintnvoice(request, slug):
        # fetch that invoice
    try:
        invoice = Invoice.objects.get(slug=slug)
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoices')
    


    vendor_profile = invoice.vendor.user.userprofile  # Adjust here

    
    other_fee_name = invoice.other_fees_name
    other_fee_amount = invoice.other_fees_amount or 0 
    total = (invoice.sub_total or 0) + other_fee_amount 
    total_in_words = invoice.get_total_in_words()  # Get total in words
    total_in_words = total_in_words.replace("euro", "inr").replace("cents", "paise")  # Replace terms with Indian equivalents
    total_in_words = total_in_words.capitalize() 


    context = {
        'invoice': invoice,
        'other_fee_name' : other_fee_name,
        'other_fee_amount' : other_fee_amount,
        'total' : total,
        'total_in_words' : total_in_words, 
        'vendor_profile' : vendor_profile,
    }
    return render(request, 'invoice/inv.html', context)

@login_required(login_url='login')
def deleteInvoice(request, slug):
    try:
        Invoice.objects.get(slug=slug).delete()
        messages.success(request, 'Invoice deleted successfully')
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoiceList')

    return redirect('InvoiceList')