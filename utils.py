import random
import string
from app import db
from models import Category, Product

def generate_order_number():
    """Generate a unique order number"""
    return 'ORD-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def init_sample_data():
    """Initialize sample categories and products if database is empty"""
    if Category.query.count() > 0:
        return  # Data already exists
    
    # Sample categories
    categories_data = [
        {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
        {'name': 'Fashion', 'description': 'Clothing and fashion accessories'},
        {'name': 'Home & Garden', 'description': 'Home decoration and garden items'},
        {'name': 'Sports & Outdoors', 'description': 'Sports equipment and outdoor gear'},
    ]
    
    categories = []
    for cat_data in categories_data:
        category = Category(**cat_data)
        db.session.add(category)
        categories.append(category)
    
    db.session.commit()
    
    # Sample products with stock photos
    products_data = [
        # Electronics
        {
            'name': 'Wireless Headphones',
            'description': 'High-quality wireless headphones with noise cancellation',
            'price': 299.99,
            'stock_quantity': 25,
            'category_id': categories[0].id,
            'image_url': 'https://pixabay.com/get/g19b22938c01e8033d246e15a5e208723a493fc5587931e6388964ecf0746cde6738c8c2e6ddc437f5d9f9de7c776bb3ca0cf6afbedb5d3596272a5a35c542ed9_1280.jpg'
        },
        {
            'name': 'Smart Watch',
            'description': 'Advanced smartwatch with fitness tracking and notifications',
            'price': 399.99,
            'stock_quantity': 15,
            'category_id': categories[0].id,
            'image_url': 'https://pixabay.com/get/gd05a1d18f5529f83528e77a3dd23559c43407359b6dc488004651c752f29ae37aa5a0c523e55b582bd343496d8b5805b655d799214c1ad543e1483318db00604_1280.jpg'
        },
        {
            'name': 'Laptop Computer',
            'description': 'Powerful laptop for work and entertainment',
            'price': 1299.99,
            'stock_quantity': 8,
            'category_id': categories[0].id,
            'image_url': 'https://pixabay.com/get/gce21fea8cc3fcde872dd4e03886bc0bc7cddb2189b4840b696a64b8c96ed4ab8ee1575482df6966e2e2b87680d52c5131d9842280b5d21b81804b21c1f00ef17_1280.jpg'
        },
        {
            'name': 'Smartphone',
            'description': 'Latest smartphone with advanced camera and features',
            'price': 899.99,
            'stock_quantity': 20,
            'category_id': categories[0].id,
            'image_url': 'https://pixabay.com/get/ga107155791b382b10c89a2d95a7971ddf10f01aff12c4ea8699c258bdbc6330a714abb0ccd4a3e67a2bfb5c53675734c0835a48e9f9153cef90ef5ed96f99576_1280.jpg'
        },
        
        # Fashion
        {
            'name': 'Designer Sunglasses',
            'description': 'Stylish sunglasses with UV protection',
            'price': 189.99,
            'stock_quantity': 30,
            'category_id': categories[1].id,
            'image_url': 'https://pixabay.com/get/g54a9bf90aac084c140db0ecb1362c2b63eb4300eab86cf33ed798dde8e7de567f594a5a0cba149349d8fff933731338e5d168c460a4ad8273a955b968e2f9561_1280.jpg'
        },
        {
            'name': 'Luxury Handbag',
            'description': 'Premium leather handbag with elegant design',
            'price': 459.99,
            'stock_quantity': 12,
            'category_id': categories[1].id,
            'image_url': 'https://pixabay.com/get/g353beb8cc984a33c16483c1bb566d6dad8b1bccdcc1277f3932578eaadfcf233bd0c9bf26d0178d19114d730ca74159b6b092cae4656618625da1aec42837a27_1280.jpg'
        },
        {
            'name': 'Fashion Watch',
            'description': 'Elegant fashion watch for any occasion',
            'price': 249.99,
            'stock_quantity': 18,
            'category_id': categories[1].id,
            'image_url': 'https://pixabay.com/get/gf5fc030e126b77a6d82ec9ae9b090710d9323072f3c52147ba780c53a5fb4acd00e5f05e02d3ecb9f19acadc6abf3a8ce525b586516f0fd0bef5030de6484c30_1280.jpg'
        },
        {
            'name': 'Casual Sneakers',
            'description': 'Comfortable sneakers for everyday wear',
            'price': 129.99,
            'stock_quantity': 35,
            'category_id': categories[1].id,
            'image_url': 'https://pixabay.com/get/g21dbef53203ec77ff74521e0d236a72a2a833cea65d4e0f435d48162c8d5a356bd4a1ea2f3ece61128d8ac6176faee74ea28eb079f48e4ee8d18755504a1602e_1280.jpg'
        },
        
        # Home & Garden
        {
            'name': 'Coffee Machine',
            'description': 'Professional espresso coffee machine',
            'price': 699.99,
            'stock_quantity': 10,
            'category_id': categories[2].id,
            'image_url': 'https://pixabay.com/get/gdf73f45d09a1f8eca3c4e134e661909c276530b741cfde4f2dbbf7b8fa78769cbc91632315d267a327a272be78ef46a57253cf293fd4c78d256b8ebe4cefac1c_1280.jpg'
        },
        {
            'name': 'Kitchen Appliance Set',
            'description': 'Complete kitchen appliance set for modern cooking',
            'price': 899.99,
            'stock_quantity': 5,
            'category_id': categories[2].id,
            'image_url': 'https://pixabay.com/get/gab40f4a1404e8ede9652565097d00d2df39ec72c529d35088796dfb71594bd8fa0a7d4cc673368d291b37ca49872ca29f0e09f5f081d8ada67703fe67777fe32_1280.jpg'
        },
        {
            'name': 'Home Decor Items',
            'description': 'Beautiful home decoration pieces',
            'price': 149.99,
            'stock_quantity': 22,
            'category_id': categories[2].id,
            'image_url': 'https://pixabay.com/get/ga8bd8974bea19eb0281bfc2b44af43902773f70a1c0544ee74df6574f4adb808952f247fca03b72521de55772184e9b4703988d77cf919664cdc537e5c87ac21_1280.jpg'
        },
        {
            'name': 'Garden Tools',
            'description': 'Professional garden tools set',
            'price': 199.99,
            'stock_quantity': 15,
            'category_id': categories[2].id,
            'image_url': 'https://pixabay.com/get/gc35d90f06398a933cdb42688d3c6ec331a3d9d3dc0420c2c7d753d7d13c57ce5ea521fa34967b9afcb5a118319e7d8528d55ad5d075ec691e217759ea87ac635_1280.jpg'
        },
        
        # Sports & Outdoors
        {
            'name': 'Fitness Equipment',
            'description': 'Complete home fitness equipment set',
            'price': 599.99,
            'stock_quantity': 8,
            'category_id': categories[3].id,
            'image_url': 'https://pixabay.com/get/g2363323520af4a3d2bced1f274a7868780353baf83d4ef8118a61a51ababd912503b7ac0f154904454f3f1b6b20bab54e5f4d0f70691934cff701e123bb48655_1280.jpg'
        },
        {
            'name': 'Outdoor Camping Gear',
            'description': 'Essential camping gear for outdoor adventures',
            'price': 349.99,
            'stock_quantity': 12,
            'category_id': categories[3].id,
            'image_url': 'https://pixabay.com/get/g012c773211abcc5f91d855a7b919ce0acda690c49c7f4156238deff1be2f2b9ca96dbc64df27471fe46699b832eb02d135af4b7d65cca310fbdd9101295e3b4d_1280.jpg'
        },
        {
            'name': 'Sports Accessories',
            'description': 'Various sports accessories and equipment',
            'price': 79.99,
            'stock_quantity': 40,
            'category_id': categories[3].id,
            'image_url': 'https://pixabay.com/get/g32d2ee486564b7e1c0becce79bf3b98b1e2f6b162a2a5a935613e5c20bcf1f8a6c86930dd535eb33f01c4ac827351dfa0908e355f5896f00415e63e17a3677cc_1280.jpg'
        },
        {
            'name': 'Athletic Shoes',
            'description': 'Professional athletic shoes for sports',
            'price': 159.99,
            'stock_quantity': 28,
            'category_id': categories[3].id,
            'image_url': 'https://pixabay.com/get/g4502f1a95043a3a7c4048d2dd46393b77c3fc6f2926751458bc5e73421626df601f56b85cc64fa0f5680a5949da7989ec1534e666942b6031b7e179f889f334d_1280.jpg'
        }
    ]
    
    for product_data in products_data:
        product = Product(**product_data)
        db.session.add(product)
    
    db.session.commit()
    print("Sample data initialized successfully!")

def calculate_cart_total(cart_items):
    """Calculate total amount for cart items"""
    total = 0
    for item in cart_items:
        total += item['price'] * item['quantity']
    return total

def get_cart_item_count(cart_items):
    """Get total number of items in cart"""
    return sum(item['quantity'] for item in cart_items)
