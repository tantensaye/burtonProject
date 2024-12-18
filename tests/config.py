# config.py
# CONFIGURATION FILE to manage SFCC environments & test data

# Staging credentials
staging_credentials = "storefront:backside180"

# Locales by region
north_america = ["us/en", "ca/en"]
europe = ["at/en", "be/en", "de/en", "se/en"]
asia_pacific = ["jp/en"]

# Locale test data
locale_test_data = {
    "us/en": {
        "customer_name": "WebDev Testing",
        "email": "webdevtesting@burton.com",
        "first_name": "WebDev",
        "last_name": "Testing",
        "shipping_address1": "180 Queen City Park Rd",
        "shipping_postal_code": "05401",
        "shipping_city": "Burlington",
        "shipping_state": "VT",
        "phone_number": "(802) 660-3200",
        "login_email": "webdevtesting@burton.com",
        "login_password": "W3bD3vT3$ting24/7",
        "egc_sender_name": "Donna Carpenter",
        "egc_gift_message": "Happy Birthday WebDev!!!",
        "billing_address1": "162 College Street",
        "billing_postal_code": "05401",
        # other locale-specific test data
    },
    "ca/en": {
        "customer_name": "WebDev Testing",
        "email": "webdevtesting@burton.com",
        "first_name": "WebDev",
        "last_name": "Testing",
        "shipping_address1": "98 Ossington Ave",
        "shipping_postal_code": "M6J 2Z4",
        "shipping_city": "Toronto",
        "shipping_state": "ON",
        "phone_number": "(647) 361-4400",
        "login_email": "webdevtesting@burton.com",
        "login_password": "W3bD3vT3$ting24/7",
        "egc_sender_name": "Donna Carpenter",
        "egc_gift_message": "Happy Birthday WebDev!!!",
        # other locale-specific test data
    },
    "at/en": {
        "customer_name": "WebDev Testing",
        "email": "webdevtesting@burton.com",
        "first_name": "WebDev",
        "last_name": "Testing",
        "shipping_address1": "Hallerstrasse 111",
        "shipping_postal_code": "6020",
        "shipping_city": "Innsbruck",
        "phone_number": "512 230 5440",
        "login_email": "webdevtesting@burton.com",
        "login_password": "W3bD3vT3$ting24/7",
        # other locale-specific test data
    },
    "be/en": {
        "customer_name": "WebDev Testing",
        "email": "webdevtesting@burton.com",
        "first_name": "WebDev",
        "last_name": "Testing",
        "shipping_address1": "Doornstraat 110",
        "shipping_postal_code": "8200",
        "shipping_city": "Bruges",
        "phone_number": "049 549 0157",
        "login_email": "webdevtesting@burton.com",
        "login_password": "W3bD3vT3$ting24/7",
        # other locale-specific test data
    },
    "de/en": {
        "customer_name": "WebDev Testing",
        "email": "webdevtesting@burton.com",
        "first_name": "WebDev",
        "last_name": "Testing",
        "shipping_address1": "Frauenstrasse 10",
        "shipping_postal_code": "80469",
        "shipping_city": "Munich",
        "phone_number": "892 323 6890",
        "login_email": "webdevtesting@burton.com",
        "login_password": "W3bD3vT3$ting24/7",
        # other locale-specific test data
    },
    "se/en": {
        "customer_name": "WebDev Testing",
        "email": "webdevtesting@burton.com",
        "first_name": "WebDev",
        "last_name": "Testing",
        "shipping_address1": "Norrlandsgatan 20",
        "shipping_postal_code": "111 44",
        "shipping_city": "Stockholm",
        "phone_number": "03218372570",
        "login_email": "webdevtesting@burton.com",
        "login_password": "W3bD3vT3$ting24/7",
        # other locale-specific test data
    },
    "jp/en": {
        "customer_name": "Testing WebDev",
        "email": "webdevtesting@burton.com",
        "first_name": "WebDev",
        "last_name": "Testing",
        "first_name_pronunciation": "Web-Dev",
        "last_name_pronunciation": "Tes-ting",
        "shipping_address1": "5-17-4",
        "shipping_postal_code": "150-0001",
        "shipping_state": "Tokyo",
        "shipping_city": "ShibuyaJingumae",
        "phone_number": "503 506 8000",
        "login_email": "webdevtesting@burton.com",
        "login_password": "W3bD3vT3$ting24/7",
        # other locale-specific test data
    },
    # add more locales and their test data as needed
}


# Function to get the product ID based on the locale
def get_product_id(locale):
    if locale == "jp/en":
        return "W25JP-216881"
    else:
        return "W25-216881"


# Additional function to retrieve the test data based on the locale
def get_locale_test_data(locale):
    return locale_test_data.get(locale, {})
