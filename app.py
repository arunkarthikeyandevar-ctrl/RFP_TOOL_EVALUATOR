"""
app.py
Streamlit Frontend for the Bugatti Hypercar Seatbelt RFP Evaluator (RAG + Gemini 2.5 Flash).
Features:
- Enterprise Login Gateway with Username & Password Authentication
- Contender Comparison Charts with Winner in Green (#1), 2nd in Blue (#2), and 3rd in Amber (#3)
- Ephemeral Bring-Your-Own-Key (BYOK) Session Vault (auto-forgotten when session ends)
- Granular Veteran Score Justifications (Points Earned vs. Points Deducted)
- Interactive Color-Coded Highlighting of Scored Evidence Inside Full Vendor Proposals
- Built-in Salient Features & Step-by-Step User Guide
"""

import html
import os
import re
import zipfile
from io import BytesIO
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from bugatti_rfp_knowledge import BUGATTI_RFP_MASTER_DOCUMENT, EVALUATION_PILLARS
from generate_vendor_files import VENDOR_PROPOSALS_DATA, generate_all_vendor_files, create_pdf_bytes
from rag_engine import HybridRAGEngine, extract_text_from_uploaded_file
from evaluator_engine import evaluate_vendor_with_gemini_rag, generate_chief_engineer_executive_report

st.set_page_config(
    page_title="Bugatti Molsheim | Automated Seatbelt RFP Evaluator",
    page_icon="🏎️",
    layout="wide"
)

# ─────────────────────────────────────────────────────────────
#  AUTHORIZED ENTERPRISE CREDENTIALS
# ─────────────────────────────────────────────────────────────
VALID_CREDENTIALS = {
    "bugatti_admin": "Molsheim2026!",
    "chief_engineer": "TourbillonV16",
    "procurement": "BugattiRestraint2026",
    "admin": "admin123"
}

# --- COLOR PALETTE FOR HIGHLIGHTING EACH SCORING PILLAR IN THE PROPOSAL ---
PILLAR_HIGHLIGHT_STYLES = {
    "crash_homologation": {
        "bg": "#FFE4E6", "border": "#E11D48", "text": "#881337",
        "badge": "Pillar 1: Crash & Homologation (25%)"
    },
    "lightweighting_materials": {
        "bg": "#E0F2FE", "border": "#0284C7", "text": "#0C4A6E",
        "badge": "Pillar 2: Lightweighting & Materials (20%)"
    },
    "luxury_acoustics_nvh": {
        "bg": "#F3E8FF", "border": "#9333EA", "text": "#581C87",
        "badge": "Pillar 3: Luxury & Acoustics/NVH (20%)"
    },
    "quality_traceability": {
        "bg": "#DCFCE7", "border": "#16A34A", "text": "#14532D",
        "badge": "Pillar 4: Zero-Defect Quality (15%)"
    },
    "commercial_economics": {
        "bg": "#FEF3C7", "border": "#D97706", "text": "#78350F",
        "badge": "Pillar 5: Commercials & NRE (10%)"
    },
    "supply_chain_logistics": {
        "bg": "#CCFBF1", "border": "#0D9488", "text": "#134E4A",
        "badge": "Pillar 6: Molsheim Supply Chain (10%)"
    },
}


def render_highlighted_vendor_proposal(raw_text: str, pillar_scores: dict, filter_pillar_id: str = "ALL") -> str:
    """
    Finds the exact verbatim quotes cited by the 6 veteran pillars inside the vendor's
    proposal text and wraps them in color-coded HTML highlight spans with inline pillar tags.
    """
    safe_text = html.escape(raw_text)

    for pillar in EVALUATION_PILLARS:
        pid = pillar["id"]
        if filter_pillar_id != "ALL" and filter_pillar_id != pid:
            continue

        p_data = pillar_scores.get(pid, {})
        style = PILLAR_HIGHLIGHT_STYLES[pid]
        score_val = p_data.get("score_out_of_100", "?")
        quotes = p_data.get("verbatim_proposal_quotes", [])

        for quote in quotes:
            clean_q = quote.strip().strip('"').strip("'")
            if len(clean_q) < 12:
                continue
            escaped_q = html.escape(clean_q)
            tokens = [re.escape(tok) for tok in escaped_q.split() if tok]
            if not tokens:
                continue
            pattern_str = r"\s+".join(tokens)

            replacement_html = (
                f'<span style="background-color:{style["bg"]}; color:{style["text"]}; '
                f'border-left: 4px solid {style["border"]}; padding: 2px 6px; border-radius: 4px; '
                f'font-weight: 600; display: inline;">'
                f'\\g<0> '
                f'<span style="background-color:{style["border"]}; color:#FFFFFF; font-size:0.75em; '
                f'padding:1px 5px; border-radius:3px; margin-left:4px; vertical-align:middle;">'
                f'{style["badge"]} • {score_val}/100</span></span>'
            )

            try:
                safe_text, count = re.subn(pattern_str, replacement_html, safe_text, count=1, flags=re.IGNORECASE)
            except re.error:
                pass

    formatted_body = safe_text.replace("\n", "<br>")
    return (
        '<div style="font-family: \'Courier New\', monospace; font-size: 0.93rem; line-height: 1.75; '
        'background-color: #FFFFFF; color: #1E293B; padding: 22px; border-radius: 10px; '
        'border: 1px solid #CBD5E1; box-shadow: 0 1px 3px rgba(0,0,0,0.06); overflow-x: auto;">'
        f'{formatted_body}</div>'
    )


# --- SESSION STATE INITIALIZATION ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "current_user" not in st.session_state:
    st.session_state["current_user"] = ""
if "user_ephemeral_api_key" not in st.session_state:
    st.session_state["user_ephemeral_api_key"] = ""
if "evaluated_vendors" not in st.session_state:
    st.session_state["evaluated_vendors"] = {}
