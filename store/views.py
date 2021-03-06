from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import Product, Basket, Customer, Address, Order, ProductReview
from django.contrib.auth.models import User
from store.forms import OrderAddressForm, ProductReviewForm
from django.contrib import messages
# from django.http import JsonResponse


def home(request):
    user = request.user
    products = Product.objects.all()
    latest = [] # aka favorite brands
    most_popular = []
    just_for_you = []

    for product in products:
        latest.append(product)
        if product.times_ordered > 4:
            most_popular.append(product)
    latest.reverse()

    if user.is_authenticated:
        try:
            customer = Customer.objects.get(name=user)
            baskets = customer.basket_set.filter(open_basket=True)
            if baskets:
                totalItems = 0
                categories = []

                for basket in baskets:
                    totalItems += basket.quantity
                    if basket.product.category not in categories:
                        categories.append(basket.product.category)

                for category in categories:
                    category_items = Product.objects.filter(category=category)
                    for item in category_items:
                        just_for_you.append(item)

                # customer.total_items = totalItems
                customer.save()

                context = {
                        "most_popular_len": len(most_popular),
                        "latest_len": len(latest),
                        "just_for_you_len": len(just_for_you),
                        "most_popular": most_popular,
                        "latest": latest,
                        "just_for_you": just_for_you,
                    }
                return render(request, "store/home.html", context)

            else:
                context = {
                    "most_popular": most_popular,
                    "most_popular_len": len(most_popular),
                    "latest": latest,
                    "latest_len": len(latest),
                }
                return render(request, "store/home.html", context)

        except Customer.DoesNotExist:
            Customer.objects.create(name=user, total_items=0)
            context = {
                "most_popular": most_popular,
                "most_popular_len": len(most_popular),
                "latest": latest,
                "latest_len": len(latest),
            }
            return render(request, "store/home.html", context)

    else:
        context = {
                    "most_popular": most_popular,
                    "most_popular_len": len(most_popular),
                    "latest_len": len(latest),
                    "latest": latest,
                }
        return render(request, "store/home.html", context)


def category(request, pk):
    product = get_object_or_404(Product, pk=pk)
    category = product.category
    products = Product.objects.filter(category=category)

    if request.GET.get("string"):
        string_data = request.GET.get("string")
        string_list = string_data.split("_")
        sort_price_by = "_".join(string_list[1: ])
        
        if sort_price_by == "price_low_to_high":
            sorted_items = Product.objects.filter(category=category).order_by("price")
            context = {
                "category": category,
                "products": sorted_items,
                "product": product,
                "products_len": len(sorted_items),
                "price_low_to_high": "Price low to high"
            }
            return  render(request, "store/category.html", context)

        elif sort_price_by == "price_high_to_low":
            sorted_items = Product.objects.filter(category=category).order_by("-price")
            context = {
                "category": category,
                "products": sorted_items,
                "products_len": len(sorted_items),
                "product": product,
                "price_high_to_low": "Price high to low"
            }
            return  render(request, "store/category.html", context)

        else:
            context = {
                "category": category,
                "products": products,
                "product": product,
                "products_len": len(products),
                "best_match": "Best match"
            }
            return  render(request, "store/category.html", context)
    else:
        context = {
            "category": category,
            "products": products,
            "product": product,
            "products_len": len(products),
            "best_match": "Best match"
        }
        return  render(request, "store/category.html", context)


def sub_category(request, pk):
    product = get_object_or_404(Product, pk=pk)
    sub_category = product.sub_category
    products = Product.objects.filter(sub_category=sub_category)
    
    if request.GET.get("string"):
        string = request.GET.get("string")
        choice = ""
        items = ""
        products_len = ""

        if string == "high_to_low":
            choice = "Price high to low"
            items = products.order_by("-price")
            products_len = len(items)
        elif string == "low_to_high":
            choice = "Price low to high"
            items = products.order_by("price")
            products_len = len(items)
        elif string == "best_match":
            choice = "Best match"
            items = products
            products_len = len(items) 
        context = {
            "choice": choice,
            "products": items,
            "products_len": products_len,
            "sub_category": sub_category,
            "product": product,
        }
        return render(request, "store/sub_category.html", context)
    else:
        context = {
            "sub_category": sub_category,
            "products": products,
            "product": product,
            "products_len": len(products),
            "choice": "Best match",
        }
        return render(request, "store/sub_category.html", context)


