
import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

LANGUAGES = {
    "rw": "Kinyarwanda",
    "en": "English",
    "fr": "Français",
    "sw": "Kiswahili",
    "am": "አማርኛ (Amharic)",
    "ha": "Hausa",
    "yo": "Yorùbá",
    "zu": "isiZulu",
    "pt": "Português",
    "es": "Español",
    "ar": "العربية",
    "zh": "中文",
}

TEXTS = {
    "rw": {
        "title": "Agri-Vincent AI",
        "subtitle": "Umufasha mu buhinzi bw'ibigori",
        "location": "Aho uhinga",
        "location_hint": "Urugero: Nyagatare, Katabagemu",
        "language": "Hitamo ururimi",
        "question": "Andika ikibazo cyawe",
        "question_hint": "Urugero: Ni ryari nakoresha UREA ku bigori?",
        "button": "Shaka inama",
        "about": "Uko ikora",
        "about_text": "Iyi ni prototype y'ubuntu itanga inama z'ibanze ku bigori. Nta makuru y'ako kanya y'ikirere cyangwa ibiciro by'amasoko ifite.",
        "fertilizer": "IFUMBIRE: Koresha ifumbire ukurikije amabwiriza y'inzobere z'ubuhinzi n'ibikubiye ku gikapu cyayo. Ifumbire irimo azote nka UREA ishobora gukoreshwa mu ntangiriro yo gukura kw'ibigori, ariko igihe n'ingano biterwa n'ubutaka n'amabwiriza y'aho uhinga. Ntugakeke ingano.",
        "planting": "GUTERA: Koresha imbuto nziza zemewe zibereye aho uhinga. Tera igihe ubutaka bufite ubuhehere buhagije, ukurikize intera isabwa ku bwoko bw'imbuto. Irinde ubutaka bwuzuyemo amazi.",
        "pests": "INDWARA N'UDUKOKO: Reba amababi, ibiti n'ibigori ushakishe ibimenyetso by'indwara cyangwa udukoko. Sobanurira umukozi w'ubuhinzi ikibazo cyangwa umwereke ifoto. Ntukoreshe imiti utaramenya ikibazo kandi ukurikize amabwiriza yayo.",
        "harvest": "ISARURA NO KUBIKA: Sarura ibigori byeze neza. Banza ubyumishe bihagije mbere yo kubibika. Bika ahantu hasukuye, humutse, hirindwa amazi, udukoko n'imbeba.",
        "market": "ISOKO: Gereranya ibiciro by'abaguzi batandukanye. Bara amafaranga y'ubwikorezi, kubika no gutunganya umusaruro. Iyi porogaramu ntitanga ibiciro by'ako kanya; banza ubyemeze ku isoko ryo hafi.",
        "weather": "IKIRERE: Kurikirana iteganyagihe ryizewe mbere yo gutera cyangwa gufumbira. Irinde gukoresha ifumbire mbere y'imvura nyinshi. Iyi prototype ntitanga iteganyagihe ry'ako kanya.",
        "general": "Sobanura ikibazo ufite, icyiciro ibigori bigezeho n'ibimenyetso wabonye. Ushobora kugisha inama umukozi w'ubuhinzi wa RAB/MINAGRI. Iyi prototype itanga inama z'ibanze gusa.",
        "result": "Inama ku bigori",
        "empty": "Banza wandike ikibazo cyawe.",
    },
    "en": {
        "title": "Agri-Vincent AI",
        "subtitle": "Your maize farming assistant",
        "location": "Your location",
        "location_hint": "Example: Nyagatare, Katabagemu",
        "language": "Choose language",
        "question": "Enter your question",
        "question_hint": "Example: When should I apply UREA to maize?",
        "button": "Get advice",
        "about": "How it works",
        "about_text": "This free prototype provides basic maize-farming advice. It does not provide live weather forecasts or current market prices.",
        "fertilizer": "FERTILIZER: Apply fertilizer according to local agricultural recommendations and the product label. Nitrogen fertilizer such as UREA may be applied during early maize growth, but timing and rates depend on soil and local guidance. Never guess the rate.",
        "planting": "PLANTING: Use quality seed suited to your area. Plant when soil moisture is adequate and follow the recommended spacing for your variety. Avoid waterlogged soil.",
        "pests": "PESTS AND DISEASES: Inspect leaves, stems and cobs for symptoms. Describe the problem or show a clear photo to an agricultural extension officer. Do not apply pesticides before identifying the problem; follow the product label.",
        "harvest": "HARVEST AND STORAGE: Harvest mature maize and dry it properly before storage. Store grain in a clean, dry place protected from moisture, insects and rodents.",
        "market": "MARKETS: Compare offers from several buyers. Include transport, storage and handling costs. This prototype does not provide live market prices; verify current prices locally.",
        "weather": "WEATHER: Check a reliable local forecast before planting or applying fertilizer. Avoid applying fertilizer immediately before heavy rain. This prototype has no live weather data.",
        "general": "Please describe the crop's growth stage and the problem you observe. Ask a local agricultural extension officer for advice specific to your farm. This prototype provides basic guidance only.",
        "result": "Maize farming advice",
        "empty": "Please enter a question first.",
    },
    "fr": {
        "title": "Agri-Vincent AI",
        "subtitle": "Votre assistant pour la culture du maïs",
        "location": "Votre localisation",
        "location_hint": "Exemple : Nyagatare, Katabagemu",
        "language": "Choisir la langue",
        "question": "Écrivez votre question",
        "question_hint": "Exemple : Quand appliquer l'urée au maïs ?",
        "button": "Obtenir des conseils",
        "about": "Comment ça marche",
        "about_text": "Ce prototype gratuit fournit des conseils de base sur le maïs. Il ne fournit ni prévisions météo en direct ni prix actuels du marché.",
        "fertilizer": "ENGRAIS : Utilisez les engrais selon les recommandations agricoles locales et l'étiquette du produit. L'urée peut être utilisée au début de la croissance, mais le moment et la dose dépendent du sol et des conseils locaux. Ne devinez jamais les doses.",
        "planting": "SEMIS : Utilisez des semences de qualité adaptées à votre région. Semez lorsque le sol est suffisamment humide et respectez l'espacement recommandé. Évitez les sols inondés.",
        "pests": "RAVAGEURS ET MALADIES : Examinez les feuilles, les tiges et les épis. Décrivez les symptômes ou montrez une photo à un conseiller agricole. N'utilisez pas de pesticide avant d'avoir identifié le problème.",
        "harvest": "RÉCOLTE ET STOCKAGE : Récoltez le maïs à maturité et séchez-le correctement. Stockez-le dans un endroit propre et sec, à l'abri de l'humidité, des insectes et des rongeurs.",
        "market": "MARCHÉ : Comparez les offres de plusieurs acheteurs et calculez les coûts de transport et de stockage. Ce prototype ne fournit pas les prix en temps réel ; vérifiez-les localement.",
        "weather": "MÉTÉO : Consultez des prévisions locales fiables avant de semer ou de fertiliser. Évitez d'appliquer l'engrais juste avant de fortes pluies. Ce prototype ne dispose pas de données météo en direct.",
        "general": "Précisez le stade de croissance du maïs et le problème observé. Consultez un conseiller agricole local pour des recommandations adaptées. Ce prototype fournit uniquement des conseils de base.",
        "result": "Conseils pour le maïs",
        "empty": "Veuillez d'abord saisir une question.",
    },
    "sw": {
        "title": "Agri-Vincent AI",
        "subtitle": "Msaidizi wako wa kilimo cha mahindi",
        "location": "Eneo lako",
        "location_hint": "Mfano: Nyagatare, Katabagemu",
        "language": "Chagua lugha",
        "question": "Andika swali lako",
        "question_hint": "Mfano: Ni lini nitumie UREA kwenye mahindi?",
        "button": "Pata ushauri",
        "about": "Jinsi inavyofanya kazi",
        "about_text": "Programu hii ya majaribio ya bure hutoa ushauri wa msingi kuhusu mahindi. Haina utabiri wa hali ya hewa wa moja kwa moja au bei za sasa za soko.",
        "fertilizer": "MBolea: Tumia mbolea kulingana na ushauri wa wataalamu wa kilimo wa eneo lako na maelekezo ya bidhaa. UREA inaweza kutumika wakati mahindi yanaanza kukua, lakini muda na kiasi hutegemea udongo na ushauri wa eneo lako. Usikisie kipimo.",
        "planting": "KUPANDA: Tumia mbegu bora zinazofaa eneo lako. Panda udongo unapokuwa na unyevu wa kutosha na fuata nafasi inayopendekezwa kwa aina ya mbegu. Epuka udongo wenye maji mengi.",
        "pests": "WADUDU NA MAGONJWA: Kagua majani, mashina na mahindi. Eleza dalili au onyesha picha kwa afisa ugani wa kilimo. Usitumie dawa kabla ya kutambua tatizo.",
        "harvest": "KUVUNA NA KUHIFADHI: Vuna mahindi yaliyokomaa na uyakaushe vizuri. Hifadhi mahindi sehemu safi na kavu, mbali na maji, wadudu na panya.",
        "market": "SOKO: Linganisha bei kutoka kwa wanunuzi mbalimbali na uhesabu gharama za usafiri na uhifadhi. Programu hii haina bei za sasa za soko; thibitisha bei eneo lako.",
        "weather": "HALI YA HEWA: Angalia utabiri wa eneo lako kabla ya kupanda au kuweka mbolea. Epuka kuweka mbolea kabla ya mvua kubwa. Programu hii haina taarifa za hali ya hewa za moja kwa moja.",
        "general": "Eleza hatua ya ukuaji wa mahindi na tatizo unaloona. Wasiliana na afisa ugani wa kilimo wa eneo lako kwa ushauri unaofaa shamba lako. Programu hii hutoa ushauri wa msingi tu.",
        "result": "Ushauri wa kilimo cha mahindi",
        "empty": "Tafadhali andika swali kwanza.",
    },
    "am": {
        "title": "Agri-Vincent AI",
        "subtitle": "የበቆሎ እርሻ አጋዥዎ",
        "location": "የእርሻ ቦታ",
        "location_hint": "ምሳሌ፦ Nyagatare, Katabagemu",
        "language": "ቋንቋ ይምረጡ",
        "question": "ጥያቄዎን ያስገቡ",
        "question_hint": "ምሳሌ፦ ዩሪያን መቼ መጠቀም አለብኝ?",
        "button": "ምክር ያግኙ",
        "about": "እንዴት እንደሚሰራ",
        "about_text": "ይህ ነፃ የሙከራ ፕሮግራም ስለ በቆሎ እርሻ መሠረታዊ ምክር ይሰጣል። የቀጥታ የአየር ሁኔታ ወይም የገበያ ዋጋ መረጃ የለውም።",
        "fertilizer": "ማዳበሪያ፦ ማዳበሪያን በአካባቢያዊ የግብርና ባለሙያዎች ምክርና በምርቱ መለያ መሠረት ይጠቀሙ። የዩሪያ ጊዜና መጠን በአፈርና በአካባቢያዊ ምክር ይወሰናል። መጠንን በግምት አይወስኑ።",
        "planting": "መዝራት፦ ለአካባቢዎ የሚስማሙ ጥራት ያላቸውን ዘሮች ይጠቀሙ። አፈሩ በቂ እርጥበት ሲኖረው ይዝሩ፤ የሚመከረውን የዘር ርቀት ይከተሉ።",
        "pests": "ተባዮችና በሽታዎች፦ ቅጠሎችን፣ ግንዶችንና በቆሎን ይመርምሩ። ችግሩን ለግብርና ባለሙያ ያሳዩ። ችግሩን ከመለየት በፊት ፀረ-ተባይ አይጠቀሙ።",
        "harvest": "መሰብሰብና ማከማቸት፦ የደረሰ በቆሎ ይሰብስቡ፣ በቂ ያድርቁት፣ ከዚያም በንጹህና ደረቅ ቦታ ያከማቹት።",
        "market": "ገበያ፦ ከተለያዩ ገዢዎች ዋጋ ያነጻጽሩ፣ የመጓጓዣና የማከማቻ ወጪዎችንም ያስሉ። ይህ ፕሮግራም የቀጥታ የገበያ ዋጋ አይሰጥም።",
        "weather": "የአየር ሁኔታ፦ ከመዝራት ወይም ማዳበሪያ ከመጠቀም በፊት የአካባቢዎን ትንበያ ይመልከቱ። ይህ ፕሮግራም የቀጥታ የአየር ሁኔታ መረጃ የለውም።",
        "general": "የበቆሎውን የእድገት ደረጃና ያዩትን ችግር ይግለጹ። ለአካባቢዎ ተስማሚ ምክር ከግብርና ባለሙያ ያግኙ።",
        "result": "የበቆሎ እርሻ ምክር",
        "empty": "እባክዎ መጀመሪያ ጥያቄ ያስገቡ።",
    },
    "ha": {
        "title": "Agri-Vincent AI",
        "subtitle": "Mataimakin noman masara",
        "location": "Wurin gonar ku",
        "location_hint": "Misali: Nyagatare, Katabagemu",
        "language": "Zaɓi harshe",
        "question": "Rubuta tambayarku",
        "question_hint": "Misali: Yaushe zan yi amfani da UREA?",
        "button": "Nemi shawara",
        "about": "Yadda yake aiki",
        "about_text": "Wannan manhajar gwaji ce ta kyauta da ke ba da shawara ta asali kan noman masara. Ba ta da hasashen yanayi ko farashin kasuwa na yanzu.",
        "fertilizer": "TAKIN ƘASA: Yi amfani da taki bisa shawarar ƙwararrun noma na yankinku da umarnin samfurin. Lokaci da adadin UREA sun danganta da ƙasa da shawarar yankinku. Kada ku yi hasashen adadi.",
        "planting": "SHUKA: Yi amfani da ingantattun iri da suka dace da yankinku. Shuka lokacin da ƙasa ke da isasshen danshi kuma ku bi tazarar da aka ba da shawara. Guji ƙasa mai cike da ruwa.",
        "pests": "ƘWARO DA CUTUTTUKA: Duba ganye, kara da kunun masara. Bayyana alamun ko nuna hoto ga jami'in fadada aikin gona. Kada ku yi amfani da maganin ƙwari kafin a gano matsalar.",
        "harvest": "GIRBI DA AJIYA: Girbe masara da ta nuna balaga, sannan a busar da ita sosai. Ajiye ta a wuri mai tsabta da bushewa, nesa da danshi, ƙwari da beraye.",
        "market": "KASUWA: Kwatanta farashin masu saye daban-daban kuma ku lissafa kuɗin sufuri da ajiya. Wannan manhaja ba ta da farashin kasuwa na yanzu; ku tabbatar da farashin a yankinku.",
        "weather": "YANAYI: Duba sahihin hasashen yanayi kafin shuka ko amfani da taki. Guji sanya taki kafin ruwan sama mai yawa. Wannan manhaja ba ta da bayanan yanayi na kai tsaye.",
        "general": "Bayyana matakin girman masarar da matsalar da kuka gani. Nemi shawarar jami'in noma na yankinku. Wannan manhaja tana ba da shawara ta asali kawai.",
        "result": "Shawarar noman masara",
        "empty": "Da fatan za a fara rubuta tambaya.",
    },
    "yo": {
        "title": "Agri-Vincent AI",
        "subtitle": "Olùrànlọ́wọ́ iṣẹ́ àgbẹ̀ àgbàdo",
        "location": "Ibi oko rẹ",
        "location_hint": "Àpẹẹrẹ: Nyagatare, Katabagemu",
        "language": "Yan èdè",
        "question": "Kọ ìbéèrè rẹ",
        "question_hint": "Àpẹẹrẹ: Nígbà wo ni mo yẹ kí n lo UREA?",
        "button": "Gba ìmọ̀ràn",
        "about": "Bí ó ṣe ń ṣiṣẹ́",
        "about_text": "Ètò ìdánwò ọ̀fẹ́ yìí ń fúnni ní ìmọ̀ràn ìpìlẹ̀ nípa àgbàdo. Kò ní ìsọfúnni ojú-ọjọ́ tàbí iye ọjà tó wà lọ́wọ́lọ́wọ́.",
        "fertilizer": "AJÓNILÈ: Lo ajónilè gẹ́gẹ́ bí ìmọ̀ràn àwọn ògbóǹtarìgì iṣẹ́ àgbẹ̀ àti ìtọ́nisọ́nà ọjà. Àkókò àti iye UREA dá lórí ilẹ̀ àti ìmọ̀ràn agbègbè. Má ṣe sọ iye rẹ̀ láìmọ̀.",
        "planting": "GBÍGBÌN: Lo irúgbìn tó dára tó sì yẹ fún agbègbè rẹ. Gbìn nígbà tí ilẹ̀ bá ní ọrinrin tó, kí o sì tẹ̀lé ààyè tí a dámọ̀ràn. Yẹra fún ilẹ̀ tó kún fún omi.",
        "pests": "KOKORO ÀTI ÀÌSÀN: Ṣàyẹ̀wò ewé, èso àti èso àgbàdo. Fi àmì àìsàn hàn sí òṣìṣẹ́ iṣẹ́ àgbẹ̀. Má ṣe lo oògùn kí a tó mọ ìṣòro náà.",
        "harvest": "IKÓRÈ ÀTI ÌPAMỌ́: Kórè àgbàdo tó dàgbà, kí o sì gbẹ ẹ́ dáadáa. Pa á mọ́ sí ibi mímọ́ àti gbígbẹ, kí omi, kokoro àti eku má bà á jẹ́.",
        "market": "ỌJÀ: Fi owó àwọn oníbàárà oríṣiríṣi wé ara wọn, kí o sì ka owó ìrìnàjò àti ìpamọ́ sí i. Ètò yìí kò ní owó ọjà tó wà lọ́wọ́lọ́wọ́.",
        "weather": "OJÚ ỌJỌ́: Ṣàyẹ̀wò àsọtẹ́lẹ̀ ojú-ọjọ́ tó ṣeé gbẹ́kẹ̀lé kí o tó gbìn tàbí lo ajónilè. Ètò yìí kò ní ìsọfúnni ojú-ọjọ́ ní àkókò gidi.",
        "general": "Ṣàlàyé ìpele ìdàgbàsókè àgbàdo àti ìṣòro tí o rí. Bá òṣìṣẹ́ iṣẹ́ àgbẹ̀ agbègbè rẹ sọ̀rọ̀ fún ìmọ̀ràn tó bá oko rẹ mu.",
        "result": "Ìmọ̀ràn iṣẹ́ àgbẹ̀ àgbàdo",
        "empty": "Jọ̀wọ́ kọ ìbéèrè kọ́kọ́.",
    },
    "zu": {
        "title": "Agri-Vincent AI",
        "subtitle": "Umsizi wakho wokulima ummbila",
        "location": "Indawo yepulazi lakho",
        "location_hint": "Isibonelo: Nyagatare, Katabagemu",
        "language": "Khetha ulimi",
        "question": "Bhala umbuzo wakho",
        "question_hint": "Isibonelo: Kufanele ngifake nini i-UREA?",
        "button": "Thola iseluleko",
        "about": "Indlela esebenza ngayo",
        "about_text": "Lolu hlelo lwamahhala lokuhlola lunikeza izeluleko eziyisisekelo ngokulima ummbila. Alunaso isimo sezulu esibukhoma noma amanani emakethe amanje.",
        "fertilizer": "UMANYO: Sebenzisa umanyolo ngokulandela izeluleko zochwepheshe bezolimo bendawo kanye nemiyalelo yomkhiqizo. Isikhathi nenani le-UREA kuncike enhlabathini nasezelulekweni zendawo. Ungaqageli inani.",
        "planting": "UKUTSHALA: Sebenzisa imbewu esezingeni elifanele indawo yakho. Tshala lapho inhlabathi inomswakama owanele futhi ulandele ibanga elinconyiwe. Gwema inhlabathi egcwele amanzi.",
        "pests": "IZINAMBUZANE NEZIFO: Hlola amaqabunga, iziqu nezikhwebu. Chaza izimpawu noma ubonise isithombe kusisebenzi sezolimo. Ungasebenzisi isibulala-zinambuzane ungakawazi umthombo wenkinga.",
        "harvest": "UKUVUNA NOKUGCINA: Vuna ummbila ovuthiwe bese uwomisa kahle. Wugcine endaweni ehlanzekile neyomile, uvikeleke emanzini, ezinambuzaneni nasemagundaneni.",
        "market": "IMAKETHE: Qhathanisa amanani abathengi abahlukene, ubale nezindleko zokuthutha nokugcina. Lolu hlelo alunawo amanani emakethe esikhathi samanje.",
        "weather": "ISIMO SEZULU: Hlola isibikezelo sendawo ngaphambi kokutshala noma ukufaka umanyolo. Gwema ukufaka umanyolo ngaphambi kwemvula enkulu. Lolu hlelo alunalo ulwazi lwesimo sezulu esibukhoma.",
        "general": "Chaza isigaba sokukhula kommbila nenkinga oyibonayo. Cela iseluleko kusisebenzi sezolimo sendawo. Lolu hlelo lunikeza izeluleko eziyisisekelo kuphela.",
        "result": "Iseluleko sokulima ummbila",
        "empty": "Sicela uqale ubhale umbuzo.",
    },
    "pt": {
        "title": "Agri-Vincent AI",
        "subtitle": "Seu assistente para o cultivo de milho",
        "location": "Localização da sua lavoura",
        "location_hint": "Exemplo: Nyagatare, Katabagemu",
        "language": "Escolha o idioma",
        "question": "Escreva sua pergunta",
        "question_hint": "Exemplo: Quando devo aplicar UREA no milho?",
        "button": "Obter orientação",
        "about": "Como funciona",
        "about_text": "Este protótipo gratuito fornece orientações básicas sobre o milho. Não oferece previsão meteorológica ao vivo nem preços atuais de mercado.",
        "fertilizer": "FERTILIZANTE: Use fertilizantes conforme as recomendações agrícolas locais e o rótulo do produto. O momento e a quantidade de UREA dependem do solo e da orientação local. Não adivinhe a dose.",
        "planting": "PLANTIO: Use sementes de qualidade adequadas à sua região. Plante quando o solo tiver umidade suficiente e respeite o espaçamento recomendado. Evite solos encharcados.",
        "pests": "PRAGAS E DOENÇAS: Examine folhas, caules e espigas. Descreva os sintomas ou mostre uma foto a um técnico agrícola. Não aplique pesticidas antes de identificar o problema.",
        "harvest": "COLHEITA E ARMAZENAMENTO: Colha o milho maduro e seque-o adequadamente. Guarde os grãos num local limpo e seco, protegido da humidade, insetos e roedores.",
        "market": "MERCADO: Compare propostas de vários compradores e inclua os custos de transporte e armazenamento. Este protótipo não fornece preços atuais; confirme-os localmente.",
        "weather": "CLIMA: Consulte uma previsão local confiável antes de plantar ou fertilizar. Evite aplicar fertilizante antes de chuvas fortes. Este protótipo não possui dados meteorológicos ao vivo.",
        "general": "Descreva a fase de crescimento do milho e o problema observado. Consulte um técnico agrícola local para obter orientações adequadas. Este protótipo fornece apenas informações básicas.",
        "result": "Orientação para o cultivo de milho",
        "empty": "Por favor, escreva uma pergunta primeiro.",
    },
    "es": {
        "title": "Agri-Vincent AI",
        "subtitle": "Tu asistente para el cultivo de maíz",
        "location": "Ubicación de tu cultivo",
        "location_hint": "Ejemplo: Nyagatare, Katabagemu",
        "language": "Elige el idioma",
        "question": "Escribe tu pregunta",
        "question_hint": "Ejemplo: ¿Cuándo debo aplicar UREA al maíz?",
        "button": "Obtener consejos",
        "about": "Cómo funciona",
        "about_text": "Este prototipo gratuito ofrece consejos básicos sobre el cultivo de maíz. No proporciona pronósticos meteorológicos en tiempo real ni precios actuales del mercado.",
        "fertilizer": "FERTILIZANTE: Utiliza fertilizantes siguiendo las recomendaciones agrícolas locales y la etiqueta del producto. El momento y la cantidad de UREA dependen del suelo y de las recomendaciones locales. No adivines la dosis.",
        "planting": "SIEMBRA: Utiliza semillas de calidad adecuadas para tu zona. Siembra cuando el suelo tenga suficiente humedad y respeta la distancia recomendada. Evita los suelos encharcados.",
        "pests": "PLAGAS Y ENFERMEDADES: Revisa las hojas, los tallos y las mazorcas. Describe los síntomas o muestra una foto a un técnico agrícola. No utilices pesticidas antes de identificar el problema.",
        "harvest": "COSECHA Y ALMACENAMIENTO: Cosecha el maíz maduro y sécalo correctamente. Guárdalo en un lugar limpio y seco, protegido de la humedad, los insectos y los roedores.",
        "market": "MERCADO: Compara las ofertas de varios compradores e incluye los costes de transporte y almacenamiento. Este prototipo no proporciona precios actuales; compruébalos localmente.",
        "weather": "CLIMA: Consulta un pronóstico local fiable antes de sembrar o fertilizar. Evita aplicar fertilizante antes de lluvias intensas. Este prototipo no tiene datos meteorológicos en tiempo real.",
        "general": "Describe la etapa de crecimiento del maíz y el problema observado. Consulta a un técnico agrícola local para obtener recomendaciones adecuadas. Este prototipo ofrece orientación básica.",
        "result": "Consejos para el cultivo de maíz",
        "empty": "Por favor, escribe primero una pregunta.",
    },
    "ar": {
        "title": "Agri-Vincent AI",
        "subtitle": "مساعدك في زراعة الذرة",
        "location": "موقع المزرعة",
        "location_hint": "مثال: Nyagatare, Katabagemu",
        "language": "اختر اللغة",
        "question": "اكتب سؤالك",
        "question_hint": "مثال: متى أستخدم اليوريا للذرة؟",
        "button": "احصل على نصيحة",
        "about": "كيف يعمل",
        "about_text": "يوفر هذا النموذج المجاني إرشادات أساسية لزراعة الذرة. لا يقدم توقعات طقس مباشرة أو أسعار السوق الحالية.",
        "fertilizer": "الأسمدة: استخدم الأسمدة وفقًا لتوصيات الخبراء الزراعيين المحليين وتعليمات المنتج. يعتمد توقيت وكمية اليوريا على التربة والإرشادات المحلية. لا تخمّن الجرعة.",
        "planting": "الزراعة: استخدم بذورًا جيدة مناسبة لمنطقتك. ازرع عندما تكون رطوبة التربة كافية واتبع المسافات الموصى بها. تجنب التربة المشبعة بالماء.",
        "pests": "الآفات والأمراض: افحص الأوراق والسيقان والكيزان. صف الأعراض أو اعرض صورة على موظف الإرشاد الزراعي. لا تستخدم المبيدات قبل تحديد المشكلة.",
        "harvest": "الحصاد والتخزين: احصد الذرة الناضجة وجففها جيدًا. خزّن الحبوب في مكان نظيف وجاف بعيدًا عن الرطوبة والحشرات والقوارض.",
        "market": "السوق: قارن عروض عدة مشترين واحسب تكاليف النقل والتخزين. لا يوفر هذا النموذج أسعار السوق الحالية؛ تحقق منها محليًا.",
        "weather": "الطقس: تحقق من توقعات محلية موثوقة قبل الزراعة أو التسميد. تجنب وضع السماد قبل الأمطار الغزيرة. لا يملك هذا النموذج بيانات طقس مباشرة.",
        "general": "اشرح مرحلة نمو الذرة والمشكلة التي لاحظتها. استشر موظف الإرشاد الزراعي المحلي للحصول على نصيحة مناسبة لمزرعتك. يقدم هذا النموذج إرشادات أساسية فقط.",
        "result": "إرشادات زراعة الذرة",
        "empty": "يرجى كتابة سؤال أولًا.",
    },
    "zh": {
        "title": "Agri-Vincent AI",
        "subtitle": "您的玉米种植助手",
        "location": "农场位置",
        "location_hint": "例如：Nyagatare, Katabagemu",
        "language": "选择语言",
        "question": "请输入您的问题",
        "question_hint": "例如：什么时候给玉米施用尿素？",
        "button": "获取建议",
        "about": "工作原理",
        "about_text": "这个免费原型提供基本的玉米种植建议，但不提供实时天气预报或当前市场价格。",
        "fertilizer": "肥料：请按照当地农业专家的建议和产品标签使用肥料。尿素的施用时间和用量取决于土壤条件及当地指导。不要猜测施肥剂量。",
        "planting": "播种：使用适合当地条件的优质种子。在土壤水分充足时播种，并遵循该品种建议的种植间距。避免在积水土壤中播种。",
        "pests": "病虫害：检查叶片、茎秆和玉米穗。向农业推广人员描述症状或出示清晰照片。在确认问题之前不要使用农药，并遵循产品标签。",
        "harvest": "收获与储存：在玉米成熟后收获，并充分干燥。将玉米储存在清洁、干燥的地方，避免潮湿、虫害和鼠害。",
        "market": "市场：比较多个买家的报价，并计算运输和储存成本。此原型不提供实时市场价格，请在当地核实当前价格。",
        "weather": "天气：在播种或施肥前查看可靠的当地天气预报。避免在大雨前施肥。此原型没有实时天气数据。",
        "general": "请描述玉米目前的生长阶段以及您观察到的问题。请咨询当地农业推广人员以获得适合您农场的建议。此原型仅提供基本指导。",
        "result": "玉米种植建议",
        "empty": "请先输入问题。",
    },
}

