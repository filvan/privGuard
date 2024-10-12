init_menu_welcome = "Bienvenido a LibreTaxi 2.0!"

ask_location_menu_click_next = "Pulse \"Siguiente\" (desde teléfono celular) para compartir su ubicación. O puede 📎 Clip -> 📍 Ubicación para mejor privacidad."

ask_location_menu_next_button = "Siguiente"

feed_menu_greeting = "Encontraras 🚗 conductores y 👋 pasajeros aquí."

feed_menu_search_button = "Encontrar 🚗 o 👋"

feed_menu_location_button = "📍 Cambiar ubicación"

feed_menu_location_changed = "👌 Ubicación actualizada"

feed_menu_error = "😕 No puedo entender su elección, intente hacer clic 🔳 abajo 👇"

post_menu_report_button = "☝️️Reportar ⚠️"

post_menu_wait = "🕙 Esperar por 5 minutos"

# Do not translate /cancel
post_menu_copy_and_paste = "Copiar & pegar texto que empieza con 🚗 (conductor) o 👋 (pasajero) en el siguiente formato, or /cancel, ejemplos:"

post_menu_driver_example = "🚗 Viaje ofrecido\nDesde: foobar\nHasta: Aerpuerto\nFecha: hoy\nHorario: ahora\nPago: efectivo, venmo"

post_menu_passenger_example = "👋 Viaje deseado\nDesde: foobar, 42\nHasta: El centro\nFecha: hoy\nHorario: ahora\nPasajero: 1"

# Here is how we check if the user just copied the text or changed it. It's just a string from the previous postings.
# Note how we have "foobar" in both postings above. It's the magic string, non-existent address, you should think
# about an address that doesn't exist in your own language. Or you can leave "foobar" if you didn't get it ;)
# Keep it lowercased!
validation_dummy_addr_lowercase = "foobar"

post_menu_sent = "✅ Enviados a usuarios de hasta (25km) and to @libretaxi_all"

# "Contact" is a verb here. For example, we'll have a posting where it says "blabla, I'm looking for ride, contact @username".
# So you're translating this verb "contact" below.
post_menu_via = "Contactar"

# When we have an error we say something like:
# "Your input is invalid, try again or /cancel"
# So this "or" part needs to be translated below.
post_menu_or = "o"

validation_text_too_long = "🚫 El texto es muy largo, máximo 300 caracteres (tienes %d)"

validation_text_too_short = "🚫 El texto es muy corto, minimo 20 caracteres (tienes %d)"

validation_prefix = "🚫 El texto es debe empezar con 🚗 o 👋"

validation_no_at = "🚫 El simbolo @ no esta permitido"

validation_no_offensive_language = "🚫 Por favor sin malas palabras 🤦"

validation_change_from_to = "🚫 Publica de nuevo, cambia \"Desde\" y \"Hasta\""

validation_empty_lines1 = "🚫 Solo 2 líneas vacías como máximo (tienes %d)"

validation_empty_lines2 = "🚫 Solo 9 líneas máximas por favor (tienes %d)"

validation_min_lines = "🚫 Al menos 5 líneas por favor (tienes %d)"

main_welcome_link = "https://telegra.ph/LibreTaxi-20---te-va-a-enamorar-02-09"