def shop_by_brand(request):
    products = Product.objects.all()
    brands = {}
    total_items = {}
    for product in products:
        brands.setdefault(product.company, product)
        total_items.setdefault(product.company, 0)
        total_items[product.company] =  total_items[product.company]+1
    context = {
        "brands": brands,
        "total_items": total_items,
        "brands_len": len(brands.keys()),
    }
    
    return render(request, "store/shop_by_brand.html", context)


def brand_name(request, pk):
    product = get_object_or_404(Product, pk=pk)
    brand_name = product.company
    products = Product.objects.filter(company=brand_name)

    if request.GET.get("string"):
        string = request.GET.get("string")
        choice = ""
        items = ""
        products_len = ""

        if string == "high_to_low":
            choice = "Price high to low"
            items = products.order_by("-price")
            products_len = len(items)
        elif string == "low_to_high":
            choice = "Price low to high"
            items = products.order_by("price")
            products_len = len(items)
        elif string == "best_match":
            choice = "Best match"
            items = products
            products_len = len(items) 
        context = {
            "choice": choice,
            "products": items,
            "products_len": products_len,
            "brand_name": brand_name,
            "product": product,
        }
        return render(request, "store/brand_name.html", context)

    else:
        context = {
            "products": products, 
            "brand_name": brand_name,
            "products_len": len(products),
            "product": product,
            "choice": "Best match"
        }
        return render(request, "store/brand_name.html", context)



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "store/product_detail.html", {"product": product})


@login_required
def add_to_basket(request, pk):
    user = request.user
    customer = Customer.objects.get(name=user)
    product = Product.objects.get(pk=pk)
    baskets = customer.basket_set.filter(open_basket=True)
    counter = 0
    for basket in baskets:
        if basket.product.product_name == product.product_name:
            counter += 1
            basket.quantity += 1
            customer.total_items +=1
            product.times_ordered +=1
            basket.save()
            product.save()
            customer.save()
    if counter == 0:
        Basket.objects.create(customer=customer, product=product, quantity=1)
        customer.total_items +=1
        product.times_ordered +=1
        product.save()
        customer.save()
    return redirect("store:my_basket")


@login_required
def my_basket(request):
    user = request.user
    customer = get_object_or_404(Customer, name=user)
    baskets = customer.basket_set.filter(open_basket=True)
    products = []
    you_may_also_like = []
    new_products = []
    if not baskets:
        messages.info(request, f"Customer {customer}, your bakset is empty.")
        return redirect("store:home")
    else:
        for basket in baskets:
            products.append(basket.product.product_name)
            item_category = basket.product.category
            new_products += Product.objects.filter(category=item_category)

        for product in new_products:
            name = product.product_name
            if name not in products:
                you_may_also_like.append(product)

        products.clear()
        new_products.clear()

        for product in you_may_also_like:
            if product.product_name not in products:
                products.append(product.product_name)

        for product in products:
            product_instance = Product.objects.get(product_name=product)
            new_products.append(product_instance)

        context = {
            "new_products": new_products,
            "baskets": baskets
        }
        return render(request, "store/my_basket.html", context)


@login_required
def add_item(request, pk):
    user = request.user
    customer = get_object_or_404(Customer, name=user)
    basket = customer.basket_set.get(pk=pk)
    product = Product.objects.get(pk=basket.product.id)
    product.times_ordered += 1
    basket.quantity += 1
    basket.save()
    product.save()
    return redirect("store:my_basket")


