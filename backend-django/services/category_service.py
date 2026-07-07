"""Keyword-based auto categorization."""

CATEGORY_KEYWORDS = {
    "Food": [
        "restaurant", "cafe", "pizza", "swiggy", "zomato", "grocery",
        "food", "dominos", "kfc", "mcdonald", "hotel", "dine",
    ],
    "Travel": [
        "uber", "ola", "petrol", "fuel", "bus", "train", "taxi",
        "cab", "flight", "airlines", "metro", "irctc",
    ],
    "Bills": [
        "electricity", "mobile", "internet", "gas", "bill",
        "recharge", "broadband", "water", "dth", "postpaid",
    ],
    "Shopping": [
        "amazon", "flipkart", "mall", "clothes", "fashion",
        "myntra", "shopping", "store", "shop", "nike", "adidas",
    ],
    "Health": [
        "hospital", "pharmacy", "medicine", "doctor", "clinic",
        "medical", "apollo", "health", "lab",
    ],
    "Education": [
        "course", "book", "college", "school", "exam",
        "tuition", "udemy", "coursera", "fees", "university",
    ],
    "Entertainment": [
        "movie", "netflix", "game", "concert", "spotify",
        "cinema", "pvr", "prime", "hotstar", "bookmyshow",
    ],
}

DEFAULT_CATEGORY = "Other"


def detect_category(text):
    if not text:
        return DEFAULT_CATEGORY
    lowered = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in lowered:
                return category
    return DEFAULT_CATEGORY
