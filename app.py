import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# --- ۱. تنظیمات اولیه و مدیریت نشست ---
if 'step' not in st.session_state: st.session_state.step = 0
if 'data' not in st.session_state: st.session_state.data = {}

def next_step(): st.session_state.step += 1; st.rerun()
def prev_step(): st.session_state.step -= 1; st.rerun()

st.set_page_config(page_title="Dental SEO Architect Pro", page_icon="🦷", layout="wide")

# --- ۲. استایل دهی اختصاصی ---
st.markdown("""
    <style>
    .stProgress > div > div > div > div { background-color: #00cc99; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { background-color: #1E3A8A; color: white; }
    .report-box { padding: 20px; border-radius: 15px; border: 1px solid #e0e0e0; background-color: #ffffff; line-height: 1.8; color: #333; }
    .sidebar-info { font-size: 12px; color: #666; }
    </style>
    """, unsafe_allow_html=True)

# --- ۳. تابع ارتباط با Gemini ---
def get_gemini_response(prompt_task):
    api_key = st.session_state.get('api_key')
    if not api_key: return "⚠️ کلید API در سایدبار وارد نشده است!"
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        context = f"You are a Dental SEO Manager in Canada. Data: {st.session_state.data}. Task: {prompt_task}"
        response = model.generate_content(context)
        return response.text
    except Exception as e: return f"❌ خطا در ارتباط با هوش مصنوعی: {str(e)}"

# --- ۴. نوار پیشرفت بصری ---
steps_titles = ["Welcome", "Data Input", "Keyword & Semantic", "SERP & Authority", "Psychology & Trust", "Tools & Finance", "Content & Meta", "Wireframe & Assets"]
st.progress(st.session_state.step / (len(steps_titles) - 1))
cols = st.columns(len(steps_titles))
for i, title in enumerate(steps_titles):
    if i == st.session_state.step: cols[i].markdown(f"**{title}**")
    else: cols[i].caption(title)
st.divider()

# --- ۵. مدیریت گام‌ها ---

# گام ۰: معرفی
if st.session_state.step == 0:
    st.title("Dental SEO & CRO Architect Pro 🇨🇦")
    st.markdown("### پلتفرم استراتژی محتوا و معماری تبدیل برای کلینیک‌های دندانپزشکی")
    st.info("این ابزار فرآیند تحلیل رقیب، استخراج کلمات کلیدی، رفع شکاف‌های موضوعی و طراحی وایرفریم را به صورت یکپارچه انجام می‌دهد.")
    if st.button("شروع آنالیز استراتژیک"): next_step()

