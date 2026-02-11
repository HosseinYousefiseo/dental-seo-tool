import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# --- پایداری وضعیت ---
if 'step' not in st.session_state: st.session_state.step = 0
if 'data' not in st.session_state: st.session_state.data = {}

def next_step(): st.session_state.step += 1; st.rerun()
def prev_step(): st.session_state.step -= 1; st.rerun()

st.set_page_config(page_title="Dental SEO Architect Pro", page_icon="🦷", layout="wide")

# --- تابع هوشمند (حل قطعی مشکل 404) ---
def get_gemini_response(prompt_task):
    api_key = st.session_state.get('api_key')
    if not api_key: return "⚠️ کلید API را وارد کنید."
    try:
        genai.configure(api_key=api_key)
        # آدرس‌دهی مستقیم به مدل پایدار
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
        
        full_prompt = f"Role: Dental SEO Expert. Data Context: {st.session_state.data}. Task: {prompt_task}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"❌ خطا در مدل: {str(e)}"

# --- نوار پیشرفت و مراحل ---
steps_titles = ["Welcome", "Inputs", "Keyword Map", "SERP Analysis", "EEAT & Trust", "Tools & Finance", "Content & CTA", "Final Wireframe"]
st.progress(st.session_state.step / (len(steps_titles) - 1))
st.write(f"📍 گام: **{steps_titles[st.session_state.step]}**")
st.divider()

if st.session_state.step == 0:
    st.title("Dental SEO & CRO Architect Pro 🦷")
    if st.button("شروع آنالیز"): next_step()

elif st.session_state.step == 1:
    st.header("Step 1: Core Data")
    u = st.text_input("URL:", value=st.session_state.data.get('url',''))
    s = st.text_input("Service:", value=st.session_state.data.get('service',''))
    l = st.text_input("Location:", value=st.session_state.data.get('location',''))
    mk = st.text_input("Main Keyword:", value=st.session_state.data.get('main_k',''))
    
    if st.button("Save & Next"):
        st.session_state.data.update({'url':u, 'service':s, 'location':l, 'main_k':mk})
        next_step()

elif 2 <= st.session_state.step <= 7:
    task_map = {
        2: "Keyword mapping & Semantic gaps.",
        3: "SERP analysis (Local, Ads, Organic).",
        4: "Psychology, fears & trust signals.",
        5: "Interactive tools & Finance transparency.",
        6: "Copywriting, Meta tags & Sectional CTAs.",
        7: "Visual Wireframe & Sitemap flow."
    }
    st.header(steps_titles[st.session_state.step])
    if st.button(f"اجرای تحلیل {steps_titles[st.session_state.step]}"):
        with st.spinner("AI is thinking..."):
            res = get_gemini_response(task_map[st.session_state.step])
            st.session_state.data[f'res_{st.session_state.step}'] = res
    
    if f'res_{st.session_state.step}' in st.session_state.data:
        edited = st.text_area("بررسی و ویرایش:", value=st.session_state.data[f'res_{st.session_state.step}'], height=300)
        st.session_state.data[f'res_{st.session_state.step}'] = edited
        if st.button("تایید و گام بعد"): next_step()
    if st.button("بازگشت"): prev_step()

with st.sidebar:
    st.title("تنظیمات")
    st.session_state.api_key = st.text_input("Gemini API Key:", type="password")
    if st.button("ریست"): 
        st.session_state.step = 0
        st.rerun()
