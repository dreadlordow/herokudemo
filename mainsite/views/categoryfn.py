from mainsite.models import Product


def category_fn():
    categories = [c[0] for c in Product.cat]
    return categories