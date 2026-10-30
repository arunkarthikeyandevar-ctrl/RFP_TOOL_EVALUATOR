"""
generate_vendor_files.py
Generates 10 separate, 100% original and realistic RFP Proposal files (.TXT and .PDF)
from real-world supercar and hypercar restraint system suppliers so you can manually
upload them into the Streamlit app one by one (or all together).
"""

import os
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

VENDOR_PROPOSALS_DATA = [
    {
        "filename_base": "01_Sabelt_SpA_Italy_Proposal",
        "vendor_name": "Sabelt S.p.A.",
        "country": "Turin (Moncalieri), Italy",
        "oem_pedigree": "Official OEM Restraint & Seat Supplier for Ferrari Daytona SP3, Ferrari SF90 XX, McLaren 750S, and Alpine A110 R.",
        "content": """RFP RESPONSE: BUGATTI-W16-V16-HYPER-RESTRAINT-2026
SUBMITTED BY: Sabelt S.p.A. (Viaapperlo 12, Moncalieri, Turin, Italy)
OEM SUPERCAR PEDIGREE: Primary restraint supplier to Ferrari, McLaren, Maserati MC20, and Pagani track programs.

1. CRASH PHYSICS, PYROTECHNICS & GLOBAL HOMOLOGATION
- Homologation Coverage: Full dual-homologation under UN/ECE R16, FMVSS 209/210, GB 14166, and FIA 8853-2016 (for optional 6-point Sur Mesure Track Harness).
- Pyrotechnic Retractor & Buckle: Co-developed with European pyrotechnic partner; dual-stage gas generator fires in 5.8 milliseconds upon CAN-FD crash trigger.
- Load Limiter Architecture: CNC-machined progressive torsion bar switching smoothly from 4.4 kN peak arrest load down to 2.7 kN thoracic relief threshold.
- Pre-Crash Integration: Integrated reversible brushless DC electric motor (180 N tensioning) paired with pyrotechnic backup for 0.8G panic braking pre-tensioning.

2. HYPERCAR LIGHTWEIGHTING & EXOTIC MATERIALS
- Total Installed Vehicle Mass (2 Seats Complete): 1,790 grams per car (895 grams per seat).
- Hardware Metallurgy: Grade 5 Ti-6Al-4V Titanium D-rings and anchor plates; forged carbon-fiber retractor casing; billet 7075-T6 aluminum buckle chassis.
- Webbing Spec: Proprietary Sabelt Ultralight Hybrid Polyester-Dyneema weave, 1.02 mm thickness, 28.4 kN minimum breaking load, 4.9% elongation at 11 kN.

3. BUGATTI BESPOKE CRAFTSMANSHIP, LUXURY & ACOUSTICS/NVH
- Bespoke Customization: Dedicated Turin Atelier dye-house supports unlimited Pantone matching (MOQ: 1 vehicle) plus woven Tricolore or Bugatti EB monograms.
- UV & Abrasion Resistance: Xenon-Arc 1,500-hour tested at Delta-E = 0.85. Zero edge fraying at 60,000 cycles.
- Tactile & Acoustic Engineering: Hand-stitched Poltrona Frau / Bugatti specification full-grain leather buckle sleeve with CNC-milled titanium release button. Buckle latch click tuned via internal neodymium magnetic damper to 54.5 dB horological acoustic signature.
- NVH Performance: Felt-lined carbon retractor spool eliminates harmonic rattle across 10-1,600 Hz (0 dB buzz). Fully compatible with motorized B-pillar belt presenter.

4. MANUFACTURING QUALITY & ZERO-DEFECT TRACEABILITY
- Certifications: IATF 16949:2016, ISO 9001, ISO 14001, VDA 6.3 Audit Score 95% (Rating A).
- Historical Defect Rate: 1.1 PPM across Ferrari and McLaren OEM programs.
- Inspection Protocol: 100% 3D micro-CT X-ray scan of every pyrotechnic squib and locking pawl; automated vision camera checks every stitch; 35-year QR digital archive.

5. COMMERCIAL ECONOMICS & LOW-VOLUME NRE STRUCTURE
- Upfront NRE & Homologation Sled Testing: EUR 680,000 total (leveraging existing modular hypercar crash sled fixtures).
- Unit BOM Price (Per 2-Seat Vehicle Shipset): EUR 2,650.
- Bespoke Sur Mesure Color Surcharge: EUR 380 per custom vehicle order (MOQ 1 car).

6. SUPPLY CHAIN RESILIENCE & MOLSHEIM ATELIER LOGISTICS
- Delivery to Molsheim: 4.5-week lead time from spec freeze; direct road transport from Turin to Molsheim via climate-controlled velvet flight cases (420 km alpine transit).
- Sub-Tier Sourcing: 100% Italian and German titanium and webbing mills. 15-year structural warranty and 40-year Bugatti Classic spare parts commitment."""
    },
    {
        "filename_base": "02_Schroth_Safety_Germany_Proposal",
        "vendor_name": "Schroth Safety Products GmbH",
        "country": "Arnsberg, Germany",
        "oem_pedigree": "Official OEM Harness & Restraint Supplier for Porsche 911 GT3 RS, Porsche 918 Spyder, Bugatti Bolide & Pur Sport Track Packages, and Mercedes-AMG ONE.",
        "content": """RFP RESPONSE: BUGATTI-W16-V16-HYPER-RESTRAINT-2026
SUBMITTED BY: Schroth Safety Products GmbH (Im Ohl 14, Arnsberg, Germany)
OEM SUPERCAR PEDIGREE: Supplier to Porsche GT RS division, Mercedes-AMG ONE, McLaren Senna, and Bugatti Bolide FIA systems.

1. CRASH PHYSICS, PYROTECHNICS & GLOBAL HOMOLOGATION
- Homologation Coverage: UN/ECE R16, FMVSS 209/210, GB 14166, TRIAS, and industry-gold-standard FIA 8853-2016 homologation. Includes patented Schroth ASM (Anti-Submarining) technology integrated into the 3-point and 6-point hybrid belt geometry.
- Pyrotechnic Retractor & Buckle: Dual-stage pyrotechnic rotary actuator firing in 5.2 milliseconds (fastest in motorsport/hypercar segment).
- Load Limiter Architecture: Patented dual-stage RLL (Rotary Load Limiter) transitioning from 4.5 kN to 2.8 kN with surgical repeatability (+/- 2% variance).
- Pre-Crash Integration: CAN-FD reversible motorized pre-crash tensioner providing 210 N of instantaneous slack removal under 0.8G braking.

2. HYPERCAR LIGHTWEIGHTING & EXOTIC MATERIALS
- Total Installed Vehicle Mass (2 Seats Complete): 1,720 grams per car (860 grams per seat).
- Hardware Metallurgy: Aerospace Ti-6Al-4V titanium rotary cam/buckle mechanisms and carbon-composite retractor frames borrowed from aviation defense programs.
- Webbing Spec: Schroth Profi-Hyper 1.00 mm ultra-thin hybrid polyester/liquid-crystal polymer webbing, 29.8 kN breaking strength, 4.2% elongation at 11 kN.

3. BUGATTI BESPOKE CRAFTSMANSHIP, LUXURY & ACOUSTICS/NVH
- Bespoke Customization: Supports 35 bespoke Pantone colors; custom contrast stitching available, though ultra-complex multi-tone gradient weaves require a 3-car minimum dye batch.
- UV & Abrasion Resistance: Delta-E = 1.05 after 1,500 hours Xenon-Arc testing. 75,000 cycle abrasion endurance.
- Tactile & Acoustic Engineering: Billet CNC-milled titanium buckle with Alcantara and Nappa leather trim inserts. Buckle click measures 56.0 dB--crisp, mechanical, aviation-inspired lock.
- NVH Performance: 0 dB rattle up to 1,500 Hz; precision spring-loaded tongue park stops B-pillar contact. Compatible with motorized presenters.

4. MANUFACTURING QUALITY & ZERO-DEFECT TRACEABILITY
- Certifications: IATF 16949:2016, EN 9100 (Aerospace Quality Management), ISO 14001, VDA 6.3 Audit Score 96% (Rating A).
- Historical Defect Rate: 0.4 PPM across aviation and hypercar OEM lines.
- Inspection Protocol: 100% aerospace-grade X-ray tomography on all pyrotechnic and locking assemblies; individual serial laser engraving with 40-year archive.

5. COMMERCIAL ECONOMICS & LOW-VOLUME NRE STRUCTURE
- Upfront NRE & Homologation Sled Testing: EUR 740,000 total.
- Unit BOM Price (Per 2-Seat Vehicle Shipset): EUR 2,780.
- Bespoke Sur Mesure Color Surcharge: EUR 520 per custom color setup (slightly above EUR 450 target for rare metallic shades).

6. SUPPLY CHAIN RESILIENCE & MOLSHEIM ATELIER LOGISTICS
- Delivery to Molsheim: 4.0-week lead time; direct 380 km logistics corridor from Arnsberg, Germany to Molsheim, France in sealed flight cases.
- Sub-Tier Sourcing: 100% German and Austrian sub-tier metallurgy and pyrotechnics. 15-year warranty and 40-year classic spares guarantee."""
    },
    {
        "filename_base": "03_Autoliv_AB_Sweden_Proposal",
        "vendor_name": "Autoliv AB",
        "country": "Stockholm / Vargarda, Sweden",
        "oem_pedigree": "World's Largest Tier-1 Automotive Safety Supplier; supplies Porsche, Mercedes-Maybach, Bentley, Aston Martin, and Koenigsegg pyrotechnic modules.",
        "content": """RFP RESPONSE: BUGATTI-W16-V16-HYPER-RESTRAINT-2026
SUBMITTED BY: Autoliv AB (Wallentinsvagen 22, Vargarda / Stockholm, Sweden)
OEM SUPERCAR PEDIGREE: Global Tier-1 safety leader supplying Bentley Continental GT Speed, Porsche 911 Turbo S, and Mercedes-Maybach.

1. CRASH PHYSICS, PYROTECHNICS & GLOBAL HOMOLOGATION
- Homologation Coverage: Unmatched global certification library covering UN/ECE R16, FMVSS 209/210, CMVSS, GB 14166, TRIAS, KMVSS, and ADR. Note: Standard proposal covers 3-point street homologation; FIA 8853 6-point track harness requires an external motorsport partner.
- Pyrotechnic Retractor & Buckle: Proprietary dual-stage micro-gas generator with 5.0 milliseconds firing time and active crash-pulse shaping.
- Load Limiter Architecture: Electronically switchable multi-level torsion bar (4.5 kN / 2.6 kN) that adapts automatically to occupant mass via seat weight sensors.
- Pre-Crash Integration: Active Seatbelt Retractor (ASR) seamlessly integrated with Volkswagen Group / Rimac / Bugatti CAN-FD safety architecture.

2. HYPERCAR LIGHTWEIGHTING & EXOTIC MATERIALS
- Total Installed Vehicle Mass (2 Seats Complete): 2,480 grams per car (1,240 grams per seat) -- slightly exceeds the 2,400g target due to heavy-duty dual-motor electric pre-tensioner gearbox and high-strength steel retractor frame.
- Hardware Metallurgy: High-strength micro-alloyed boron steel retractor frame with forged aluminum D-rings (Titanium upgrade requires extra tooling).
- Webbing Spec: 1.18 mm high-tenacity polyester webbing, 27.0 kN breaking strength, 5.8% elongation.

3. BUGATTI BESPOKE CRAFTSMANSHIP, LUXURY & ACOUSTICS/NVH
- Bespoke Customization: Supports 25 standard luxury colors; custom single-car Sur Mesure Pantone dyeing requires outsourcing to boutique textile partners with longer lead times.
- UV & Abrasion Resistance: Delta-E = 0.90 after 1,500 hours Xenon-Arc. 80,000 cycle abrasion durability.
- Tactile & Acoustic Engineering: Leather-wrapped buckle housing over engineered polymer core (contains internal structural polymer shell). Buckle click is 53.0 dB.
- NVH Performance: Benchmark mass-luxury silent retractor (0 dB rattle) with integrated motorized presenter gear drive.

4. MANUFACTURING QUALITY & ZERO-DEFECT TRACEABILITY
- Certifications: IATF 16949:2016, ISO 14001, VDA 6.3 Audit Score 97% (Rating A).
- Historical Defect Rate: 0.3 PPM across luxury OEM lines.
- Inspection Protocol: 100% automated inline X-ray inspection, acoustic end-of-line testing, and cloud digital twin archiving for 30 years.

5. COMMERCIAL ECONOMICS & LOW-VOLUME NRE STRUCTURE
- Upfront NRE & Homologation Sled Testing: EUR 1,650,000 total (high corporate Tier-1 engineering overhead for a 250-unit production run).
- Unit BOM Price (Per 2-Seat Vehicle Shipset): EUR 2,150.
- Bespoke Sur Mesure Color Surcharge: EUR 1,200 per single-car custom dye lot due to large industrial dye vats.

6. SUPPLY CHAIN RESILIENCE & MOLSHEIM ATELIER LOGISTICS
- Delivery to Molsheim: 8.5-week lead time for bespoke single-vehicle colors (5 weeks for standard black/tan/blue).
- Sub-Tier Sourcing: 100% European supply chain with massive financial stability. 15-year warranty and 35-year spares support."""
    },
    {
        "filename_base": "04_ZF_Lifetec_Germany_Proposal",
        "vendor_name": "ZF Lifetec (Passive Safety Systems)",
        "country": "Alfdorf, Germany",
        "oem_pedigree": "Tier-1 Passive Safety Leader supplying Porsche Taycan Turbo GT, Audi R8, Lamborghini Revuelto active retractors, and Aston Martin Valour.",
        "content": """RFP RESPONSE: BUGATTI-W16-V16-HYPER-RESTRAINT-2026
SUBMITTED BY: ZF Lifetec GmbH (voormals ZF Passive Safety Systems, Alfdorf, Germany)
OEM SUPERCAR PEDIGREE: Supplier of ACR8 Active Control Retractors and luxury illuminated/heated buckles for Lamborghini, Porsche, and BMW M.

1. CRASH PHYSICS, PYROTECHNICS & GLOBAL HOMOLOGATION
- Homologation Coverage: Full UN/ECE R16, FMVSS 209/210, GB 14166, and TRIAS road certification. (FIA 8853 track harness offered via modular drop-in kit).
- Pyrotechnic Retractor & Buckle: Next-gen ACR8.S combines reversible electro-mechanical tensioning with a 5.4 millisecond dual-stage pyrotechnic squib.
- Load Limiter Architecture: Adaptive 3-stage torsion bar (4.5 kN -> 3.4 kN -> 2.7 kN) with high-speed webbing payout damping.
- Pre-Crash Integration: Industry-leading ACR8 active haptic pulsing (warns driver via high-frequency belt vibrations) and 220 N pre-crash tensioning during 0.8G braking or drift/oversteer intervention.

2. HYPERCAR LIGHTWEIGHTING & EXOTIC MATERIALS
- Total Installed Vehicle Mass (2 Seats Complete): 2,190 grams per car (1,095 grams per seat).
- Hardware Metallurgy: Magnesium-aluminum die-cast retractor housing paired with CNC Ti-6Al-4V titanium load anchors.
- Webbing Spec: 1.10 mm multi-filament high-tenacity polyester/aramid edge webbing, 27.6 kN breaking strength, 5.1% elongation.

3. BUGATTI BESPOKE CRAFTSMANSHIP, LUXURY & ACOUSTICS/NVH
- Bespoke Customization: Dedicated Small-Series Luxury Cell in Alfdorf supports 50+ Pantone colors (MOQ 1 vehicle) plus optional fiber-optic ambient edge illumination.
- UV & Abrasion Resistance: Delta-E = 0.95 after 1,500 hours Xenon-Arc. 65,000 cycle abrasion rating.
- Tactile & Acoustic Engineering: Billet aluminum buckle housing wrapped in Molsheim-matched leather, featuring optional heated buckle tongue (warms to 36C in winter). Buckle click engineered to 55.2 dB.
- NVH Performance: Zero rattle (0 dB across 10-1,500 Hz) with magnetic tongue damper and active motorized presenter integration.

4. MANUFACTURING QUALITY & ZERO-DEFECT TRACEABILITY
- Certifications: IATF 16949:2016, ISO 14001, VDA 6.3 Audit Score 96% (Rating A).
- Historical Defect Rate: 0.6 PPM.
- Inspection Protocol: 100% 3D CT X-ray scan of pyrotechnics and gears, automated laser serializing, 35-year digital twin retention.

5. COMMERCIAL ECONOMICS & LOW-VOLUME NRE STRUCTURE
- Upfront NRE & Homologation Sled Testing: EUR 920,000 total (slightly above the EUR 850,000 target due to ACR8 active software calibration).
- Unit BOM Price (Per 2-Seat Vehicle Shipset): EUR 2,720.
- Bespoke Sur Mesure Color Surcharge: EUR 440 per custom color vehicle.

6. SUPPLY CHAIN RESILIENCE & MOLSHEIM ATELIER LOGISTICS
- Delivery to Molsheim: 5.0-week lead time; Alfdorf facility is only 195 km across the Rhine from Molsheim, enabling rapid 3-hour direct courier delivery in custom flight cases.
- Sub-Tier Sourcing: 100% German/European sub-tiers. 15-year structural warranty and 35-year classic spares program."""
    },
    {
        "filename_base": "05_Sparco_SpA_Italy_Proposal",
        "vendor_name": "Sparco S.p.A.",
        "country": "Volpiano (Turin), Italy",
        "oem_pedigree": "Official OEM Carbon & Restraint Supplier for Lamborghini Revuelto, Lamborghini Huracan STO, Koenigsegg Jesko, and Ford GT.",
        "content": """RFP RESPONSE: BUGATTI-W16-V16-HYPER-RESTRAINT-2026
SUBMITTED BY: Sparco S.p.A. (Via Leini 524, Volpiano, Turin, Italy)
OEM SUPERCAR PEDIGREE: OEM carbon monocoque and restraint supplier to Lamborghini, Koenigsegg, Lotus Evija, and Aston Martin Valkyrie.

1. CRASH PHYSICS, PYROTECHNICS & GLOBAL HOMOLOGATION
- Homologation Coverage: UN/ECE R16, FMVSS 209/210, and FIA 8853-2016 certified.
- Pyrotechnic Retractor & Buckle: Single-stage pyrotechnic retractor with auxiliary buckle pretensioner (sourced via external Tier-1 pyrotechnic partner); firing time is 6.4 milliseconds.
- Load Limiter Architecture: Dual-stage mechanical torsion bar rated at 4.5 kN / 2.9 kN.
- Pre-Crash Integration: Supports standard 12V reversible electric motor pre-tensioning (150 N pull force) over CAN bus.

2. HYPERCAR LIGHTWEIGHTING & EXOTIC MATERIALS
- Total Installed Vehicle Mass (2 Seats Complete): 1,680 grams per car (840 grams per seat) -- ultra-lightweight autoclave carbon construction.
- Hardware Metallurgy: Autoclave pre-preg carbon-fiber retractor shells and buckle covers with CNC Grade 5 Titanium (Ti-6Al-4V) tongues and D-rings.
- Webbing Spec: Sparco Superleggera 0.98 mm Dyneema-Polyester hybrid ribbon, 28.9 kN breaking strength, 4.5% elongation.

3. BUGATTI BESPOKE CRAFTSMANSHIP, LUXURY & ACOUSTICS/NVH
- Bespoke Customization: Full Italian bespoke leather, Alcantara, and exposed tinted carbon-fiber weave matching Bugatti bodywork (50+ Pantone colors, MOQ 1 car).
- UV & Abrasion Resistance: Delta-E = 1.12 after 1,500 hours Xenon-Arc. 52,000 cycle abrasion endurance.
- Tactile & Acoustic Engineering: Exposed forged carbon and billet titanium buckle. Buckle latch click is slightly louder and more motorsport-raw at 59.5 dB (exceeds the 58 dB upper horological target).
- NVH Performance: Minor mechanical pawl clicking audible during rapid belt extraction; 0 dB rattle once latched.

4. MANUFACTURING QUALITY & ZERO-DEFECT TRACEABILITY
- Certifications: IATF 16949:2016, ISO 9001, ISO 14001, VDA 6.3 Audit Score 91% (Rating B+, just shy of 92% Rating A threshold).
- Historical Defect Rate: 2.3 PPM (slightly above the 2.0 PPM ceiling due to manual hand-laid carbon trim cosmetic variations).
- Inspection Protocol: 100% ultrasonic and X-ray inspection of structural hardware; 30-year QR traceability.

5. COMMERCIAL ECONOMICS & LOW-VOLUME NRE STRUCTURE
- Upfront NRE & Homologation Sled Testing: EUR 610,000 total.
- Unit BOM Price (Per 2-Seat Vehicle Shipset): EUR 2,590.
- Bespoke Sur Mesure Color Surcharge: EUR 350 per vehicle.

6. SUPPLY CHAIN RESILIENCE & MOLSHEIM ATELIER LOGISTICS
- Delivery to Molsheim: 5.5-week lead time from Turin to Molsheim in carbon-shell presentation cases.
- Sub-Tier Sourcing: European titanium and Italian textiles; pyrotechnic gas generators single-sourced from external partner. 15-year warranty and 35-year spares."""
    },
    {
        "filename_base": "06_OMP_Racing_Italy_Proposal",
        "vendor_name": "OMP Racing S.p.A.",
        "country": "Ronco Scrivia (Genoa), Italy",
        "oem_pedigree": "Official Supplier to Formula 1 (Mercedes-AMG F1, Aston Martin F1), Dallara Stradale, Pagani Huayra R, and Kimera EVO37.",
        "content": """RFP RESPONSE: BUGATTI-W16-V16-HYPER-RESTRAINT-2026
SUBMITTED BY: OMP Racing S.p.A. (Via Bazzano 5, Ronco Scrivia, Genoa, Italy)
OEM SUPERCAR PEDIGREE: World leader in FIA Formula 1 and Le Mans hypercar harnesses (Dallara, Pagani track cars, Maserati GT2).

1. CRASH PHYSICS, PYROTECHNICS & GLOBAL HOMOLOGATION
- Homologation Coverage: FIA 8853-2016 and UN/ECE R16 certified. WARNING: FMVSS 209/210 (USA) and GB 14166 (China) road homologation for pyrotechnic 3-point retractors is NOT currently held in-house and requires an estimated 9-month external certification program.
- Pyrotechnic Retractor & Buckle: Third-party integrated pyrotechnic module firing in 6.8 milliseconds (slightly slower than the <= 6.5 ms requirement).
- Load Limiter Architecture: Single-stage 4.2 kN torsion bar with stitched energy-absorbing webbing tear-loops.
- Pre-Crash Integration: Basic CAN trigger support; lacks native reversible motorized ADAS pre-tensioner experience.

2. HYPERCAR LIGHTWEIGHTING & EXOTIC MATERIALS
- Total Installed Vehicle Mass (2 Seats Complete): 1,590 grams per car (795 grams per seat) -- lightest proposal in the field using F1 Dyneema technology.
- Hardware Metallurgy: 5-axis CNC-machined Ti-6Al-4V titanium and Ergal 7075 aluminum hardware throughout.
- Webbing Spec: OMP Dyneema-Pro 0.95 mm ultra-light webbing, 31.0 kN breaking strength, 3.8% elongation.

3. BUGATTI BESPOKE CRAFTSMANSHIP, LUXURY & ACOUSTICS/NVH
- Bespoke Customization: 50+ Pantone colors with custom jacquard embroidery (MOQ 1 car).
- UV & Abrasion Resistance: Dyneema blend exhibits slightly higher UV sensitivity (Delta-E = 1.45 after 1,500 hours Xenon-Arc, exceeding the < 1.2 limit unless treated with darker pigments).
- Tactile & Acoustic Engineering: Billet anodized aluminum and Alcantara buckle; click sound is 61.0 dB (loud racing rotary/latch click).
- NVH Performance: Motorsport-grade retractor springs produce mild mechanical wind-up sound; requires extra acoustic foam isolation in Bugatti B-pillar.

4. MANUFACTURING QUALITY & ZERO-DEFECT TRACEABILITY
- Certifications: ISO 9001, FIA 8853 Quality Standard. Note: Full IATF 16949:2016 certification is currently in progress for their road-car division (VDA 6.3 score: 88%).
- Historical Defect Rate: 3.1 PPM.
- Inspection Protocol: 100% tensile proof-load testing and optical verification; X-ray CT outsourced for pyrotechnics.

5. COMMERCIAL ECONOMICS & LOW-VOLUME NRE STRUCTURE
- Upfront NRE & Homologation Sled Testing: EUR 540,000 total.
- Unit BOM Price (Per 2-Seat Vehicle Shipset): EUR 2,390.
- Bespoke Sur Mesure Color Surcharge: EUR 290 per car.

6. SUPPLY CHAIN RESILIENCE & MOLSHEIM ATELIER LOGISTICS
- Delivery to Molsheim: 4.5-week lead time from Genoa, Italy to Molsheim.
- Sub-Tier Sourcing: Italian hardware, outsourced pyrotechnic initiators. 10-year standard warranty (extendable to 15 years at extra cost)."""
    },
    {
        "filename_base": "07_Joyson_Safety_Systems_Proposal",
        "vendor_name": "Joyson Safety Systems (JSS)",
        "country": "Aschaffenburg, Germany / Auburn Hills, USA",
        "oem_pedigree": "Global Tier-1 Supplier for Bugatti Chiron (legacy airbag/steering wheel modules), Audi Sport, Bentley, Rolls-Royce, and Corvette ZR1.",
        "content": """RFP RESPONSE: BUGATTI-W16-V16-HYPER-RESTRAINT-2026
SUBMITTED BY: Joyson Safety Systems GmbH (Bahnweg 1, Aschaffenburg, Germany)
OEM SUPERCAR PEDIGREE: Existing supplier to Volkswagen Group ultra-luxury brands (Bentley, Porsche, Lamborghini) and historical Bugatti safety component partner.

1. CRASH PHYSICS, PYROTECHNICS & GLOBAL HOMOLOGATION
- Homologation Coverage: Complete worldwide certification: UN/ECE R16, FMVSS 209/210, CMVSS, GB 14166, and TRIAS. Optional inflatable belt (Beltbag) technology available. Does not manufacture FIA 8853 6-point racing harnesses in-house.
- Pyrotechnic Retractor & Buckle: Dual-stage pyrotechnic retractor + buckle pretensioner firing in 5.6 milliseconds.
- Load Limiter Architecture: Stepless adaptive torsion bar (4.5 kN to 2.7 kN) with pyrotechnic switchover valve.
- Pre-Crash Integration: Full native VW/Bugatti CAN-FD & PSI5 reversible motorized pre-tensioning (195 N).

2. HYPERCAR LIGHTWEIGHTING & EXOTIC MATERIALS
- Total Installed Vehicle Mass (2 Seats Complete): 2,380 grams per car (1,190 grams per seat) -- just inside the 2,400g maximum limit.
- Hardware Metallurgy: High-strength alloy steel spool with CNC aluminum housing and titanium anchor plates.
- Webbing Spec: 1.14 mm luxury soft-touch high-tenacity polyester webbing, 26.8 kN breaking strength, 5.7% elongation.

3. BUGATTI BESPOKE CRAFTSMANSHIP, LUXURY & ACOUSTICS/NVH
- Bespoke Customization: Aschaffenburg Luxury Atelier supports 50+ Pantone webbing colors and hand-sewn leather buckle covers matched to Bugatti hides.
- UV & Abrasion Resistance: Delta-E = 0.88 after 1,500 hours Xenon-Arc. 70,000 cycle abrasion endurance.
- Tactile & Acoustic Engineering: Zero visible plastic; full leather and brushed palladium-plated aluminum buckle. Latch click is 54.0 dB.
- NVH Performance: Whisper-quiet luxury retractor (0 dB rattle) engineered for Rolls-Royce and Bentley cabin silence.

4. MANUFACTURING QUALITY & ZERO-DEFECT TRACEABILITY
- Certifications: IATF 16949:2016, ISO 14001, VDA 6.3 Audit Score 93% (Rating A).
- Historical Defect Rate: 1.4 PPM on current European luxury lines.
- Inspection Protocol: 100% automated 3D X-ray CT inspection of pyrotechnic assemblies and 30-year digital traceability.

5. COMMERCIAL ECONOMICS & LOW-VOLUME NRE STRUCTURE
- Upfront NRE & Homologation Sled Testing: EUR 1,180,000 total (exceeds EUR 850k target due to corporate Tier-1 validation overhead).
- Unit BOM Price (Per 2-Seat Vehicle Shipset): EUR 2,490.
- Bespoke Sur Mesure Color Surcharge: EUR 650 per vehicle (above EUR 450 target).

6. SUPPLY CHAIN RESILIENCE & MOLSHEIM ATELIER LOGISTICS
- Delivery to Molsheim: 6.0-week lead time from Aschaffenburg, Germany (230 km from Molsheim) in JIS sequenced cases.
- Sub-Tier Sourcing: Dual-sourced European and North American sub-tiers. 15-year warranty and 35-year spares guarantee."""
    },
    {
        "filename_base": "08_Tokai_Rika_Japan_Proposal",
        "vendor_name": "Tokai Rika Co., Ltd.",
        "country": "Oguchi, Aichi, Japan",
        "oem_pedigree": "Official OEM Restraint Supplier for Lexus LFA, Toyota GR GT3 / Century, Nissan GT-R Nismo, and Honda NSX Type S.",
        "content": """RFP RESPONSE: BUGATTI-W16-V16-HYPER-RESTRAINT-2026
SUBMITTED BY: Tokai Rika Co., Ltd. (3-260 Toyota, Oguchi-cho, Niwa-gun, Aichi, Japan)
OEM SUPERCAR PEDIGREE: Creators of the legendary Lexus LFA motorized carbon/airbag seatbelt system and Japanese ultra-luxury Century restraints.

1. CRASH PHYSICS, PYROTECHNICS & GLOBAL HOMOLOGATION
- Homologation Coverage: UN/ECE R16, FMVSS 209/210, TRIAS (Japan), and GB 14166. (Does not produce FIA 8853 6-point track harnesses).
- Pyrotechnic Retractor & Buckle: Ultra-reliable Japanese dual-stage gas generator firing in 5.5 milliseconds.
- Load Limiter Architecture: Precision-machined coaxial dual-stage torsion bar (4.5 kN / 2.8 kN) with zero lot-to-lot variance.
- Pre-Crash Integration: High-torque brushless Japanese motor for silky-smooth pre-crash tensioning and motorized belt retraction assist.

2. HYPERCAR LIGHTWEIGHTING & EXOTIC MATERIALS
- Total Installed Vehicle Mass (2 Seats Complete): 2,120 grams per car (1,060 grams per seat).
- Hardware Metallurgy: Forged titanium anchor plates and ultra-thin magnesium-alloy retractor housings.
- Webbing Spec: Japanese Takumi-weave 1.08 mm high-density silk-sheen polyester webbing, 27.9 kN breaking strength, 5.0% elongation.

3. BUGATTI BESPOKE CRAFTSMANSHIP, LUXURY & ACOUSTICS/NVH
- Bespoke Customization: Supports 50+ bespoke colors dyed using traditional Japanese fade-resistant reactive dyes (MOQ 1 car).
- UV & Abrasion Resistance: Industry-best Delta-E = 0.65 after 1,500 hours Xenon-Arc testing. 90,000 cycle abrasion endurance.
- Tactile & Acoustic Engineering: Takumi master craftsmen tune every buckle latch by hand; produces a Grand Seiko-like 53.8 dB horological click. Zero visible plastic.
- NVH Performance: Absolute 0 dB rattle; world benchmark in motorized seatbelt presenter smoothness.

4. MANUFACTURING QUALITY & ZERO-DEFECT TRACEABILITY
- Certifications: IATF 16949:2016, ISO 14001, VDA 6.3 Equivalent Score 98% (Rating A+).
- Historical Defect Rate: 0.1 PPM (virtually zero defects over 15 years of Lexus LFA and Century production).
- Inspection Protocol: 100% micro-focus X-ray CT scan, acoustic spectrum verification of every buckle click, 40-year digital ledger.

5. COMMERCIAL ECONOMICS & LOW-VOLUME NRE STRUCTURE
- Upfront NRE & Homologation Sled Testing: EUR 1,050,000 total (above EUR 850k target).
- Unit BOM Price (Per 2-Seat Vehicle Shipset): EUR 2,950 (slightly above EUR 2,800 target due to air-freight logistics and Japanese Takumi hand-finishing).
- Bespoke Sur Mesure Color Surcharge: EUR 420 per car.

6. SUPPLY CHAIN RESILIENCE & MOLSHEIM ATELIER LOGISTICS
- Delivery to Molsheim: 7.5-week lead time (exceeds the <= 6-week requirement due to air/customs transit from Nagoya, Japan to Strasbourg/Molsheim, France, though buffer stock in Valenciennes is proposed).
- Sub-Tier Sourcing: 100% Japanese domestic titanium and pyrotechnics. 15-year warranty and 40-year classic spares guarantee."""
    },
    {
        "filename_base": "09_Willans_UK_Proposal",
        "vendor_name": "Willans Harness Manufacture Ltd.",
        "country": "Silverstone / Towcester, United Kingdom",
        "oem_pedigree": "Bespoke Hypercar Harness Supplier for McLaren F1, Gordon Murray Automotive T.50 & T.33, Lanzante Porsche 935, and Singer Vehicle Design.",
        "content": """RFP RESPONSE: BUGATTI-W16-V16-HYPER-RESTRAINT-2026
SUBMITTED BY: Willans Harness Manufacture Ltd. (Silverstone Technology Cluster, United Kingdom)
OEM SUPERCAR PEDIGREE: Iconic British artisan supplier for the McLaren F1, Gordon Murray T.50 fan-car, and bespoke Concours hypercar commissions.

1. CRASH PHYSICS, PYROTECHNICS & GLOBAL HOMOLOGATION
- Homologation Coverage: FIA 8853-2016 and UN/ECE R16 small-series certification. LIMITATION: Does NOT hold independent FMVSS 209/210 active pyrotechnic retractor certification for US road cars without partnering with a Tier-1 pyrotechnic integrator.
- Pyrotechnic Retractor & Buckle: Partner-supplied pyrotechnic retractor fires in 6.6 milliseconds; Willans specializes in mechanical inertia reels and multi-point rotary buckles.
- Load Limiter Architecture: Mechanical 4.3 kN torsion bar with calibrated energy-rip stitch folds.
- Pre-Crash Integration: Passive mechanical lock only; requires external ECU actuator module for active pre-crash tensioning.

2. HYPERCAR LIGHTWEIGHTING & EXOTIC MATERIALS
- Total Installed Vehicle Mass (2 Seats Complete): 1,640 grams per car (820 grams per seat) -- Gordon Murray T.50 inspired featherweight philosophy.
- Hardware Metallurgy: 100% bespoke 5-axis CNC-machined British Ti-6Al-4V titanium buckles, D-rings, and hollowed titanium mounting bolts.
- Webbing Spec: 1.00 mm bespoke British-woven high-tenacity polyester/Vectran ribbon, 28.1 kN breaking strength, 4.6% elongation.

3. BUGATTI BESPOKE CRAFTSMANSHIP, LUXURY & ACOUSTICS/NVH
- Bespoke Customization: Unrivaled Savile Row-level customization--unlimited Pantone colors, sterling silver or 18k gold-inlaid Bugatti Macaron buckle badges, Bridge of Weir leather sleeves (MOQ 1 car).
- UV & Abrasion Resistance: Delta-E = 0.92 after 1,500 hours Xenon-Arc. 60,000 cycle abrasion endurance.
- Tactile & Acoustic Engineering: Hand-polished solid billet titanium buckle tuned to a 55.0 dB mechanical watch-clasp click.
- NVH Performance: 0 dB rattle on static buckles; mechanical retractor pawl has mild vintage click during extraction.

4. MANUFACTURING QUALITY & ZERO-DEFECT TRACEABILITY
- Certifications: ISO 9001:2015, FIA 8853 Approved Manufacturer. Note: Does NOT hold mass-production IATF 16949 certification (VDA 6.3 equivalent: 86%).
- Historical Defect Rate: 1.8 PPM (100% hand-built and individually inspected by master technicians).
- Inspection Protocol: 100% individual tensile proof test and dye-penetrant/X-ray inspection of titanium billets; signed craftsman build book + 40-year archive.

5. COMMERCIAL ECONOMICS & LOW-VOLUME NRE STRUCTURE
- Upfront NRE & Homologation Sled Testing: EUR 490,000 total (lowest NRE in the field, tailored specifically for 250-car hypercar runs).
- Unit BOM Price (Per 2-Seat Vehicle Shipset): EUR 3,150 (above EUR 2,800 target due to 100% billet CNC machining per car).
- Bespoke Sur Mesure Color Surcharge: EUR 250 per car.

6. SUPPLY CHAIN RESILIENCE & MOLSHEIM ATELIER LOGISTICS
- Delivery to Molsheim: 4.0-week lead time from Silverstone, UK to Molsheim, France (post-Brexit bonded air/road express courier included).
- Sub-Tier Sourcing: UK and European titanium; external pyrotechnic sub-supplier. 15-year warranty and lifetime heritage re-webbing service."""
    },
    {
        "filename_base": "10_Holmbergs_Safety_Sweden_Proposal",
        "vendor_name": "Holmbergs Safety System AB",
        "country": "Halmstad, Sweden",
        "oem_pedigree": "Scandinavian High-Precision Restraint Hardware & Extreme-Load Buckle Specialist supplying Koenigsegg sub-assemblies, Polestar 6 concept, and defense/motorsport OEMs.",
        "content": """RFP RESPONSE: BUGATTI-W16-V16-HYPER-RESTRAINT-2026
SUBMITTED BY: Holmbergs Safety System AB (montorgatan 9, Halmstad, Sweden)
OEM SUPERCAR PEDIGREE: Swedish high-load precision buckle and restraint engineering specialist supplying boutique Scandinavian hypercars and specialty OEMs.

1. CRASH PHYSICS, PYROTECHNICS & GLOBAL HOMOLOGATION
- Homologation Coverage: UN/ECE R16, FMVSS 209/210, and GB 14166 certified. FIA 8853 track harness available as secondary kit.
- Pyrotechnic Retractor & Buckle: Swedish-German co-engineered dual-stage pyrotechnic retractor firing in 6.1 milliseconds.
- Load Limiter Architecture: Dual-stage torsion bar (4.5 kN / 2.8 kN) machined from Swedish Uddeholm tool steel and titanium.
- Pre-Crash Integration: CAN-FD reversible motorized retractor (175 N pre-tensioning) compatible with modern hypercar architectures.

2. HYPERCAR LIGHTWEIGHTING & EXOTIC MATERIALS
- Total Installed Vehicle Mass (2 Seats Complete): 1,980 grams per car (990 grams per seat).
- Hardware Metallurgy: Swedish Grade 5 Titanium and ultra-clean recycled Scandinavian billet aluminum housings.
- Webbing Spec: 1.06 mm high-tenacity polyester webbing, 27.4 kN breaking strength, 5.2% elongation.

3. BUGATTI BESPOKE CRAFTSMANSHIP, LUXURY & ACOUSTICS/NVH
- Bespoke Customization: Supports 40 Pantone webbing colors; custom leather wrapping performed via partner saddlery in Sweden (MOQ 1 car).
- UV & Abrasion Resistance: Delta-E = 1.02 after 1,500 hours Xenon-Arc. 65,000 cycle abrasion endurance.
- Tactile & Acoustic Engineering: Minimalist Scandinavian CNC metal buckle with leather trim; latch click is 56.8 dB.
- NVH Performance: 0 dB cabin rattle; smooth retractor payout and motorized presenter compatibility.

4. MANUFACTURING QUALITY & ZERO-DEFECT TRACEABILITY
- Certifications: IATF 16949:2016, ISO 9001, ISO 14001, VDA 6.3 Audit Score 93% (Rating A).
- Historical Defect Rate: 1.5 PPM.
- Inspection Protocol: 100% automated optical and X-ray inspection of locking mechanisms; 30-year QR digital traceability.

5. COMMERCIAL ECONOMICS & LOW-VOLUME NRE STRUCTURE
- Upfront NRE & Homologation Sled Testing: EUR 760,000 total.
- Unit BOM Price (Per 2-Seat Vehicle Shipset): EUR 2,520.
- Bespoke Sur Mesure Color Surcharge: EUR 410 per vehicle.

6. SUPPLY CHAIN RESILIENCE & MOLSHEIM ATELIER LOGISTICS
- Delivery to Molsheim: 5.5-week lead time from Halmstad, Sweden to Molsheim, France inside custom protective cases.
- Sub-Tier Sourcing: 100% Scandinavian and German metallurgy. 15-year structural warranty and 35-year classic spares commitment."""
    }
]


