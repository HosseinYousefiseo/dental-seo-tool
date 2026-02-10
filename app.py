import streamlit as st
import requests
from bs4 import BeautifulSoup
import json

# --- پایداری وضعیت برنامه ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'data' not in st.session_state:
    st.session_state.data = {}

def next_step():
    st.session_state.step += 1
    st.rerun()

# --- تنظیمات ظاهر حرفه‌ای ---
st.set_page_config(page_title="Dental SEO Architect", page_icon="🦷", layout="wide")

# --- تابع ارتباط با Gemini (بدون واسطه و مستقیم) ---
def get_gemini_response(prompt_task):
    api_key = st.session_state.get('api_key')
    if not api_key:
        return "⚠️ کلید API وارد نشده است."
    
    # آدرس رسمی API گوگل
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    # ساختار درخواست طبق مستندات ۲۰۲۶ گوگل
    payload = {
        "contents": [{
            "parts": [{"text": f"Task: {prompt_task}. Context Data: {st.session_state.data}"}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        elif response.status_code == 403:
            return "❌ خطا 403: سرور شما در لیست تحریم گوگل است (آی‌پی ایران شناسایی شد)."
        else:
            return f"❌ خطای گوگل: {response.status_code}"
    except Exception as e:
        return f"❌ خطای اتصال: {str(e)}"

# --- رابط کاربری ---
st.title("🦷 Dental SEO & CRO Architect")

with st.sidebar:
    st.title("Settings")
    st.session_state.api_key = st.text_input("Gemini API Key:", type="password")
    if st.button("شروع دوباره"):
        st.session_state.step = 1
        st.session_state.data = {}
        st.rerun()

# --- پیاده‌سازی گام‌ها ---
if st.session_state.step == 1:
    st.header("Step 1: URL Lock")
    u = st.text_input("لینک سایت:")
    s = st.text_input("نوع خدمت (مثلا Invisalign):")
    if st.button("ذخیره و مرحله بعد"):
        if u and s:
            st.session_state.data['url'], st.session_state.data['service'] = u, s
            next_step()

elif st.session_state.step == 2:
    st.header("Step 2: Scraper")
    if st.button("استخراج تیترها"):
        try:
            res = requests.get(st.session_state.data['url'], headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            st.session_state.data['headings'] = [h.text.strip() for h in soup.find_all(['h1','h2','h3'])]
            st.success("تیترها با موفقیت استخراج شد.")
        except:
            st.error("اسکرپ خودکار مسدود شد.")
    
    m = st.text_area("ورود دستی تیترها:")
    if st.button("تایید و ادامه"):
        if m: st.session_state.data['headings'] = m.split('\n')
        next_step()

elif 3 <= st.session_state.step <= 12:
    tasks = {3: "Keywords", 4: "SERP Analysis", 5: "Patient Fears", 6: "Quiz Design", 
             7: "CTA Strategy", 8: "Wayfinding", 9: "Copywriting", 10: "Visual Brief", 
             11: "Internal Links", 12: "Technical Assets"}
    
    st.header(f"Step {st.session_state.step}: {tasks[st.session_state.step]}")
    if st.button("اجرای تحلیل"):
        with st.spinner("در حال محاسبه..."):
            res = get_gemini_response(tasks[st.session_state.step])
            st.session_state.data[f'res_{st.session_state.step}'] = res
    
    if f'res_{st.session_state.step}' in st.session_state.data:
        st.info(st.session_state.data[f'res_{st.session_state.step}'])
        if st.button("برو به مرحله بعدی"): next_step()