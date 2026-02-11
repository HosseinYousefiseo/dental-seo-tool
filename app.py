import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# --- ۰. تنظیمات مستقیم API ---
# استفاده از ساده‌ترین روش پیکربندی برای جلوگیری از خطای نسخه
genai.configure(api_key="AIzaSyAp7s-XmkTvqPh1fnJlnQCu9D0M6QNdEuw")

# --- ۱. مدیریت نشست و گام‌ها ---
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

# --- ۲. ظاهر برنامه ---
st.markdown("""
    <style>
    .stProgress > div > div > div > div { background-color: #00cc99; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; background-color: #004a99; color: white; }
    .report-box { padding: 20px; border-radius: 15px; border: 1px solid #e0e0e0; background-color: #ffffff; line-height: 1.8; }
    </style>
    """, unsafe_allow_html=True)

# --- ۳. تابع فراخوانی هوش مصنوعی (نسخه فوق‌پایدار) ---
def get_gemini_response(prompt_task):
    try:
        # متد استاندارد برای فراخوانی مدل بدون آپشن‌های دردسرساز
        model = genai.GenerativeModel('gemini-1.5-flash')
        context = f"You are a Senior Dental SEO Manager in Canada. Data: {st.session_state.data}. Task: {prompt_task}"
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- ۴. نوار وضعیت ---
steps_titles = ["Welcome", "Data Input", "Keyword & Semantic", "SERP & Authority", "Psychology & Trust", "Tools & Finance", "Content & Meta", "Wireframe & Assets"]
st.progress(st.session_state.step / (len(steps_titles) - 1))
st.write(f"📍 Phase: **{steps_titles[st.session_state.step]}**")
st.divider()

# --- ۵. اجرای گام‌ها ---

# گام ۰: خوش‌آمدگویی
if st.session_state.step == 0:
    st.title("Dental SEO & CRO Architect Pro 🇨🇦")
    st.info("ابزار هوشمند تحلیل استراتژیک سئو دندانپزشکی. برای شروع روی دکمه زیر کلیک کنید.")
    if st.button("شروع آنالیز"): next_step()

# گام ۱: دریافت ورودی‌ها
elif st.session_state.step == 1:
    st.header("Step 1: Deep Data Input")
    col1, col2 = st.columns(2)
    with col1:
        u = st.text_input("URL:", value=st.session_state.data.get('url',''))
        s = st.text_input("Service:", value=st.session_state.data.get('service',''))
        l = st.text_input("Location:", value=st.session_state.data.get('location',''))
        c = st.multiselect("Conversion Goals (CTA):", ["Phone Call", "Booking Form", "WhatsApp", "Free Consultation"], default=st.session_state.data.get('cta', ["Phone Call"]))
    
    with col2:
        mk = st.text_input("Main Keyword:", value=st.session_state.data.get('main_k',''))
        sk = st.text_area("Secondary Keywords:", value=st.session_state.data.get('sec_k',''))
    
    h = st.text_area("Existing Headings (تیترهای فعلی):", value=st.session_state.data.get('headings',''), height=100)
    
    st.divider()
    nav1, nav2 = st.columns(2)
    if nav1.button("🔙 Back"): prev_step()
    if nav2.button("Confirm & Next ➡️"):
        st.session_state.data.update({'url':u, 'service':s, 'location':l, 'cta':c, 'main_k':mk, 'sec_k':sk, 'headings':h})
        next_step()

# گام‌های ۲ تا ۷ (تحلیلی)
elif 2 <= st.session_state.step <= 7:
    task_map = {
        2: "Analyze Keyword Mapping & Semantic Gaps (Primary, Secondary, Forbidden Keywords).",
        3: "Perform SERP Deep Dive: Local Pack, Ads USPs, and Organic Top 5 Analysis.",
        4: "Identify 3 Patient Fears and provide E-E-A-T trust responses.",
        5: "Suggest 2 Interactive Tools (Quiz/Calculator) and Financial Transparency layout.",
        6: "Rewrite Content: 3 Meta sets, Heading Critique Table, and Sectional CTA strategy.",
        7: "Visual Wireframe Sitemap (Top-to-Bottom order) and Internal Linking Strategy."
    }
    
    st.header(steps_titles[st.session_state.step])
    if st.button(f"🚀 Run AI Analysis for {steps_titles[st.session_state.step]}"):
        with st.spinner("AI is thinking..."):
            res = get_gemini_response(task_map[st.session_state.step])
            st.session_state.data[f'res_{st.session_state.step}'] = res
    
    if f'res_{st.session_state.step}' in st.session_state.data:
        edited = st.text_area("Edit Output:", value=st.session_state.data[f'res_{st.session_state.step}'], height=400)
        st.session_state.data[f'res_{st.session_state.step}'] = edited
        
        st.divider()
        nav1, nav2 = st.columns(2)
        if nav1.button("🔙 Back", key=f"b_{st.session_state.step}"): prev_step()
        if nav2.button("Confirm & Next ➡️", key=f"n_{st.session_state.step}"): next_step()
    else:
        if st.button("🔙 Back"): prev_step()

# گام نهایی
elif st.session_state.step == 8:
    st.header("🏁 Final Strategy Portfolio")
    final_rep = ""
    for i in range(2, 8):
        final_rep += f"### {steps_titles[i]}\n{st.session_state.data.get(f'res_{i}', '')}\n\n---\n"
    
    st.markdown(final_rep)
    
    if st.button("Generate JSON-LD Schema"):
        st.code(get_gemini_response("Create MedicalProcedure JSON-LD Schema."), language="json")
        
    st.download_button("📥 Download Report", final_rep, file_name="dental_strategy.txt")
    if st.button("🗑 Restart Audit"):
        st.session_state.step = 0
        st.session_state.data = {}
        st.rerun()

with st.sidebar:
    st.title("Admin Panel")
    st.success("API Key is Active")
    if st.button("Reset App"):
        st.session_state.step = 0
        st.session_state.data = {}
        st.rerun()
