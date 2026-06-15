import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="MiniStore | Premium Tech & Lifestyle",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR HOMEPAGE & FLOATING BUTTON ---
st.markdown("""
<style>
    /* Main container styling */
    .main { background-color: #f8f9fa; }
    
    /* Product Card styling */
    .product-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
        border: 1px solid #e9ecef;
        transition: transform 0.2s ease;
    }
    .product-card:hover { transform: translateY(-5px); }
    
    /* Typography inside cards */
    .product-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #212529;
        margin-bottom: 8px;
        min-height: 55px;
    }
    .product-price {
        font-size: 1.3rem;
        font-weight: 700;
        color: #007bff;
        margin-bottom: 12px;
    }
    .product-desc {
        font-size: 0.9rem;
        color: #6c757d;
        height: 60px;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 15px;
    }
    .category-badge {
        display: inline-block;
        background-color: #e9ecef;
        color: #495057;
        font-size: 0.75rem;
        padding: 4px 8px;
        border-radius: 20px;
        margin-bottom: 10px;
        text-transform: uppercase;
        font-weight: 500;
    }

    /* FLOATING SUPPORT BUTTON STYLING */
    .floating-chat-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background-color: #007bff;
        color: white !important;
        text-decoration: none !important;
        padding: 15px 25px;
        border-radius: 50px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,123,255,0.4);
        z-index: 999999;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .floating-chat-btn:hover {
        background-color: #0056b3;
        transform: scale(1.05);
    }
</style>
""", unsafe_content_type=True)

# --- FLOATING SUPPORT BUTTON INJECTION ---
# Automatically routes natively to your chatbot sub-page /chatbot
st.markdown("""
<a href="/chatbot" target="_self" class="floating-chat-btn">
    💬 Live Chat Support
</a>
""", unsafe_content_type=True)

# --- SESSION STATE INITIALIZATION ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# --- SAMPLE DATA ---
PRODUCTS = [
    {"id": 1, "name": "AeroSound Max Wireless Headphones", "price": 199.99, "category": "Electronics", "desc": "Hybrid active noise cancelling with up to 40 hours of battery life and hi-res audio."},
    {"id": 2, "name": "Chronos Minimalist Smartwatch", "price": 149.50, "category": "Electronics", "desc": "Sleek AMOLED display featuring continuous heart rate monitoring and 7-day battery."},
    {"id": 3, "name": "Apex Ergonomic Mechanical Keyboard", "price": 125.00, "category": "Electronics", "desc": "Hot-swappable linear switches with customizable RGB backlighting and aluminum frame."},
    {"id": 4, "name": "HydroVibe 1L Insulated Flask", "price": 34.99, "category": "Lifestyle", "desc": "Double-wall vacuum insulation keeps drinks ice-cold for 24 hours or hot for 12."},
    {"id": 5, "name": "Nomad Daily Canvas Backpack", "price": 85.00, "category": "Lifestyle", "desc": "Water-resistant canvas with a dedicated 16-inch laptop compartment and anti-theft pockets."},
    {"id": 6, "name": "Lumina Ambient Desk Lamp", "price": 45.99, "category": "Home Decor", "desc": "Touch-controlled LED lamp with adjustable color temperatures and integrated Qi wireless charger."}
]

# --- SIDEBAR: NAVIGATION, FILTERS & CART ---
st.sidebar.title("🏪 MiniStore Nav")
st.sidebar.markdown("---")

st.sidebar.subheader("Filter Categories")
categories = ["All Products"] + list(set(p["category"] for p in PRODUCTS))
selected_category = st.sidebar.selectbox("Choose a category:", categories)

st.sidebar.markdown("---")
st.sidebar.subheader("🛒 Your Shopping Cart")

if not st.session_state.cart:
    st.sidebar.info("Your cart is empty.")
else:
    total_cost = 0.0
    for prod_id, cart_item in list(st.session_state.cart.items()):
        item_total = cart_item['price'] * cart_item['quantity']
        total_cost += item_total
        
        st.sidebar.markdown(f"**{cart_item['name']}**")
        st.sidebar.text(f"${cart_item['price']:.2f} x {cart_item['quantity']} = ${item_total:.2f}")
        
        c1, c2 = st.sidebar.columns(2)
        if c1.button(f"➖ Reduce", key=f"sub_{prod_id}"):
            st.session_state.cart[prod_id]['quantity'] -= 1
            if st.session_state.cart[prod_id]['quantity'] <= 0:
                del st.session_state.cart[prod_id]
            st.rerun()
            
        if c2.button(f"🗑️ Remove", key=f"del_{prod_id}"):
            del st.session_state.cart[prod_id]
            st.rerun()
        st.sidebar.markdown("---")
        
    st.sidebar.markdown(f"### **Grand Total: ${total_cost:.2f}**")
    
    if st.sidebar.button("💳 Proceed to Checkout", type="primary", use_container_width=True):
        st.sidebar.success("🎉 Order placed successfully! Thank you for shopping with MiniStore.")
        st.session_state.cart = {}
        st.rerun()

# --- MAIN PAGE CONTENT ---
st.title("🛍️ MiniStore")
st.subheader("Curated Essentials for Tech & Everyday Lifestyle")
st.markdown("Welcome to **MiniStore**! Browse our catalog or tap the floating chat bubble on the bottom right to speak with our support staff.")
st.markdown("---")

filtered_products = [p for p in PRODUCTS if selected_category == "All Products" or p["category"] == selected_category]

st.header(f"✨ Featured Products ({selected_category})")

GRID_COLUMNS = 3
for i in range(0, len(filtered_products), GRID_COLUMNS):
    row_products = filtered_products[i : i + GRID_COLUMNS]
    cols = st.columns(GRID_COLUMNS)
    
    for idx, product in enumerate(row_products):
        with cols[idx]:
            st.markdown(f"""
            <div class="product-card">
                <span class="category-badge">{product['category']}</span>
                <div class="product-title">{product['name']}</div>
                <div class="product-price">${product['price']:.2f}</div>
                <div class="product-desc">{product['desc']}</div>
            </div>
            """, unsafe_content_type=True)
            
            if st.button(f"Add to Cart 🛒", key=f"btn_{product['id']}", use_container_width=True):
                prod_id = product['id']
                if prod_id in st.session_state.cart:
                    st.session_state.cart[prod_id]['quantity'] += 1
                else:
                    st.session_state.cart[prod_id] = {"name": product["name"], "price": product["price"], "quantity": 1}
                st.rerun()

st.markdown("<br><hr><center style='color: #6c757d; font-size: 0.85rem;'>© 2026 MiniStore Inc. All rights reserved.</center>", unsafe_content_type=True)