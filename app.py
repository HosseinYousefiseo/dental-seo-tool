import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# --- ۰. تنظیمات امنیتی API Key ---
GEMINI_API_KEY = "AIzaSyAp7s-XmkTvqPh1fnJlnQCu9D0M6QNdEuw"
genai.configure(api_key=GEMINI_API_KEY)

# --- ۱. تنظیمات اولیه و مدیریت نشست ---
if 'step' not in st.session_state: st.session_state.step = 0
if 'data' not in st.session_state: st.session_state.data = {}

def next_step(): 
    st.session_state.step += 1
    st.rerun()

def prev_step(): 
    if st.session_state.step > 0:
        st.session_state.step -= 1
        st.rerun()

st.set_page_config(page_title="Dental SEO Architect Pro", page_icon="🦷", layout="wide")

# --- ۲. استایل دهی اختصاصی ---
st.markdown("""
    <style>
    .stProgress > div > div > div > div { background-color: #00cc99; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; background-color: #004a99; color: white; transition: 0.3s; }
    .stButton>button:hover { background-color: #1E3A8A; color: white; border: 1px solid #00cc99; }
    .step-text { font-size: 18px; font-weight: bold; color: #004a99; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- ۳. تابع ارتباط با Gemini ---
def get_gemini_response(prompt_task):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        context = f"Role: Senior Dental SEO Manager. Project Data: {st.session_state.data}. Task: {prompt_task}"
        response = model.generate_content(context)
        return response.text
    except Exception as e: 
        return f"❌ خطا در لایه هوش مصنوعی: {str(e)}"

# --- ۴. نوار پیشرفت (بالای صفحه) ---
steps_titles = ["Welcome", "Data Input", "Keyword & Semantic", "SERP & Authority", "Psychology & Trust", "Tools & Finance", "Content & Meta", "Wireframe & Assets", "Final Portfolio"]
total_steps = len(steps_titles)

# نمایش گرافیکی نوار پیشرفت
progress_value = st.session_state.step / (total_steps - 1)
st.markdown(f"<div class='step-text'>گام {st.session_state.step + 1} از {total_steps}: {steps_titles[st.session_state.step]}</div>", unsafe_allow_html=True)
st.progress(progress_value)
st.divider()

# --- ۵. مدیریت گام‌ها ---

# گام ۰: معرفی
if st.session_state.step == 0:
    st.title("Dental SEO & CRO Architect Pro 🇨🇦")
    st.info("اتصال به Gemini برقرار شد. آماده شروع آنالیز استراتژیک هستیم.")
    if st.button("شروع پروسه"): next_step()

# گام ۱: ورودی‌ها
elif st.session_state.step == 1:
    st.header("Step 1: Deep Data Acquisition")
    col1, col2 = st.columns(2)
    with col1:
        u = st.text_input("Target URL:", value=st.session_state.data.get('url',''))
        s = st.text_input("Service Name:", value=st.session_state.data.get('service',''))
        l = st.text_input("Target City/Location:", value=st.session_state.data.get('location',''))
        c = st.multiselect("Conversion Goals (CTA):", 
                           ["Phone Call", "Booking Form", "WhatsApp Chat", "Free Consultation", "Live Chat"],
                           default=st.session_state.data.get('cta', ["Phone Call"]))
    
    with col2:
        mk = st.text_input("Main Keyword:", value=st.session_state.data.get('main_k',''))
        if st.button("Extract Keywords from URL"):
            with st.spinner("Analyzing..."):
                res = get_gemini_response(f"Extract keywords from {u}")
                st.info(f"AI Suggestions: {res[:150]}...")
        sk = st.text_area("Secondary Keywords:", value=st.session_state.data.get('sec_k',''))
    
    h_input = st.text_area("Current Headings:", value=st.session_state.data.get('headings',''), height=100)
    
    st.divider()
    c1, c2 = st.columns(2)
    with c1: st.button("🔙 Back", on_click=prev_step)
    with c2: 
        if st.button("Save & Next Step ➡️"):
            st.session_state.data.update({'url':u, 'service':s, 'location':l, 'cta':c, 'main_k':mk, 'sec_k':sk, 'headings':h_input})
            next_step()

# گام‌های تحلیلی (۲ تا ۷)
elif 2 <= st.session_state.step <= 7:
    task_map = {
        2: "Keyword Mapping & Semantic Gap.",
        3: "SERP Deep Dive Analysis.",
        4: "Identify 3 Patient Fears & E-E-A-T responses.",
        5: "Lead-gen tools & Financial layout.",
        6: "Content & Meta Strategy.",
        7: "Wireframe & JSON-LD Schema."
    }
    
    st.header(f"Step {st.session_state.step}: {steps_titles[st.session_state.step]}")
    if st.button(f"🚀 Generate {steps_titles[st.session_state.step]} Analysis"):
        with st.spinner("Gemini is thinking..."):
            res = get_gemini_response(task_map[st.session_state.step])
            st.session_state.data[f'res_{st.session_state.step}'] = res

    if f'res_{st.session_state.step}' in st.session_state.data:
        edited = st.text_area("Edit Analysis:", value=st.session_state.data[f'res_{st.session_state.step}'], height=400)
        st.session_state.data[f'res_{st.session_state.step}'] = edited
        st.divider()
        nav1, nav2 = st.columns(2)
        with nav1: st.button("🔙 Back", on_click=prev_step, key=f"b_{st.session_state.step}")
        with nav2: st.button("Confirm & Next Step ➡️", on_click=next_step, key=f"n_{st.session_state.step}")
    else:
        st.button("🔙 Back", on_click=prev_step)

# گام ۸: خروجی نهایی
elif st.session_state.step == 8:
    st.header("🏁 Final Strategy Portfolio")
    final_output = ""
    for i in range(2, 8):
        final_output += f"### {steps_titles[i]}\n\n{st.session_state.data.get(f'res_{i}', '')}\n\n---\n"
    st.markdown(final_output)
    st.download_button("📥 Download Strategy", final_output, file_name="dental_strategy.txt")
    if st.button("🗑 Restart Audit"):
        st.session_state.step = 0
        st.session_state.data = {}
        st.rerun()

with st.sidebar:
    st.title("Admin Panel")
    st.success("API Key Active ✅")
    if st.button("Reset Everything"): 
        st.session_state.step = 0
        st.session_state.data = {}
        st.rerun()
