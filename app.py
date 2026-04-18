import streamlit as st
from ai import get_ai_response
from database import save_entry, get_entries, get_entry_count, get_mood_history
from datetime import datetime

st.set_page_config(
    page_title="Matcha Journal",
    page_icon="🍵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Matcha CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --matcha-dark:   #2d4a2d;
    --matcha-mid:    #4a7c59;
    --matcha-light:  #8ab89a;
    --matcha-pale:   #c8dfc8;
    --matcha-cream:  #f0f5ec;
    --matcha-foam:   #fafdf8;
    --brown:         #6b4f3a;
    --text-dark:     #1e2d1e;
    --text-mid:      #3d5a3d;
    --gold:          #c9a84c;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--matcha-cream);
    color: var(--text-dark);
}

/* Hide streamlit default elements */
#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { background: transparent !important; border-bottom: none !important; }
.stDeployButton { display: none; }

/* Main background */
.stApp {
    background: linear-gradient(135deg, #f0f5ec 0%, #e8f0e4 50%, #dce8d8 100%);
    min-height: 100vh;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--matcha-dark) 0%, #1e3a1e 100%) !important;
    border-right: 2px solid var(--matcha-mid);
}

[data-testid="stSidebar"] * {
    color: var(--matcha-cream) !important;
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--matcha-pale) !important;
    font-family: 'Playfair Display', serif !important;
}

/* Title area */
.journal-header {
    text-align: center;
    padding: 2rem 0 1rem 0;
    position: relative;
    z-index: 1;
}

.journal-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    color: var(--matcha-dark);
    font-style: italic;
    margin: 0;
    text-shadow: 1px 2px 8px rgba(45,74,45,0.08);
    letter-spacing: -0.5px;
}

.journal-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    color: var(--matcha-mid);
    font-weight: 300;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.3rem;
}

.matcha-divider {
    width: 80px;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--matcha-mid), transparent);
    margin: 1rem auto;
}

/* Stat cards */
.stat-row {
    display: flex;
    gap: 1rem;
    margin: 1rem 0;
    position: relative;
    z-index: 1;
}

.stat-card {
    background: var(--matcha-foam);
    border: 1px solid var(--matcha-pale);
    border-radius: 16px;
    padding: 1rem 1.5rem;
    flex: 1;
    text-align: center;
    box-shadow: 0 2px 12px rgba(45,74,45,0.06);
}

.stat-number {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: var(--matcha-dark);
    font-weight: 600;
    display: block;
}

.stat-label {
    font-size: 0.75rem;
    color: var(--matcha-mid);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 500;
}

/* Mood selector */
.mood-bar {
    background: var(--matcha-foam);
    border: 1px solid var(--matcha-pale);
    border-radius: 16px;
    padding: 1rem 1.5rem;
    margin: 1rem 0;
    position: relative;
    z-index: 1;
    box-shadow: 0 2px 12px rgba(45,74,45,0.06);
}

/* Chat area */
.stChatMessage {
    background: var(--matcha-foam) !important;
    border: 1px solid var(--matcha-pale) !important;
    border-radius: 16px !important;
    margin: 0.5rem 0 !important;
    position: relative;
    z-index: 1;
}

[data-testid="stChatMessageContent"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.97rem !important;
    line-height: 1.7 !important;
    color: var(--text-dark) !important;
}

/* Chat input */
[data-testid="stChatInput"] {
    background: var(--matcha-foam) !important;
    border: 2px solid var(--matcha-pale) !important;
    border-radius: 16px !important;
    position: relative;
    z-index: 1;
}

[data-testid="stChatInput"]:focus-within {
    border-color: var(--matcha-mid) !important;
    box-shadow: 0 0 0 3px rgba(74,124,89,0.15) !important;
}

/* Buttons */
.stButton > button {
    background: var(--matcha-dark) !important;
    color: var(--matcha-cream) !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s ease !important;
    padding: 0.5rem 1.5rem !important;
}

.stButton > button:hover {
    background: var(--matcha-mid) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(45,74,45,0.25) !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: var(--matcha-foam) !important;
    border: 1px solid var(--matcha-pale) !important;
    border-radius: 12px !important;
    color: var(--text-dark) !important;
}

