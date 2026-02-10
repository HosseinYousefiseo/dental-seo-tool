import streamlit as st
import requests
from bs4 import BeautifulSoup
import json

# --- ۱. توابع مدیریت ناوبری (Navigation) ---
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

# --- ۲. تنظیمات صفحه و ظاهر ---
st.set_page_config(page_title="Dental SEO Architect", page_icon="🦷", layout="wide")

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'data' not in st.session_state:
    st.session_state.data = {}

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #004a99; color: white; font-weight: bold; border: none; }
    .report-box { padding: 20px; border-radius: 12px; border: 1px solid #d1d5db; background-color: #f8f9fa; color: #1f2937; line-height: 1.8; }
    </style>
    """, unsafe_allow_html=True)

# --- ۳. تابع اصلاح‌شده برای ارتباط با Gemini (رفع خطای 404) ---
def get_gemini_response(prompt_task):
    api_key = st.session_state.get('api_key')
    if not api_key:
        return "⚠️ ابتدا API Key را در سایدبار وارد کنید."
    
    # تغییر نسخه به v1 و اصلاح نام مدل برای پایداری (v1 نسبت به v1beta کمتر 404 می‌دهد)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": f"Context: Dental SEO Architect (Canada). Task: {prompt_task}. Data: {st.session_state.data}"}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        res_json = response.json()
        
        if response.status_code == 200:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            # اگر v1 هم 404 داد، تلاش مجدد با ساختار جایگزین
            error_msg = res_json.get('error', {}).get('message', 'Unknown Error')
            return f"❌ خطای گوگل ({response.status_code}): {error_msg}"
    except Exception as e:
        return f"❌ خطای اتصال: {str(e)}"

# --- ۴. سایدبار (مدیریت مراحل و دکمه بازگشت) ---
with st.sidebar:
    st.title("🦷 Control Panel")
    st.session_state.api_key = st.text_input("Gemini API Key:", type="password")
    st.divider()
    st.write(f"📊 گام فعلی: **{st.session_state.step}** از ۱۲")
    
    col_back, col_reset = st.columns(2)
    with col_back:
        if st.session_state.step > 1:
            if st.button("🔙 بازگشت"): prev_step()
    with col_reset:
        if st.button("🗑 ریست"): restart()

# --- ۵. بدنه اصلی مراحل ---
st.title("Dental SEO & CRO Architect")

if st.session_state.step == 1:
    st.header("Step 1: URL & Service Lock")
    # استفاده از مقادیر قبلی برای قابلیت Edit
    url = st.text_input("آدرس صفحه خدمات:", value=st.session_state.data.get('url', ''))
    service = st.text_input("نام خدمت (مثلاً Dental Implants):", value=st.session_state.data.get('service', ''))
    
    if st.button("ذخیره و مرحله بعد"):
        if url and service:
            st.session_state.data['url'], st.session_state.data['service'] = url, service
            next_step()

elif st.session_state.step == 2:
    st.header("Step 2: Technical Extraction")
    if st.button("استخراج تیترها"):
        try:
            res = requests.get(st.session_state.data['url'], headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            st.session_state.data['headings'] = [h.text.strip() for h in soup.find_all(['h1','h2','h3'])]
            st.success("تیترها استخراج شد.")
        except: st.error("خطا در استخراج خودکار.")
    
    m = st.text_area("ویرایش یا ورود دستی تیترها:", value="\n".join(st.session_state.data.get('headings', [])))
    if st.button("تایید و ادامه"):
        st.session_state.data['headings'] = [line for line in m.split('\n') if line.strip()]
        next_step()

elif 3 <= st.session_state.step <= 12:
    tasks = {
        3: "Keyword Mapping (Primary, Secondary, Forbidden)",
        4: "SERP & Competitor Analysis",
        5: "Patient Fears & Trust Signals",
        6: "Interactive Conversion Mechanism",
        7: "CTA Strategy",
        8: "Local Wayfinding (Canada Context)",
        9: "Final Page Copy",
        10: "Visual Brief",
        11: "Internal Linking Cluster",
        12: "Technical Assets (JSON-LD & HTML)"
    }
    st.header(f"Step {st.session_state.step}: {tasks[st.session_state.step]}")
    
    if st.button(f"اجرای آنالیز هوشمند مرحله {st.session_state.step}"):
        with st.spinner("Gemini در حال تحلیل است..."):
            res = get_gemini_response(tasks[st.session_state.step])
            st.session_state.data[f'res_{st.session_state.step}'] = res

    if f'res_{st.session_state.step}' in st.session_state.data:
        st.markdown(f"<div class='report-box'>{st.session_state.data[f'res_{st.session_state.step}']}</div>", unsafe_allow_html=True)
        if st.button("تایید و گام بعدی ➡️"):
            if st.session_state.step == 12: st.balloons()
            else: next_step()
