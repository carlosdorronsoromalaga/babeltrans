"""Los pocos textos de interfaz que NO venían en la web original.

Todo el contenido (títulos, párrafos, listas, formularios, menús) sale de
contenido/<idioma>.json, que es el texto publicado tal cual. Aquí solo van
rótulos de botones y accesibilidad que la web nueva necesita y la vieja no
tenía. Si Martijn quiere cambiar alguno, es aquí.
"""

UI = {
    "es": {
        "idioma": "Español", "menu": "Menú", "saltar": "Saltar al contenido",
        "leer": "Leer más", "pedir": "Solicite presupuesto", "llamar": "Llamar",
        "escribir": "Escribir un e-mail", "contacto": "Contacto", "inicio": "Inicio",
        "obligatorio": "obligatorio", "elegir_archivo": "Adjuntar archivo",
        "enviado": "Gracias por ponerse en contacto con nosotros.",
        "error": "No se ha podido enviar. Inténtelo de nuevo o escríbanos a",
        "desde": "desde", "idiomas": "Idiomas", "servicios": "Servicios",
        "enviar": "Enviar",
    },
    "en": {
        "idioma": "English", "menu": "Menu", "saltar": "Skip to content",
        "leer": "Read more", "pedir": "Request a quote", "llamar": "Call",
        "escribir": "Send an email", "contacto": "Contact", "inicio": "Home",
        "obligatorio": "required", "elegir_archivo": "Attach file",
        "enviado": "Thank you for contacting with us.",
        "error": "The form could not be sent. Please try again or write to",
        "desde": "since", "idiomas": "Languages", "servicios": "Services",
        "enviar": "Submit",
    },
    "de": {
        "idioma": "Deutsch", "menu": "Menü", "saltar": "Zum Inhalt springen",
        "leer": "Weiterlesen", "pedir": "Kostenvoranschlag", "llamar": "Anrufen",
        "escribir": "E-Mail schreiben", "contacto": "Kontakt", "inicio": "Home",
        "obligatorio": "Pflichtfeld", "elegir_archivo": "Datei anhängen",
        "enviado": "Vielen Dank für Ihre Nachricht.",
        "error": "Das Formular konnte nicht gesendet werden. Bitte versuchen Sie es erneut oder schreiben Sie an",
        "desde": "seit", "idiomas": "Sprachen", "servicios": "Dienste",
        "enviar": "Senden",
    },
    "nl": {
        "idioma": "Nederlands", "menu": "Menu", "saltar": "Naar de inhoud",
        "leer": "Lees meer", "pedir": "Vrijblijvende offerte", "llamar": "Bellen",
        "escribir": "E-mail sturen", "contacto": "Contact", "inicio": "Home",
        "obligatorio": "verplicht", "elegir_archivo": "Bestand toevoegen",
        "enviado": "Bedankt voor uw bericht.",
        "error": "Het formulier kon niet worden verzonden. Probeer het opnieuw of schrijf naar",
        "desde": "sinds", "idiomas": "Talen", "servicios": "Diensten",
        "enviar": "Verzenden",
    },
}

# Retoques de texto que eran maquetación y no contenido: Joomla pintaba la
# primera o la última letra de otro color partiendo la palabra.
RETOQUES = {
    "TraduccioneS": "Traducciones",
}

# Las entradas de diccionario de los servicios (ver docs/DISENO.md). Palabra
# con su silabeo, pronunciación (AFI) y categoría, como en un diccionario de
# cada idioma. Las acepciones son la propia lista de servicios de la web.
ENTRADAS = {
    "es": {"traduccion": ("tra·duc·ción", "/tɾa.ðukˈθjon/", "f."),
           "interpretacion": ("in·ter·pre·ta·ción", "/in.teɾ.pɾe.taˈθjon/", "f.")},
    "en": {"traduccion": ("trans·la·tion", "/trænsˈleɪʃ(ə)n/", "n."),
           "interpretacion": ("in·ter·pret·ing", "/ɪnˈtɜːprɪtɪŋ/", "n.")},
    "de": {"traduccion": ("Über·set·zung", "/yːbɐˈzɛtsʊŋ/", "f."),
           "interpretacion": ("Dol·met·schen", "/ˈdɔlmɛtʃn̩/", "n.")},
    "nl": {"traduccion": ("ver·ta·ling", "/vərˈtaːlɪŋ/", "de"),
           "interpretacion": ("tol·ken", "/ˈtɔlkə(n)/", "ww.")},
}

