"""
bugatti_rfp_knowledge.py
Contains the official Bugatti Automobiles S.A.S. (Molsheim) Master RFP Specification
and the 6 Veteran Evaluation Pillars for the Tourbillon / Chiron Successor Hypercar Platform.
"""

BUGATTI_RFP_MASTER_DOCUMENT = """
[CLAUSE-1.0: PROGRAM OVERVIEW & VOLUME]
Program Code: BUGATTI-W16-V16-HYPER-RESTRAINT-2026
Issuing OEM: Bugatti Automobiles S.A.S., Chateau Saint-Jean, Dorlisheim / Molsheim, France.
Production Volume: 250 units total run (50 units/year over 5 years) + 15% service spares.
System Scope: Complete 2-seat Occupant Restraint System (Driver & Passenger) supporting up to 445 km/h top speed, 2.0s 0-100 km/h acceleration, and 1.6G lateral cornering.

[CLAUSE-2.0: CRASH PHYSICS, PYROTECHNICS & GLOBAL HOMOLOGATION (WEIGHT: 25%)]
- Mandatory Global Road Homologation: UN/ECE R16 (Europe), FMVSS 209 & FMVSS 210 (USA), CMVSS 209 (Canada), GB 14166 (China), and TRIAS (Japan).
- Track Package Certification: Optional 6-point harness variant or dual-homologated system must comply with FIA 8853-2016 standard.
- Pretensioner Performance: Dual-stage pyrotechnic retractor and buckle pretensioning required. Time-to-fire and slack removal must be <= 6.5 milliseconds upon Crash ECU CAN-FD / PSI5 trigger.
- Load Limiting: Adaptive digressive torsion bar load limiter switching between 4.5 kN (high kinetic energy phase) and 2.8 kN (thoracic protection phase) to prevent clavicle/rib fractures during high-delta-V impacts (>75 km/h barrier test).
- Pre-Crash Integration: System must interface with vehicle ADAS / ESC sensors to pre-tension belt smoothly during >= 0.8G panic braking or evasive maneuvers.

[CLAUSE-3.0: HYPERCAR LIGHTWEIGHTING & EXOTIC MATERIALS (WEIGHT: 20%)]
- Target System Mass: Total installed mass per vehicle (2 seats complete with retractors, webbing, buckles, D-rings, and mounting bolts) must NOT exceed 2,400 grams (1,200 grams per seat). Ideal benchmark: <= 1,950 grams per vehicle.
- Structural Hardware: Stampings from conventional heavy mild steel are discouraged. Vendors must utilize Grade 5 Titanium (Ti-6Al-4V) CNC-machined load plates, forged carbon-fiber housings, or aerospace 7075-T6 aluminum.
- Webbing Construction: Ultra-high-tenacity polyester or hybrid Dyneema/Vectran weave with thickness <= 1.15 mm, minimum breaking strength >= 26.5 kN (ECE/FMVSS benchmark is 14.7 kN; Bugatti requires 80% safety margin), and low elongation (< 6% at 11 kN load).

[CLAUSE-4.0: BUGATTI BESPOKE CRAFTSMANSHIP, LUXURY & ACOUSTICS/NVH (WEIGHT: 20%)]
- Bespoke Color Matching: Must support Bugatti Sur Mesure customization across 50+ custom Pantone webbing shades and custom contrast edge stitching without degrading abrasion resistance or edge energy absorption.
- UV & Abrasion Durability: Delta-E color shift must remain < 1.2 after 1,500 hours of Xenon-Arc solar radiation testing (ISO 105-B06). Zero fraying after 50,000 buckle pass-through cycles.
- Tactile & Acoustic Signature: No visible injection-molded plastic on any occupant-facing surface. Buckle housing must be wrapped in full-grain semi-aniline leather, Alcantara, or billet anodized titanium/aluminum with laser-etched Bugatti Macaron logo.
- Buckle Acoustic Requirement: Insertion latch click must produce a crisp, mechanical horological sound between 52 dB and 58 dB with zero metallic tinny resonance.
- NVH (Noise, Vibration, Harshness): Retractor rattle and tongue-against-B-pillar buzz must be 0 dB across 10 Hz to 1,500 Hz engine harmonic sweep. Motorized or magnetic belt presenter compatibility required.

[CLAUSE-5.0: MANUFACTURING QUALITY & ZERO-DEFECT TRACEABILITY (WEIGHT: 15%)]
- Mandatory Quality Certifications: IATF 16949:2016, ISO 9001, ISO 14001, and VDA 6.3 Process Audit rating 'A' (>= 92%).
- Defect Rate Ceiling: Maximum allowable field and line defect rate is <= 2 PPM (Parts Per Million), targeting 0 PPM for safety-critical pyrotechnic and latching assemblies.
- 100% End-of-Line (EOL) Inspection: Every single retractor and buckle delivered to Molsheim must undergo automated 3D X-ray CT inspection of internal pawls/pyrotechnic squibs, optical laser stitch verification, and serialized QR digital twin traceability retained for 30 years.

[CLAUSE-6.0: COMMERCIAL ECONOMICS & LOW-VOLUME NRE STRUCTURE (WEIGHT: 10%)]
- Non-Recurring Engineering (NRE) & Homologation Sled Testing Target: <= EUR 850,000 total upfront tooling, crash sled validation, and certification cost. Proposals exceeding EUR 1,500,000 NRE will be heavily penalized due to the 250-car volume amortisation.
- Unit Bill of Materials (BOM) Target: <= EUR 2,800 per vehicle shipset (2 seats complete).
- Color Customization Fee: <= EUR 450 surcharge per bespoke Sur Mesure single-vehicle color setup with minimum order quantity (MOQ) of 1 vehicle.

[CLAUSE-7.0: SUPPLY CHAIN RESILIENCE & MOLSHEIM ATELIER LOGISTICS (WEIGHT: 10%)]
- Delivery Model: Just-In-Sequence (JIS) bespoke kit delivery to Bugatti Atelier in Molsheim, Alsace, France, inside climate-sealed Alcantara-lined flight cases.
- Lead Time: <= 6 weeks from final customer specification lock to Molsheim dock arrival.
- Sub-Tier Sourcing: 100% European, Japanese, or North American dual-sourced raw titanium and pyrotechnic initiators. Full IMDS material reporting and REACH/RoHS compliance.
- Warranty & Service Spares: 15-year structural/corrosion guarantee and guaranteed spare parts reproduction capability for 35 years post-production (Bugatti Classic program).
"""

