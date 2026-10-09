
import os
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

OPEN_METEO_GEOCODING = "https://geocoding-api.open-meteo.com/v1/search"
OPEN_METEO_WEATHER = "https://api.open-meteo.com/v1/forecast"

LANGUAGES = {
    "en": "English",
    "rw": "Kinyarwanda",
    "fr": "Français",
    "sw": "Kiswahili",
}

# General guidance only. Exact recommendations must be checked
# against local agricultural extension advice and product labels.
ADVICE = {
    "en": {
        "planting": (
            "Check the recommended planting season, locally adapted seed "
            "varieties, soil moisture, and the crop calendar for your area. "
            "Avoid planting solely on the basis of a general forecast."
        ),
        "soil": (
            "Assess soil texture, drainage, organic matter and soil pH. "
            "A soil test is the best starting point for crop-specific "
            "nutrient decisions."
        ),
        "fertilizer": (
            "Choose fertilizer according to the crop, soil test, growth "
            "stage and local recommendations. Follow the product label. "
            "Do not use a universal dose: needs vary by crop and location."
        ),
        "pests": (
            "Inspect the crop and identify the pest before taking action. "
            "Use integrated pest management, including field monitoring, "
            "sanitation and locally approved control methods. Do not apply "
            "pesticides without confirming the pest and the product label."
        ),
        "disease": (
            "Check symptoms on several plants and note when they appeared. "
            "Disease symptoms can resemble nutrient deficiencies or pest "
            "damage. Seek local extension or laboratory confirmation before "
            "choosing a treatment."
        ),
        "water": (
            "Consider crop stage, soil moisture, rainfall and drainage. "
            "Water needs differ among crops and soils. Avoid waterlogging "
            "and use local irrigation guidance where available."
        ),
        "harvest": (
            "Harvest at the crop's appropriate maturity stage. Follow "
            "local guidance for maturity signs and safe harvesting, and "
            "handle produce carefully to reduce losses."
        ),
        "storage": (
            "Clean and dry produce appropriately before storage. Protect "
            "it from moisture, pests and contamination. Safe moisture "
            "requirements differ by crop and storage method."
        ),
        "market": (
            "Compare prices from several local buyers and markets. Confirm "
            "the date, currency, unit, quality grade, transport cost and "
            "buyer conditions. This prototype does not provide live prices."
        ),
        "general": (
            "For a more specific answer, provide the crop, country or "
            "region, growth stage and the problem you are seeing. Verify "
            "important decisions with local agricultural extension advice."
        ),
    },
    "rw": {
        "planting": (
            "Reba igihe cyiza cyo gutera muri ako gace, imbuto zihamenyereye, "
            "ubushuhe bw'ubutaka n'ingengabihe y'igihingwa. Ntushingire ku "
            "iteganyagihe rusange gusa."
        ),
        "soil": (
            "Reba ubwoko bw'ubutaka, uko amazi ayungururamo, ifumbire "
            "y'imborera n'ubusharire bw'ubutaka. Gupima ubutaka bifasha "
            "kumenya intungamubiri zikenewe."
        ),
        "fertilizer": (
            "Hitamo ifumbire ukurikije igihingwa, ibisubizo byo gupima "
            "ubutaka, icyiciro cy'ikura n'amabwiriza y'inzobere zo muri "
            "ako gace. Kurikiza amabwiriza ari ku gikoresho. Nta rugero "
            "rumwe rw'ifumbire rukwiriye ibihingwa n'ibihugu byose."
        ),
        "pests": (
            "Banza umenye neza agakoko kangiza igihingwa. Kigenzure mu "
            "murima, usukure aho bikenewe kandi ukoreshe uburyo bwo "
            "kukirwanya bwemewe muri ako gace. Ntukoreshe umuti utaramenya "
            "agakoko ugomba kuvura."
        ),
        "disease": (
            "Reba ibimenyetso ku bimera byinshi kandi wandike igihe "
            "byatangiriye. Indwara ishobora gusa n'ikibazo cy'intungamubiri "
            "cyangwa udukoko. Saba ubufasha bw'umukozi w'ubuhinzi mbere "
            "yo guhitamo umuti."
        ),
        "water": (
            "Reba icyiciro igihingwa kigezeho, ubuhehere bw'ubutaka, "
            "imvura n'uko amazi atembera. Ibihingwa n'ubutaka ntibikenera "
            "amazi angana. Irinde ko umurima wuzuramo amazi."
        ),
        "harvest": (
            "Sarura igihingwa kigeze igihe cyacyo cyo kwera. Kurikiza "
            "amabwiriza y'aho uherereye kandi wirinde kwangiza umusaruro."
        ),
        "storage": (
            "Sukura kandi wumishe umusaruro uko bikwiye mbere yo kuwubika. "
            "Wurinde ubuhehere, udukoko n'ibindi byawuhumanya. Uburyo "
            "bwo kuwumisha buterwa n'igihingwa."
        ),
        "market": (
            "Gereranya ibiciro by'abaguzi n'amasoko atandukanye. Banza "
            "wemeze itariki, ifaranga, igipimo, ubwiza, ikiguzi cyo "
            "gutwara umusaruro n'amasezerano y'umuguzi. Iyi verisiyo "
            "ntitanga ibiciro by'isoko biriho ako kanya."
        ),
        "general": (
            "Kugira ngo ubone igisubizo cyihariye, andika igihingwa, "
            "igihugu cyangwa akarere, icyiciro cy'ikura n'ikibazo ufite. "
            "Banza ugenzure inama zikomeye ku nzobere z'ubuhinzi zo muri ako gace."
        ),
    },
    "fr": {
        "planting": (
            "Vérifiez la période de semis locale, les variétés adaptées, "
            "l'humidité du sol et le calendrier cultural de votre région. "
            "Ne vous fiez pas uniquement à une prévision générale."
        ),
        "soil": (
            "Évaluez la texture du sol, le drainage, la matière organique "
            "et le pH. Une analyse du sol aide à déterminer les besoins "
            "en éléments nutritifs."
        ),
        "fertilizer": (
            "Choisissez l'engrais selon la culture, l'analyse du sol, "
            "le stade de croissance et les recommandations locales. "
            "Respectez l'étiquette. Il n'existe pas de dose universelle."
        ),
        "pests": (
            "Identifiez le ravageur avant d'agir. Surveillez les cultures "
            "et utilisez des méthodes de lutte intégrée approuvées localement. "
            "N'appliquez pas de pesticide sans identification et vérification "
            "de son étiquette."
        ),
        "disease": (
            "Examinez plusieurs plantes et notez l'apparition des symptômes. "
            "Une maladie peut ressembler à une carence ou à des dégâts "
            "d'insectes. Demandez une confirmation locale avant le traitement."
        ),
        "water": (
            "Tenez compte du stade de la culture, de l'humidité du sol, "
            "des pluies et du drainage. Les besoins en eau varient selon "
            "la culture et le sol."
        ),
        "harvest": (
            "Récoltez au stade de maturité approprié et suivez les conseils "
            "locaux pour réduire les pertes."
        ),
        "storage": (
            "Nettoyez et séchez correctement les récoltes avant le stockage. "
            "Protégez-les de l'humidité, des ravageurs et de la contamination."
        ),
        "market": (
            "Comparez plusieurs acheteurs et marchés. Vérifiez la date, "
            "la devise, l'unité, la qualité et les frais de transport. "
            "Cette version ne fournit pas de prix en direct."
        ),
        "general": (
            "Précisez la culture, le pays ou la région, le stade de croissance "
            "et le problème observé. Vérifiez les décisions importantes auprès "
            "des services agricoles locaux."
        ),
    },
    "sw": {
        "planting": (
            "Angalia msimu unaofaa wa kupanda katika eneo lako, mbegu "
            "zinazofaa, unyevunyevu wa udongo na kalenda ya kilimo. "
            "Usitumie utabiri wa jumla pekee kuamua kupanda."
        ),
        "soil": (
            "Chunguza aina ya udongo, mifereji ya maji, mabaki ya viumbe "
            "na pH. Kipimo cha udongo husaidia kujua virutubisho vinavyohitajika."
        ),
        "fertilizer": (
            "Chagua mbolea kulingana na zao, kipimo cha udongo, hatua ya "
            "ukuaji na ushauri wa eneo lako. Fuata maelekezo kwenye kifungashio. "
            "Hakuna kiwango kimoja kinachofaa kila zao na kila eneo."
        ),
        "pests": (
            "Tambua mdudu kabla ya kuchukua hatua. Kagua shamba na tumia "
            "mbinu za udhibiti jumuishi zilizoidhinishwa eneo lako. Usitumie "
            "dawa bila kuthibitisha mdudu na maelekezo ya bidhaa."
        ),
        "disease": (
            "Kagua mimea kadhaa na uangalie dalili zilipoanza. Ugonjwa "
            "unaweza kufanana na upungufu wa virutubisho au uharibifu wa wadudu. "
            "Tafuta ushauri wa mtaalamu kabla ya kuchagua tiba."
        ),
        "water": (
            "Zingatia hatua ya ukuaji, unyevunyevu wa udongo, mvua na mifereji "
            "ya maji. Mahitaji ya maji hutofautiana kulingana na zao na udongo."
        ),
        "harvest": (
            "Vuna zao linapofikia ukomavu unaofaa. Fuata ushauri wa eneo lako "
            "ili kupunguza upotevu wa mazao."
        ),
        "storage": (
            "Safisha na kausha mazao ipasavyo kabla ya kuyahifadhi. Yakinge "
            "dhidi ya unyevunyevu, wadudu na uchafuzi."
        ),
        "market": (
            "Linganisha bei kutoka kwa wanunuzi na masoko kadhaa. Hakikisha "
            "tarehe, sarafu, kipimo, ubora na gharama za usafirishaji. "
            "Toleo hili halitoi bei za soko za moja kwa moja."
        ),
        "general": (
            "Taja zao, nchi au eneo, hatua ya ukuaji na tatizo unaloona "
            "ili kupata ushauri unaofaa zaidi. Thibitisha maamuzi muhimu "
            "kwa huduma za ugani za eneo lako."
        ),
    },
}

