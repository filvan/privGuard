init_menu_welcome = "Welcome to LibreTaxi 2.0!\n Source code: https://github.com/ro31337/libretaxi\n Made by Roman Pushkin and supporters\n License: AGPL-3.0"

ask_location_menu_click_next = "Click \"Next\" (from mobile phone) to share your location. Or fake it with 📎 Paperclip -> 📍 Location"

ask_location_menu_next_button = "Next"

feed_menu_greeting = "You'll see 🚗 drivers and 👋 passengers here."

feed_menu_search_button = "Find 🚗 or 👋"

feed_menu_location_button = "📍 Change location"

feed_menu_location_changed = "👌 Location updated"

feed_menu_error = "😕 Can't understand your choice, try clicking 🔳 icon below 👇"

post_menu_report_button = "☝️️Report ⚠️"

post_menu_wait = "🕙 Wait for 5 minutes"

# Do not translate /cancel
post_menu_copy_and_paste = "Copy & paste text starting with 🚗 (driver) or 👋 (passenger) in the following format, or /cancel, examples:"

post_menu_driver_example = "🚗 Ride offer\nFrom: foobar square\nTo: airport\nDate: today\nTime: now\nPayment: cash, venmo"

post_menu_passenger_example = "👋 Ride wanted\nFrom: foobar st, 42\nTo: downtown\nDate: today\nTime: now\nPax: 1"

# Here is how we check if the user just copied the text or changed it. It's just a string from the previous postings.
# Note how we have "foobar" in both postings above. It's the magic string, non-existent address, you should think
# about an address that doesn't exist in your own language. Or you can leave "foobar" if you didn't get it ;)
# Keep it lowercased!
validation_dummy_addr_lowercase = "foobar"

post_menu_sent = "✅ Sent to users around you (25km) and to @libretaxi_all"

# "Contact" is a verb here. For example, we'll have a posting where it says "blabla, I'm looking for ride, contact @username".
# So you're translating this verb "contact" below.
post_menu_via = "Contact"

# When we have an error we say something like:
# "Your input is invalid, try again or /cancel"
# So this "or" part needs to be translated below.
post_menu_or = "or"

validation_text_too_long = "🚫 Text is too long, 300 characters max (you have %d)"

validation_text_too_short = "🚫 Text is too short, 20 characters min (you have %d)"

validation_prefix = "🚫 Text must start with 🚗 or 👋"

validation_no_at = "🚫 No @ symbol please"

validation_no_offensive_language = "🚫 No bad words please 🤦"

validation_change_from_to = "🚫 Post again, change \"From\" and \"To\""

validation_empty_lines1 = "🚫 Only 2 empty lines max please (you have %d)"

validation_empty_lines2 = "🚫 Only 9 max lines please (you have %d)"

validation_min_lines = "🚫 At least 5 lines please (you have %d)"

main_welcome_link = "https://telegra.ph/LibreTaxi-20---you-will-love-it-02-02"