# گام ۱: ورودی‌های جامع
elif st.session_state.step == 1:
    st.header("Step 1: Deep Data Acquisition")
    col1, col2 = st.columns(2)
    with col1:
        u = st.text_input("Target URL:", value=st.session_state.data.get('url',''), placeholder="https://example.com/service")
        s = st.text_input("Service Name:", value=st.session_state.data.get('service',''))
        l = st.text_input("Target City/Location:", value=st.session_state.data.get('location',''))
        c = st.selectbox("Conversion Goal (CTA):", ["Phone Call", "Booking Form", "WhatsApp Chat", "Free Consultation"], index=0)
    
    with col2:
        mk = st.text_input("Main Keyword:", value=st.session_state.data.get('main_k',''))
        if st.button("Extract Keywords from URL", disabled=(mk != ""), help="اگر کلمه کلیدی ندارید، بگذارید هوش مصنوعی استخراج کند"):
            with st.spinner("Analyzing..."):
                res = get_gemini_response(f"Extract the primary and secondary keywords from {u}")
                st.info(f"AI Suggested: {res[:150]}...")
        
        sk = st.text_area("Secondary Keywords:", value=st.session_state.data.get('sec_k',''))
        
    st.divider()
    h_val = st.session_state.data.get('headings','')
    h_input = st.text_area("Current Page Headings:", value=h_val, height=100)
    if st.button("Scrape Headings Automatically", disabled=(h_input != "")):
        try:
            r = requests.get(u, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            st.session_state.data['headings'] = "\n".join([f"{h.name.upper()}: {h.text.strip()}" for h in soup.find_all(['h1','h2','h3'])])
            st.rerun()
        except: st.error("Scraping failed. Please paste manually.")

    c1, c2 = st.columns(2)
    with c1: st.button("🔙 Back", on_click=prev_step)
    with c2: 
        if st.button("Save & Analyze Context ➡️"):
            st.session_state.data.update({'url':u, 'service':s, 'location':l, 'cta':c, 'main_k':mk, 'sec_k':sk, 'headings':h_input})
            next_step()

# گام‌های هوشمند (۲ تا ۷)
elif 2 <= st.session_state.step <= 7:
    task_map = {
        2: "Keyword Mapping & Semantic Gap. Identify Primary, Secondary, Forbidden Keywords, and Entities/Topics that competitors use but we lack (Topical Authority).",
        3: "SERP & Authority Benchmarking. Analyze Top 3 Local Pack, Google Ads USPs, and Top 5 Organic Results. Estimate the brand authority needed to rank #1.",
        4: "Patient Psychology & Trust (E-E-A-T). Identify 3 main fears in this location and provide strategic trust-building responses.",
        5: "Interactive Tools & Financial Strategy. Suggest 2 Lead-gen tools (Quiz/Calculator) with details + A trust-based pricing and financing display plan.",
        6: "Copywriting & Sectional CTA. Provide 3 Meta sets, Rewrite headings (Table: Old|Weakness|New), suggest body intro for each, and a Specific CTA for EVERY section.",
        7: "Visual Wireframe & Internal Linking. Define the Top-to-Bottom section order (Psychological Flow) + Suggest 3 Blog topics for internal linking (Silo Strategy)."
    }
    
    st.header(f"Step {st.session_state.step}: {steps_titles[st.session_state.step]}")
    if st.button(f"🚀 Generate {steps_titles[st.session_state.step]} Analysis"):
        with st.spinner("AI Architect is processing..."):
            res = get_gemini_response(task_map[st.session_state.step])
            st.session_state.data[f'res_{st.session_state.step}'] = res

    if f'res_{st.session_state.step}' in st.session_state.data:
        edited_val = st.text_area("Review & Edit Output:", value=st.session_state.data[f'res_{st.session_state.step}'], height=400)
        st.session_state.data[f'res_{st.session_state.step}'] = edited_val
        
        c1, c2 = st.columns(2)
        with c1: st.button("🔙 Back", on_click=prev_step)
        with c2: st.button("Confirm & Next Step ➡️", on_click=next_step)
    else:
        st.button("🔙 Back", on_click=prev_step)

# گام نهایی
elif st.session_state.step == 8:
    st.header("🏁 Final Strategy & Assets")
    final_output = ""
    for i in range(2, 8):
        final_output += f"## {steps_titles[i]}\n\n{st.session_state.data.get(f'res_{i}', '')}\n\n---\n"
    
    st.markdown(final_output)
    
    # تولید اسکیما
    if st.button("Generate Technical Schema (JSON-LD)"):
        with st.spinner("Coding..."):
            schema = get_gemini_response("Generate a MedicalProcedure JSON-LD Schema for this service.")
            st.code(schema, language="json")
    
    st.download_button("📥 Download Full Report", final_output, file_name="dental_seo_strategy.txt")
    if st.button("🗑 Restart Audit"):
        st.session_state.step = 0
        st.session_state.data = {}
        st.rerun()

# --- سایدبار ---
with st.sidebar:
    st.title("⚙️ Architect Control")
    st.session_state.api_key = st.text_input("Gemini API Key:", type="password")
    st.markdown("---")
    st.markdown(f"**Progress:** {st.session_state.step}/8")
    if st.button("Quick Reset"): 
        st.session_state.step = 0
        st.rerun()