TOPICS = {
    "planting": "Planting / Gutera / Semis",
    "soil": "Soil / Ubutaka / Sol",
    "fertilizer": "Fertilizer / Ifumbire / Engrais",
    "pests": "Pests / Udukoko / Ravageurs",
    "disease": "Disease / Indwara / Maladie",
    "water": "Water / Amazi / Eau",
    "harvest": "Harvest / Gusarura / Récolte",
    "storage": "Storage / Kubika / Stockage",
    "market": "Market / Isoko / Marché",
    "general": "General question / Ikindi / Autre",
}


def get_weather(place):
    """Look up a place, then request its current weather and short forecast."""
    if not place:
        return None, "Enter a town, district, region or country to check weather."

    try:
        geo_response = requests.get(
            OPEN_METEO_GEOCODING,
            params={
                "name": place,
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=12,
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        results = geo_data.get("results", [])

        if not results:
            return None, "Location not found. Try a nearby town or a different spelling."

        location = results[0]
        lat = location["latitude"]
        lon = location["longitude"]

        weather_response = requests.get(
            OPEN_METEO_WEATHER,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": (
                    "temperature_2m,relative_humidity_2m,"
                    "precipitation,wind_speed_10m"
                ),
                "daily": (
                    "temperature_2m_max,temperature_2m_min,"
                    "precipitation_sum,precipitation_probability_max"
                ),
                "forecast_days": 3,
                "timezone": "auto",
            },
            timeout=15,
        )
        weather_response.raise_for_status()
        weather = weather_response.json()

        current = weather.get("current", {})
        daily = weather.get("daily", {})
        place_parts = [
            location.get("name"),
            location.get("admin1"),
            location.get("country"),
        ]
        place_name = ", ".join(
            part for i, part in enumerate(place_parts)
            if part and part not in place_parts[:i]
        )

        forecast = []
        dates = daily.get("time", [])
        for i, date in enumerate(dates):
            forecast.append({
                "date": date,
                "min": value_at(daily, "temperature_2m_min", i),
                "max": value_at(daily, "temperature_2m_max", i),
                "rain": value_at(daily, "precipitation_sum", i),
                "rain_chance": value_at(
                    daily, "precipitation_probability_max", i
                ),
            })

        return {
            "place": place_name,
            "temperature": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "rain": current.get("precipitation"),
            "wind": current.get("wind_speed_10m"),
            "forecast": forecast,
        }, None

    except (requests.RequestException, ValueError, KeyError, TypeError):
        return None, (
            "Weather data is temporarily unavailable. Try again later "
            "or check your local meteorological service."
        )


