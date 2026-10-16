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
