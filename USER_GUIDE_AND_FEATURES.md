# Bugatti Molsheim | Tier-1 Occupant Restraint RFP Evaluator
## Salient Features & Step-by-Step Operator Guide

---

### 1. Platform Overview & Engineering Scope
The **Bugatti Molsheim RFP Evaluator** is an enterprise-grade artificial intelligence and retrieval-augmented generation (RAG) platform purpose-built for technical procurement evaluation of hypercar seatbelt and occupant restraint systems. 

- **Platform Target:** Bugatti Tourbillon (W16/V16 Platform) & Bolide Track Programs (`BUGATTI-W16-V16-HYPER-RESTRAINT-2026`)
- **Production Scope:** 250 units (50 units/year over 5 years) + 15% service spares — Atelier Molsheim, Alsace, France
- **AI Engine:** Google Gemini 2.5 Flash / Gemini 2.0 Flash paired with dense semantic vector retrieval and technical n-gram TF-IDF cosine similarity

---

### 2. Salient Features

#### 🛡️ Enterprise Login Gateway (RBAC Security)
- **Role-Based Personnel Authentication:** Secure login screen requiring username and password credentials before granting access to technical RFP data.
- **Pre-Configured Personnel Accounts:**
  - `chief_engineer` / `TourbillonV16`: Lead Vehicle Engineer & Technical Authority
  - `bugatti_admin` / `Molsheim2026!`: Executive Director of Procurement
  - `admin` / `admin123`: System Diagnostics & Operations
- **Quick-Access 1-Click Login:** Built-in evaluation button for instant single-click access during evaluations.
- **Session Control:** Instant sign-out controls available on both the top header and sidebar.

