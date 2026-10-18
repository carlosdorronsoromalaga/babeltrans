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
    "es": [("en", "It’s raining cats and dogs.", "Llueven gatos y perros.", "Llueve a cántaros."),
           ("de", "Ich verstehe nur Bahnhof.", "Solo entiendo estación.", "Me suena a chino."),
           ("nl", "Nu komt de aap uit de mouw.", "Ahora sale el mono de la manga.", "Ahora se descubre el pastel.")],
    "en": [("es", "Me suena a chino.", "It sounds Chinese to me.", "It’s all Greek to me."),
           ("de", "Das ist nicht mein Bier.", "That’s not my beer.", "That’s not my problem."),
           ("nl", "Nu komt de aap uit de mouw.", "Now the monkey comes out of the sleeve.", "Now the cat is out of the bag.")],
    "de": [("en", "It’s raining cats and dogs.", "Es regnet Katzen und Hunde.", "Es gießt in Strömen."),
           ("es", "Me estás tomando el pelo.", "Du nimmst mir die Haare.", "Du nimmst mich auf den Arm."),
           ("nl", "Nu komt de aap uit de mouw.", "Jetzt kommt der Affe aus dem Ärmel.", "Jetzt ist die Katze aus dem Sack.")],
    "nl": [("en", "It’s raining cats and dogs.", "Het regent katten en honden.", "Het regent pijpenstelen."),
           ("es", "Me estás tomando el pelo.", "Je neemt mijn haar.", "Je houdt me voor de gek."),
           ("de", "Ich verstehe nur Bahnhof.", "Ik begrijp alleen station.", "Ik snap er geen snars van.")],
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