# Rótulos nuevos de la v2
UI2 = {
    "es": {"ver": "Ver el servicio", "en_seccion": "En esta sección", "metodo": "Cómo trabajamos",
           "herramientas": "Herramientas", "llame": "Llámenos o escríbanos"},
    "en": {"ver": "See the service", "en_seccion": "In this section", "metodo": "How we work",
           "herramientas": "Tools", "llame": "Call or write to us"},
    "de": {"ver": "Zum Angebot", "en_seccion": "In diesem Bereich", "metodo": "Wie wir arbeiten",
           "herramientas": "Werkzeuge", "llame": "Rufen Sie uns an oder schreiben Sie uns"},
    "nl": {"ver": "Bekijk de dienst", "en_seccion": "In dit onderdeel", "metodo": "Zo werken wij",
           "herramientas": "Werktuigen", "llame": "Bel of mail ons"},
}

# ---------------------------------------------------------------- v3
# Alineación de la frase de la portada, como en una herramienta de traducción
# asistida: cada [trozo|n] se ilumina junto a los trozos con el mismo n en los
# otros idiomas. Lo que queda fuera de corchetes no tiene equivalente (el «is»
# inglés y holandés), y se ve así a propósito: es lo que pasa al traducir.
ALINEACION = {
    "es": "[Todo lo|1] [verdaderamente|2] [excelente|3] [es traducible|4]",
    "en": "[All that|1] is [truly|2] [excellent|3] [can be translated|4]",
    "de": "[Alles|1] [wirklich|2] [Herausragende|3] [ist übersetzbar|4]",
    "nl": "[Alles wat|1] [werkelijk|2] [uitmuntend|3] is, [kan worden vertaald|4]",
}

# Modismos: el original, la traducción palabra por palabra (tachada) y la buena.
# CONTENIDO NUEVO, no estaba en la web vieja: ilustra su frase «evitando
# traducciones demasiado literales». Martijn puede cambiarlos o quitarlos.
MODISMOS = {
    "es": [("de", "Ich verstehe nur Bahnhof.", "Solo entiendo estación.", "Me suena a chino."),
           ("en", "It’s raining cats and dogs.", "Llueven gatos y perros.", "Llueve a cántaros."),
           ("fr", "Poser un lapin.", "Poner un conejo.", "Dar plantón."),
           ("nl", "Nu komt de aap uit de mouw.", "Ahora sale el mono de la manga.", "Ahora se descubre el pastel."),
           ("it", "In bocca al lupo!", "¡En la boca del lobo!", "¡Mucha suerte!"),
           ("en", "It’s a piece of cake.", "Es un trozo de pastel.", "Está chupado."),
           ("en", "You’re pulling my leg.", "Me estás tirando de la pierna.", "Me estás tomando el pelo.")],
    "en": [("es", "Me suena a chino.", "It sounds Chinese to me.", "It’s all Greek to me."),
           ("de", "Das ist nicht mein Bier.", "That’s not my beer.", "That’s not my problem."),
           ("fr", "Poser un lapin.", "To put down a rabbit.", "To stand someone up."),
           ("nl", "Nu komt de aap uit de mouw.", "Now the monkey comes out of the sleeve.", "Now the cat is out of the bag."),
           ("it", "In bocca al lupo!", "In the mouth of the wolf!", "Break a leg!"),
           ("es", "Es pan comido.", "It’s eaten bread.", "It’s a piece of cake.")],
    "de": [("en", "It’s raining cats and dogs.", "Es regnet Katzen und Hunde.", "Es gießt in Strömen."),
           ("es", "Me estás tomando el pelo.", "Du nimmst mir die Haare.", "Du nimmst mich auf den Arm."),
           ("fr", "Poser un lapin.", "Ein Kaninchen hinstellen.", "Jemanden versetzen."),
           ("nl", "Nu komt de aap uit de mouw.", "Jetzt kommt der Affe aus dem Ärmel.", "Jetzt ist die Katze aus dem Sack."),
           ("it", "In bocca al lupo!", "In den Mund des Wolfes!", "Hals- und Beinbruch!"),
           ("es", "Es pan comido.", "Es ist gegessenes Brot.", "Das ist ein Kinderspiel.")],
    "nl": [("en", "It’s raining cats and dogs.", "Het regent katten en honden.", "Het regent pijpenstelen."),
           ("es", "Me estás tomando el pelo.", "Je neemt mijn haar.", "Je houdt me voor de gek."),
           ("de", "Ich verstehe nur Bahnhof.", "Ik begrijp alleen station.", "Ik snap er geen snars van."),
           ("fr", "Poser un lapin.", "Een konijn neerzetten.", "Iemand laten zitten."),
           ("it", "In bocca al lupo!", "In de bek van de wolf!", "Veel succes!"),
           ("es", "Es pan comido.", "Het is gegeten brood.", "Het is een eitje.")],
}

