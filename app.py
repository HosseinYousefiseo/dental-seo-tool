import streamlit as st
import requests
from bs4 import BeautifulSoup
import json

# --- توابع مدیریت ناوبری (Navigation) ---
def next_step():
    st.session_state.step += 1
    st.rerun()

def prev_step():
    if st.session_state.step > 1:
        st.session_state.step -= 1
        st.rerun()

def restart():
    st.session_state.step = 1
    st.session_state.data = {}
    st.rerun()

# --- تنظیمات صفحه ---
st.set_page_config(page_title="Dental SEO Architect", page_icon="🦷", layout="wide")

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'data' not in st.session_state:
    st.session_state.data = {}

# --- استایل دهی ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #004a99; color: white; font-weight: bold; }
    .report-box { padding: 20px; border-radius: 12px; border: 1px solid #d1d5db; background-color: white; color: #1f2937; line-height: 1.8; }
    </style>
    """, unsafe_allow_html=True)

# --- تابع هوشمند ارتباط با Gemini (رفع خطای 404) ---
def get_gemini_response(prompt_task):
    api_key = st.session_state.get('api_key')
    if not api_key:
        return "⚠️ ابتدا API Key را در منوی سمت چپ وارد کنید."
    
    # آدرس استاندارد API برای جلوگیری از 404
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": f"Task: {prompt_task}. Existing Data: {st.session_state.data}"}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ خطای گوگل ({response.status_code}): {response.text}"
    except Exception as e:
        return f"❌ خطای اتصال: {str(e)}"

# --- سایدبار ---
with st.sidebar:
    st.title("🦷 Control Panel")
    st.session_state.api_key = st.text_input("Gemini API Key:", type="password")
    st.divider()
    st.write(f"📊 گام فعلی: {st.session_state.step} از ۱۲")
    
    # دکمه بازگشت (Back Button)
    if st.session_state.step > 1:
        if st.button("🔙 بازگشت به گام قبلی"):
            prev_step()
            
    if st.button("🗑 ریست کامل برنامه"):
        restart()

# --- بدنه اصلی ---
st.title("Dental SEO & CRO Architect")

if st.session_state.step == 1:
    st.header("Step 1: URL & Service")
    # استفاده از مقادیر قبلی برای قابلیت ویرایش (Edit)
    u = st.text_input("آدرس صفحه خدمات:", value=st.session_state.data.get('url', ''))
    s = st.text_input("نام خدمت:", value=st.session_state.data.get('service', ''))
    if st.button("ذخیره و مرحله بعد"):
        if u and s:
            st.session_state.data['url'], st.session_state.data['service'] = u, s
            next_step()

elif st.session_state.step == 2:
    st.header("Step 2: Technical Extraction")
    if st.button("استخراج خودکار"):
        try:
            res = requests.get(st.session_state.data['url'], headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            st.session_state.data['headings'] = [h.text.strip() for h in soup.find_all(['h1','h2','h3'])]
            st.success("انجام شد.")
        except: st.error("خطا در اسکرپ.")
    
    m = st.text_area("ویرایش دستی تیترها:", value="\n".join(st.session_state.data.get('headings', [])))
    if st.button("تایید و ادامه"):
        if m: st.session_state.data['headings'] = m.split('\n')
        next_step()

elif 3 <= st.session_state.step <= 12:
    tasks = {3: "Keyword Mapping", 4: "Competitor Analysis", 5: "Patient Fears", 6: "Quiz Design", 7: "CTA Strategy", 8: "Wayfinding", 9: "Copywriting", 10: "Visual Brief", 11: "Internal Links", 12: "Technical Assets"}
    st.header(f"Step {st.session_state.step}: {tasks[st.session_state.step]}")
    
    if st.button("اجرای تحلیل مرحله فعلی"):
        with st.spinner("در حال محاسبه..."):
            res = get_gemini_response(tasks[st.session_state.step])
            st.session_state.data[f'res_{st.session_state.step}'] = res

    if f'res_{st.session_state.step}' in st.session_state.data:
        st.markdown(f"<div class='report-box'>{st.session_state.data[f'res_{st.session_state.step}']}</div>", unsafe_allow_html=True)
        if st.button("YES - برو مرحله بعد"):
            if st.session_state.step == 12: st.balloons()
            else: next_step()
