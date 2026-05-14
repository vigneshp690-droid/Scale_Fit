THEME_CHOICES = [
    {
        "slug": "scale-orange",
        "name": "ScaleFit Orange",
        "description": "The current energetic ScaleFit look.",
        "colors": ["#ff6417", "#19b8c9", "#10213f"],
    },
    {
        "slug": "lean-green",
        "name": "Lean Green",
        "description": "Fresh weight-loss focused greens and teal.",
        "colors": ["#16a34a", "#14b8a6", "#123524"],
    },
    {
        "slug": "muscle-blue",
        "name": "Muscle Blue",
        "description": "Strong training blues with a clean gym feel.",
        "colors": ["#2563eb", "#06b6d4", "#0f172a"],
    },
    {
        "slug": "active-berry",
        "name": "Active Berry",
        "description": "Bold berry and coral for high-energy plans.",
        "colors": ["#d9467c", "#f97316", "#241230"],
    },
    {
        "slug": "dark-gym",
        "name": "Dark Gym",
        "description": "A darker premium fitness theme for contrast.",
        "colors": ["#f97316", "#22d3ee", "#111827"],
    },
]

DEFAULT_THEME = THEME_CHOICES[0]["slug"]
THEME_SLUGS = {theme["slug"] for theme in THEME_CHOICES}
THEME_CLASS_MAP = {
    "scale-orange": "theme-orange",
    "lean-green": "theme-green",
    "dark-gym": "theme-dark",
    "muscle-blue": "theme-blue",
    "active-berry": "theme-berry",
}


def get_theme(slug):
    for theme in THEME_CHOICES:
        if theme["slug"] == slug:
            return theme
    return THEME_CHOICES[0]


def get_theme_class(slug):
    return THEME_CLASS_MAP.get(slug, THEME_CLASS_MAP[DEFAULT_THEME])