EVALUATION_PILLARS = [
    {
        "id": "crash_homologation",
        "name": "1. Crash Physics & Global Homologation",
        "weight": 0.25,
        "rag_query": "ECE R16 FMVSS 209 FIA 8853 crash homologation pyrotechnic pretensioner ms firing time load limiter kN pre-crash",
        "veteran_role": "Chief Occupant Safety & Pyrotechnics Engineer (28 yrs exp)"
    },
    {
        "id": "lightweighting_materials",
        "name": "2. Hypercar Lightweighting & Materials",
        "weight": 0.20,
        "rag_query": "total weight mass grams titanium carbon fiber aluminum webbing breaking strength kN Dyneema polyester",
        "veteran_role": "Lead Hypercar Mass & Exotic Metallurgy Specialist (25 yrs exp)"
    },
    {
        "id": "luxury_acoustics_nvh",
        "name": "3. Bespoke Craftsmanship & Acoustics/NVH",
        "weight": 0.20,
        "rag_query": "bespoke Pantone color UV fade leather Alcantara billet buckle click sound dB rattle NVH presenter",
        "veteran_role": "Master Atelier Trim, Tactile & Acoustic Director (26 yrs exp)"
    },
    {
        "id": "quality_traceability",
        "name": "4. Manufacturing Quality & Zero-Defect Record",
        "weight": 0.15,
        "rag_query": "IATF 16949 VDA 6.3 PPM defect rate X-ray CT inspection traceability warranty quality",
        "veteran_role": "VP of Automotive Quality & VDA 6.3 Auditor (30 yrs exp)"
    },
    {
        "id": "commercial_economics",
        "name": "5. Commercials & Low-Volume Economics",
        "weight": 0.10,
        "rag_query": "NRE upfront tooling cost EUR unit BOM price per vehicle shipset bespoke color fee MOQ",
        "veteran_role": "Director of Low-Volume Supercar Procurement (25 yrs exp)"
    },
    {
        "id": "supply_chain_logistics",
        "name": "6. Supply Chain & Molsheim Delivery",
        "weight": 0.10,
        "rag_query": "Molsheim France delivery lead time weeks JIS flight case warranty spare parts years sub-tier",
        "veteran_role": "Global Supply Chain & Molsheim Logistics Lead (27 yrs exp)"
    }
]