/* Text input */
.stTextInput > div > div > input {
    background: var(--matcha-foam) !important;
    border: 1px solid var(--matcha-pale) !important;
    border-radius: 12px !important;
    color: var(--text-dark) !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--matcha-mid) !important;
    box-shadow: 0 0 0 3px rgba(74,124,89,0.15) !important;
}

/* Sidebar entry cards */
.entry-card {
    background: rgba(200, 223, 200, 0.15);
    border: 1px solid rgba(200, 223, 200, 0.3);
    border-radius: 12px;
    padding: 0.75rem 1rem;
    margin: 0.5rem 0;
}

.entry-date {
    font-family: 'Playfair Display', serif;
    font-size: 0.85rem;
    color: var(--matcha-pale) !important;
    font-style: italic;
}

.entry-preview {
    font-size: 0.8rem;
    color: rgba(200,223,200,0.7) !important;
    margin-top: 0.2rem;
    line-height: 1.4;
}

/* Mood badge */
.mood-badge {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* Progress bar override */
.stProgress > div > div {
    background: var(--matcha-mid) !important;
    border-radius: 4px !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--matcha-cream); }
::-webkit-scrollbar-thumb { background: var(--matcha-pale); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--matcha-light); }

/* Floating leaves */
.leaf {
    position: fixed;
    font-size: 1.2rem;
    opacity: 0.15;
    animation: float-leaf linear infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes float-leaf {
    0%   { transform: translateY(-20px) rotate(0deg); opacity: 0; }
    10%  { opacity: 0.15; }
    90%  { opacity: 0.15; }
    100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
}
</style>

<!-- Floating leaves -->
<div class="leaf" style="left:10%; animation-duration:12s; animation-delay:0s; top:-20px;">🍃</div>
<div class="leaf" style="left:30%; animation-duration:16s; animation-delay:4s; top:-20px;">🌿</div>
<div class="leaf" style="left:60%; animation-duration:14s; animation-delay:8s; top:-20px;">🍃</div>
<div class="leaf" style="left:80%; animation-duration:18s; animation-delay:2s; top:-20px;">🌿</div>
<div class="leaf" style="left:50%; animation-duration:20s; animation-delay:10s; top:-20px;">🍃</div>
""", unsafe_allow_html=True)

# ── Mood config ──────────────────────────────────────────────────────────────
MOOD_CONFIG = {
    "happy":    {"emoji": "😊", "color": "#4a7c59"},
    "grateful": {"emoji": "🙏", "color": "#6b9e7a"},
    "okay":     {"emoji": "😌", "color": "#8ab89a"},
    "anxious":  {"emoji": "😰", "color": "#c9a84c"},
    "stressed": {"emoji": "😤", "color": "#b87333"},
    "sad":      {"emoji": "😢", "color": "#7a8fa6"},
}

# ── Session state ────────────────────────────────────────────────────────────
for key, val in [
    ("logged_in", False),
    ("username", ""),
    ("chat_history", []),
    ("show_analytics", False),
]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="journal-header">
    <h1 class="journal-title">Matcha Journal</h1>
    <p class="journal-subtitle">your private space to think out loud</p>
    <div class="matcha-divider"></div>
</div>
""", unsafe_allow_html=True)

