import os
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

PAGE = r"""<!doctype html>
<html lang="rw">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Agri-Vincent AI</title>
  <style>
    :root { --green:#176b3a; --pale:#edf7ef; --ink:#17251b; }
    * { box-sizing:border-box; }
    body { margin:0; font-family:Arial,sans-serif; background:#f5f8f5; color:var(--ink); }
    header { background:var(--green); color:white; padding:24px 18px; text-align:center; }
    header h1 { margin:0 0 8px; font-size:clamp(25px,5vw,38px); }
    header p { margin:0; line-height:1.5; }
    main { width:min(760px, calc(100% - 24px)); margin:22px auto; }
    .card { background:white; border-radius:16px; padding:20px; box-shadow:0 4px 18px #122b1710; margin-bottom:16px; }
    label { display:block; font-weight:bold; margin:12px 0 6px; }
    select, textarea, input { width:100%; padding:12px; border:1px solid #cbd8ce; border-radius:9px; font:inherit; background:white; }
    textarea { min-height:120px; resize:vertical; }
    button { border:0; background:var(--green); color:white; padding:13px 18px; border-radius:9px; font-weight:bold; font-size:16px; cursor:pointer; margin-top:12px; }
    button:hover { filter:brightness(.92); }
    .answer { background:var(--pale); border-left:4px solid var(--green); padding:16px; border-radius:8px; white-space:pre-wrap; line-height:1.6; }
    .muted { color:#526157; font-size:14px; line-height:1.5; }
    footer { text-align:center; padding:18px; color:#526157; font-size:13px; }
  </style>
</head>
<body>
<header>
  <h1>🌽 Agri-Vincent AI</h1>
  <p>Umufasha w'abahinzi b'ibigori mu Rwanda</p>
  <p>Inama ku gutera, ifumbire, indwara, ikirere, gusarura n'amasoko.</p>
</header>
<main>
  <section class="card">
    <h2>Baza ikibazo cy'ubuhinzi</h2>
    <form method="post">
      <label for="language">Ururimi</label>
      <select id="language" name="language">
        <option value="Kinyarwanda" {% if language == 'Kinyarwanda' %}selected{% endif %}>Ikinyarwanda</option>
        <option value="English" {% if language == 'English' %}selected{% endif %}>English</option>
        <option value="Français" {% if language == 'Français' %}selected{% endif %}>Français</option>
      </select>
      <label for="location">Aho uhinga (urugero: Katabagemu, Nyagatare)</label>
      <input id="location" name="location" value="{{ location }}" placeholder="Aho uhinga">
      <label for="question">Ikibazo cyawe</label>
      <textarea id="question" name="question" required placeholder="Urugero: Ni ryari nakoresha ifumbire ku bigori?">{{ question }}</textarea>
      <button type="submit">Shaka inama</button>
    </form>
  </section>
  {% if answer %}
  <section class="card">
    <h2>Igisubizo cya Agri-Vincent AI</h2>
    <div class="answer">{{ answer }}</div>
  </section>
  {% endif %}
  <section class="card">
    <h3>Uko ikora</h3>
    <p class="muted">Iyo MISTRAL_API_KEY yashyizwe muri environment variables za Render, porogaramu ikoresha Mistral AI. Niba itarashyirwamo, itanga ubutumwa bw'ibanze bukubwira icyo wakora. Ntukoreshe inama rusange mu mwanya w'amabwiriza y'inzobere z'ubuhinzi ku bibazo bikomeye.</p>
  </section>
</main>
<footer>Agri-Vincent AI · Climate-smart maize farming · Rwanda</footer>
</body>
</html>"""

def fallback_answer(question, location, language):
    if language == "English":
        return ("AI service is not configured yet. Add MISTRAL_API_KEY in Render Environment to enable AI answers. "
                "For now, check local RAB/MINAGRI guidance and ask an agronomist before applying chemicals or changing fertilizer rates. "
                f"Your question: {question}")
    if language == "Français":
        return ("Le service IA n'est pas encore configuré. Ajoutez MISTRAL_API_KEY dans les variables d'environnement de Render. "
                "En attendant, vérifiez les recommandations locales du RAB/MINAGRI et consultez un conseiller agricole avant d'utiliser des produits chimiques. "
                f"Votre question : {question}")
    return ("Serivisi ya AI iracyategurwa. Kugira ngo ubone ibisubizo bya AI, shyira MISTRAL_API_KEY muri Environment Variables za Render. "
            "Hagati aho, banza ugishe inama umukozi w'ubuhinzi cyangwa amabwiriza yemewe ya RAB/MINAGRI, cyane cyane mbere yo gukoresha imiti cyangwa guhindura ingano y'ifumbire. "
            f"\nAho uhinga: {location or 'Ntabwo wahagaragaje'}\nIkibazo cyawe: {question}")

def ask_mistral(question, location, language):
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        return None
    prompt = (
        "You are Agri-Vincent AI, an agricultural information assistant focused ONLY on maize farming "
        "for smallholder farmers in Rwanda, especially Nyagatare District. "
        "Answer in the user's selected language. Give practical, clear, cautious advice. "
        "Do not invent current weather, market prices, or official recommendations. "
        "Ask for missing details if needed. For pesticide or fertilizer dosage, advise following the product label "
        "and local RAB/MINAGRI extension guidance; do not guess dangerous dosages. "
        "Mention when advice should be confirmed with a qualified agricultural extension officer.\n"
        f"Selected language: {language}\nFarmer location: {location or 'Not specified'}\nQuestion: {question}"
    )
    try:
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": os.getenv("MISTRAL_MODEL", "mistral-small-latest"),
                "messages": [
                    {"role": "system", "content": "You are a careful, practical maize-farming assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 700
            },
            timeout=35
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        app.logger.exception("Mistral API request failed")
        return None

@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""
    question = ""
    location = ""
    language = "Kinyarwanda"
    if request.method == "POST":
        question = request.form.get("question", "").strip()[:3000]
        location = request.form.get("location", "").strip()[:200]
        language = request.form.get("language", "Kinyarwanda")
        if language not in ("Kinyarwanda", "English", "Français"):
            language = "Kinyarwanda"
        if question:
            answer = ask_mistral(question, location, language) or fallback_answer(question, location, language)
    return render_template_string(PAGE, answer=answer, question=question, location=location, language=language)

@app.route("/health")
def health():
    return {"status": "ok", "app": "Agri-Vincent AI"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