#### 📊 Podium Comparison Charts (Winner: Green | 2nd: Blue | 3rd: Amber)
- **Podium Visual Highlight Cards:** Displays the top 3 ranked contenders with high-visibility color-themed badges:
  - 🥇 **Winner (#1 Position):** Highlighted in vibrant **Green** (`#10B981`)
  - 🥈 **Second Position (#2):** Highlighted in deep **Blue** (`#2563EB`)
  - 🥉 **Third Position (#3):** Highlighted in warm **Amber** (`#F59E0B`)
  - **Subsequent Positions (#4+):** Highlighted in neutral Slate Gray (`#94A3B8`)
- **Dual Interactive Plotly Visualizations:**
  1. *Overall Composite Leaderboard:* Compares total weighted scores (/100) with color-coded bars, benchmark threshold lines (75 shortlist pass, 50 conditional minimum), and interactive hover inspection.
  2. *6-Pillar Grouped Contender Breakdown:* Direct side-by-side comparison across Crash (25%), Mass (20%), Luxury (20%), Quality (15%), Commercials (10%), and Logistics (10%).

#### 🔐 Ephemeral Bring-Your-Own-Key (BYOK) Session Vault
- **Zero Disk Persistence:** Your Google Gemini API key is stored exclusively in temporary browser session RAM (`st.session_state`).
- **Instant Eviction:** Keys are completely forgotten when you close your browser tab or click **"🔥 End Session & Forget API Key Now"**.
- **Offline Veteran Mode:** Supports instant offline evaluation using deterministic, high-fidelity quantitative extraction heuristics when operating in air-gapped environments without an API key.

#### 🧠 6-Member Veteran Engineering Panel
Every proposal is evaluated by a simulated panel of automotive veterans with 25+ years of OEM hypercar pedigree (Bugatti, Porsche Motorsport, Ferrari):
1. **Crash Physics & Global Homologation (25% Weight):** Validates ECE R16, FMVSS 209/210, GB 14166, FIA 8853-2016, <= 6.5 ms pyrotechnic firing, and adaptive torsion load limiting.
2. **Hypercar Lightweighting & Materials (20% Weight):** Enforces the <= 2,400g total vehicle ceiling (1,200g/seat) with a stretch goal of <= 1,950g, evaluating Ti-6Al-4V titanium, carbon fiber, and Dyneema webbing.
3. **Bespoke Craftsmanship & Acoustics/NVH (20% Weight):** Grades Sur Mesure color customization, Xenon-Arc UV stability (Delta-E < 1.2), horological buckle click sound (52–58 dB), and 0 dB cabin harmonic resonance.
4. **Manufacturing Quality & Traceability (15% Weight):** Evaluates IATF 16949:2016, VDA 6.3 Grade A (>= 92%), <= 2.0 PPM defect rate, and 100% 3D micro-CT X-ray squib inspection.
5. **Commercial Economics & NRE (10% Weight):** Screens upfront tooling NRE (<= EUR 850,000) and unit shipset BOM (<= EUR 2,800/car).
6. **Molsheim Atelier Logistics (10% Weight):** Verifies Just-In-Sequence (JIS) delivery in climate-sealed flight cases, <= 6.0 week lead times, and 35-year classic spares commitment.

#### ⚖️ Granular Score Justifications (Points Earned vs. Points Deducted)
Unlike black-box AI scores, the platform itemizes:
- **Points Earned:** Specific engineering specifications, certifications, and metallurgical innovations that gained points.
- **Points Deducted:** Exact non-compliances, missed targets, or missing certifications that reduced the score relative to the Bugatti specification.

#### 🖍️ Verbatim Evidence Highlighting Inside Proposals
- The engine identifies exact sentences and data cited by each veteran pillar and highlights them directly inside the full vendor proposal viewer using color-coded badges.
- Interactive radio filters let you view all pillars simultaneously or isolate individual pillars (Crash, Mass, Luxury, Quality, Commercials, Logistics).

#### 🏆 Board-Ready Executive Procurement Memorandum
- Generates an official memorandum from **Dr. Maximilian Reuter (Chief Vehicle Engineer & Director of Procurement)**.
- Features primary award recommendation, optional FIA 8853 dual-sourcing track strategy, top contender head-to-head matrix, remediation conditions for disqualified vendors, and binding purchasing mandates.
- Single-click export to Markdown (`.MD`) and tabular scorecard to Excel (`.CSV`).

---

### 3. Step-by-Step Operator Guide

#### Step 1: Login & Authentication
1. Open `http://localhost:8501` in your browser.
2. Enter your authorized username and password (e.g. `chief_engineer` / `TourbillonV16`), or click **"⚡ 1-Click Fast Login as Lead Vehicle Engineer"**.
3. Upon authentication, you will be redirected to the main evaluation cockpit.

#### Step 2: Session Security & API Vault
1. In the left sidebar under **"1. Your Session-Only API Key"**, enter your Gemini API key from [Google AI Studio](https://aistudio.google.com/).
2. Click **"🔓 Activate Key for This Session Only"** (or click **"⚡ Offline Veteran Demo Mode"**).
3. The status indicator will switch to green showing your active session status.

#### Step 3: Ingest & Evaluate Proposals (Tab 1)
1. Navigate to **Tab 1 ("📤 1. Upload & Evaluate")**.
2. Click the expander **"⚡ Rapid Benchmark: Ingest Pre-Loaded Proposals Directly"** and hit **"⚡ Ingest Selected Pre-Loaded Proposals"** (or drag and drop custom `.pdf`, `.txt`, `.md` files).
3. The Hybrid RAG engine indexes clauses, builds TF-IDF vector matrices, and convenes the 6-veteran panel.

#### Step 4: Inspect Leaderboard & Comparison Charts (Tab 2)
1. Open **Tab 2 ("📊 2. Veteran Scorecard & Comparison")**.
2. Review the **Podium Cards** and the **Contender Comparison Chart**:
   - 🥇 **Winner** in **Green**
   - 🥈 **Second Position** in **Blue**
   - 🥉 **Third Position** in **Amber**
3. Toggle between the **Overall Composite Score** and the **6-Pillar Grouped Contender Breakdown**.
4. Examine the detailed numeric telemetry matrix (Mass, ms, kN, Delta-E, dB, PPM, NRE, BOM, 250-Car Total Cost).

#### Step 5: Audit Justifications & Highlighted Proposals (Tab 3)
1. Switch to **Tab 3 ("🖍️ 3. Score Justifications & Highlighted Proposals")**.
2. Select any vendor from the dropdown.
3. Review the **Annotated Proposal Viewer** with color-coded verbatim highlights.
4. Filter by pillar or inspect the **Why Points Were Awarded** vs. **Why Points Were Deducted** breakdown cards.

#### Step 6: Generate Executive Memorandum & Exports (Tab 4)
1. Open **Tab 4 ("🏆 4. Executive Winner Report")**.
2. Review the visual podium summary and click **"🎖️ Generate Executive Winner Recommendation Report"**.
3. Download the Chief Engineer's board report as `.MD` or export the full numeric scorecard as `.CSV`.
