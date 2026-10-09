
def fallback_answer(question, location, language):
    q = question.lower()

    if language == "English":
        if any(w in q for w in ["fertilizer", "fertiliser", "urea", "dap"]):
            advice = (
                "Fertilizer: Apply planting fertilizer according to local "
                "recommendations. Nitrogen top-dressing is commonly done during "
                "early maize growth, often around 3–4 weeks after emergence, "
                "but timing and rates depend on soil, variety and local guidance. "
                "Do not guess application rates."
            )
        elif any(w in q for w in ["plant", "planting", "seed", "sow"]):
            advice = (
                "Planting: Use quality seed suited to your area. Plant when "
                "soil moisture is adequate and rainfall is established. Follow "
                "the recommended spacing for your variety and avoid waterlogged soil."
            )
        elif any(w in q for w in ["pest", "disease", "worm", "yellow", "spots"]):
            advice = (
                "Pests and diseases: Inspect leaves, stems and maize cobs. "
                "Describe the symptoms or share a clear photo with an extension "
                "officer for identification. Do not apply pesticides before "
                "identifying the problem."
            )
        elif any(w in q for w in ["harvest", "storage", "dry", "mould", "mold"]):
            advice = (
                "Harvest and storage: Harvest mature maize and dry it properly "
                "before storage. Keep grain in a clean, dry place and protect "
                "it from moisture, insects and rodents."
            )
        elif any(w in q for w in ["market", "price", "sell", "buyer"]):
            advice = (
                "Markets: Compare offers from several buyers and account for "
                "transport and storage costs. This prototype does not have live "
                "market prices; verify current prices locally."
            )
        elif any(w in q for w in ["weather", "rain", "drought", "climate"]):
            advice = (
                "Weather: Check a reliable local forecast before planting or "
                "fertilizing. Conserve soil moisture and avoid applying fertilizer "
                "immediately before heavy rain."
            )
        else:
            advice = (
                "Please describe the maize crop stage and the main problem. "
                "For location-specific advice, consult your local agricultural "
                "extension officer. This free prototype does not provide live "
                "weather or market data."
            )

        return f"Agri-Vincent AI — Maize advice\nLocation: {location or 'Not specified'}\n\n{advice}"

    if language == "Français":
        if any(w in q for w in ["fertilis", "urée", "dap", "engrais"]):
            advice = (
                "Engrais : appliquez l'engrais de fond selon les recommandations "
                "locales. L'apport d'azote se fait souvent au début de la croissance, "
                "environ 3 à 4 semaines après la levée, mais le moment et la dose "
                "dépendent du sol et des conseils locaux. Ne devinez pas les doses."
            )
        elif any(w in q for w in ["planter", "semis", "graine"]):
            advice = (
                "Semis : utilisez des semences de qualité adaptées à votre région. "
                "Semez lorsque l'humidité du sol est suffisante et suivez l'espacement "
                "recommandé pour la variété."
            )
        elif any(w in q for w in ["maladie", "ravageur", "chenille", "feuille"]):
            advice = (
                "Maladies et ravageurs : examinez les feuilles, les tiges et les épis. "
                "Faites identifier le problème par un agent agricole avant d'utiliser "
                "un pesticide."
            )
        elif any(w in q for w in ["récolte", "stockage", "sécher"]):
            advice = (
                "Récolte et stockage : récoltez à maturité, séchez correctement le maïs "
                "et stockez-le dans un endroit propre et sec, à l'abri de l'humidité "
                "et des ravageurs."
            )
        elif any(w in q for w in ["marché", "prix", "vendre", "acheteur"]):
            advice = (
                "Marché : comparez plusieurs offres et tenez compte du transport et "
                "du stockage. Ce prototype ne fournit pas les prix en temps réel."
            )
        else:
            advice = (
                "Précisez le stade de la culture et le problème observé. Consultez "
                "un conseiller agricole local pour des recommandations adaptées. "
                "Ce prototype ne fournit pas de météo en temps réel."
            )

        return f"Agri-Vincent AI — Conseils sur le maïs\nLieu : {location or 'Non précisé'}\n\n{advice}"

    if any(w in q for w in ["ifumbire", "urea", "dap", "ifumbire", "gufumbira"]):
        advice = (
            "IFUMBIRE KU BIGORI\n"
            "• Ifumbire ishyirwa igihe cyo gutera igomba gukurikiza amabwiriza y'inzobere z'ubuhinzi.\n"
            "• Ifumbire irimo azote, nka UREA, akenshi ikoreshwa mu ntangiriro yo gukura kw'ibigori, hafi ibyumweru 3–4 bimaze kumera. Igihe nyacyo n'ingano biterwa n'ubwoko bw'ibigori, ubutaka n'amabwiriza y'aho uhinga.\n"
            "• Yishyire kure gato y'uruti kandi uyitwikire n'ubutaka; ntuyishyire ku mababi.\n"
            "• Irinde kuyikoresha mbere y'imvura nyinshi. Ntugakeke ingano y'ifumbire; kurikiza amabwiriza ya RAB/MINAGRI."
        )
    elif any(w in q for w in ["tera", "gutera", "imbuto", "umurima", "intera"]):
        advice = (
            "GUTERA IBIGORI\n"
            "• Koresha imbuto nziza zemewe kandi zibereye aho uhinga.\n"
            "• Tera igihe ubutaka bufite ubuhehere buhagije kandi imvura yatangiye neza.\n"
            "• Kurikiza intera yo gutera isabwa ku bwoko bw'imbuto ukoresha.\n"
            "• Irinde gutera mu butaka bwuzuyemo amazi.\n"
            "• Ku gihe nyacyo cyo gutera muri Katabagemu, banza urebe iteganyagihe n'inama z'abakozi b'ubuhinzi."
        )
    elif any(w in q for w in ["indwara", "udukoko", "inyo", "ibibabi", "by'umuhondo", "ibyago"]):
        advice = (
            "INDWARA N'UDUKOKO\n"
            "• Genzura amababi, ibiti n'ibigori buri gihe.\n"
            "• Reba ibimenyetso: amabara adasanzwe, imyobo, inyo cyangwa kubora.\n"
            "• Gerageza gusobanura ibimenyetso neza cyangwa werekane ifoto umukozi w'ubuhinzi.\n"
            "• Ntukoreshe umuti utaramenya ikibazo; kurikiza amabwiriza y'umuti n'inama z'inzobere."
        )
    elif any(w in q for w in ["isarura", "gusaru", "kubika", "kumisha", "ibigori byumye"]):
        advice = (
            "GUSARURA NO KUBIKA\n"
            "• Sarura ibigori byeze neza.\n"
            "• Banza wumishe ibigori bihagije mbere yo kubibika.\n"
            "• Bika mu bubiko busukuye kandi bwumutse, wirinde amazi, udukoko n'imbeba.\n"
            "• Genzura ibigori biri mu bubiko kenshi kugira ngo umenye ibimenyetso byo kubora."
        )
    elif any(w in q for w in ["isoko", "igiciro", "kugurisha", "umuguzi"]):
        advice = (
            "ISOKO RY'IBIGORI\n"
            "• Baza abaguzi benshi ugereranye ibiciro.\n"
            "• Bara amafaranga y'ubwikorezi, kubika no gutunganya umusaruro.\n"
            "• Shaka abaguzi mbere y'isarura niba bishoboka.\n"
            "• Iyi prototype nta biciro by'isoko byo muri iki gihe itanga; banza ubyemeze ku isoko ryo hafi."
        )
    elif any(w in q for w in ["imvura", "ikirere", "izuba", "amapfa", "amapfa"]):
        advice = (
            "IKIRERE N'UBUHINZI\n"
            "• Kurikirana iteganyagihe ryizewe mbere yo gutera cyangwa gukoresha ifumbire.\n"
            "• Bika ubuhehere mu butaka uko bishoboka kandi urinde ubutaka isuri.\n"
            "• Irinde gushyira ifumbire mbere y'imvura nyinshi.\n"
            "• Iyi prototype ntitanga iteganyagihe ry'ako kanya."
        )
    else:
        advice = (
            "Murakoze kubaza Agri-Vincent AI!\n"
            "Mpa amakuru arambuye: ibigori bigeze mu kihe cyiciro cyo gukura, "
            "kandi ikibazo nyamukuru ni ikihe?\n"
            "Iyi ni prototype y'ubuntu itanga inama z'ibanze; nta makuru y'ikirere "
            "cyangwa ibiciro by'amasoko yo muri iki gihe ifite. Ku bibazo bikomeye, "
            "ganira n'umukozi w'ubuhinzi wa RAB/MINAGRI."
        )

    return (
        f"Agri-Vincent AI — Inama ku bigori\n"
        f"Aho uhinga: {location or 'Ntabwo wahagaragaje'}\n\n{advice}"
    )
