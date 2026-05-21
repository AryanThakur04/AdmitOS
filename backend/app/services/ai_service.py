from app.config import get_settings

settings = get_settings()


async def generate_text(prompt: str) -> str:
    """AI text generation with fallback for demo mode."""
    if settings.ai_provider == "openai" and settings.openai_api_key:
        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=settings.openai_api_key)
            resp = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
            )
            return resp.choices[0].message.content or ""
        except Exception:
            pass

    if settings.gemini_api_key:
        try:
            import google.generativeai as genai

            genai.configure(api_key=settings.gemini_api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            resp = model.generate_content(prompt)
            return resp.text or ""
        except Exception:
            pass

    return _demo_fallback(prompt)


def _demo_fallback(prompt: str) -> str:
    if "whatsapp" in prompt.lower():
        return (
            "Hi {name}! 👋 This is AdmitOS following up on your application to "
            "{program}. We'd love to help you with the next steps. "
            "Could you share your preferred time for a quick call this week?"
        )
    if "acceptance" in prompt.lower() or "letter" in prompt.lower():
        return (
            "Dear {name},\n\nWe are pleased to offer you admission to {program} "
            "starting Fall 2026. Please find your acceptance documents attached. "
            "Complete enrollment by the deadline indicated.\n\nCongratulations!"
        )
    if "call" in prompt.lower() or "summary" in prompt.lower():
        return (
            "Call Summary: Student expressed strong interest in {program}. "
            "Asked about scholarship options and housing. Follow up with fee "
            "structure PDF and schedule campus tour. Sentiment: positive."
        )
    return "AI response generated in demo mode. Configure GEMINI_API_KEY or OPENAI_API_KEY for live output."


async def whatsapp_followup_simulate(lead_name: str, program: str, days_silent: int) -> dict:
    prompt = (
        f"Generate a professional WhatsApp follow-up message for student {lead_name} "
        f"interested in {program}. They have been silent for {days_silent} days. "
        "Keep under 80 words, friendly but professional."
    )
    text = await generate_text(prompt)
    text = text.replace("{name}", lead_name).replace("{program}", program or "our program")
    return {
        "message": text,
        "channel": "whatsapp",
        "tone": "professional-friendly",
        "suggested_send_time": "Tuesday 10:00 AM local",
    }


async def generate_acceptance_letter(lead_name: str, program: str, campus: str = "Main Campus") -> str:
    prompt = (
        f"Write a formal university acceptance letter for {lead_name} "
        f"admitted to {program} at {campus}. Include congratulations and next steps."
    )
    text = await generate_text(prompt)
    return text.replace("{name}", lead_name).replace("{program}", program or "your selected program")


async def summarize_call_transcript(transcript: str, lead_name: str) -> str:
    prompt = (
        f"Summarize this admissions call transcript for counsellor review. "
        f"Student: {lead_name}\n\nTranscript:\n{transcript}"
    )
    return await generate_text(prompt)
