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
    .report-box { padding: 20px; border-radius: 15px; border: 1px solid #e0e0e0; background-color: #ffffff; line-height: 1.8; color: #333; }
    </style>
    """, unsafe_allow_html=True)

# --- ۳. تابع ارتباط با Gemini ---
def get_gemini_response(prompt_task):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        context = f"You are a Senior Dental SEO Manager in Canada. Project Data: {st.session_state.data}. Task: {prompt_task}"
        response = model.generate_content(context)
        return response.text
    except Exception as e: 
        return f"❌ خطا در لایه هوش مصنوعی: {str(e)}"

# --- ۴. نوار پیشرفت بصری ---
steps_titles = ["Welcome", "Data Input", "Keyword & Semantic", "SERP & Authority", "Psychology & Trust", "Tools & Finance", "Content & Meta", "Wireframe & Assets"]
st.progress(st.session_state.step / (len(steps_titles) - 1))
st.write(f"📍 گام فعلی: **{steps_titles[st.session_state.step]}**")
st.divider()

# --- ۵. مدیریت گام‌ها ---

# گام ۰: معرفی ابزار
if st.session_state.step == 0:
    st.title("Dental SEO & CRO Architect Pro 🇨🇦")
    st.markdown("### پلتفرم استراتژی محتوا و معماری تبدیل برای کلینیک‌های دندانپزشکی")
    st.info("این ابزار با تحلیل عمیق SERP، رقبا و رفتارهای روانی بیمار، صفحه خدمات شما را بازنویسی می‌کند.")
    if st.button("شروع آنالیز استراتژیک"): next_step()

# گام ۱: دریافت ورودی‌های ۷گانه
elif st.session_state.step == 1:
    st.header("Step 1: Deep Data Acquisition")
    col1, col2 = st.columns(2)
    with col1:
        u = st.text_input("Target URL:", value=st.session_state.data.get('url',''), placeholder="https://example.com/service")
        s = st.text_input("Service Name:", value=st.session_state.data.get('service',''))
        l = st.text_input("Target City/Location:", value=st.session_state.data.get('location',''))
        c = st.multiselect("Conversion Goals (CTA):", 
                           ["Phone Call", "Booking Form", "WhatsApp Chat", "Free Consultation", "Live Chat"],
                           default=st.session_state.data.get('cta', ["Phone Call"]))
    
    with col2:
        mk = st.text_input("Main Keyword:", value=st.session_state.data.get('main_k',''))
        if st.button("Extract Keywords from URL", disabled=(not u or mk != "")):
            with st.spinner("Analyzing URL..."):
                res = get_gemini_response(f"Based on the URL {u}, what is the target primary and secondary keywords?")
                st.info(f"AI Suggestions: {res[:200]}...")
        
        sk = st.text_area("Secondary Keywords:", value=st.session_state.data.get('sec_k',''))
    
    st.divider()
    h_val = st.session_state.data.get('headings','')
    h_input = st.text_area("Existing Headings (تیترهای فعلی):", value=h_val, height=100)
    if st.button("Scrape Headings Automatically", disabled=(not u or h_input != "")):
        try:
            r = requests.get(u, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            scraped_h = "\n".join([f"{h.name.upper()}: {h.text.strip()}" for h in soup.find_all(['h1','h2','h3'])])
            st.session_state.data['headings'] = scraped_h
            st.rerun()
        except Exception as e: 
            st.error(f"Scraping failed: {e}")

    st.divider()
    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        st.button("🔙 Back", on_click=prev_step)
    with nav_col2:
        if st.button("Save & Next Step ➡️"):
            st.session_state.data.update({'url':u, 'service':s, 'location':l, 'cta':c, 'main_k':mk, 'sec_k':sk, 'headings':h_input})
            next_step()

# گام‌های هوشمند (۲ تا ۷)
elif 2 <= st.session_state.step <= 7:
    task_map = {
        2: "Keyword Mapping & Semantic Gap. Identify Primary, Secondary, Forbidden Keywords, and Topics (Entities) that competitors use but we lack.",
        3: "SERP Deep Dive: Analyze Top 3 Local Pack, Google Ads USPs in this area, and Top 5 Organic Results. Benchmark Brand Authority.",
        4: "Identify the top 3 psychological fears patients have for this service in this location. Design E-E-A-T responses.",
        5: "Suggest 2 Interactive Lead-gen tools (Quiz/Calculator) + A trust-based pricing and financing display plan.",
        6: "Rewrite Content: Provide 3 Meta sets, a Table of Heading Critiques (Old vs New), Body Intros, and a Specific CTA for EVERY section.",
        7: "Visual Wireframe Sitemap: Define the logical order of sections (Top to Bottom) and suggest 3 internal link topics (Silo Strategy)."
    }
    
    st.header(f"Step {st.session_state.step}: {steps_titles[st.session_state.step]}")
    if st.button(f"🚀 Generate {steps_titles[st.session_state.step]} Analysis"):
        with st.spinner("Gemini is thinking..."):
            res = get_gemini_response(task_map[st.session_state.step])
            st.session_state.data[f'res_{st.session_state.step}'] = res

    if f'res_{st.session_state.step}' in st.session_state.data:
        edited_val = st.text_area("Review & Edit Output:", value=st.session_state.data[f'res_{st.session_state.step}'], height=400)
        st.session_state.data[f'res_{st.session_state.step}'] = edited_val
        
        st.divider()
        nav_col1, nav_col2 = st.columns(2)
        with nav_col1:
            st.button("🔙 Back", on_click=prev_step, key=f"back_{st.session_state.step}")
        with nav_col2:
            st.button("Confirm & Next Step ➡️", on_click=next_step, key=f"next_{st.session_state.step}")
    else:
        st.button("🔙 Back", on_click=prev_step, key=f"back_no_res_{st.session_state.step}")

# گام ۸: خروجی نهایی و دانلود گزارش
elif st.session_state.step == 8:
    st.header("🏁 Final Strategy Portfolio")
    final_output = ""
    for i in range(2, 8):
        final_output += f"### {steps_titles[i]}\n\n{st.session_state.data.get(f'res_{i}', '')}\n\n---\n"
    
    st.markdown(final_output)
    
    if st.button("Generate Technical Schema (JSON-LD)"):
        with st.spinner("Coding..."):
            schema = get_gemini_response("Create a comprehensive MedicalProcedure JSON-LD Schema for this service.")
            st.code(schema, language="json")
    
    st.download_button("📥 Download Full Report", final_output, file_name="dental_seo_strategy.txt")
    if st.button("🗑 Restart Audit"):
        st.session_state.step = 0
        st.session_state.data = {}
        st.rerun()

# --- سایدبار ---
with st.sidebar:
    st.title("⚙️ Architect Control")
    st.success("API Key is Active ✅")
    st.markdown("---")
    st.markdown(f"**Progress:** {st.session_state.step}/8")
    if st.button("Quick Reset"): 
        st.session_state.step = 0
        st.session_state.data = {}
        st.rerun()
