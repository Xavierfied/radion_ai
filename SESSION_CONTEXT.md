# DENTAL-AI — SESSION CONTEXT FILE
# Paste this at the start of every new Claude session

## PROJECT OVERVIEW
Dental X-ray (OPG) analysis SaaS for US dental schools and clinics.
AI analyzes panoramic dental X-rays and generates structured clinical draft reports.
Target users: dental students + dentists (USA market)
Co-founder setup: Developer in Pakistan, dentist cousin in USA for domain expertise + sales

## CURRENT STATUS
✅ PHASE 1 COMPLETE — MVP is live and deployed
GitHub repo: github.com/Xavierfied/radion_ai (public)
Currently in: Validation phase — waiting for cousin's feedback from real users


## IMPORTANT — IMPORT PATHS
Since files are in subfolders, imports in app.py use:
    from utils.analyzer_g import analyze_xray
    from utils.pdf_generator import generate_pdf
    from prompts.report_template import DENTAL_ANALYSIS_PROMPT

And analyzer_g.py loads env from:
    from dotenv import load_dotenv
    load_dotenv("keys/.env")

## ACTIVE AI SETUP
Currently using:  Gemini 2.5 Flash (analyzer_g.py)
Free tier limits: 1,500 requests/day, 15 requests/minute
Streamlit secret: GEMINI_API_KEY = "your_key"

Future switch:    Claude Sonnet (analyzer.py) — when ready to go paid
Reason for swap:  Better structured output, prompt caching, more reliable

## ENVIRONMENT VARIABLES
Local:            keys/.env → GEMINI_API_KEY=your_key
Streamlit Cloud:  Secrets → GEMINI_API_KEY = "your_key"

## FEATURES BUILT (PHASE 1)
```
- X-ray image upload (JPEG/PNG/WebP)
- Patient ID input
- Gemini Vision API analysis with structured OPG report
- PDF report download
- TXT report download
- Session history (in-memory)
- Token usage + cost estimate per analysis
- Disclaimer on every report
- Dark mode UI
- Deployed publicly on Streamlit Cloud
```
## WHAT'S NOT BUILT (PHASE 2 — in priority order)
1. Login + user accounts (Supabase auth)
2. Persistent database (save reports between sessions)
3. Patient profile management
4. PDF export improvements
5. Side-by-side X-ray comparison
6. Trial limit system (20 free → paywall)
7. Stripe payments
8. Chrome extension
9. Multi-user org accounts (school admin + students)

## COMPLIANCE NOTES
- Disclaimer on every report
- Patient IDs only, no real names
- Not HIPAA compliant yet (comes in Phase 2)
- Not FDA cleared — educational/workflow tool only

## NEXT SESSION OPTIONS
A) Start Phase 2 — Supabase + FastAPI backend + user auth
B) Add features to Streamlit app (login, database) using Supabase directly

