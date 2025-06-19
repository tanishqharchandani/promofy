from firebase_admin import firestore
import datetime

db = firestore.client()

# USERS

def get_all_users():
    users = db.collection('users').stream()
    return [user.to_dict() | {'id': user.id} for user in users]

# BUYERS

def get_buyers():
    buyers_ref = db.collection('buyers')
    return [doc.to_dict() | {'id': doc.id} for doc in buyers_ref.stream()]

def get_buyer_by_id(buyer_id):
    doc = db.collection('buyers').document(buyer_id).get()
    return doc.to_dict() if doc.exists else None

def add_buyer(data):
    db.collection('buyers').add(data)

def update_buyer(buyer_id, data):
    data['modified_at'] = datetime.datetime.utcnow().isoformat()
    db.collection('buyers').document(buyer_id).update(data)

def delete_buyer(buyer_id):
    db.collection('buyers').document(buyer_id).delete()

def get_filtered_sorted_buyers(filter_active=None, sort_by=None, search=None):
    buyers_ref = db.collection('buyers')
    if filter_active is not None:
        buyers_ref = buyers_ref.where('is_active', '==', filter_active)
    buyers = [doc.to_dict() | {'id': doc.id} for doc in buyers_ref.stream()]
    if search:
        search = search.lower()
        buyers = [
            b for b in buyers
            if search in b.get('name', '').lower() or search in b.get('email', '').lower()
        ]
    if sort_by == 'name':
        buyers.sort(key=lambda x: x.get('name', '').lower())
    elif sort_by == 'created_at':
        buyers.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return buyers

# SELLERS

def get_sellers():
    sellers_ref = db.collection('sellers')
    return [doc.to_dict() | {'id': doc.id} for doc in sellers_ref.stream()]

def get_seller_by_id(seller_id):
    doc = db.collection('sellers').document(seller_id).get()
    return doc.to_dict() if doc.exists else None

def add_seller(data):
    db.collection('sellers').add(data)

def update_seller(seller_id, data):
    data['modified_at'] = datetime.datetime.utcnow().isoformat()
    db.collection('sellers').document(seller_id).update(data)

def delete_seller(seller_id):
    db.collection('sellers').document(seller_id).delete()

def toggle_seller_verification(user_id, current_status):
    db.collection('sellers').document(user_id).update({'is_verified': not current_status})

def get_filtered_sorted_sellers(filter_active=None, sort_by=None, search=None):
    sellers_ref = db.collection('sellers')
    if filter_active is not None:
        sellers_ref = sellers_ref.where('is_active', '==', filter_active)
    sellers = [doc.to_dict() | {'id': doc.id} for doc in sellers_ref.stream()]
    if search:
        search = search.lower()
        sellers = [
            s for s in sellers
            if search in s.get('name', '').lower() or search in s.get('email', '').lower()
        ]
    if sort_by == 'name':
        sellers.sort(key=lambda x: x.get('name', '').lower())
    elif sort_by == 'created_at':
        sellers.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return sellers

# CATEGORIES

def get_categories():
    return [doc.to_dict() | {'id': doc.id} for doc in db.collection('categories').stream()]

def get_category_by_id(category_id):
    doc = db.collection('categories').document(category_id).get()
    return doc.to_dict() if doc.exists else None

def add_category(data):
    db.collection('categories').add(data)

def update_category(category_id, data):
    db.collection('categories').document(category_id).update(data)

def delete_category(category_id):
    db.collection('categories').document(category_id).delete()

# LISTINGS

def get_all_listings():
    listings_ref = db.collection('listings')
    return [doc.to_dict() | {'id': doc.id} for doc in listings_ref.stream()]

