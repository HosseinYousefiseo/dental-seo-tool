import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# --- تنظیمات پایداری وضعیت ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'data' not in st.session_state:
    st.session_state.data = {}

def next_step():
    st.session_state.step += 1
    st.rerun()

def prev_step():
    if st.session_state.step > 1:
        st.session_state.step -= 1
        st.rerun()

# --- تنظیمات صفحه ---
st.set_page_config(page_title="Dental SEO Architect", page_icon="🦷", layout="wide")

# --- تابع هوشمند ارتباط با Gemini (حل مشکل 404) ---
def get_gemini_response(prompt_task):
    api_key = st.session_state.get('api_key')
    if not api_key:
        return "⚠️ ابتدا API Key را در منوی سمت چپ وارد کنید."
    
    try:
        genai.configure(api_key=api_key)
        # استفاده از نام دقیق مدل برای نسخه v1
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        full_prompt = f"Role: Dental SEO Expert. Task: {prompt_task}. Context: {st.session_state.data}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"❌ خطای مدل گوگل: {str(e)}"

# --- رابط کاربری ---
st.title("🦷 Dental SEO & CRO Architect")

with st.sidebar:
    st.title("Control Panel")
    st.session_state.api_key = st.text_input("Gemini API Key:", type="password")
    st.divider()
    if st.session_state.step > 1:
        st.button("🔙 بازگشت به مرحله قبل", on_click=prev_step)
    if st.button("🗑 ریست کامل"):
        st.session_state.step = 1
        st.session_state.data = {}
        st.rerun()

# --- پیاده‌سازی گام‌ها ---
if st.session_state.step == 1:
    st.header("Step 1: URL & Service")
    u = st.text_input("لینک سایت:", value=st.session_state.data.get('url', ''))
    s = st.text_input("نام خدمت:", value=st.session_state.data.get('service', ''))
    if st.button("ثبت و ادامه"):
        if u and s:
            st.session_state.data['url'], st.session_state.data['service'] = u, s
            next_step()

elif st.session_state.step == 2:
    st.header("Step 2: Technical Extraction")
    if st.button("استخراج تیترها"):
        try:
            res = requests.get(st.session_state.data['url'], headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            st.session_state.data['headings'] = [h.text.strip() for h in soup.find_all(['h1','h2','h3'])]
            st.success("تیترها استخراج شد.")
        except:
            st.error("اسکرپ خودکار مسدود شد.")
    
    m = st.text_area("ورود دستی تیترها:", value="\n".join(st.session_state.data.get('headings', [])))
    if st.button("تایید و مرحله بعد"):
        st.session_state.data['headings'] = m.split('\n')
        next_step()

elif 3 <= st.session_state.step <= 12:
    tasks = {3: "Keyword Mapping", 4: "SERP Analysis", 5: "Patient Fears", 6: "Quiz Design", 
             7: "CTA Strategy", 8: "Wayfinding", 9: "Copywriting", 10: "Visual Brief", 
             11: "Internal Links", 12: "Technical Assets"}
    
    st.header(f"Step {st.session_state.step}: {tasks[st.session_state.step]}")
    if st.button("اجرای تحلیل"):
        with st.spinner("Gemini در حال تحلیل است..."):
            res = get_gemini_response(tasks[st.session_state.step])
            st.session_state.data[f'res_{st.session_state.step}'] = res
    
    if f'res_{st.session_state.step}' in st.session_state.data:
        st.info(st.session_state.data[f'res_{st.session_state.step}'])
        if st.button("YES - برو مرحله بعد"): next_step()
