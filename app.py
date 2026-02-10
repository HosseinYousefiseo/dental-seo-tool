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

# --- استایل دهی اختصاصی ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #004a99; color: white; font-weight: bold; }
    .report-box { padding: 20px; border-radius: 12px; border: 1px solid #d1d5db; background-color: white; color: #1f2937; line-height: 1.8; }
    </style>
    """, unsafe_allow_html=True)

# --- تابع هوشمند ارتباط با Gemini (اصلاح آدرس برای رفع 404) ---
def get_gemini_response(prompt_task):
    api_key = st.session_state.get('api_key')
    if not api_key:
        return "⚠️ ابتدا API Key را وارد کنید."
    
    # آدرس دقیق و اصلاح شده API گوگل
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": f"System: Dental SEO/CRO Architect Canada. Task: {prompt_task}. Data: {st.session_state.data}"}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        elif response.status_code == 404:
            return "❌ خطای 404: مدل پیدا نشد. احتمالاً آدرس API یا نام مدل اشتباه است."
        else:
            return f"❌ خطای گوگل ({response.status_code}): {response.text}"
    except Exception as e:
        return f"❌ خطای اتصال: {str(e)}"

# --- سایدبار کنترلی ---
with st.sidebar:
    st.title("🦷 Control Panel")
    st.session_state.api_key = st.text_input("Gemini API Key:", type="password")
    st.divider()
    st.write(f"📊 گام **{st.session_state.step}** از ۱۲")
    
    # دکمه بازگشت (Back)
    if st.session_state.step > 1:
        if st.button("🔙 بازگشت به گام قبلی"):
            prev_step()
            
    if st.button("🗑 ریست کامل"):
        restart()

# --- بدنه اصلی برنامه ---
st.title("Dental SEO & CRO Architect")

if st.session_state.step == 1:
    st.header("Step 1: URL & Service")
    u = st.text_input("آدرس صفحه خدمات:", value=st.session_state.data.get('url', ''))
    s = st.text_input("نام خدمت (مثلا Dental Implants):", value=st.session_state.data.get('service', ''))
    if st.button("ذخیره و مرحله بعد"):
        if u and s:
            st.session_state.data['url'], st.session_state.data['service'] = u, s
            next_step()

elif st.session_state.step == 2:
    st.header("Step 2: Technical Extraction")
    if st.button("استخراج تیترها (Scrape)"):
        try:
            res = requests.get(st.session_state.data['url'], headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            st.session_state.data['headings'] = [h.text.strip() for h in soup.find_all(['h1','h2','h3'])]
            st.success("تیترها استخراج شد.")
        except:
            st.error("خطا در استخراج. دستی وارد کنید.")
    
    m = st.text_area("ورود دستی تیترها:", value="\n".join(st.session_state.data.get('headings', [])))
    if st.button("تایید و ادامه"):
        if m: st.session_state.data['headings'] = m.split('\n')
        next_step()

elif 3 <= st.session_state.step <= 12:
    tasks = {
        3: "Keyword Mapping & Search Intent", 4: "SERP & Competitor Breakdown",
        5: "Patient Fears & E-E-A-T", 6: "Interactive Mechanism",
        7: "CTA Strategy", 8: "Local Wayfinding (Canada)",
        9: "Final Conversion Copy", 10: "Visual Brief",
        11: "Internal Linking", 12: "Technical Assets (JSON-LD/HTML)"
    }
    st.header(f"Step {st.session_state.step}: {tasks[st.session_state.step]}")
    
    if st.button(f"اجرای آنالیز گام {st.session_state.step}"):
        with st.spinner("در حال تحلیل..."):
            res = get_gemini_response(tasks[st.session_state.step])
            st.session_state.data[f'res_{st.session_state.step}'] = res

    if f'res_{st.session_state.step}' in st.session_state.data:
        st.markdown(f"<div class='report-box'>{st.session_state.data[f'res_{st.session_state.step}']}</div>", unsafe_allow_html=True)
        if st.button("تایید و گام بعدی"):
            if st.session_state.step == 12: st.balloons()
            else: next_step()