# ─────────────────────────────────────────────────────────────
#  SUPPLEMENTARY CONSTANTS  (used by evaluator_engine.py and
#  generate_vendor_files.py — not part of the RFP document itself)
# ─────────────────────────────────────────────────────────────

# Automatic disqualification triggers (Phase-1 eligibility screen)
DISQUALIFIERS = [
    "No IATF 16949:2016 certification or expired/lapsed certification",
    "Active pyrotechnic product recall, regulatory sanction, or ongoing safety investigation",
    "No demonstrated global homologation capability (ECE R16 + FMVSS 209 minimum)",
    "Less than 10 years of OEM automotive safety restraint supply experience",
    "No VDA 6.3 Process Audit score or score below 92% (Grade A)",
    "Proposed field PPM > 50 for pyrotechnic or safety-critical latch assemblies",
    "Cannot demonstrate system mass compliance path to <= 2,400 grams per vehicle",
    "Refusal to sign Bugatti standard NDA and IP agreement",
    "REACH / IMDS non-compliance for pyrotechnic initiators or webbing chemistry",
    "No in-house crash sled or homologation test capability (or certified test partner)",
    "Missing or unverifiable CE / ECE type-approval certificates",
    "Proposed NRE exceeding EUR 2,500,000 (hard ceiling, unacceptable for 250-unit run)",
]

# Chief Engineer final report synthesis prompt
CHIEF_ENGINEER_REPORT_TEMPLATE = """
You are Dr. Maximilian Reuter, Chief Engineer — Occupant Safety & Active Systems,
Bugatti Automobiles S.A.S., with 28 years of pyrotechnic restraint system development
across Veyron, Chiron, Divo, Bolide, and now the Tourbillon programme.

You have just reviewed the six specialist pillar evaluations from your expert panel.
Your task is to write the FINAL BOARD RECOMMENDATION for this restraint system supplier.

This is NOT a bureaucratic summary — it is YOUR personal engineering and strategic verdict
that will go directly to the Bugatti Executive Board and the Rimac Group Procurement Council.

Your final report MUST include all of these sections, clearly labelled:

1. OVERALL VERDICT: one of — APPROVED FOR SHORTLIST / CONDITIONAL APPROVE / FURTHER REVIEW / REJECTED
   (Write this in bold at the very top)

2. COMPOSITE WEIGHTED SCORE: calculated from all six pillar scores

3. EXECUTIVE SUMMARY (3–5 sentences): the essence of this vendor — what they are, why they matter or don't

4. TOP 3 STRENGTHS: specific, evidence-backed reasons with direct reference to proposal data

5. TOP 3 RISKS / CONCERNS: specific technical, commercial, or safety risks — be precise

6. CONDITIONS (if Conditional Approve): exact, numbered, measurable conditions required before award

7. SAFETY-CRITICAL FLAG: any pyrotechnic, homologation, or occupant safety concern that
   overrides a commercial or aesthetic score — e.g. "SAFETY HOLD — resolve before any award"

8. RECOMMENDED NEXT STEP: e.g. sled test audit, prototype buckle submission, shortlist, reject

9. VETERAN INSTINCT (1 sentence): your gut feeling as a 28-year hypercar safety engineer

Write with precision and authority. Reference specific numbers from the proposal.
Do not soften verdicts. Bugatti lives or dies on occupant safety — be direct.
"""