if "executive_report" not in st.session_state:
    st.session_state["executive_report"] = ""


def wipe_session_and_forget_key():
    """Immediately erases the API key and all session data from server memory."""
    st.session_state["user_ephemeral_api_key"] = ""
    st.session_state["evaluated_vendors"] = {}
    st.session_state["executive_report"] = ""


# ─────────────────────────────────────────────────────────────
#  LOGIN GATEWAY (AUTHENTICATION BARRIER)
# ─────────────────────────────────────────────────────────────
def render_login_page():
    st.markdown("""
    <style>
    .login-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 2rem;
    }
    .login-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08), 0 8px 10px -6px rgba(15, 23, 42, 0.04);
        max-width: 500px;
        width: 100%;
        text-align: center;
    }
    .login-brand-chip {
        background: #1e1b4b;
        color: #ffffff;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        padding: 4px 12px;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 0.75rem;
        text-transform: uppercase;
    }
    .login-title {
        color: #0f172a;
        font-size: 1.5rem;
        font-weight: 800;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.02em;
    }
    .login-subtitle {
        color: #64748b;
        font-size: 0.88rem;
        margin-bottom: 1.8rem;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

    c_left, c_center, c_right = st.columns([1, 1.6, 1])
    with c_center:
        st.markdown("""
        <div class="login-wrapper">
            <div class="login-card">
                <span class="login-brand-chip">BUGATTI AUTOMOBILES S.A.S.</span>
                <h2 class="login-title">🏎️ Molsheim Restraint RFP Gateway</h2>
                <p class="login-subtitle">
                    Level-4 Classified Technical Evaluation Portal for Tourbillon & Bolide Occupant Restraint Systems.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("portal_login_form", clear_on_submit=False):
            st.markdown("### 🔐 Personnel Authentication")
            u_input = st.text_input("Username", placeholder="e.g. bugatti_admin", key="inp_user")
            p_input = st.text_input("Password", type="password", placeholder="Enter your security credentials", key="inp_pass")
            submit_login = st.form_submit_button("🔓 Sign In to Evaluation Gateway", use_container_width=True, type="primary")

            if submit_login:
                u_clean = u_input.strip()
                p_clean = p_input.strip()
                if u_clean in VALID_CREDENTIALS and VALID_CREDENTIALS[u_clean] == p_clean:
                    st.session_state["authenticated"] = True
                    st.session_state["current_user"] = u_clean
                    st.success(f"✔ Access granted for user `{u_clean}`! Loading intelligence cockpit...")
                    st.rerun()
                else:
                    st.error("❌ Authentication Failed: Invalid Username or Password. Please see credentials below.")

        st.markdown("---")
        with st.expander("🔑 Quick-Access Demo Credentials (Click to Inspect)", expanded=True):
            st.markdown("""
| Role / Designation | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Lead Vehicle Engineer** | `chief_engineer` | `TourbillonV16` | Chief Engineer & Board Approval |
| **Executive Procurement** | `bugatti_admin` | `Molsheim2026!` | Full RFP Ingestion & Scoring |
| **System Administrator** | `admin` | `admin123` | Administrative Diagnostics |
            """)

            if st.button("⚡ 1-Click Fast Login as Lead Vehicle Engineer", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["current_user"] = "chief_engineer"
                st.rerun()


# --- CHECK AUTHENTICATION STATUS ---
if not st.session_state.get("authenticated", False):
    render_login_page()
    st.stop()


# ─────────────────────────────────────────────────────────────
#  AUTHENTICATED PORTAL (MAIN INTERFACE)
# ─────────────────────────────────────────────────────────────

# --- TOP HEADER WITH USER STATUS & LOGOUT ---
col_head1, col_head2 = st.columns([5, 1.2])
with col_head1:
    st.title("🏎️ Bugatti Automobiles S.A.S. — Hypercar Seatbelt RFP Evaluator")
    st.caption(
        "**RAG-Powered Technical Procurement Platform** | 6-Pillar Veteran Justification & Live Proposal Highlighting | "
        "**Zero-Persistence BYOK Security**"
    )
with col_head2:
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='text-align:right; font-size:0.85rem; color:#475569;'>👤 <b>{st.session_state.get('current_user', 'Admin')}</b></div>",
        unsafe_allow_html=True
    )
    if st.button("🚪 Sign Out", key="top_signout_btn", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["current_user"] = ""
        st.rerun()

# --- SIDEBAR: USER BADGE, BYOK VAULT & PROPOSAL TEST LIBRARY ---
with st.sidebar:
    st.markdown(f"""
    <div style="background:#F8FAFC; border:1px solid #CBD5E1; border-radius:10px; padding:12px 14px; margin-bottom:12px;">
        <div style="font-size:0.7rem; color:#64748B; font-weight:800; text-transform:uppercase; letter-spacing:0.8px;">Active Session</div>
        <div style="font-size:0.95rem; color:#0F172A; font-weight:800; margin-top:2px;">👤 {st.session_state.get('current_user', 'User')}</div>
        <div style="font-size:0.75rem; color:#10B981; font-weight:600; margin-top:2px;">● Level-4 Procurement Clearance</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Sign Out of Session", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["current_user"] = ""
        st.rerun()

    st.divider()
    st.header("🔐 1. Your Session-Only API Key")
    st.caption(
        "**Bring Your Own Key (BYOK):** Enter your free Google Gemini API key below. "
        "It is held **strictly in temporary browser session RAM**—never saved to disk or GitHub—and "
        "automatically vanishes when you close this tab or click **End Session**."
    )

    if not st.session_state["user_ephemeral_api_key"]:
        with st.form("ephemeral_key_form", clear_on_submit=True):
            entered_key = st.text_input(
                "Paste Free Gemini API Key:",
                type="password",
                placeholder="AIzaSy..."
            )
            submitted = st.form_submit_button("🔓 Activate Key for This Session Only", use_container_width=True)
            if submitted and entered_key.strip():
                st.session_state["user_ephemeral_api_key"] = entered_key.strip()
                st.rerun()

        st.markdown(
            "👉 *Don't have a key? Get a 100% free key in 10 seconds at "
            "[Google AI Studio](https://aistudio.google.com/).*"
        )
        st.markdown("---")
        if st.button("⚡ Offline Veteran Demo Mode (No Key Needed)", use_container_width=True):
            st.session_state["user_ephemeral_api_key"] = "DEMO_MODE"
            st.rerun()
    else:
        if st.session_state["user_ephemeral_api_key"] == "DEMO_MODE":
            st.success("✅ **Offline Veteran Demo Mode Active**\n\n*(High-fidelity deterministic heuristic extraction)*")
        else:
            masked = st.session_state["user_ephemeral_api_key"][:4] + "••••••••••••" + st.session_state["user_ephemeral_api_key"][-3:]
            st.success(f"✅ **Session Key Active:** `{masked}`\n\n*(Stored in temporary RAM only—forgotten on tab close)*")

        if st.button("🔥 End Session & Forget API Key Now", type="primary", use_container_width=True):
            wipe_session_and_forget_key()
            st.rerun()

    api_key = st.session_state["user_ephemeral_api_key"]

    st.divider()
    st.header("📂 2. Get the 10 Separate Vendor Proposals")
    st.write(
        "Download or generate all **10 original supercar seatbelt vendor proposals** (`.PDF` and `.TXT`) "
        "to upload into the evaluator:"
    )

    if st.button("⚡ Generate 10 Files in Local Folder", use_container_width=True):
        out_folder = generate_all_vendor_files("vendor_proposals")
        st.success(f"Created 10 `.pdf` and 10 `.txt` files inside `{out_folder}`!")

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for v in VENDOR_PROPOSALS_DATA:
            zf.writestr(f"{v['filename_base']}.txt", v["content"])
            pdf_b = create_pdf_bytes(
                title=f"BUGATTI HYPERCAR RFP PROPOSAL: {v['vendor_name']}",
                subtitle=f"Location: {v['country']} | {v['oem_pedigree']}",
                body_text=v["content"]
            )
            zf.writestr(f"{v['filename_base']}.pdf", pdf_b)

    st.download_button(
        label="📥 Download All 10 Proposals (.ZIP)",
        data=zip_buffer.getvalue(),
        file_name="Bugatti_10_Supercar_Vendor_Proposals.zip",
        mime="application/zip",
        use_container_width=True
    )

    with st.expander("Or download individual vendor PDFs"):
        for v in VENDOR_PROPOSALS_DATA:
            single_pdf = create_pdf_bytes(
                title=f"BUGATTI HYPERCAR RFP PROPOSAL: {v['vendor_name']}",
                subtitle=f"Location: {v['country']} | {v['oem_pedigree']}",
                body_text=v["content"]
            )
            st.download_button(
                label=f"📄 {v['vendor_name']} (.pdf)",
                data=single_pdf,
                file_name=f"{v['filename_base']}.pdf",
                mime="application/pdf",
                key=f"dl_{v['filename_base']}"
            )

    st.divider()
    if st.button("🗑️ Clear Evaluated Proposals Only", use_container_width=True):
        st.session_state["evaluated_vendors"] = {}
        st.session_state["executive_report"] = ""
        st.rerun()

# --- TOP BANNER IF NO KEY IS ACTIVE YET ---
if not api_key:
    st.info(
        "👋 **Session Ready! To begin evaluating:** Paste your personal free Google Gemini API key in the **left sidebar** "
        "(`1. Your Session-Only API Key`), or click **'Offline Veteran Demo Mode'** for instant keyless testing."
    )


# ─────────────────────────────────────────────────────────────
#  COMPARISON CHART HELPER (WINNER: GREEN | 2ND: BLUE | 3RD: AMBER)
# ─────────────────────────────────────────────────────────────
def render_podium_cards_and_charts(sorted_vendors: list, key_prefix: str = "podium"):
    """
    Renders executive podium highlight cards and Plotly comparison charts:
    - 1st Place (Winner): Green (#10B981)
    - 2nd Place: Blue (#2563EB)
    - 3rd Place: Amber (#F59E0B)
    - Others: Slate Gray (#94A3B8)
    """
    if not sorted_vendors:
        return

    # 1. PODIUM CARDS (Top 3)
    cols = st.columns(min(3, len(sorted_vendors)))

    # 1st Place (Winner - Green)
    top_1 = sorted_vendors[0]
    m1 = top_1.get("quantitative_metrics", {})
    with cols[0]:
        st.markdown(f"""
        <div style="background:#ECFDF5; border:2.5px solid #10B981; border-radius:12px; padding:16px; margin-bottom:12px; box-shadow:0 4px 6px -1px rgba(16,185,129,0.18);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="background:#10B981; color:#FFFFFF; font-size:0.75rem; font-weight:800; padding:3px 9px; border-radius:4px; letter-spacing:0.5px;">🥇 1ST • WINNER</span>
                <span style="font-size:1.45rem; font-weight:800; color:#065F46;">{top_1['weighted_total_score']:.1f}/100</span>
            </div>
            <div style="font-size:1.2rem; font-weight:800; color:#064E3B; margin-top:8px;">{top_1['vendor_name']}</div>
            <div style="font-size:0.82rem; color:#047857; margin-bottom:8px;">📍 {top_1.get('country', 'Europe')}</div>
            <hr style="border:none; border-top:1px solid #A7F3D0; margin:6px 0;">
            <div style="font-size:0.8rem; color:#065F46; line-height:1.6;">
                • <b>Vehicle Mass:</b> {m1.get('weight_grams_per_car', 'N/A')}g<br>
                • <b>Pretensioner Fire:</b> {m1.get('pretensioner_ms', 'N/A')} ms<br>
                • <b>Tooling NRE:</b> €{m1.get('nre_cost_eur', 0):,}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 2nd Place (Blue)
    if len(sorted_vendors) >= 2:
        top_2 = sorted_vendors[1]
        m2 = top_2.get("quantitative_metrics", {})
        with cols[1]:
            st.markdown(f"""
            <div style="background:#EFF6FF; border:2.5px solid #2563EB; border-radius:12px; padding:16px; margin-bottom:12px; box-shadow:0 4px 6px -1px rgba(37,99,235,0.18);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="background:#2563EB; color:#FFFFFF; font-size:0.75rem; font-weight:800; padding:3px 9px; border-radius:4px; letter-spacing:0.5px;">🥈 2ND POSITION</span>
                    <span style="font-size:1.45rem; font-weight:800; color:#1E40AF;">{top_2['weighted_total_score']:.1f}/100</span>
                </div>
                <div style="font-size:1.2rem; font-weight:800; color:#1E3A8A; margin-top:8px;">{top_2['vendor_name']}</div>
                <div style="font-size:0.82rem; color:#1D4ED8; margin-bottom:8px;">📍 {top_2.get('country', 'Europe')}</div>
                <hr style="border:none; border-top:1px solid #BFDBFE; margin:6px 0;">
                <div style="font-size:0.8rem; color:#1E40AF; line-height:1.6;">
                    • <b>Vehicle Mass:</b> {m2.get('weight_grams_per_car', 'N/A')}g<br>
                    • <b>Pretensioner Fire:</b> {m2.get('pretensioner_ms', 'N/A')} ms<br>
                    • <b>Tooling NRE:</b> €{m2.get('nre_cost_eur', 0):,}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 3rd Place (Amber)
    if len(sorted_vendors) >= 3:
        top_3 = sorted_vendors[2]
        m3 = top_3.get("quantitative_metrics", {})
        with cols[2]:
            st.markdown(f"""
            <div style="background:#FFFBEB; border:2.5px solid #F59E0B; border-radius:12px; padding:16px; margin-bottom:12px; box-shadow:0 4px 6px -1px rgba(245,158,11,0.18);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="background:#F59E0B; color:#FFFFFF; font-size:0.75rem; font-weight:800; padding:3px 9px; border-radius:4px; letter-spacing:0.5px;">🥉 3RD POSITION</span>
                    <span style="font-size:1.45rem; font-weight:800; color:#92400E;">{top_3['weighted_total_score']:.1f}/100</span>
                </div>
                <div style="font-size:1.2rem; font-weight:800; color:#78350F; margin-top:8px;">{top_3['vendor_name']}</div>
                <div style="font-size:0.82rem; color:#B45309; margin-bottom:8px;">📍 {top_3.get('country', 'Europe')}</div>
                <hr style="border:none; border-top:1px solid #FDE68A; margin:6px 0;">
                <div style="font-size:0.8rem; color:#92400E; line-height:1.6;">
                    • <b>Vehicle Mass:</b> {m3.get('weight_grams_per_car', 'N/A')}g<br>
                    • <b>Pretensioner Fire:</b> {m3.get('pretensioner_ms', 'N/A')} ms<br>
                    • <b>Tooling NRE:</b> €{m3.get('nre_cost_eur', 0):,}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 2. INTERACTIVE PLOTLY COMPARISON CHARTS
    chart_tab1, chart_tab2 = st.tabs([
        "🏆 Overall Composite Score (Podium Colors)",
        "📊 6-Pillar Grouped Contender Breakdown"
    ])

    with chart_tab1:
        v_names = []
        scores = []
        bar_colors = []
        labels = []
        hovers = []

        for i, v in enumerate(sorted_vendors):
            v_names.append(v["vendor_name"])
            scores.append(v["weighted_total_score"])
            m = v.get("quantitative_metrics", {})
            total_250 = m.get("nre_cost_eur", 0) + (250 * m.get("unit_bom_eur", 0))

            if i == 0:
                bar_colors.append("#10B981")  # Green (Winner)
                tag = "🥇 Winner (#1)"
            elif i == 1:
                bar_colors.append("#2563EB")  # Blue (2nd Position)
                tag = "🥈 2nd Position"
            elif i == 2:
                bar_colors.append("#F59E0B")  # Amber (3rd Position)
                tag = "🥉 3rd Position"
            else:
                bar_colors.append("#94A3B8")  # Slate Gray
                tag = f"#{i+1}"

            labels.append(f"<b>{v['weighted_total_score']:.1f}</b>")
            hovers.append(
                f"<b>{v['vendor_name']}</b> ({v.get('country', '')})<br>"
                f"<b>Standing:</b> {tag}<br>"
                f"<b>Composite Score:</b> {v['weighted_total_score']:.1f} / 100<br>"
                f"<b>System Mass:</b> {m.get('weight_grams_per_car', 'N/A')} g (Max: 2,400g)<br>"
                f"<b>Pretensioner Latency:</b> {m.get('pretensioner_ms', 'N/A')} ms<br>"
                f"<b>Webbing Strength:</b> {m.get('webbing_strength_kn', 'N/A')} kN<br>"
                f"<b>Quality PPM:</b> {m.get('defect_ppm', 'N/A')} PPM<br>"
                f"<b>Upfront NRE:</b> €{m.get('nre_cost_eur', 0):,}<br>"
                f"<b>Unit BOM:</b> €{m.get('unit_bom_eur', 0):,}<br>"
                f"<b>Total 250-Car Cost:</b> €{total_250:,}<br>"
                f"<b>Lead Time:</b> {m.get('lead_time_weeks', 'N/A')} wks"
            )

        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(
            x=v_names,
            y=scores,
            marker=dict(
                color=bar_colors,
                line=dict(color="#0F172A", width=1.2)
            ),
            text=labels,
            textposition="outside",
            hovertext=hovers,
            hoverinfo="text",
            width=0.5 if len(v_names) <= 3 else 0.6
        ))

        fig_comp.add_hline(
            y=75, line_dash="dash", line_color="#10B981",
            annotation_text="Shortlist Approval Threshold (75 pts)",
            annotation_position="top right"
        )
        fig_comp.add_hline(
            y=50, line_dash="dot", line_color="#EF4444",
            annotation_text="Conditional Minimum Pass (50 pts)",
            annotation_position="bottom right"
        )

        fig_comp.update_layout(
            title=dict(
                text="<b>Contender Evaluation Comparison — Winner (Green) | 2nd (Blue) | 3rd (Amber)</b>",
                font=dict(size=16, color="#0F172A")
            ),
            xaxis=dict(title="<b>Restraint System Supplier</b>", tickangle=-10 if len(v_names) > 3 else 0),
            yaxis=dict(title="<b>Weighted Score (/100)</b>", range=[0, 110], dtick=20, gridcolor="#E2E8F0"),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            height=460,
            margin=dict(l=40, r=40, t=60, b=50)
        )
        st.plotly_chart(fig_comp, use_container_width=True, key=f"{key_prefix}_composite_chart")

    with chart_tab2:
        top_candidates = sorted_vendors[:3]
        pillar_labels = [
            "1. Crash (25%)",
            "2. Mass (20%)",
            "3. Luxury (20%)",
            "4. Quality (15%)",
            "5. Commercials (10%)",
            "6. Supply Chain (10%)"
        ]
        pillar_keys = [
            "crash_homologation",
            "lightweighting_materials",
            "luxury_acoustics_nvh",
            "quality_traceability",
            "commercial_economics",
            "supply_chain_logistics"
        ]

        fig_pillars = go.Figure()
        podium_colors = ["#10B981", "#2563EB", "#F59E0B"]
        podium_badges = ["🥇 Winner", "🥈 2nd Position", "🥉 3rd Position"]

        for idx, cand in enumerate(top_candidates):
            c_scores = [cand["pillar_scores"][pk]["score_out_of_100"] for pk in pillar_keys]
            fig_pillars.add_trace(go.Bar(
                name=f"{podium_badges[idx]} — {cand['vendor_name']}",
                x=pillar_labels,
                y=c_scores,
                marker_color=podium_colors[idx],
                text=[f"{s}" for s in c_scores],
                textposition="outside"
            ))

        fig_pillars.update_layout(
            barmode="group",
            title=dict(
                text="<b>Pillar-by-Pillar Benchmark: Winner (Green) vs. 2nd (Blue) vs. 3rd (Amber)</b>",
                font=dict(size=16, color="#0F172A")
            ),
            yaxis=dict(title="<b>Pillar Score (/100)</b>", range=[0, 115], dtick=20, gridcolor="#E2E8F0"),
            xaxis=dict(title="<b>Evaluation Engineering Pillars</b>"),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=480,
            margin=dict(l=40, r=40, t=70, b=50)
        )
        st.plotly_chart(fig_pillars, use_container_width=True, key=f"{key_prefix}_pillars_chart")


# ─────────────────────────────────────────────────────────────
#  MAIN 6 TABS
# ─────────────────────────────────────────────────────────────
tab_upload, tab_leaderboard, tab_highlight, tab_exec, tab_rfp_spec, tab_guide = st.tabs([
    "📤 1. Upload & Evaluate (RAG)",
    "📊 2. Veteran Scorecard & Comparison",
    "🖍️ 3. Score Justifications & Highlighted Proposals",
    "🏆 4. Executive Winner Report",
    "📘 5. Bugatti Master RFP Rulebook",
    "📖 6. Salient Features & User Guide"
])

# === TAB 1: UPLOAD & EVALUATE ===
with tab_upload:
    st.subheader("Upload Vendor RFP Proposals (`.pdf`, `.txt`, or `.md`)")
    st.markdown(
        "Upload the **10 separate supercar vendor files** one by one (or all together), **OR upload any brand-new "
        "seatbelt RFP proposal**. Our **Hybrid RAG Engine** chunks the document, retrieves matching Bugatti RFP "
        "clauses, justifies every score, and highlights the exact evidence inside the vendor's proposal."
    )

    # Convenient 1-click evaluation of pre-generated proposals
    with st.expander("⚡ Rapid Benchmark: Ingest Pre-Loaded Proposals Directly (1-Click)", expanded=False):
        col_bench1, col_bench2 = st.columns([2, 1])
        with col_bench1:
            pregen_names = [v["vendor_name"] for v in VENDOR_PROPOSALS_DATA]
            selected_pregen = st.multiselect(
                "Select Pre-Configured Tier-1 Proposals:",
                options=pregen_names,
                default=[pregen_names[0], pregen_names[1]]
            )
        with col_bench2:
            eval_all = st.checkbox("Select All 10 Proposals", value=False)
            if st.button("⚡ Ingest Selected Pre-Loaded Proposals", use_container_width=True):
                if not api_key:
                    st.error("🔒 Please activate your session key or Offline Demo Mode in the sidebar first.")
                else:
                    targets = VENDOR_PROPOSALS_DATA if eval_all else [v for v in VENDOR_PROPOSALS_DATA if v["vendor_name"] in selected_pregen]
                    rag_engine = HybridRAGEngine(api_key=api_key)
                    p_bar = st.progress(0)
                    s_box = st.empty()
                    for idx, v in enumerate(targets):
                        fname = f"{v['filename_base']}.txt"
                        s_box.warning(f"Evaluating `{v['vendor_name']}` ({idx+1}/{len(targets)})...")
                        rag_bundle = rag_engine.retrieve_context_for_proposal(v["content"], v["filename_base"][:12])
                        res = evaluate_vendor_with_gemini_rag(api_key, fname, v["content"], rag_bundle)
                        res["full_proposal_text"] = v["content"]
                        st.session_state["evaluated_vendors"][fname] = res
                        p_bar.progress((idx + 1) / len(targets))
                    s_box.success(f"✔ Evaluated {len(targets)} proposals! Proceed to Tab 2 or Tab 3.")
                    st.rerun()

    uploaded_files = st.file_uploader(
        "Drag and drop seatbelt RFP proposal files here (.pdf, .txt, .md)",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.info(f"**{len(uploaded_files)} file(s)** ready. Click below to run the RAG Veteran Evaluator.")
        if st.button("🚀 Run RAG Evaluation on Uploaded Proposal(s)", type="primary"):
            if not api_key:
                st.error("🔒 Please activate your session-only Gemini API key or Demo Mode in the left sidebar first.")
            else:
                rag_engine = HybridRAGEngine(api_key=api_key)
                progress = st.progress(0)
                status_box = st.empty()

                for idx, uf in enumerate(uploaded_files):
                    if uf.name in st.session_state["evaluated_vendors"]:
                        status_box.info(f"✅ `{uf.name}` already evaluated in this session — skipping re-run.")
                    else:
                        status_box.warning(
                            f"🔍 **Step 1/2 (RAG Retrieval):** Chunking `{uf.name}` and retrieving Bugatti RFP clauses..."
                        )
                        text_content = extract_text_from_uploaded_file(uf)
                        rag_bundle = rag_engine.retrieve_context_for_proposal(
                            proposal_text=text_content,
                            vendor_label=uf.name.split(".")[0].upper()
                        )
                        status_box.warning(
                            f"🧠 **Step 2/2 (Veteran Scoring & Quote Highlighting):** Grading `{uf.name}` across 6 pillars..."
                        )
                        try:
                            eval_result = evaluate_vendor_with_gemini_rag(
                                api_key=api_key,
                                filename=uf.name,
                                full_proposal_text=text_content,
                                rag_bundle=rag_bundle
                            )
                            eval_result["full_proposal_text"] = text_content
                            st.session_state["evaluated_vendors"][uf.name] = eval_result
                        except Exception as e:
                            st.error(f"Error evaluating `{uf.name}`: {e}")

                    progress.progress((idx + 1) / len(uploaded_files))

                status_box.success(
                    f"🎉 Evaluation complete! Open **Tab 2** for the Leaderboard or **Tab 3** to see the "
                    f"detailed justifications and color-highlighted vendor proposals!"
                )
                st.rerun()

    if st.session_state["evaluated_vendors"]:
        st.markdown("---")
        st.markdown("### Currently Evaluated Proposals in This Session")
        quick_rows = []
        for fname, data in st.session_state["evaluated_vendors"].items():
            quick_rows.append({
                "Uploaded File": fname,
                "Vendor Name": data["vendor_name"],
                "Country": data["country"],
                "Weighted Score (/100)": data["weighted_total_score"],
                "RAG Chunks Indexed": data["rag_metadata"]["total_vendor_chunks"],
                "Compliance Alert": data["homologation_blocker_flag"]
            })
        st.dataframe(
            pd.DataFrame(quick_rows).sort_values("Weighted Score (/100)", ascending=False),
            use_container_width=True,
            hide_index=True
        )

# === TAB 2: LEADERBOARD & COMPARISON MATRIX ===
with tab_leaderboard:
    eval_list = list(st.session_state["evaluated_vendors"].values())
    if not eval_list:
        st.info("Upload and evaluate at least 1 vendor proposal in **Tab 1** to view the Leaderboard and Comparison Chart.")
    else:
        sorted_vendors = sorted(eval_list, key=lambda x: x["weighted_total_score"], reverse=True)
        top_v = sorted_vendors[0]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🥇 Current #1 Vendor", top_v["vendor_name"], f"{top_v['weighted_total_score']} / 100")
        col2.metric("⚖️ #1 System Weight", f"{top_v['quantitative_metrics']['weight_grams_per_car']} g", "Target: <= 2,400 g")
        col3.metric("⚡ #1 Pretensioner Fire", f"{top_v['quantitative_metrics']['pretensioner_ms']} ms", "Target: <= 6.5 ms")
        col4.metric("💶 #1 Upfront NRE", f"€{top_v['quantitative_metrics']['nre_cost_eur']:,}", "Target: <= €850,000")

        st.markdown("---")
        st.subheader("1. Contender Benchmark & Podium Comparison Charts")
        st.caption(
            "Side-by-side graphical comparison of supplier performance. "
            "**Winner (#1)** highlighted in **Green**, **Second Position (#2)** in **Blue**, and **Third Position (#3)** in **Amber**."
        )
        render_podium_cards_and_charts(sorted_vendors, key_prefix="tab2_leaderboard")

        st.markdown("---")
        st.subheader("2. Weighted 6-Pillar Veteran Scorecard (Sorted by Rank)")
        score_rows = []
        for rank, v in enumerate(sorted_vendors, start=1):
            ps = v["pillar_scores"]
            score_rows.append({
                "Rank": f"#{rank}",
                "Vendor": v["vendor_name"],
                "Country": v["country"],
                "Weighted Total (/100)": v["weighted_total_score"],
                "1. Crash & Homologation (25%)": ps["crash_homologation"]["score_out_of_100"],
                "2. Lightweighting (20%)": ps["lightweighting_materials"]["score_out_of_100"],
                "3. Luxury & NVH (20%)": ps["luxury_acoustics_nvh"]["score_out_of_100"],
                "4. Zero-Defect Quality (15%)": ps["quality_traceability"]["score_out_of_100"],
                "5. Commercials & NRE (10%)": ps["commercial_economics"]["score_out_of_100"],
                "6. Molsheim Supply Chain (10%)": ps["supply_chain_logistics"]["score_out_of_100"],
            })
        df_scores = pd.DataFrame(score_rows)
        st.dataframe(df_scores, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("3. Side-by-Side Real Quantitative Engineering & Commercial Comparison")
        metric_rows = []
        for v in sorted_vendors:
            m = v["quantitative_metrics"]
            total_250_cost = m["nre_cost_eur"] + (250 * m["unit_bom_eur"])
            metric_rows.append({
                "Vendor": v["vendor_name"],
                "Mass / Car (g) [<=2400g]": m["weight_grams_per_car"],
                "Pretensioner (ms) [<=6.5ms]": m["pretensioner_ms"],
                "Webbing Strength (kN) [>=26.5]": m["webbing_strength_kn"],
                "UV Delta-E [<1.2]": m["uv_delta_e"],
                "Buckle Click (dB) [52-58dB]": m["buckle_click_db"],
                "Defect Rate (PPM) [<=2.0]": m["defect_ppm"],
                "Upfront NRE (€) [<=€850k]": f"€{m['nre_cost_eur']:,}",
                "Unit BOM / Car (€) [<=€2,800]": f"€{m['unit_bom_eur']:,}",
                "Total 250-Car Program (€)": f"€{total_250_cost:,}",
                "Lead Time (Wks) [<=6.0]": m["lead_time_weeks"],
                "ECE + FMVSS": "✅" if m["has_ece_fmvss"] else "❌",
                "FIA 8853": "✅" if m["has_fia_8853"] else "⚠️",
                "IATF 16949": "✅" if m["has_iatf_16949"] else "❌"
            })
        st.dataframe(pd.DataFrame(metric_rows), use_container_width=True, hide_index=True)

# === TAB 3: SCORE JUSTIFICATIONS & HIGHLIGHTED VENDOR PROPOSALS ===
with tab_highlight:
    eval_list = list(st.session_state["evaluated_vendors"].values())
    if not eval_list:
        st.info("Upload and evaluate proposals in **Tab 1** to inspect score justifications and highlighted vendor proposals.")
    else:
        sorted_eval = sorted(eval_list, key=lambda x: x["weighted_total_score"], reverse=True)
        vendor_names = [
            f"#{idx+1} — {v['vendor_name']} ({v['weighted_total_score']}/100) [{v['uploaded_filename']}]"
            for idx, v in enumerate(sorted_eval)
        ]
        selected_label = st.selectbox("Select an Evaluated Vendor Proposal to Inspect:", vendor_names)
        selected_vendor = sorted_eval[vendor_names.index(selected_label)]

        st.markdown(f"### {selected_vendor['vendor_name']} — {selected_vendor['country']}")
        st.write(f"**OEM Supercar Pedigree:** {selected_vendor['oem_pedigree_summary']}")

        # --- PART A: HIGHLIGHTED FULL VENDOR PROPOSAL VIEWER ---
        st.markdown("#### 🖍️ Annotated Vendor Proposal (Exact Scored Evidence Highlighted in Color)")
        st.caption(
            "Every highlighted sentence below was extracted verbatim by the AI Veteran Panel as direct evidence "
            "justifying the vendor's score in that specific pillar."
        )

        filter_options = {"ALL": "🌈 Show All 6 Pillars Highlighted Together"}
        for p in EVALUATION_PILLARS:
            filter_options[p["id"]] = f"Filter: {p['name']} ({int(p['weight']*100)}%)"

        chosen_filter = st.radio(
            "Highlight Filter:",
            options=list(filter_options.keys()),
            format_func=lambda k: filter_options[k],
            horizontal=True
        )

        highlighted_html = render_highlighted_vendor_proposal(
            raw_text=selected_vendor.get("full_proposal_text", ""),
            pillar_scores=selected_vendor["pillar_scores"],
            filter_pillar_id=chosen_filter
        )
        st.markdown(highlighted_html, unsafe_allow_html=True)

        st.markdown("---")

        # --- PART B: COMPONENT-BY-COMPONENT SCORE JUSTIFICATION CARDS ---
        st.markdown("#### 📋 Detailed Component-by-Component Score Justifications & RAG Citations")
        for pillar in EVALUATION_PILLARS:
            pid = pillar["id"]
            p_eval = selected_vendor["pillar_scores"][pid]
            p_rag = selected_vendor["rag_metadata"]["pillar_retrievals"][pid]
            style = PILLAR_HIGHLIGHT_STYLES[pid]
            score_num = p_eval["score_out_of_100"]
            weighted_contrib = round(score_num * pillar["weight"], 2)

            with st.expander(
                f"{pillar['name']} — Score: {score_num}/100 "
                f"(Contributes {weighted_contrib} pts of {int(pillar['weight']*100)} max pts) | {pillar['veteran_role']}",
                expanded=True
            ):
                st.markdown(
                    f'<div style="background-color:{style["bg"]}; border-left:5px solid {style["border"]}; '
                    f'padding:12px 16px; border-radius:6px; color:{style["text"]}; margin-bottom:12px;">'
                    f'<strong>25-Year Veteran Justification:</strong> {html.escape(p_eval.get("veteran_verdict", ""))}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                j_col1, j_col2 = st.columns(2)
                with j_col1:
                    st.success(f"**✅ Why Points Were Awarded:**\n\n{p_eval.get('points_earned_for', 'N/A')}")
                with j_col2:
                    st.warning(f"**⚠️ Why Points Were Deducted (vs. Bugatti Spec):**\n\n{p_eval.get('points_deducted_for', 'N/A')}")

                st.markdown("**🖍️ Exact Verbatim Quotes Highlighted in Proposal for This Pillar:**")
                quotes_to_show = p_eval.get("verbatim_proposal_quotes", [])
                if quotes_to_show:
                    for q in quotes_to_show:
                        st.code(f'"{q}"', language="text")
                else:
                    st.caption("No verbatim quotes extracted for this pillar.")

                with st.popover("🔍 View Underlying RAG Vector Chunks (Bugatti Clause vs. Vendor Chunk)"):
                    st.markdown("**📘 Retrieved Bugatti Master RFP Requirement Chunk:**")
                    for bc in p_rag["bugatti_requirement_chunks"]:
                        st.code(f"[{bc['chunk_id']} | Sim: {bc['similarity']}]\n{bc['text']}", language="text")
                    st.markdown("**📄 Retrieved Vendor Proposal Evidence Chunks:**")
                    for vc in p_rag["vendor_evidence_chunks"]:
                        st.code(f"[{vc['chunk_id']} | Sim: {vc['similarity']}]\n{vc['text']}", language="text")

# === TAB 4: EXECUTIVE WINNER RECOMMENDATION & DOWNLOADABLE REPORT ===
with tab_exec:
    eval_list = list(st.session_state["evaluated_vendors"].values())
    if not eval_list:
        st.info("Evaluate your uploaded vendor proposals in **Tab 1** first, then generate the Chief Engineer's Report here.")
    else:
        sorted_vendors = sorted(eval_list, key=lambda x: x["weighted_total_score"], reverse=True)
        st.subheader("🏆 Bugatti Chief Engineer — Executive Winner Recommendation & Downloadable Report")

        # Visual podium summary before the formal board text
        with st.expander("📊 Executive Visual Podium Summary", expanded=True):
            render_podium_cards_and_charts(sorted_vendors, key_prefix="tab4_exec")

        if st.button("🎖️ Generate Executive Winner Recommendation Report", type="primary"):
            if not api_key:
                st.error("Please activate your session-only Gemini API key or Demo Mode in the sidebar first.")
            else:
                with st.spinner("Chief Engineer is analyzing all evaluated proposals and drafting the Molsheim Board Memo..."):
                    st.session_state["executive_report"] = generate_chief_engineer_executive_report(
                        api_key=api_key,
                        evaluated_vendors=eval_list
                    )

        if st.session_state["executive_report"]:
            st.markdown("---")
            st.markdown(st.session_state["executive_report"])
            st.markdown("---")

            dl_col1, dl_col2 = st.columns(2)
            with dl_col1:
                st.download_button(
                    label="📥 Download Executive Board Report (.MD)",
                    data=st.session_state["executive_report"].encode("utf-8"),
                    file_name="Bugatti_Seatbelt_RFP_Executive_Recommendation.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            with dl_col2:
                csv_rows = []
                for v in sorted_vendors:
                    m = v["quantitative_metrics"]
                    ps = v["pillar_scores"]
                    csv_rows.append({
                        "Vendor": v["vendor_name"],
                        "Country": v["country"],
                        "Weighted_Score": v["weighted_total_score"],
                        "Crash_Score": ps["crash_homologation"]["score_out_of_100"],
                        "Crash_Justification": ps["crash_homologation"]["veteran_verdict"],
                        "Lightweighting_Score": ps["lightweighting_materials"]["score_out_of_100"],
                        "Lightweighting_Justification": ps["lightweighting_materials"]["veteran_verdict"],
                        "Luxury_NVH_Score": ps["luxury_acoustics_nvh"]["score_out_of_100"],
                        "Luxury_Justification": ps["luxury_acoustics_nvh"]["veteran_verdict"],
                        "Quality_Score": ps["quality_traceability"]["score_out_of_100"],
                        "Quality_Justification": ps["quality_traceability"]["veteran_verdict"],
                        "Commercial_Score": ps["commercial_economics"]["score_out_of_100"],
                        "Commercial_Justification": ps["commercial_economics"]["veteran_verdict"],
                        "Supply_Chain_Score": ps["supply_chain_logistics"]["score_out_of_100"],
                        "Supply_Chain_Justification": ps["supply_chain_logistics"]["veteran_verdict"],
                        "Weight_g_per_car": m["weight_grams_per_car"],
                        "Pretensioner_ms": m["pretensioner_ms"],
                        "NRE_EUR": m["nre_cost_eur"],
                        "Unit_BOM_EUR": m["unit_bom_eur"],
                        "Lead_Time_Weeks": m["lead_time_weeks"]
                    })
                csv_bytes = pd.DataFrame(csv_rows).to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📊 Download Full Scorecard + Justifications (.CSV)",
                    data=csv_bytes,
                    file_name="Bugatti_Seatbelt_RFP_Scorecard_With_Justifications.csv",
                    mime="text/csv",
                    use_container_width=True
                )

# === TAB 5: BUGATTI MASTER RFP SPECIFICATION ===
with tab_rfp_spec:
    st.subheader("📘 Official Bugatti Automobiles S.A.S. (Molsheim) Master RFP Knowledge Base")
    st.code(BUGATTI_RFP_MASTER_DOCUMENT, language="text")

# === TAB 6: SALIENT FEATURES & STEP-BY-STEP USER GUIDE ===
with tab_guide:
    st.subheader("📖 Salient Features & Step-by-Step User Guide for New Users")
    guide_path = "USER_GUIDE_AND_FEATURES.md"
    if not os.path.exists(guide_path):
        guide_path = os.path.join(os.path.dirname(__file__), "USER_GUIDE_AND_FEATURES.md")

    if os.path.exists(guide_path):
        with open(guide_path, "r", encoding="utf-8") as gf:
            guide_md = gf.read()
        st.markdown(guide_md)
        st.download_button(
            "📥 Download Complete User Guide (.MD)",
            data=guide_md.encode("utf-8"),
            file_name="Bugatti_RFP_Evaluator_User_Guide.md",
            mime="text/markdown",
            key="dl_user_guide"
        )
    else:
        st.info("Create `USER_GUIDE_AND_FEATURES.md` in your project folder to view and download the full manual here.")