KEYWORDS = {
    "fertilizer": [
        "ifumbire", "urea", "dap", "gufumbira", "fertilizer",
        "fertiliser", "engrais", "urée", "mbolea", "takinkasa",
        "ajónilè", "umanyolo", "fertilizante", "abono", "سماد",
        "肥料", "尿素", "ማዳበሪያ", "تاک", "urea"
    ],
    "planting": [
        "gutera", "imbuto", "intera", "planting", "plant", "seed",
        "sow", "semis", "planter", "mbegu", "kupanda", "زرع",
        "播种", "种植", "መዝራት", "shuka", "siembra", "plantio"
    ],
    "pests": [
        "indwara", "udukoko", "inyo", "ibibabi", "pest", "disease",
        "worm", "yellow", "spots", "ravageur", "maladie", "wadudu",
        "magonjwa", "pragas", "plagas", "مرض", "آفات", "病虫害",
        "በሽታ", "ተባይ", "izinambuzane", "àìsàn"
    ],
    "harvest": [
        "isarura", "gusaru", "kubika", "kumisha", "harvest",
        "storage", "dry", "mould", "mold", "récolte", "stockage",
        "kuvuna", "kuhifadhi", "colheita", "almacenamiento",
        "حصاد", "تخزين", "收获", "储存", "መሰብሰብ", "ukuvuna"
    ],
    "market": [
        "isoko", "igiciro", "kugurisha", "umuguzi", "market",
        "price", "sell", "buyer", "marché", "prix", "vendre",
        "soko", "bei", "kuuza", "mercado", "preço", "precio",
        "سوق", "سعر", "市场", "价格", "ገበያ", "kasuwa"
    ],
    "weather": [
        "imvura", "ikirere", "izuba", "amapfa", "weather", "rain",
        "drought", "climate", "météo", "pluie", "hali ya hewa",
        "mvua", "clima", "lluvia", "tempo", "chuva", "طقس",
        "雨", "天气", "የአየር ሁኔታ"
    ],
}