@login_required
def delete_item(request, pk):
    user = request.user
    customer = get_object_or_404(Customer, name=user)
    basket = customer.basket_set.get(pk=pk)
    product = Product.objects.get(pk=basket.product.id)
    product.times_ordered -= 1
    product.save()
    if basket.quantity == 1:
        basket.delete()
    else:
        basket.quantity -= 1
        basket.save()
    return redirect("store:my_basket")


@login_required
def delete_basket(request, pk):
    user = request.user
    customer = get_object_or_404(Customer, name=user)
    basket = customer.basket_set.get(pk=pk)
    product_in_basket = basket.product.product_name
    product = Product.objects.filter(product_name=product_in_basket).first()
    product.times_ordered -= basket.quantity
    product.save()
    basket.delete()
    return redirect("store:my_basket")

@login_required
def shipping_address(request):
    user = request.user
    customer = Customer.objects.get(name=user)
    addresses = Address.objects.filter(customer=customer)
    if request.method == "POST":
        form = OrderAddressForm(request.POST)
        addresses.delete()
        if form.is_valid():
            address = form.save()
            customer = Customer.objects.get(name=user)
            address.customer = customer
            address.save()
            # create order
            baskets = customer.basket_set.filter(open_basket=True)
            for basket in baskets:
                Order.objects.create(customer=customer, basket=basket)
                basket.open_basket = False # set open baskets to False
                basket.save()
            orders = customer.order_set.filter(open_order=True)
            total_amount_due = 0
            total_items = 0
            for order in orders:
                total_items += order.basket.quantity
                total_amount_due += order.basket.quantity * order.basket.product.price
            context = {
                "orders": orders,
                "total_items": total_items,
                "total_amount_due": total_amount_due
            }
            return render(request, "store/paypal_payment.html", context)
    else:
        # customer = Customer.objects.get(name=user)
        # addresses = Address.objects.filter(customer=customer)
        customer_address = []
        if addresses.count() > 0:
            for address in addresses:
                customer_address.append(address)
            form = OrderAddressForm(instance=customer_address[-1])
            # addresses.delete()
            customer = get_object_or_404(Customer, name=user)
            baskets = customer.basket_set.filter(open_basket=True)
            if not baskets:
                return redirect("store:home")
            else:
                return render(request, "store/shipping_address.html", {"form": form})
        else:
            form = OrderAddressForm()
        return render(request, "store/shipping_address.html", {"form": form})


@login_required
def my_orders(request):
    user = request.user
    products = Product.objects.all()
    customer = get_object_or_404(Customer, name=user)
    closed_orders = customer.order_set.filter(open_order=False)
    orders = customer.order_set.filter(open_order=True)
    total_amount_due = 0
    total_items = 0
    popular = []

    if not closed_orders and not orders:
        messages.info(request, f"Customer {customer}, you do not have order history.")
        return redirect("store:home")
    else:
        for product in products:
            if product.times_ordered >= 10:
                popular.append(product)

        for order in orders:
            total_items += order.basket.quantity
            total_amount_due += order.basket.quantity * order.basket.product.price

        context = {
            "popular": popular,
            "orders": orders,
            "closed_orders": closed_orders,
            "total_items": total_items,
            "total_amount_due": total_amount_due
        }
        return render(request, "store/my_orders.html", context)



@login_required
def paypal_payment(request):
    user = request.user
    customer = get_object_or_404(Customer, name=user)
    orders = customer.order_set.filter(open_order=True)
    if orders:
        total_amount_due = 0
        total_items = 0
        for order in orders:
            total_items += order.basket.quantity
            total_amount_due += order.basket.quantity * order.basket.product.price
        context = {
            "orders": orders,
            "total_items": total_items,
            "total_amount_due": total_amount_due
        }
        return render(request, "store/paypal_payment.html", context)
    else:
        messages.info(request, f"Customer {customer}, you do not have payment due.")
        return redirect("store:home")