# La torre de Babel: «traducción» en otros idiomas, de la cima a la base. Los
# pisos están repartidos para que cada uno sea más ancho que el de encima
# (medido en pantalla el 17/10/2026: 292, 420, 473, 531, 535, 636, 672, 774 px).
TORRE = [
    [("es", "traducción")],
    [("en", "translation"), ("de", "Übersetzung")],
    [("nl", "vertaling"), ("fr", "traduction"), ("it", "traduzione")],
    [("pt", "tradução"), ("ca", "traducció"), ("eu", "itzulpena"), ("gl", "tradución")],
    [("el", "μετάφραση"), ("ru", "перевод"), ("pl", "tłumaczenie"), ("ar", "ترجمة"), ("zh", "翻译")],
    [("ja", "翻訳"), ("ko", "번역"), ("hi", "अनुवाद"), ("he", "תרגום"), ("tr", "çeviri"), ("da", "oversættelse"),
     ("fa", "ترجمه"), ("sw", "tafsiri")],
    [("fi", "käännös"), ("hu", "fordítás"), ("cs", "překlad"), ("ro", "traducere"), ("uk", "переклад"),
     ("sv", "översättning")],
    [("vi", "bản dịch"), ("id", "terjemahan"), ("bn", "অনুবাদ"), ("bg", "превод"), ("no", "oversettelse"),
     ("ga", "aistriúchán"), ("th", "การแปล")],
]

UI3 = {
    "es": {"alinear": "Pase el cursor por una palabra para ver su equivalente.",
           "alinear_tactil": "Toque una palabra para ver su equivalente.",
           "literal": "Palabra por palabra", "bien": "Traducido", "otro": "Otro ejemplo",
           "torre": "Todos los idiomas", "torre_pie": "«Traducción» en 36 idiomas."},
    "en": {"alinear": "Hover over a word to see its equivalent.",
           "alinear_tactil": "Tap a word to see its equivalent.",
           "literal": "Word for word", "bien": "Translated", "otro": "Another example",
           "torre": "All languages", "torre_pie": "“Translation” in 36 languages."},
    "de": {"alinear": "Fahren Sie über ein Wort, um seine Entsprechung zu sehen.",
           "alinear_tactil": "Tippen Sie auf ein Wort, um seine Entsprechung zu sehen.",
           "literal": "Wort für Wort", "bien": "Übersetzt", "otro": "Noch ein Beispiel",
           "torre": "Alle Sprachen", "torre_pie": "„Übersetzung“ in 36 Sprachen."},
    "nl": {"alinear": "Beweeg over een woord om het equivalent te zien.",
           "alinear_tactil": "Tik op een woord om het equivalent te zien.",
           "literal": "Woord voor woord", "bien": "Vertaald", "otro": "Nog een voorbeeld",
           "torre": "Alle talen", "torre_pie": "‘Vertaling’ in 36 talen."},
}

