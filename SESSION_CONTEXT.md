# DENTAL-AI — SESSION CONTEXT FILE
# Paste this at the start of every new Claude session

## PROJECT OVERVIEW
Building a dental X-ray (OPG) analysis SaaS for US dental schools and clinics.
AI analyzes panoramic dental X-rays and generates structured clinical draft reports.
Target users: dental students + dentists (USA market)
Co-founder setup: Developer in Pakistan, dentist cousin in USA for domain expertise + sales

## CURRENT PHASE
Phase 1 — Streamlit MVP (validate with real users before full build)

## TECH STACK (FINAL DECIDED)
- Phase 1 (now):  Streamlit + Claude Vision API + ReportLab PDF
- Phase 2 (next): FastAPI (Python backend) + Next.js (frontend) + Supabase (DB) + Railway (hosting)
- AI: Claude Sonnet (claude-sonnet-4-5) Vision API with prompt caching
- Payments (later): Stripe
- Pricing model: 20 free analyses trial → $299/mo school plan, $149/mo clinic, $49/mo solo

## WHAT HAS BEEN BUILT (SESSION 1 — COMPLETE)
Full Streamlit MVP with these features:
✅ X-ray image upload (JPEG/PNG/WebP)
✅ Patient ID input (no real names — basic HIPAA awareness)
✅ Claude Vision API integration with prompt caching
✅ Structured OPG report generation (full dental analysis format)
✅ PDF report download (via ReportLab)
✅ TXT report download
✅ Session history (in-memory, shows past analyses this session)
✅ Token usage + cost estimate per analysis
✅ Disclaimer on every report (legal protection)
✅ Clean professional UI with custom CSS

## FILE STRUCTURE
dental-ai/
├── app.py                  ← Main Streamlit app (UI + state management)
├── analyzer.py             ← Claude API integration + error handling
├── report_template.py      ← Full OPG analysis system prompt
├── pdf_generator.py        ← ReportLab PDF generation
├── requirements.txt        ← Python dependencies
├── .env                    ← API key (ANTHROPIC_API_KEY=...) — NOT committed to git
├── .env.example            ← Template for .env
└── SESSION_CONTEXT.md      ← This file

## ENVIRONMENT VARIABLES NEEDED
ANTHROPIC_API_KEY=your_key_here
(Get from console.anthropic.com → API Keys)

## HOW TO RUN LOCALLY
1. pip install -r requirements.txt
2. Add your API key to .env file
3. streamlit run app.py
4. Opens at http://localhost:8501

## WHAT'S NOT BUILT YET (PHASE 2)
- User authentication (login/signup)
- Persistent database (analyses saved between sessions)
- Patient profile management (attach multiple X-rays to one patient)
- Side-by-side X-ray comparison
- Organization/multi-user management (school admin + students)
- Trial system (20 free analyses then paywall)
- Stripe payments
- Proper cloud deployment

## KNOWN LIMITATIONS OF CURRENT BUILD
- History only persists within one browser session (no database yet)
- No user accounts — anyone with the URL can use it
- No DICOM support (only JPEG/PNG — fine for Phase 1)
- Not HIPAA compliant yet (no BAA signed, no encrypted storage)

## COMPLIANCE NOTES
- Disclaimer on every report (AI draft, must be reviewed by licensed professional)
- Using Patient IDs not real names (keeps us outside HIPAA territory for now)
- Not FDA cleared — positioned as educational/workflow assistance tool
- HIPAA BAA + proper compliance comes in Phase 2 before charging real clinics

## NEXT SESSION — WHAT TO BUILD
Option A: Deploy to Streamlit Cloud (free, shareable link for cousin to test)
Option B: Start Phase 2 — Supabase setup + FastAPI backend + user auth
Recommended: Do Option A first (get real user feedback), then Option B

## DEPLOYMENT (WHEN READY)
Streamlit Cloud (free):
1. Push code to GitHub (without .env file)
2. Go to streamlit.io → New app → connect GitHub repo
3. Add ANTHROPIC_API_KEY in Streamlit Cloud secrets
4. Get a public URL to share with cousin

## COST ESTIMATE PER ANALYSIS
~$0.02 per analysis (2 cents) with Claude Sonnet + prompt caching
At 500 analyses/month: ~$10 API cost
Charging $299/month → ~97% margin