# Ten vendor scenarios matching generate_vendor_files.py
VENDOR_SCENARIOS = [
    {
        "name": "Sabelt S.p.A.",
        "filename_base": "01_Sabelt_SpA_Italy_Proposal",
        "category": "Hypercar Restraint & Track Harness",
        "country": "Turin (Moncalieri), Italy",
        "profile": "excellent",
        "description": "Official OEM Restraint Supplier for Ferrari Daytona SP3, SF90 XX, McLaren 750S. Full dual ECE R16 & FIA 8853 homologation, 1,790g, 1.1 PPM, €680k NRE.",
    },
    {
        "name": "Schroth Safety Products GmbH",
        "filename_base": "02_Schroth_Safety_Germany_Proposal",
        "category": "Hypercar Restraint & Track Harness",
        "country": "Arnsberg, Germany",
        "profile": "excellent",
        "description": "OEM restraint leader for Porsche 918, GT3 RS, Bugatti Bolide. Patented ASM tech, titanium hardware, 1,720g, 0.4 PPM, €740k NRE.",
    },
    {
        "name": "Autoliv AB",
        "filename_base": "03_Autoliv_AB_Sweden_Proposal",
        "category": "Global Tier-1 Restraint Systems",
        "country": "Stockholm, Sweden",
        "profile": "good_with_gaps",
        "description": "World's largest safety Tier-1. Flawless 0.3 PPM quality, but 2,480g mass exceeds 2,400g ceiling and €1.65M NRE is high for low-volume run.",
    },
    {
        "name": "ZF Lifetec (Passive Safety Systems)",
        "filename_base": "04_ZF_Lifetec_Germany_Proposal",
        "category": "Global Tier-1 Active Restraints",
        "country": "Alfdorf, Germany",
        "profile": "good",
        "description": "Supplies Porsche Taycan Turbo GT, Audi R8. ACR8 active reversible pretensioner, 2,190g, 0.6 PPM, only 195 km from Molsheim.",
    },
    {
        "name": "Sparco S.p.A.",
        "filename_base": "05_Sparco_SpA_Italy_Proposal",
        "category": "Motorsport & Hypercar Restraint",
        "country": "Volpiano (Turin), Italy",
        "profile": "good_with_gaps",
        "description": "Supplies Lamborghini Revuelto & Huracán STO. Ultra-light 1,680g carbon construction, €610k NRE, but VDA 6.3 is 91% (Grade B+) and 2.3 PPM.",
    },
    {
        "name": "OMP Racing S.p.A.",
        "filename_base": "06_OMP_Racing_Italy_Proposal",
        "category": "Motorsport & Hypercar Restraint",
        "country": "Ronco Scrivia (Genoa), Italy",
        "profile": "risky",
        "description": "Formula 1 supplier to Mercedes-AMG & Aston Martin. Featherweight 1,590g, €540k NRE, but lacks FMVSS/GB road homologation and IATF 16949 is in progress.",
    },
    {
        "name": "Joyson Safety Systems (JSS)",
        "filename_base": "07_Joyson_Safety_Systems_Proposal",
        "category": "Global Tier-1 Safety Systems",
        "country": "Aschaffenburg, Germany",
        "profile": "mixed",
        "description": "Legacy Bugatti Chiron supplier. Complete worldwide road homologation, 2,380g mass, €1.18M NRE, but lacks FIA 8853 in-house and Takata heritage scrutiny.",
    },
    {
        "name": "Tokai Rika Co., Ltd.",
        "filename_base": "08_Tokai_Rika_Japan_Proposal",
        "category": "Precision Luxury Restraints",
        "country": "Oguchi, Aichi, Japan",
        "profile": "good_with_gaps",
        "description": "Lexus LFA & Century supplier. Outstanding 0.1 PPM, VDA 98%, horological acoustics, but 7.5-week lead time and Japan logistics.",
    },
    {
        "name": "Willans Harness Manufacture Ltd.",
        "filename_base": "09_Willans_UK_Proposal",
        "category": "Bespoke Hypercar Restraints",
        "country": "Silverstone, United Kingdom",
        "profile": "risky",
        "description": "McLaren F1 & Gordon Murray T.50 heritage. 1,640g, lowest NRE €490k, but lacks FMVSS pyrotechnic certification and IATF 16949.",
    },
    {
        "name": "Holmbergs Safety System AB",
        "filename_base": "10_Holmbergs_Safety_Sweden_Proposal",
        "category": "Scandinavian Precision Restraints",
        "country": "Halmstad, Sweden",
        "profile": "good",
        "description": "Koenigsegg supplier. Robust Swedish engineering, 1,980g, 1.5 PPM, full road homologation, €760k NRE, 5.5-week delivery.",
    },
]