# ---------------------------------------------------------------- v4
# Primera capa de información de privacidad bajo cada formulario (RGPD art. 13;
# la AEPD recomienda dar lo básico junto al formulario y el resto en la
# política). Dos variantes: solicitudes (presupuesto, contacto) y candidaturas.
INFO_FORM = {
    "es": {
        "tit": "Información básica sobre protección de datos",
        "responsable": "Responsable", "finalidad": "Finalidad", "legitimacion": "Legitimación",
        "destinatarios": "Destinatarios", "derechos": "Derechos", "mas": "Más información",
        "fin_solicitud": "responder a su solicitud y, en su caso, preparar el presupuesto y realizar el encargo.",
        "leg_solicitud": "su propia solicitud (medidas precontractuales).",
        "fin_candidatura": "valorar su candidatura como colaborador. Se conserva un año.",
        "leg_candidatura": "su consentimiento.",
        "dest": "no se ceden datos a terceros, salvo obligación legal.",
        "der": "acceder, rectificar y suprimir sus datos, y otros derechos, escribiendo a",
        "ver": "en la Política de privacidad",
    },
    "en": {
        "tit": "Basic data protection information",
        "responsable": "Controller", "finalidad": "Purpose", "legitimacion": "Legal basis",
        "destinatarios": "Recipients", "derechos": "Rights", "mas": "More information",
        "fin_solicitud": "to answer your request and, where applicable, prepare the quote and carry out the job.",
        "leg_solicitud": "your own request (pre-contractual steps).",
        "fin_candidatura": "to assess your application as a collaborator. Kept for one year.",
        "leg_candidatura": "your consent.",
        "dest": "no data is passed on to third parties unless required by law.",
        "der": "access, rectify and erase your data, among other rights, by writing to",
        "ver": "in the Privacy policy",
    },
    "de": {
        "tit": "Basisinformationen zum Datenschutz",
        "responsable": "Verantwortlicher", "finalidad": "Zweck", "legitimacion": "Rechtsgrundlage",
        "destinatarios": "Empfänger", "derechos": "Rechte", "mas": "Weitere Informationen",
        "fin_solicitud": "Beantwortung Ihrer Anfrage und gegebenenfalls Kostenvoranschlag und Ausführung des Auftrags.",
        "leg_solicitud": "Ihre Anfrage (vorvertragliche Maßnahmen).",
        "fin_candidatura": "Prüfung Ihrer Bewerbung als Mitarbeiter. Speicherung für ein Jahr.",
        "leg_candidatura": "Ihre Einwilligung.",
        "dest": "keine Weitergabe an Dritte, außer bei gesetzlicher Verpflichtung.",
        "der": "Auskunft, Berichtigung, Löschung und weitere Rechte per E-Mail an",
        "ver": "in der Datenschutzerklärung",
    },
    "nl": {
        "tit": "Basisinformatie over gegevensbescherming",
        "responsable": "Verantwoordelijke", "finalidad": "Doel", "legitimacion": "Grondslag",
        "destinatarios": "Ontvangers", "derechos": "Rechten", "mas": "Meer informatie",
        "fin_solicitud": "uw aanvraag beantwoorden en zo nodig de offerte opstellen en de opdracht uitvoeren.",
        "leg_solicitud": "uw eigen aanvraag (precontractuele maatregelen).",
        "fin_candidatura": "uw sollicitatie als medewerker beoordelen. Wordt een jaar bewaard.",
        "leg_candidatura": "uw toestemming.",
        "dest": "geen verstrekking aan derden, tenzij wettelijk verplicht.",
        "der": "inzage, rectificatie, verwijdering en andere rechten, via",
        "ver": "in de privacyverklaring",
    },
}

UI4 = {
    "es": {"trabaja_txt": "Buscamos traductores e intérpretes profesionales que traduzcan a su lengua materna.",
           "error404": "Esta página no existe", "error404_txt": "Puede que la dirección haya cambiado con la web nueva. Estas son las secciones principales:"},
    "en": {"trabaja_txt": "We are looking for professional translators and interpreters who translate into their mother tongue.",
           "error404": "This page does not exist", "error404_txt": "The address may have changed with the new website. These are the main sections:"},
    "de": {"trabaja_txt": "Wir suchen professionelle Übersetzer und Dolmetscher, die in ihre Muttersprache übersetzen.",
           "error404": "Diese Seite gibt es nicht", "error404_txt": "Vielleicht hat sich die Adresse mit der neuen Website geändert. Das sind die wichtigsten Bereiche:"},
    "nl": {"trabaja_txt": "We zoeken professionele vertalers en tolken die naar hun moedertaal vertalen.",
           "error404": "Deze pagina bestaat niet", "error404_txt": "Misschien is het adres veranderd met de nieuwe website. Dit zijn de belangrijkste onderdelen:"},
}