# ── Login ─────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("### 🍵 Welcome back")
        st.markdown("*Enter your name to begin your journaling session*")
        st.markdown("")
        username = st.text_input("Your name", placeholder="e.g. Yusra", label_visibility="collapsed")
        if st.button("Begin Journaling", use_container_width=True):
            if username.strip():
                st.session_state.logged_in = True
                st.session_state.username = username.strip()
                st.rerun()
            else:
                st.error("Please enter your name to continue.")
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### 🍵 {st.session_state.username}'s Journal")
    st.markdown("---")

    # Stats
    count = get_entry_count(st.session_state.username)
    st.markdown(f"""
    <div style="text-align:center; padding: 1rem 0;">
        <span style="font-family:'Playfair Display',serif; font-size:2.5rem; color:#c8dfc8;">{count}</span><br>
        <span style="font-size:0.7rem; letter-spacing:2px; text-transform:uppercase; color:#8ab89a;">entries written</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Analytics toggle
    if st.button("Mood Analytics", use_container_width=True):
        st.session_state.show_analytics = not st.session_state.show_analytics

    # Clear chat
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    # Logout
    if st.button("Log Out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")
    st.markdown("**Past Entries**")

    entries = get_entries(st.session_state.username)
    if entries:
        for entry in entries:
            mood = entry.get("mood", "okay")
            emoji = MOOD_CONFIG.get(mood, {}).get("emoji", "")
            ts = entry.get("timestamp")
            date_str = ts.strftime("%b %d") if ts else ""
            preview = entry.get("message", "")[:55]
            st.markdown(f"""
            <div class="entry-card">
                <div class="entry-date">{date_str} &nbsp; {emoji} {mood}</div>
                <div class="entry-preview">{preview}...</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("*No entries yet. Start writing!*")

# ── Main area ─────────────────────────────────────────────────────────────────
col_main, col_side = st.columns([2, 1])

with col_main:
    # Mood + stats row
    mood_options = list(MOOD_CONFIG.keys())
    mood = st.selectbox(
        "How are you feeling today?",
        mood_options,
        format_func=lambda m: f"{MOOD_CONFIG[m]['emoji']}  {m.capitalize()}"
    )

    # Entry counter stat
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card">
            <span class="stat-number">{count}</span>
            <span class="stat-label">Total Entries</span>
        </div>
        <div class="stat-card">
            <span class="stat-number">{MOOD_CONFIG[mood]['emoji']}</span>
            <span class="stat-label">Today's Mood</span>
        </div>
        <div class="stat-card">
            <span class="stat-number">{len(st.session_state.chat_history) // 2}</span>
            <span class="stat-label">This Session</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Input
    user_input = st.chat_input(f"What's on your mind, {st.session_state.username}?")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.spinner(""):
            response = get_ai_response(user_input, mood)

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

        save_entry(st.session_state.username, user_input, response, mood)
        st.rerun()

with col_side:
    # Mood analytics panel
    if st.session_state.show_analytics:
        st.markdown("### Mood History")
        mood_history = get_mood_history(st.session_state.username)

        if mood_history:
            mood_counts = {}
            for m in mood_history:
                mood_counts[m] = mood_counts.get(m, 0) + 1

            total = sum(mood_counts.values())
            for m, c in sorted(mood_counts.items(), key=lambda x: -x[1]):
                emoji = MOOD_CONFIG.get(m, {}).get("emoji", "")
                pct = int((c / total) * 100)
                st.markdown(f"{emoji} **{m.capitalize()}** — {c}x")
                st.progress(pct / 100)
        else:
            st.markdown("*Write a few entries to see your mood patterns.*")

    else:
        # Matcha tips
        st.markdown("### 🌿 Today's Prompt")
        import random
        prompts = [
            "What made you smile today, even briefly?",
            "What is one thing you are grateful for right now?",
            "What has been weighing on your mind lately?",
            "Describe how your body feels at this moment.",
            "What would you tell your past self from one year ago?",
            "What is something you are looking forward to?",
            "What is one thing you want to let go of today?",
            "How did you show up for yourself today?",
        ]
        st.markdown(f"""
        <div style="background:var(--matcha-foam); border:1px solid var(--matcha-pale);
             border-radius:16px; padding:1.5rem; font-family:'Playfair Display',serif;
             font-style:italic; color:var(--matcha-dark); font-size:1.05rem; line-height:1.6;">
            "{random.choice(prompts)}"
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        st.markdown("### 🍵 Matcha Moment")
        st.markdown("""
        <div style="background:var(--matcha-foam); border:1px solid var(--matcha-pale);
             border-radius:16px; padding:1rem 1.5rem; font-size:0.88rem;
             color:var(--matcha-mid); line-height:1.7;">
            Take a breath. You showed up today. That matters more than you know.
            Your thoughts deserve a home, and this is it.
        </div>
        """, unsafe_allow_html=True)