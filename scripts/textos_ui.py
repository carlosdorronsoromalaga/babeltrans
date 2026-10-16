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