# El lema del logo original, «| Expertos en Traducción e Interpretación |». En
# el logo era parte de la imagen y salía en castellano en todos los idiomas;
# ahora es texto, con la letra y las barras doradas del original.
LEMA = {
    "es": "Expertos en Traducción e Interpretación",
    "en": "Experts in Translation and Interpreting",
    "de": "Experten für Übersetzen und Dolmetschen",
    "nl": "Experts in vertalen en tolken",
}

# ---------------------------------------------------------------- v5
# Palabras de la torre de Babel. El reparto en pisos lo calcula construir.py
# (cada piso más ancho que el de encima), así que añadir un idioma es añadir
# una línea aquí. La primera es la cima de la versión en castellano.
PALABRAS_TORRE = [
    ("es", "traducción"), ("en", "translation"), ("de", "Übersetzung"), ("nl", "vertaling"),
    ("fr", "traduction"), ("it", "traduzione"), ("pt", "tradução"), ("ca", "traducció"),
    ("eu", "itzulpena"), ("gl", "tradución"), ("la", "translatio"), ("el", "μετάφραση"),
    ("ru", "перевод"), ("pl", "tłumaczenie"), ("ar", "ترجمة"), ("zh", "翻译"), ("ja", "翻訳"),
    ("ko", "번역"), ("hi", "अनुवाद"), ("he", "תרגום"), ("tr", "çeviri"), ("da", "oversættelse"),
    ("fa", "ترجمه"), ("sw", "tafsiri"), ("fi", "käännös"), ("hu", "fordítás"), ("cs", "překlad"),
    ("ro", "traducere"), ("uk", "переклад"), ("sv", "översättning"), ("vi", "bản dịch"),
    ("id", "terjemahan"), ("bn", "অনুবাদ"), ("bg", "превод"), ("no", "oversettelse"),
    ("ga", "aistriúchán"), ("th", "การแปล"), ("hr", "prijevod"), ("sk", "preklad"), ("sl", "prevod"),
    ("lt", "vertimas"), ("lv", "tulkojums"), ("et", "tõlge"), ("is", "þýðing"), ("mt", "traduzzjoni"),
    ("cy", "cyfieithiad"), ("sq", "përkthim"), ("hy", "թարգմանություն"), ("ka", "თარგმანი"),
    ("ur", "ترجمہ"), ("ta", "மொழிபெயர்ப்பு"), ("tl", "pagsasalin"), ("eo", "traduko"),
    ("am", "ትርጉም"), ("zu", "ukuhumusha"),
]

# Nombre de cada idioma en su propia lengua, para el selector. Para añadir un
# idioma a la web basta con su contenido/<código>.json y una línea aquí.
NOMBRES_IDIOMA = {"es": "Español", "en": "English", "de": "Deutsch", "nl": "Nederlands"}

UI5 = {
    "es": {"idioma": "Idioma", "traduciendo": "Traduciendo"},
    "en": {"idioma": "Language", "traduciendo": "Translating"},
    "de": {"idioma": "Sprache", "traduciendo": "Übersetzen"},
    "nl": {"idioma": "Taal", "traduciendo": "Vertalen"},
}

