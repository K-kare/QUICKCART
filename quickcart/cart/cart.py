from decimal import Decimal
from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key', {})

        if 'session_key' not in self.session:
            self.session['session_key'] = cart

        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = int(quantity)

        if product_id in self.cart:
            self.cart[product_id] += product_qty  # Update quantity instead of ignoring
        else:
            self.cart[product_id] = product_qty

        self.session.modified = True

    def cart_total(self):
        from decimal import Decimal  # Ensure Decimal is imported
        total = Decimal(0)
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            product_id = str(product.id)  # Convert to string for lookup
            if product_id in self.cart:
                if product.is_sale:
                    total += product.sale_price * self.cart[product_id]
                else:
                     total += product.price * self.cart[product_id]# Ensure correct multiplication

        return total

    def __len__(self):
        return len(self.cart)

    def get_prods(self): 
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quants(self):
        return self.cart  # No need to redefine

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        self.cart[product_id] = product_qty
        self.session.modified = True
        return self.cart  # Return updated cart

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True