@login_required
def order_complete(request):
    user = request.user
    customer = get_object_or_404(Customer, name=user)
    orders = customer.order_set.filter(open_order=True)
    for order in orders:
        order.open_order = False
        order.save()
    return render(request, "store/order_complete.html", {})


@login_required
def product_review(request, pk):
    user = request.user
    customer = Customer.objects.filter(name=user).first()
    product = Product.objects.get(pk=pk)
    reviews =  ProductReview.objects.filter(author=customer)
    reviewed_products = reviews.filter(product=product)
    if request.method == "POST":
        form = ProductReviewForm(request.POST)
        reviewed_products.delete()
        if form.is_valid():
            review_form = form.save()
            review = ProductReview.objects.get(pk=review_form.pk)
            review.author= customer
            review.product = product
            product_rating = request.POST["rate"]
            if product_rating == int(0):
                pass
            else:
                review.review_rating = int(product_rating)
                review.save()
                total_reviewed_products = ProductReview.objects.filter(product=product)
                num_of_items = 0
                stars = 0
                for total_product in total_reviewed_products:
                    stars += total_product.review_rating
                    num_of_items += 1
                rating_percent = stars / (num_of_items * 5)
                average = rating_percent * 5
                product.product_rating = round(average)
                product.save()
        return redirect("store:my_orders")
    else:
        review_instance = []
        if reviewed_products:
            for reviewed_product in reviewed_products:
                review_instance.append(reviewed_product)
            form = ProductReviewForm(instance=review_instance[-1])
            context = {
                "form": form,
                "product": product,
                "review_instance": review_instance[-1]
            }
            return render(request, "store/product_review.html", context)
        else:
            form = ProductReviewForm()
            context = {
                "form": form,
                "product": product
            }
        return render(request, "store/product_review.html", context)


def read_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.productreview_set.all()
    context = {
        "product": product,
        "reviews": reviews,
        "reviews_len": len(reviews)
    }
    return render(request, "store/read_review.html", context)


def search(request):
    if "q" in request.GET:
        if request.GET["q"]:
            search = request.GET["q"]
            products = Product.objects.filter(product_name__icontains=search)
            categories = Product.objects.filter(category__icontains=search)
            sub_categories = Product.objects.filter(sub_category__icontains=search)
            found_products = {}
            for product in products:
                found_products.setdefault(product, product.id)
            for category in categories:
                found_products.setdefault(category, category.id)
            for sub_category in sub_categories:
                found_products.setdefault(sub_category, sub_category.id)
            context = {
                "found_products": found_products,
                "found_product_len": len(found_products),
                "search": search,
                "choice": "Best match",
            }
            return render(request, "store/search_result.html", context)
        else:
            context = {
                "error": "Your search did not contain any data. Please try your search again."
            }
            return render(request, "store/search_result.html", context)

    elif request.GET.get("string"):
        string = request.GET.get("string").split(",")
        search = "".join(string[-1])
        product_sorted = "".join(string[0])
        products = Product.objects.filter(product_name__icontains=search)
        categories = Product.objects.filter(category__icontains=search)
        sub_categories = Product.objects.filter(sub_category__icontains=search)
        dict_products = {}
        sort_price = []
        found_products = {}
        choice = ''

        for product in products:
            dict_products.setdefault(product, product.id)
        for category in categories:
            dict_products.setdefault(category, category.id)
        for sub_category in sub_categories:
            dict_products.setdefault(sub_category, sub_category.id)
        
        for key in dict_products:
            sort_price.append(key.price)

        if product_sorted == "low_to_high":
            sort_price.sort() # price low to high 
            choice = "Price low to high"
        elif product_sorted == "high_to_low":
            sort_price.sort()
            sort_price.reverse() # price high to low
            choice = "Price high to low"
        else:
            choice = "Best match"
       
        for item in sort_price:
            for key, value in dict_products.items():
                if key.price == item:
                    found_products.setdefault(key, value)
        
        context = {
            "found_products": found_products,
            "found_product_len": len(found_products),
            "search": search,
            "choice": choice,
        }
        return render(request, "store/search_result.html", context)


