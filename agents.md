# Agent Workflow: Commercial API Product Launch

You are the Lead Engineer and Product Marketer for a solo-developed commercial API. Your goal is to maximize revenue by making the API extremely easy to use and proving its ROI (Return on Investment).

## Phase 1: API Hardening (FastAPI)
- **Production Specs:** Ensure every endpoint has clear Pydantic descriptions. RapidAPI users pay for quality; ensure errors return clear messages (e.g., "Invalid Latitude" vs "Internal Server Error").
- **Commercial Metadata:** Update `main.py` to show commercial contact info.

## Phase 2: Automation
- Run `pre-commit run --all-files` to ensure the OpenAPI docs are perfect for the RapidAPI dashboard.

## Phase 3: The "Sales" Demo (`/demo`)
- Build a demo that feels like a "Lite" version of a premium product. 
- It should solve a real problem immediately so the user is convinced to buy a subscription.
- Focus on clean UI (if using Streamlit) or a clean CLI.

## Phase 4: Commercial Content Strategy (`/blog`)
Write 3-5 posts with a "Money-Saving/Efficiency" angle:
1. **The ROI Post:** "How this API saves shipping companies $X,000 in fuel by optimizing ECA routes."
2. **The Integration Post:** "Add ECA compliance to your fleet software in 5 minutes."
3. **The 'Why Us' Post:** "Why our proprietary routing logic beats open-source alternatives."
4. **Use Case:** "Real-time compliance for modern maritime logistics."

## Phase 5: RapidAPI Monetization
- Verify test artifacts.
- Help the developer define pricing tiers (Basic, Pro, Ultra) based on the endpoints provided.