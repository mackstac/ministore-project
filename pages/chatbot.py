import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Support Chatbot | MiniStore", page_icon="💬", layout="centered")

st.title("💬 MiniStore Assistant")
st.markdown("How can we help you today? Ask us about our products, delivery, order status, payments, or return policies.")
st.markdown("---")

# --- KNOWLEDGE BASE ---
PRODUCTS_INFO = [
    {"name": "AeroSound Max Wireless Headphones", "price": "$199.99", "details": "Active noise cancelling with 40-hour battery life."},
    {"name": "Chronos Minimalist Smartwatch", "price": "$149.50", "details": "AMOLED screen with continuous heart rate monitoring."},
    {"name": "Apex Ergonomic Mechanical Keyboard", "price": "$125.00", "details": "Hot-swappable linear switches with customizable RGB layout."},
    {"name": "HydroVibe 1L Insulated Flask", "price": "$34.99", "details": "Double-wall vacuum insulation keeping drinks cold for 24 hours."},
    {"name": "Nomad Daily Canvas Backpack", "price": "$85.00", "details": "Water-resistant build with a secure 16-inch laptop partition."},
    {"name": "Lumina Ambient Desk Lamp", "price": "$45.99", "details": "Touch-controlled LED lamp offering integrated Qi wireless charging capabilities."}
]

# --- INTENT INTERPRETATION LOGIC ---
def get_rule_based_response(user_text):
    text = user_text.lower()
    
    # 1. Product Related Queries
    if "product" in text or "item" in text or "stock" in text or "catalog" in text:
        reply = "We offer premium selected products. Here is our live collection:\n\n"
        for p in PRODUCTS_INFO:
            reply += f"• **{p['name']}** ({p['price']}) - _{p['details']}_\n"
        return reply
        
    # Check for individual specific products
    for p in PRODUCTS_INFO:
        if p['name'].lower().split()[0] in text:
            return f"The **{p['name']}** is currently available for **{p['price']}**. Description: {p['details']} It's fully backed by our 30-day structural warranty!"

    # 2. Delivery & Shipping Queries
    if "delivery" in text or "shipping" in text or "ship" in text or "arrive" in text:
        return "📦 **Shipping Info:** Standard fulfillment takes 3-5 business days. Express shipping options take 1-2 business days. We provide free tracking coordinates as soon as packages ship out!"

    # 3. Order Tracking Status
    if "status" in text or "track" in text or "order" in text:
        return "🔍 **Order Lookups:** You can check status updates by referencing your 8-digit order number from your receipt email. If you don't have it, drop your email here and an agent will follow up!"

    # 4. Refunds Policy
    if "refund" in text or "money back" in text:
        return "💰 **Refund Policy:** Once processed internally, credit adjustments reflect on your original billing statement within 5-7 business banking loops."

    # 5. Returns Actions
    if "return" in text or "exchange" in text:
        return "🔄 **Hassle-Free Returns:** We accept unopened/unused merchandise returns within 30 days of standard drop-off dates. Contact returns@ministore.com to print your free return shipping label."

    # 6. Payment Support
    if "payment" in text or "pay" in text or "card" in text or "paypal" in text:
        return "💳 **Accepted Payments:** MiniStore accepts all major credit networks (Visa, Mastercard, AMEX), Apple Pay, Google Pay, and PayPal securely."

    # Default fallback
    return "🤖 I'm specialized in answering store inquiries! Try asking about our **products**, **delivery times**, **order status**, **payments**, or our **return policy**."

# --- CHAT HISTORY RETRIEVAL ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there! I'm your MiniStore Virtual Assistant. How can I guide you today?"}
    ]

# Render existing thread elements
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- USER SUBMISSION ENGINE ---
if user_prompt := st.chat_input("Ask MiniStore Support..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    bot_reply = get_rule_based_response(user_prompt)
    
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})