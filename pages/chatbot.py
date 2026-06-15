import streamlit as st
from openai import OpenAI

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Support Chatbot | MiniStore", page_icon="💬", layout="centered")

st.title("💬 MiniStore AI Assistant")
st.markdown("Our intelligent support assistant is online and ready to help you with product queries, store operations, shipping, and returns.")
st.markdown("---")

# --- INITIALIZE OPENAI CLIENT ---
# Reads automatically from .streamlit/secrets.toml or deployment environment variables
if "OPENAI_API_KEY" not in st.secrets:
    st.error("Missing OpenAI API Key! Please configure OPENAI_API_KEY in your Streamlit secrets.", icon="🔑")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- SYSTEM PROMPT & BOUNDARY DESIGN ---
# Injects context constraints and store parameters directly into the context window
SYSTEM_PROMPT = """
You are a helpful, professional, and friendly customer support representative for 'MiniStore', a premium online store specializing in tech and everyday lifestyle products.

Here is the exact live product catalog of MiniStore:
1. AeroSound Max Wireless Headphones - $199.99: Hybrid active noise cancelling with up to 40 hours of battery life and hi-res audio. (Category: Electronics)
2. Chronos Minimalist Smartwatch - $149.50: Sleek AMOLED display featuring continuous heart rate monitoring and 7-day battery. (Category: Electronics)
3. Apex Ergonomic Mechanical Keyboard - $125.00: Hot-swappable linear switches with customizable RGB backlighting and aluminum frame. (Category: Electronics)
4. HydroVibe 1L Insulated Flask - $34.99: Double-wall vacuum insulation keeps drinks ice-cold for 24 hours or hot for 12. (Category: Lifestyle)
5. Nomad Daily Canvas Backpack - $85.00: Water-resistant canvas with a dedicated 16-inch laptop compartment and anti-theft pockets. (Category: Lifestyle)
6. Lumina Ambient Desk Lamp - $45.99: Touch-controlled LED lamp with adjustable color temperatures and integrated Qi wireless charger. (Category: Home Decor)

Store Policies:
- Shipping: Standard delivery takes 3-5 business days. Express shipping takes 1-2 business days. Free tracking coordinates are provided.
- Returns & Refunds: We accept returns for unopened/unused items within 30 days of standard drop-off dates. Refund processing takes 5-7 business banking days to settle. Contact returns@ministore.com for labels.
- Payments: We accept Visa, Mastercard, AMEX, Apple Pay, Google Pay, and PayPal.
- Order Status: Customers can look up status updates using their 8-digit order number from their receipt email.

STRICT BEHAVIOR RULES:
- You may ONLY assist users with topics directly related to MiniStore (products, orders, checkout, delivery, refunds, returns, operations, or payments).
- If the user asks general-knowledge questions, programming assistance, creative tasks, or anything unrelated to MiniStore, you must politely decline and redirect them back to store support topics. Keep your answers concise, clear, and helpful.
"""

# --- CHAT HISTORY INITIALIZATION ---
if "openai_messages" not in st.session_state:
    st.session_state.openai_messages = [
        {"role": "assistant", "content": "Hello! I am your MiniStore Support Assistant. How can I assist you with your shopping experience today?"}
    ]

# Render existing conversation thread to UI container view
for msg in st.session_state.openai_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- USER ENTRY AND API PIPELINE ---
if user_prompt := st.chat_input("Ask about products, orders, returns..."):
    # 1. Render and commit user input to context array
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.openai_messages.append({"role": "user", "content": user_prompt})
    
    # 2. Call chat completion endpoint
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Build payload incorporating system constraints along with the current session state
            api_payload = [{"role": "system", "content": SYSTEM_PROMPT}] + [
                {"role": m["role"], "content": m["content"]} for m in st.session_state.openai_messages
            ]
            
            # Request response completion
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=api_payload,
                temperature=0.3 # Low temperature ensures high predictability and stricter policy adherence
            )
            
            bot_reply = response.choices[0].message.content
            message_placeholder.markdown(bot_reply)
            
            # 3. Save assistant reply state
            st.session_state.openai_messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            st.error(f"An error occurred while connecting to the assistant: {str(e)}")