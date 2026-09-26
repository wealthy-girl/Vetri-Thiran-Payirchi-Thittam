from urllib.parse import quote_plus


def search_url(platform: str, query: str) -> str:

    bases = {

        "Amazon":
            "https://www.amazon.in/s?k=",

        "Flipkart":
            "https://www.flipkart.com/search?q=",

        "IKEA":
            "https://www.ikea.com/in/en/search/?q=",

        "Swiggy":
            "https://www.swiggy.com/search?query=",

        "Zomato":
            "https://www.zomato.com/search?q=",

        "OYO":
            "https://www.oyorooms.com/search?location=",
    }

    base = bases.get(
        platform,
        "https://www.google.com/search?q="
    )

    return base + quote_plus(query)


HOME_CATALOG = [

    (
        "Furniture",
        "Minimalist Study Table",
        6999,
        "IKEA"
    ),

    (
        "Furniture",
        "Compact 3-Seater Sofa",
        18999,
        "IKEA"
    ),

    (
        "Lighting",
        "LED Floor Lamp",
        2499,
        "Amazon"
    ),

    (
        "Lighting",
        "Pendant Ceiling Light",
        3299,
        "Amazon"
    ),

    (
        "Decor",
        "Abstract Wall Art Set",
        1799,
        "Amazon"
    ),

    (
        "Decor",
        "Indoor Planter Set",
        1299,
        "IKEA"
    ),

    (
        "Storage",
        "Modular Storage Unit",
        5999,
        "IKEA"
    ),

    (
        "Dining",
        "4-Seater Dining Table",
        14999,
        "IKEA"
    ),
]


PARTY_CATALOG = [

    (
        "Food",
        "Catering / Food Delivery",
        0,
        "Zomato"
    ),

    (
        "Food",
        "Food Delivery",
        0,
        "Swiggy"
    ),

    (
        "Decor",
        "Party Decoration Supplies",
        1999,
        "Amazon"
    ),

    (
        "Venue",
        "Hotel / Stay Search",
        0,
        "OYO"
    )
]


JEWELRY_CATALOG = [

    (
        "Earrings",
        "Gold-tone Jhumka Earrings",
        899,
        "Amazon"
    ),

    (
        "Necklace",
        "Pearl Layered Necklace",
        1299,
        "Amazon"
    ),

    (
        "Bracelet",
        "Minimal Bracelet",
        699,
        "Flipkart"
    ),

    (
        "Earrings",
        "Crystal Drop Earrings",
        999,
        "Flipkart"
    )
]


def fallback_home(req):

    budget = req.budget

    allocations = {
        "Furniture": budget * 0.45,
        "Lighting": budget * 0.15,
        "Decor": budget * 0.20,
        "Storage": budget * 0.20
    }

    items = []

    remaining = budget

    for category, name, price, platform in HOME_CATALOG:

        if category in allocations and price <= remaining:

            items.append({

                "category": category,

                "name": name,

                "price": price,

                "quantity": 1,

                "platform": platform,

                "url": search_url(
                    platform,
                    name
                ),

                "reason":
                    f"Fits the {req.style} "
                    "style and budget."
            })

            remaining -= price

        if len(items) >= 8:
            break

    return {

        "planner": "home",

        "budget": budget,

        "allocated":
            round(budget - remaining, 2),

        "remaining":
            round(remaining, 2),

        "summary":
            "A practical starter set selected "
            "within the requested budget.",

        "items": items,

        "allocations": {
            key: round(value, 2)
            for key, value in allocations.items()
        },

        "source":
            "local fallback catalog"
    }


def fallback_party(req):

    budget = req.budget

    allocations = {

        "Food":
            budget * 0.50,

        "Decor":
            budget * 0.15,

        "Venue":
            budget * 0.25,

        "Entertainment":
            budget * 0.10
    }

    items = [

        {

            "category": "Food",

            "name":
                "Food delivery/catering options",

            "price":
                round(
                    allocations["Food"],
                    2
                ),

            "quantity": 1,

            "platform": "Zomato",

            "url":
                search_url(
                    "Zomato",
                    req.event_type + " catering"
                ),

            "reason":
                "Budget allocation for guest food."
        },

        {

            "category": "Decor",

            "name":
                "Party decoration supplies",

            "price":
                min(
                    1999,
                    round(
                        allocations["Decor"],
                        2
                    )
                ),

            "quantity": 1,

            "platform": "Amazon",

            "url":
                search_url(
                    "Amazon",
                    "party decorations"
                ),

            "reason":
                "Basic decoration within "
                "the allocated budget."
        },

        {

            "category": "Venue",

            "name":
                "Venue and stay options",

            "price":
                round(
                    allocations["Venue"],
                    2
                ),

            "quantity": 1,

            "platform": "OYO",

            "url":
                search_url(
                    "OYO",
                    req.city or "nearby"
                ),

            "reason":
                "Search options using "
                "the venue allocation."
        }
    ]

    allocated = sum(
        item["price"]
        for item in items
    )

    return {

        "planner": "party",

        "budget": budget,

        "allocated":
            round(allocated, 2),

        "remaining":
            round(
                budget - allocated,
                2
            ),

        "summary":
            f"Starter plan for {req.guests} "
            f"guests and a {req.event_type} event.",

        "items": items,

        "allocations": {
            key: round(value, 2)
            for key, value in allocations.items()
        },

        "source":
            "local fallback catalog"
    }


def fallback_jewelry(
    budget,
    occasion,
    style
):

    items = []

    remaining = budget

    for (
        category,
        name,
        price,
        platform
    ) in JEWELRY_CATALOG:

        if price <= remaining:

            items.append({

                "category": category,

                "name": name,

                "price": price,

                "quantity": 1,

                "platform": platform,

                "url":
                    search_url(
                        platform,
                        name
                    ),

                "reason":
                    f"Selected for a {style} "
                    f"style and {occasion} occasion."
            })

            remaining -= price

        if len(items) >= 4:
            break

    return {

        "planner": "jewelry",

        "budget": budget,

        "allocated":
            round(
                budget - remaining,
                2
            ),

        "remaining":
            round(
                remaining,
                2
            ),

        "summary":
            f"Style-matched starter jewelry "
            f"options for {occasion}.",

        "items": items,

        "allocations": {
            "Jewelry":
                round(
                    budget - remaining,
                    2
                )
        },

        "source":
            "local fallback catalog"
    }