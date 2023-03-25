init_menu_welcome = "Bemvindo a LibreTaxi 2.0!"

ask_location_menu_click_next = "Clicar \"Seguinte\" para partilhar localização (do telemovel) . Ou editar com 📎 Clipe -> 📍 Localização"

ask_location_menu_next_button = "Seguinte"

feed_menu_greeting = "Ofertas de 🚗 motoristas e 👋 passageiros serão publicadas aqui."

feed_menu_search_button = "Encontrar 🚗 ou 👋"

feed_menu_location_button = "📍 Actualizar localização"

feed_menu_location_changed = "👌 Localização actualizada"

feed_menu_error = "😕 Pedido não entendido, intente hacer clic 🔳 abajo 👇"

post_menu_report_button = "☝️️Reportar ⚠️"

post_menu_wait = "🕙 Esperar 5 minutos por favor"

# Do not translate /cancel
post_menu_copy_and_paste = "Copiar & colar o texto començando com 🚗 (motorista) ou 👋 (passageiro) no seguinte formato, ou escrever /cancel (para anular), exemplos:"

post_menu_driver_example = "🚗 Oferta de boleia\nDe: praça fulano\nPara: aeroporto\nData: hoje\nHora: agora\nPagamento: cash, coins, troca,..."

post_menu_passenger_example = "👋 Procura de boleia\nDe: Avenida fulano, 42\nPara: Baixa\nData: hoje\nHora: agora\nPax: 2"

# Here is how we check if the user just copied the text or changed it. It's just a string from the previous postings.
# Note how we have "foobar" in both postings above. It's the magic string, non-existent address, you should think
# about an address that doesn't exist in your own language. Or you can leave "foobar" if you didn't get it ;)
# Keep it lowercased!
validation_dummy_addr_lowercase = "fulano"

post_menu_sent = "✅ Enviado para usuários na zona (25km) and to @libretaxi_all"

# "Contact" is a verb here. For example, we'll have a posting where it says "blabla, I'm looking for ride, contact @username".
# So you're translating this verb "contact" below.
post_menu_via = "Contactar"

# When we have an error we say something like:
# "Your input is invalid, try again or /cancel"
# So this "or" part needs to be translated below.
post_menu_or = "ou"

validation_text_too_long = "🚫 Texto demasiado longo, 300 caracteres max (tem %d)"

validation_text_too_short = "🚫 Texto demasiado curto, 20 caracteres min (tem %d)"

validation_prefix = "🚫 Texto deve começar com 🚗 ou 👋"

validation_no_at = "🚫 Simbolo @ não autorisado"

validation_no_offensive_language = "🚫 Respeito por favor! 🤦"

validation_change_from_to = "🚫 Recomeça por favor, mude \"De\" e \"Para\""

validation_empty_lines1 = "🚫 Maximo 2 linhas vazias por favor (tem %d)"

validation_empty_lines2 = "🚫 Maximo 9 linhas por favor (tem %d)"

validation_min_lines = "🚫 Minimo 5 linhas por favor (tem %d)"

main_welcome_link = "https://telegra.ph/LibreTaxi-20---Vai-o-amar-02-12"