def value_at(data, key, index):
    values = data.get(key, [])
    return values[index] if index < len(values) else None


PAGE = r"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Agri-Vincent AI Global</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      max-width: 900px;
      margin: auto;
      padding: 18px;
      background: #f4f7f2;
      color: #202820;
      line-height: 1.55;
    }
    header, section {
      background: white;
      padding: 18px;
      border-radius: 12px;
      margin-bottom: 16px;
      box-shadow: 0 2px 8px #00000010;
    }
    h1 { color: #23652f; margin-bottom: 4px; }
    label { display: block; font-weight: bold; margin-top: 12px; }
    input, select, textarea, button {
      box-sizing: border-box;
      width: 100%;
      padding: 11px;
      margin-top: 5px;
      border: 1px solid #b9c6b8;
      border-radius: 7px;
      font-size: 16px;
    }
    button {
      background: #23652f;
      color: white;
      font-weight: bold;
      border: 0;
      margin-top: 18px;
      cursor: pointer;
    }
    .muted { color: #5a675a; font-size: 14px; }
    .warning {
      background: #fff6dc;
      padding: 12px;
      border-radius: 8px;
    }
    .weather-day {
      border-top: 1px solid #e0e6df;
      padding: 8px 0;
    }
    a { overflow-wrap: anywhere; }
  </style>
</head>
<body>
<header>
  <h1>🌱 Agri-Vincent AI Global</h1>
  <p>Practical agricultural guidance for farmers around the world.</p>
  <p class="muted">
    This prototype provides general guidance and live weather where available.
    Always verify local farming recommendations.
  </p>
</header>

<section>
  <h2>Ask an agricultural question</h2>
  <form method="post">
    <label for="language">Language / Ururimi / Langue</label>
    <select name="language" id="language">
      {% for code, name in languages.items() %}
        <option value="{{ code }}"
          {% if code == selected_language %}selected{% endif %}>
          {{ name }}
        </option>
      {% endfor %}
    </select>

    <label for="place">Country, region or nearest town</label>
    <input id="place" name="place" required
           value="{{ place }}"
           placeholder="Example: Nairobi, Kenya">

    <label for="crop">Crop or plant</label>
    <input id="crop" name="crop" required
           value="{{ crop }}"
           placeholder="Example: maize, rice, beans, tomato, coffee">

    <label for="stage">Crop growth stage (optional)</label>
    <select id="stage" name="stage">
      {% for value, label in stages.items() %}
        <option value="{{ value }}"
          {% if value == stage %}selected{% endif %}>{{ label }}</option>
      {% endfor %}
    </select>

    <label for="topic">Topic</label>
    <select id="topic" name="topic">
      {% for value, label in topics.items() %}
        <option value="{{ value }}"
          {% if value == topic %}selected{% endif %}>{{ label }}</option>
      {% endfor %}
    </select>

    <label for="question">Describe your question or problem (optional)</label>
    <textarea id="question" name="question" rows="4"
      placeholder="Describe what you see in your field...">{{ question }}</textarea>

    <button type="submit">Get agricultural guidance</button>
  </form>
</section>

{% if advice %}
<section>
  <h2>Guidance for {{ crop }}</h2>
  <p><strong>Location:</strong> {{ place }}</p>
  <p><strong>Growth stage:</strong> {{ stages.get(stage, stage) }}</p>
  <p>{{ advice }}</p>
  {% if question %}
    <p><strong>Your question:</strong> {{ question }}</p>
    <p class="muted">
      The question is recorded on this result page, but this version does
      not use a generative AI model to interpret every possible question.
      The advice is based on the topic you selected.
    </p>
  {% endif %}
  <div class="warning">
    <strong>Safety:</strong> Fertilizer and pesticide rates depend on the
    crop, local conditions, product label and applicable regulations.
    Confirm exact rates and treatments with a qualified local adviser.
  </div>
</section>
{% endif %}

{% if weather %}
<section>
  <h2>Local weather</h2>
  <p><strong>{{ weather.place }}</strong></p>
  <p>Current temperature: {{ weather.temperature }} °C</p>
  <p>Relative humidity: {{ weather.humidity }}%</p>
  <p>Current precipitation: {{ weather.rain }} mm</p>
  <p>Wind speed: {{ weather.wind }} km/h</p>

  <h3>Three-day forecast</h3>
  {% for day in weather.forecast %}
    <div class="weather-day">
      <strong>{{ day.date }}</strong><br>
      Temperature: {{ day.min }} °C to {{ day.max }} °C<br>
      Precipitation: {{ day.rain }} mm<br>
      Maximum precipitation probability: {{ day.rain_chance }}%
    </div>
  {% endfor %}
  <p class="muted">
    Weather by <a href="https://open-meteo.com/" target="_blank"
    rel="noopener">Open-Meteo</a>. Forecasts can change and do not replace
    local meteorological warnings.
  </p>
</section>
{% elif weather_error %}
<section>
  <h2>Weather</h2>
  <p>{{ weather_error }}</p>
</section>
{% endif %}

<section>
  <h2>Trusted agricultural resources</h2>
  <ul>
    <li><a href="https://www.fao.org/agriculture/crops/"
      target="_blank" rel="noopener">FAO — crops and plant production</a></li>
    <li><a href="https://www.fao.org/agriculture/crops/thematic-sitemap/theme/spi/scpi-home/managing-ecosystems/"
      target="_blank" rel="noopener">FAO — crop production resources</a></li>
    <li><a href="https://www.fao.org/faostat/"
      target="_blank" rel="noopener">FAOSTAT — agricultural statistics</a></li>
    <li><a href="https://open-meteo.com/en/docs"
      target="_blank" rel="noopener">Open-Meteo — weather documentation</a></li>
    <li><a href="https://plantvillage.psu.edu/"
      target="_blank" rel="noopener">PlantVillage — plant health resources</a></li>
  </ul>
  <p class="muted">
    These links are reference resources, not proof that every recommendation
    has been verified for your exact farm. Look for your country's official
    agriculture ministry, extension service or plant-health authority.
  </p>
</section>

<footer class="muted">
  Agri-Vincent AI Global — prototype. No live market prices, soil test,
  image diagnosis or country-specific fertilizer database is connected yet.
</footer>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    languages = LANGUAGES
    topics = TOPICS
    stages = {
        "unknown": "Not sure / Ntabizi / Je ne sais pas",
        "planning": "Before planting",
        "planting": "Planting / sowing",
        "vegetative": "Vegetative growth",
        "flowering": "Flowering",
        "fruiting": "Fruit or grain development",
        "harvest": "Harvest",
        "storage": "Post-harvest / storage",
    }

    selected_language = request.form.get("language", "en")
    if selected_language not in LANGUAGES:
        selected_language = "en"

    place = request.form.get("place", "").strip()[:160]
    crop = request.form.get("crop", "").strip()[:100]
    stage = request.form.get("stage", "unknown")
    if stage not in stages:
        stage = "unknown"

    topic = request.form.get("topic", "general")
    if topic not in TOPICS:
        topic = "general"

    question = request.form.get("question", "").strip()[:1500]
    advice = None
    weather = None
    weather_error = None

    if request.method == "POST":
        advice = ADVICE[selected_language].get(
            topic, ADVICE[selected_language]["general"]
        )
        weather, weather_error = get_weather(place)

    return render_template_string(
        PAGE,
        languages=languages,
        topics=topics,
        stages=stages,
        selected_language=selected_language,
        place=place,
        crop=crop,
        stage=stage,
        topic=topic,
        question=question,
        advice=advice,
        weather=weather,
        weather_error=weather_error,
    )


@app.route("/health")
def health():
    return {"status": "ok", "app": "Agri-Vincent AI Global"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port, debug=False)