# 6-Pillar Scoring Rubric Reference
SCORING_RUBRIC = {
    "1. Crash Physics & Global Homologation": {
        "weight": 0.25,
        "veteran": "Chief Occupant Safety & Pyrotechnics Engineer (28 yrs exp)",
        "sub_criteria": {
            "Global Road Homologation (UN/ECE R16, FMVSS 209/210, GB, TRIAS)": 35,
            "Dual-Stage Pyrotechnic Pretensioner (<= 6.5 ms Time-to-Fire)": 25,
            "Adaptive Digressive Torsion Bar (4.5 kN to 2.8 kN Thoracic Relief)": 20,
            "Pre-Crash Dynamic Integration (>= 0.8G Panic Braking Motorized Spool)": 20,
        },
    },
    "2. Hypercar Lightweighting & Materials": {
        "weight": 0.20,
        "veteran": "Lead Hypercar Mass & Exotic Metallurgy Specialist (25 yrs exp)",
        "sub_criteria": {
            "Installed System Mass (<= 2,400g / pair; target <= 1,950g)": 40,
            "Exotic Hardware Metallurgy (Ti-6Al-4V Titanium, Forged Carbon, 7075-T6)": 35,
            "Ultra-High-Tenacity Webbing (Dyneema/Vectran, >= 26.5 kN break load)": 25,
        },
    },
    "3. Bespoke Craftsmanship & Acoustics/NVH": {
        "weight": 0.20,
        "veteran": "Master Atelier Trim, Tactile & Acoustic Director (26 yrs exp)",
        "sub_criteria": {
            "Sur Mesure Color Atelier (50+ Pantone dyes, contrast stitching, MOQ 1)": 30,
            "UV & Abrasion Durability (Delta-E < 1.2 after 1,500h Xenon-Arc)": 25,
            "Horological Latch Acoustics (52-58 dB crisp mechanical click, no rattle)": 25,
            "NVH & Cabin Acoustic Isolation (0 dB rattle 10-1500 Hz sweep)": 20,
        },
    },
    "4. Manufacturing Quality & Zero-Defect Record": {
        "weight": 0.15,
        "veteran": "VP of Automotive Quality & VDA 6.3 Auditor (30 yrs exp)",
        "sub_criteria": {
            "Certifications & Audit Grade (IATF 16949, ISO 14001, VDA 6.3 >= 92% Grade A)": 40,
            "Historical Defect Rate (<= 2 PPM field/line, 0 PPM pyrotechnics)": 30,
            "100% CT X-Ray Inspection & 30-Year QR Digital Traceability": 30,
        },
    },
    "5. Commercials & Low-Volume Economics": {
        "weight": 0.10,
        "veteran": "Director of Low-Volume Supercar Procurement (25 yrs exp)",
        "sub_criteria": {
            "Non-Recurring Engineering (<= EUR 850,000 for 250-car run)": 50,
            "Unit BOM Cost (<= EUR 2,800 per 2-seat vehicle shipset)": 35,
            "Sur Mesure Single-Car Surcharge (<= EUR 450 per bespoke car)": 15,
        },
    },
    "6. Supply Chain & Molsheim Delivery": {
        "weight": 0.10,
        "veteran": "Global Supply Chain & Molsheim Logistics Lead (27 yrs exp)",
        "sub_criteria": {
            "Delivery Model & Lead Time (JIS flight-case delivery, <= 6 weeks lead)": 40,
            "Geographic Proximity & Supply Chain Sovereignty (EU/US/JP tier sourcing)": 30,
            "Warranty & Bugatti Classic Support (15-yr warranty, 35-yr spare parts)": 30,
        },
    },
}