def get_topic(question):
    q = question.casefold()

    for topic in (
        "fertilizer",
        "planting",
        "pests",
        "harvest",
        "market",
        "weather",
    ):
        if any(word.casefold() in q for word in KEYWORDS[topic]):
            return topic

    return "general"


def fallback_answer(question, location, language):
    language = language if language in TEXTS else "rw"
    translations = TEXTS[language]
    topic = get_topic(question)

    advice = translations[topic]
    place_label = translations["location"]
    place = location.strip() or "—"

    return (
        f"{translations['result']}\n"
        f"{place_label}: {place}\n\n"
        f"{advice}"
    )


PAGE = r"""
<!doctype html>
<html lang="{{ language }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#176b3a">
  <title>{{ t.title }}</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      padding: 22px 14px;
      background: #f2f7f1;
      color: #203328;
      font-family: Arial, "Noto Sans", sans-serif;
    }
    .container { max-width: 720px; margin: 0 auto; }
    header {
      background: #176b3a;
      color: white;
      padding: 26px 20px;
      border-radius: 18px;
      margin-bottom: 18px;
    }
    header h1 { margin: 0 0 8px; font-size: 28px; }
    header p { margin: 0; line-height: 1.6; }
    .card {
      background: white;
      border-radius: 16px;
      padding: 20px;
      margin-bottom: 16px;
      box-shadow: 0 3px 14px #183d2510;
    }
    label {
      display: block;
      font-weight: 700;
      margin: 14px 0 7px;
    }
    input, select, textarea {
      display: block;
      width: 100%;
      padding: 12px;
      border: 1px solid #ccd8ce;
      border-radius: 9px;
      font: inherit;
      background: white;
      color: #203328;
    }
    textarea { min-height: 115px; resize: vertical; }
    button {
      width: 100%;
      margin-top: 16px;
      padding: 14px;
      border: 0;
      border-radius: 10px;
      background: #176b3a;
      color: white;
      font-size: 16px;
      font-weight: 700;
      cursor: pointer;
    }
    button:active { opacity: .85; }
    .answer {
      white-space: pre-wrap;
      line-height: 1.8;
      overflow-wrap: anywhere;
    }
    .muted { color: #52655a; line-height: 1.7; }
    footer {
      text-align: center;
      color: #52655a;
      font-size: 13px;
      padding: 12px;
    }
  </style>
</head>
<body>
  <main class="container">
    <header>
      <h1>🌽 {{ t.title }}</h1>
      <p>{{ t.subtitle }}</p>
    </header>

    <section class="card">
      <form method="post">
        <label for="language">{{ t.language }}</label>
        <select id="language" name="language">
          {% for code, name in languages.items() %}
          <option value="{{ code }}"
            {% if code == language %}selected{% endif %}>
            {{ name }}
          </option>
          {% endfor %}
        </select>

        <label for="location">{{ t.location }}</label>
        <input id="location" name="location"
          maxlength="200"
          placeholder="{{ t.location_hint }}"
          value="{{ location }}">

        <label for="question">{{ t.question }}</label>
        <textarea id="question" name="question"
          maxlength="3000" required
          placeholder="{{ t.question_hint }}">{{ question }}</textarea>

        <button type="submit">{{ t.button }}</button>
      </form>
    </section>

    {% if answer %}
    <section class="card" aria-live="polite">
      <h2>🌱 {{ t.result }}</h2>
      <div class="answer">{{ answer }}</div>
    </section>
    {% endif %}

    <section class="card">
      <h3>{{ t.about }}</h3>
      <p class="muted">{{ t.about_text }}</p>
    </section>

    <footer>Agri-Vincent AI · Maize farming · Free prototype</footer>
  </main>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""
    question = ""
    location = ""
    language = "rw"

    if request.method == "POST":
        question = request.form.get("question", "").strip()[:3000]
        location = request.form.get("location", "").strip()[:200]
        language = request.form.get("language", "rw")

        if language not in LANGUAGES:
            language = "rw"

        if question:
            answer = fallback_answer(question, location, language)
        else:
            answer = TEXTS[language]["empty"]

    return render_template_string(
        PAGE,
        answer=answer,
        question=question,
        location=location,
        language=language,
        languages=LANGUAGES,
        t=TEXTS[language],
    )


@app.route("/health")
def health():
    return {"status": "ok", "app": "Agri-Vincent AI"}


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000"))
    )