def sort_products(request):
    user = request.user
    sort_products = Product.objects.all().order_by("price")
    products = Product.objects.all()
    latest = [] # aka favorite brands
    most_popular = []
    just_for_you = []
    sorted_most_popular = [] # for most popular at line 521 
    for product in products:
        latest.append(product)
        if product.times_ordered > 4:
            most_popular.append(product)
    latest.reverse()

    # sorted products for best_match, price_low_to_high, and price_high_to_low.
    for item in sort_products:
        if item.times_ordered > 4:
            sorted_most_popular.append(item)
    # sorted_most_popular.reverse()
    
    # if user is authenticated/logged in/ registered.
    if user.is_authenticated:
        try:
            customer = Customer.objects.get(name=user)
            # try to get user from customer class
        except Customer.DoesNotExist:
            # if user does not exist in customer class.
            Customer.objects.create(name=user, total_items=0)
            context = {
                "most_popular": most_popular,
                "most_popular_len": len(most_popular),
                "latest": latest,
                "latest_len": len(latest),
            }
            return render(request, "store/home.html", context)
            # after creating customer account, send the user to home page.
        else:
            # if user exist in customer class.
            customer = get_object_or_404(Customer, name=user)
            baskets = customer.basket_set.filter(open_basket=True)
            totalItems = 0
            categories = []
            sorted_just_for_you = [] # for just for you at line 572.

            for basket in baskets:
                totalItems += basket.quantity
                if basket.product.category not in categories:
                    categories.append(basket.product.category)

            for category in categories:
                category_items = Product.objects.filter(category=category)
                sorted_items = category_items.order_by("-price") # for just for you at line 572.
                for item in category_items:
                    just_for_you.append(item)

                for item in sorted_items:
                    sorted_just_for_you.append(item)

            customer.total_items = totalItems
            customer.save()

            # get optional string dat from the browser
            if request.GET.get("string"):
                string_parameter = request.GET.get("string")

                # sorted most popular
                if string_parameter == "most_popular_price_low_to_high":
                    context = {
                        "most_popular": sorted_most_popular,
                        "most_popular_len": len(sorted_most_popular),
                        "latest": latest,
                        "latest_len": len(latest),
                        "just_for_you": just_for_you,
                        "just_for_you_len": len(just_for_you),
                        "text_content": "most_popular_price_low_to_high"
                    }
                    return render(request, "store/home.html", context)
                elif string_parameter == "most_popular_price_high_to_low":
                    sorted_most_popular.reverse()
                    context = {
                        "most_popular": sorted_most_popular,
                        "most_popular_len": len(sorted_most_popular),
                        "latest": latest,
                        "latest_len": len(latest),
                        "just_for_you": just_for_you,
                        "just_for_you_len": len(just_for_you),
                        "text_content": "most_popular_price_high_to_low"
                    }
                    return render(request, "store/home.html", context)
                # end of sorted most popular

                # favorite brands/latest 
                elif string_parameter == "favorite_brand_price_low_to_high":
                    context = {
                        "most_popular": most_popular,
                        "most_popular_len": len(most_popular),
                        "latest": sort_products,
                        "latest_len": len(sort_products),
                        "just_for_you": just_for_you,
                        "just_for_you_len": len(just_for_you),
                        "text_content": "favorite_brand_price_low_to_high"
                    }
                    return render(request, "store/home.html", context)
                elif string_parameter == "favorite_brand_price_high_to_low":
                    sort_products = Product.objects.all().order_by("-price")
                    context = {
                        "most_popular": most_popular,
                        "most_popular_len": len(most_popular),
                        "latest": sort_products,
                        "latest_len": len(sort_products),
                        "just_for_you": just_for_you,
                        "just_for_you_len": len(just_for_you),
                        "text_content": "favorite_brand_price_high_to_low" 
                    }
                    return render(request, "store/home.html", context)
                # end of favorite brands/lates 

                 # just for you 
                elif string_parameter == "just_for_you_price_low_to_high":
                    sorted_just_for_you.reverse()

                    context = {
                        "most_popular": most_popular,
                        "most_popular_len": len(most_popular),
                        "latest": sort_products,
                        "latest_len": len(sort_products),
                        "just_for_you": sorted_just_for_you,
                        "just_for_you_len": len(sorted_just_for_you),
                        "text_content": "just_for_you_price_low_to_high"
                    }
                    return render(request, "store/home.html", context)
                elif string_parameter == "just_for_you_price_high_to_low":
                    
                    context = {
                        "most_popular": most_popular,
                        "most_popular_len": len(most_popular),
                        "latest": latest,
                        "latest_len": len(latest),
                        "just_for_you": sorted_just_for_you,
                        "just_for_you_len": len(sorted_just_for_you),
                        "text_content": "just_for_you_price_high_to_low" 
                    }
                    return render(request, "store/home.html", context)
                # end of just for you
            else:
                context = {
                        "most_popular_len": len(most_popular),
                        "latest_len": len(latest),
                        "just_for_you_len": len(just_for_you),
                        "most_popular": most_popular,
                        "latest": latest,
                        "just_for_you": just_for_you
                    }
                return render(request, "store/home.html", context)

    # if customer is not authenticated/logged in/registered.
    else:
        # get optional string dat from the browser
        if request.GET.get("string"):
            string_parameter = request.GET.get("string")
            
            # sorted most popular
            if string_parameter == "most_popular_price_low_to_high":
                context = {
                    "most_popular": sorted_most_popular,
                    "most_popular_len": len(sorted_most_popular),
                    "latest": latest,
                    "latest_len": len(latest),
                    "just_for_you": just_for_you,
                    "just_for_you_len": len(just_for_you),
                    "text_content": "most_popular_price_low_to_high"
                }
                return render(request, "store/home.html", context)
            elif string_parameter == "most_popular_price_high_to_low":
                sorted_most_popular.reverse()
                context = {
                    "most_popular": sorted_most_popular,
                    "most_popular_len": len(sorted_most_popular),
                    "latest": latest,
                    "latest_len": len(latest),
                    "just_for_you": just_for_you,
                    "just_for_you_len": len(just_for_you),
                    "text_content": "most_popular_price_high_to_low"
                }
                return render(request, "store/home.html", context)
            # end of sorted most popular

            # favorite brands/latest 
            elif string_parameter == "favorite_brand_price_low_to_high":
                context = {
                    "most_popular": most_popular,
                    "most_popular_len": len(most_popular),
                    "latest": sort_products,
                    "latest_len": len(sort_products),
                    "just_for_you": just_for_you,
                    "just_for_you_len": len(just_for_you),
                    "text_content": "favorite_brand_price_low_to_high"
                }
                return render(request, "store/home.html", context)
            elif string_parameter == "favorite_brand_price_high_to_low":
                sort_products = Product.objects.all().order_by("-price")
                context = {
                    "most_popular": most_popular,
                    "most_popular_len": len(most_popular),
                    "latest": sort_products,
                    "latest_len": len(sort_products),
                    "just_for_you": just_for_you,
                    "just_for_you_len": len(just_for_you),
                    "text_content": "favorite_brand_price_high_to_low" 
                }
                return render(request, "store/home.html", context)
            # end of favorite brands/lates
        else:
            context = {
                        "most_popular": most_popular,
                        "most_popular_len": len(most_popular),
                        "latest_len": len(latest),
                        "latest": latest,
                    }
            return render(request, "store/home.html", context)