# SEO: título (<60-65 caracteres) y descripción (<155) de las páginas que más
# se buscan. Todo lo que dicen sale de la propia web (servicios, «desde 1999»,
# «todos los idiomas», traductores nativos, revisión independiente) y del
# domicilio en Madrid. Las páginas que no están aquí usan su título y su primer
# párrafo.
SEO = {
    "es": {
        "home": ("Agencia de traducción e interpretación en Madrid | Babel Translations",
                 "Traducciones técnicas, jurídicas, juradas y comerciales e interpretación en todos los idiomas. Traductores nativos y revisión independiente desde 1999."),
        "traduccion": ("Traducción técnica, jurídica y jurada | Babel Translations",
                       "Traducciones comerciales, económicas, jurídicas, técnicas y juradas, con revisión final de un traductor independiente. Presupuesto rápido y sin compromiso."),
        "interpretacion": ("Interpretación consecutiva, simultánea y jurada | Babeltrans",
                           "Intérpretes para ruedas de prensa, convenciones, negociaciones, conferencias, notarías y juicios, también por videoconferencia. Pida presupuesto."),
        "presupuesto-traduccion": ("Presupuesto de traducción sin compromiso | Babel Translations",
                                   "Envíe su documento y reciba un presupuesto de traducción rápido y sin compromiso: técnica, jurídica, jurada o comercial, en todos los idiomas."),
        "presupuesto-interpretacion": ("Presupuesto de interpretación | Babel Translations",
                                       "Pida presupuesto de interpretación consecutiva o simultánea para reuniones, convenciones, ruedas de prensa o entrevistas. Rápido y sin compromiso."),
        "quienes": ("Quiénes somos: traductores nativos desde 1999 | Babel Translations",
                    "Proveedor global de servicios lingüísticos desde 1999. Traductores que solo traducen a su lengua materna, revisión independiente y confidencialidad."),
        "contacto": ("Contacto | Babel Translations, traducción e interpretación en Madrid",
                     "Escríbanos o llámenos para pedir información sobre traducciones e interpretación en todos los idiomas."),
    },
    "en": {
        "home": ("Translation and interpreting agency in Madrid | Babel Translations",
                 "Technical, legal, sworn and commercial translation and interpreting in all languages. Native translators and independent proofreading since 1999."),
        "traduccion": ("Technical, legal and sworn translation | Babel Translations",
                       "Commercial, financial, legal, technical and sworn translations, always checked by an independent translator. Fast, no-obligation quote."),
        "interpretacion": ("Consecutive, simultaneous and sworn interpreting | Babeltrans",
                           "Interpreters for press conferences, conventions, negotiations, conferences, notaries and courts, also by videoconference. Request a quote."),
        "presupuesto-traduccion": ("Free translation quote | Babel Translations",
                                   "Send us your document and get a fast, no-obligation translation quote: technical, legal, sworn or commercial, in all languages."),
        "presupuesto-interpretacion": ("Interpreting quote | Babel Translations",
                                       "Request a quote for consecutive or simultaneous interpreting at meetings, conventions, press conferences or interviews."),
        "quienes": ("About us: native translators since 1999 | Babel Translations",
                    "Global provider of language services since 1999. Translators who only work into their mother tongue, independent proofreading and confidentiality."),
        "contacto": ("Contact | Babel Translations, translation and interpreting in Madrid",
                     "Write or call us for information about translation and interpreting in all languages."),
    },
    "de": {
        "home": ("Übersetzungs- und Dolmetschbüro in Madrid | Babel Translations",
                 "Technische, juristische, beglaubigte und Fachübersetzungen sowie Dolmetschen in allen Sprachen. Muttersprachliche Übersetzer seit 1999."),
        "traduccion": ("Technische, juristische und beglaubigte Übersetzungen | Babeltrans",
                       "Handels-, Wirtschafts-, Rechts-, technische und beglaubigte Übersetzungen, immer von einem zweiten Übersetzer geprüft. Unverbindlicher Kostenvoranschlag."),
        "interpretacion": ("Konsekutiv-, Simultan- und beeidigtes Dolmetschen | Babeltrans",
                           "Dolmetscher für Pressekonferenzen, Tagungen, Verhandlungen, Konferenzen, Notare und Gerichte, auch per Videokonferenz."),
        "presupuesto-traduccion": ("Kostenvoranschlag für Übersetzungen | Babel Translations",
                                   "Senden Sie uns Ihr Dokument und erhalten Sie einen schnellen, unverbindlichen Kostenvoranschlag für Ihre Übersetzung."),
        "presupuesto-interpretacion": ("Kostenvoranschlag für Dolmetschen | Babel Translations",
                                       "Kostenvoranschlag für Konsekutiv- oder Simultandolmetschen bei Sitzungen, Tagungen, Pressekonferenzen oder Interviews."),
        "quienes": ("Über uns: muttersprachliche Übersetzer seit 1999 | Babeltrans",
                    "Sprachdienstleister seit 1999. Übersetzer, die nur in ihre Muttersprache übersetzen, unabhängige Korrektur und Diskretion."),
        "contacto": ("Kontakt | Babel Translations, Übersetzen und Dolmetschen in Madrid",
                     "Schreiben Sie uns oder rufen Sie uns an: Übersetzungen und Dolmetschen in allen Sprachen."),
    },
    "nl": {
        "home": ("Vertaal- en tolkbureau in Madrid | Babel Translations",
                 "Technische, juridische, beëdigde en commerciële vertalingen en tolkdiensten in alle talen. Moedertaalvertalers en onafhankelijke revisie sinds 1999."),
        "traduccion": ("Technische, juridische en beëdigde vertalingen | Babel Translations",
                       "Commerciële, economische, juridische, technische en beëdigde vertalingen, altijd nagekeken door een onafhankelijke vertaler. Vrijblijvende offerte."),
        "interpretacion": ("Consecutief, simultaan en beëdigd tolken | Babel Translations",
                           "Tolken voor persconferenties, congressen, onderhandelingen, conferenties, notarissen en rechtbanken, ook via videoconferentie."),
        "presupuesto-traduccion": ("Vrijblijvende vertaalofferte | Babel Translations",
                                   "Stuur ons uw document en ontvang snel een vrijblijvende offerte voor uw vertaling, in alle talen."),
        "presupuesto-interpretacion": ("Offerte voor tolkdiensten | Babel Translations",
                                       "Vraag een offerte aan voor consecutief of simultaan tolken bij vergaderingen, congressen, persconferenties of interviews."),
        "quienes": ("Over ons: moedertaalvertalers sinds 1999 | Babel Translations",
                    "Aanbieder van taaldiensten sinds 1999. Vertalers die alleen naar hun moedertaal vertalen, onafhankelijke revisie en vertrouwelijkheid."),
        "contacto": ("Contact | Babel Translations, vertalen en tolken in Madrid",
                     "Schrijf of bel ons voor informatie over vertalingen en tolkdiensten in alle talen."),
    },
}

