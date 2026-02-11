import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# --- تنظیمات پایداری وضعیت ---
if 'step' not in st.session_state: st.session_state.step = 0
if 'data' not in st.session_state: st.session_state.data = {}

def next_step(): st.session_state.step += 1; st.rerun()
def prev_step(): st.session_state.step -= 1; st.rerun()

# --- تنظیمات صفحه ---
st.set_page_config(page_title="Dental SEO Architect Pro", page_icon="🦷", layout="wide")

# --- تابع ارتباط با Gemini (اصلاح شده برای رفع 404) ---
def get_gemini_response(prompt_task):
    api_key = st.session_state.get('api_key')
    if not api_key: return "⚠️ کلید API را وارد کنید."
    try:
        genai.configure(api_key=api_key)
        # استفاده از مدل به صورت مستقیم بدون پیشوند نسخه برای پایداری بیشتر
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        context = f"Role: Dental SEO Expert Canada. Data: {st.session_state.data}. Task: {prompt_task}"
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"❌ خطای هوش مصنوعی: {str(e)}"

# --- نوار پیشرفت ---
steps_titles = ["شروع", "ورود دیتای پایه", "کلمات و Semantic", "تحلیل SERP", "اعتماد و ترس‌ها", "ابزارها و مالی", "محتوا و CTA", "وایرفریم و اسکیما"]
st.progress(st.session_state.step / (len(steps_titles) - 1))
st.write(f"📍 گام فعلی: **{steps_titles[st.session_state.step]}**")
st.divider()

# --- پیاده‌سازی مراحل ---

if st.session_state.step == 0:
    st.title("Dental SEO & CRO Architect Pro 🇨🇦")
    st.info("خوش آمدید. این ابزار استراتژی کامل سئو و تبدیل صفحه خدمات شما را طراحی می‌کند.")
    if st.button("شروع آنالیز"): next_step()

elif st.session_state.step == 1:
    st.header("گام ۱: دریافت ورودی‌های جامع")
    col1, col2 = st.columns(2)
    with col1:
        u = st.text_input("URL:", value=st.session_state.data.get('url',''))
        s = st.text_input("Service:", value=st.session_state.data.get('service',''))
        l = st.text_input("Location:", value=st.session_state.data.get('location',''))
        c = st.selectbox("Main CTA:", ["Phone Call", "Form", "WhatsApp"], index=0)
    with col2:
        mk = st.text_input("Main Keyword (اگر ندارید خالی بگذارید):", value=st.session_state.data.get('main_k',''))
        if st.button("Extract Keywords from URL", disabled=(mk != "")):
            res = get_gemini_response(f"Extract primary and secondary keywords from {u}")
            st.info(f"AI Suggestions: {res[:150]}...")
        sk = st.text_area("Secondary Keywords:", value=st.session_state.data.get('sec_k',''))
    
    h_input = st.text_area("Existing Headings (اگر ندارید خالی بگذارید):", value=st.session_state.data.get('headings',''))
    if st.button("Scrape Headings Automatically", disabled=(h_input != "")):
        try:
            r = requests.get(u, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            st.session_state.data['headings'] = "\n".join([h.text.strip() for h in soup.find_all(['h1','h2','h3'])])
            st.rerun()
        except: st.error("Scraping failed.")

    c1, c2 = st.columns(2)
    with c1: st.button("🔙 بازگشت", on_click=prev_step)
    with c2: 
        if st.button("تایید و مرحله بعد ➡️"):
            st.session_state.data.update({'url':u, 'service':s, 'location':l, 'cta':c, 'main_k':mk, 'sec_k':sk, 'headings':h_input})
            next_step()

elif 2 <= st.session_state.step <= 7:
    task_map = {
        2: "Keyword Mapping, Semantic Gaps, and Forbidden Keywords list.",
        3: "SERP Analysis (Local Pack, Google Ads, Organic Top 5) and Authority Benchmarking.",
        4: "Psychological fears for this service and E-E-A-T trust signals.",
        5: "Interactive Lead-gen tools (Quiz/Calculator) and Financial Transparency layout.",
        6: "3 Meta sets, Heading Rewrite Table, Content Intros, and CTA for EVERY section.",
        7: "Visual Sitemap/Wireframe (Top-to-bottom order) and JSON-LD Medical Schema."
    }
    st.header(steps_titles[st.session_state.step])
    if st.button(f"اجرای تحلیل {steps_titles[st.session_state.step]}"):
        with st.spinner("هوش مصنوعی در حال پردازش..."):
            res = get_gemini_response(task_map[st.session_state.step])
            st.session_state.data[f'res_{st.session_state.step}'] = res
    
    if f'res_{st.session_state.step}' in st.session_state.data:
        edited = st.text_area("ویرایش و تایید خروجی:", value=st.session_state.data[f'res_{st.session_state.step}'], height=400)
        st.session_state.data[f'res_{st.session_state.step}'] = edited
        col_b, col_n = st.columns(2)
        with col_b: st.button("🔙 بازگشت", on_click=prev_step)
        with col_n: st.button("تایید و مرحله بعد ➡️", on_click=next_step)
    else:
        st.button("🔙 بازگشت", on_click=prev_step)

# سایدبار
with st.sidebar:
    st.title("Settings")
    st.session_state.api_key = st.text_input("Gemini API Key:", type="password")
    if st.button("🗑 ریست کامل"):
        st.session_state.step = 0
        st.session_state.data = {}
        st.rerun()