def get_filtered_sorted_listings(category=None, featured=None, sort_by=None, search=None):
    listings_ref = db.collection('listings')
    listings = [doc.to_dict() | {'id': doc.id} for doc in listings_ref.stream()]
    if category:
        listings = [l for l in listings if l.get('category', '').lower() == category.lower()]
    if featured is not None:
        listings = [l for l in listings if l.get('is_featured') == featured]
    if search:
        search = search.lower()
        filtered = []
        for l in listings:
            title = l.get('title', '').lower()
            category_val = l.get('category', '').lower()
            location = l.get('location', '').lower()
            if search in title or search in category_val or search in location:
                filtered.append(l)
        listings = filtered
    if sort_by == 'title':
        listings.sort(key=lambda x: x.get('title', '').lower())
    elif sort_by == 'price':
        listings.sort(key=lambda x: x.get('price', 0))
    elif sort_by == 'created_at':
        listings.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return listings

def get_listing_by_id(listing_id):
    doc = db.collection('listings').document(listing_id).get()
    return doc.to_dict() if doc.exists else None

def update_listing(listing_id, data):
    db.collection('listings').document(listing_id).update(data)

def delete_listing(listing_id):
    db.collection('listings').document(listing_id).delete()

def toggle_featured_status(listing_id, current_status):
    db.collection('listings').document(listing_id).update({'is_featured': not current_status})

def get_filtered_sorted_categories(filter_active=None, sort_by=None, search=None):
    categories_ref = db.collection('categories')
    
    if filter_active is not None:
        categories_ref = categories_ref.where('is_active', '==', filter_active)

    categories = [doc.to_dict() | {'id': doc.id} for doc in categories_ref.stream()]

    # Apply search
    if search:
        search = search.lower()
        categories = [
            c for c in categories
            if search in c.get('name', '').lower()
        ]

    # Sort
    if sort_by == 'name':
        categories.sort(key=lambda x: x.get('name', '').lower())
    elif sort_by == 'created_at':
        categories.sort(key=lambda x: x.get('created_at', ''), reverse=True)

    return categories

def get_filtered_sorted_ads(filter_active=None, sort_by=None, search=None):
    ads_ref = db.collection('ads')

    if filter_active is not None:
        ads_ref = ads_ref.where('is_active', '==', filter_active)

    ads = [doc.to_dict() | {'id': doc.id} for doc in ads_ref.stream()]

    # Apply search
    if search:
        search = search.lower()
        ads = [
            a for a in ads
            if search in a.get('title', '').lower() or search in a.get('description', '').lower()
        ]

    # Sort
    if sort_by == 'title':
        ads.sort(key=lambda x: x.get('title', '').lower())
    elif sort_by == 'price':
        ads.sort(key=lambda x: x.get('price', 0))
    elif sort_by == 'created_at':
        ads.sort(key=lambda x: x.get('created_at', ''), reverse=True)

    return ads

# Get single ad by ID
def get_ad_by_id(ad_id):
    doc = db.collection('ads').document(ad_id).get()
    if doc.exists:
        return doc.to_dict() | {'id': doc.id}
    return None

# Add a new ad
def add_ad(data):
    data['created_at'] = datetime.datetime.utcnow().isoformat()
    data['modified_at'] = datetime.datetime.utcnow().isoformat()
    db.collection('ads').add(data)

# Update ad
def update_ad(ad_id, data):
    data['modified_at'] = datetime.datetime.utcnow().isoformat()
    db.collection('ads').document(ad_id).update(data)

# Delete ad
def delete_ad(ad_id):
    db.collection('ads').document(ad_id).delete()


def get_all_inquiries():
    docs = db.collection('inquiries').stream()
    return [{**doc.to_dict(), 'id': doc.id} for doc in docs]

def get_inquiries_by_seller(seller_id):
    docs = db.collection('inquiries').where('seller_id', '==', seller_id).stream()
    return [{**doc.to_dict(), 'id': doc.id} for doc in docs]

def delete_inquiry(inquiry_id):
    db.collection('inquiries').document(inquiry_id).delete()

def get_ad_by_id(ad_id):
    return db.collection('ads').document(ad_id).get().to_dict()

def get_buyer_by_id(buyer_id):
    return db.collection('buyers').document(buyer_id).get().to_dict()

def get_seller_by_id(seller_id):
    return db.collection('sellers').document(seller_id).get().to_dict()