# ---------------------------------------------------------------- v6
# Correcciones de Martijn (Excel «Comentarios sobre la página web», 23/10/2026).
# Se aplican encima del contenido extraído de la web vieja, sin tocarlo.

# Nombre de la empresa: «Babel Translations» en todo el texto, no «BABELTRANS».
# (El dominio sigue siendo babeltrans.es, y en los datos para Google
# «BABELTRANS» queda como nombre alternativo, porque así la buscan.)
NOMBRE_EMPRESA = ("BABELTRANS", "Babel Translations")

# Etiquetas de formulario corregidas o traducidas.
ETIQUETAS = {
    "es": {"Persona contacto": "Persona de contacto"},
    "en": {"I have read and accpet the Privacy policy": "I have read and accept the Privacy policy",
           "Town": "City", "Commentaries": "Comments", "País": "Country"},
    "de": {"Stadt": "Ort"},
    "nl": {},
}
# Campos que en la web vieja no tenían etiqueta reconocible: salía el nombre
# interno del campo («Telefono») en los cuatro idiomas.
ETIQUETAS_VACIAS = {
    "es": {"Telefono": "Teléfono"},
    "en": {"Telefono": "Telephone"},
    "de": {"Telefono": "Telefon"},
    "nl": {"Telefono": "Telefoon"},
}
# Títulos de página que en la web vieja estaban en castellano en todos los idiomas.
NOMBRES_PAGINA = {
    "es": {"como-traductor": "Trabajar como traductor", "como-interprete": "Trabajar como intérprete"},
    "en": {"como-traductor": "As a translator", "como-interprete": "As an interpreter"},
    "de": {"como-traductor": "Als Übersetzer", "como-interprete": "Als Dolmetscher"},
    "nl": {"como-traductor": "Als vertaler", "como-interprete": "Als tolk"},
}