def create_pdf_bytes(title: str, subtitle: str, body_text: str) -> bytes:
    """Renders a clean multi-line PDF document in memory and returns bytes."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 20 * mm

    c.setFont("Helvetica-Bold", 13)
    c.drawString(18 * mm, y, title)
    y -= 6 * mm
    c.setFont("Helvetica-Oblique", 9.5)
    c.drawString(18 * mm, y, subtitle)
    y -= 8 * mm

    c.setFont("Helvetica", 9)
    for paragraph in body_text.split("\n"):
        if not paragraph.strip():
            y -= 3.5 * mm
            continue
        # Wrap long lines at ~95 characters
        words = paragraph.split(" ")
        line = ""
        for w in words:
            if len(line) + len(w) + 1 <= 95:
                line = f"{line} {w}".strip()
            else:
                if y < 18 * mm:
                    c.showPage()
                    c.setFont("Helvetica", 9)
                    y = height - 20 * mm
                c.drawString(18 * mm, y, line)
                y -= 4.3 * mm
                line = w
        if line:
            if y < 18 * mm:
                c.showPage()
                c.setFont("Helvetica", 9)
                y = height - 20 * mm
            if line.isupper() or line.startswith(("1.", "2.", "3.", "4.", "5.", "6.")):
                c.setFont("Helvetica-Bold", 9.5)
                c.drawString(18 * mm, y, line)
                c.setFont("Helvetica", 9)
            else:
                c.drawString(18 * mm, y, line)
            y -= 4.5 * mm

    c.save()
    return buffer.getvalue()


def generate_all_vendor_files(output_dir: str = "vendor_proposals") -> str:
    """Writes all 10 vendor proposals as both .TXT and .PDF files on disk."""
    os.makedirs(output_dir, exist_ok=True)
    for vendor in VENDOR_PROPOSALS_DATA:
        txt_path = os.path.join(output_dir, f"{vendor['filename_base']}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(vendor["content"])

        pdf_path = os.path.join(output_dir, f"{vendor['filename_base']}.pdf")
        pdf_bytes = create_pdf_bytes(
            title=f"BUGATTI HYPERCAR RFP PROPOSAL: {vendor['vendor_name']}",
            subtitle=f"Location: {vendor['country']} | {vendor['oem_pedigree']}",
            body_text=vendor["content"]
        )
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)

    return os.path.abspath(output_dir)


if __name__ == "__main__":
    folder = generate_all_vendor_files()
    print(f"Created 10 .TXT and 10 .PDF vendor proposals inside: {folder}")
