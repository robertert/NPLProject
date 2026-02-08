"""
data.py – Data layer for the Spanish SVO Constructor.

All vocabularies, conjugation tables, and linguistic constants
stored as module-level dictionaries and lists.
"""

# ──────────────────────────── CONSTANTS ────────────────────────────

PERSONS = ["1s", "2s", "3s", "1p", "2p", "3p"]

PERSON_LABELS = {
    "1s": "yo",
    "2s": "tú",
    "3s": "él/ella/usted",
    "1p": "nosotros",
    "2p": "vosotros",
    "3p": "ellos/ellas/ustedes",
}

TENSES = ["Presente", "Pretérito", "Futuro"]

MOODS = ["Afirmativo", "Negativo", "Interrogativo", "Imperativo", "Condicional"]

NUMBERS = ["singular", "plural"]

GENDERS = ["M", "F"]

IMPERATIVE_PERSONS = ["tú", "usted", "nosotros", "vosotros", "ustedes"]

# ──────────────────────────── NOUNS ────────────────────────────────

NOUNS = {
    # Masculine
    "gato":      {"gender": "M", "singular": "gato",      "plural": "gatos",      "meaning": "cat"},
    "perro":     {"gender": "M", "singular": "perro",     "plural": "perros",     "meaning": "dog"},
    "libro":     {"gender": "M", "singular": "libro",     "plural": "libros",     "meaning": "book"},
    "hombre":    {"gender": "M", "singular": "hombre",    "plural": "hombres",    "meaning": "man"},
    "niño":      {"gender": "M", "singular": "niño",      "plural": "niños",      "meaning": "boy"},
    "coche":     {"gender": "M", "singular": "coche",     "plural": "coches",     "meaning": "car"},
    "árbol":     {"gender": "M", "singular": "árbol",     "plural": "árboles",    "meaning": "tree"},
    "pan":       {"gender": "M", "singular": "pan",       "plural": "panes",      "meaning": "bread"},
    "pez":       {"gender": "M", "singular": "pez",       "plural": "peces",      "meaning": "fish"},
    "río":       {"gender": "M", "singular": "río",       "plural": "ríos",       "meaning": "river"},
    "amigo":     {"gender": "M", "singular": "amigo",     "plural": "amigos",     "meaning": "friend (m)"},
    "profesor":  {"gender": "M", "singular": "profesor",  "plural": "profesores", "meaning": "teacher (m)"},
    "jardín":    {"gender": "M", "singular": "jardín",    "plural": "jardines",   "meaning": "garden"},
    "papel":     {"gender": "M", "singular": "papel",     "plural": "papeles",    "meaning": "paper"},
    "reloj":     {"gender": "M", "singular": "reloj",     "plural": "relojes",    "meaning": "clock"},
    "país":      {"gender": "M", "singular": "país",      "plural": "países",     "meaning": "country"},
    "lápiz":     {"gender": "M", "singular": "lápiz",     "plural": "lápices",    "meaning": "pencil"},
    # Feminine
    "casa":      {"gender": "F", "singular": "casa",      "plural": "casas",      "meaning": "house"},
    "manzana":   {"gender": "F", "singular": "manzana",   "plural": "manzanas",   "meaning": "apple"},
    "mesa":      {"gender": "F", "singular": "mesa",      "plural": "mesas",      "meaning": "table"},
    "mujer":     {"gender": "F", "singular": "mujer",     "plural": "mujeres",    "meaning": "woman"},
    "ciudad":    {"gender": "F", "singular": "ciudad",    "plural": "ciudades",   "meaning": "city"},
    "flor":      {"gender": "F", "singular": "flor",      "plural": "flores",     "meaning": "flower"},
    "niña":      {"gender": "F", "singular": "niña",      "plural": "niñas",      "meaning": "girl"},
    "silla":     {"gender": "F", "singular": "silla",     "plural": "sillas",     "meaning": "chair"},
    "ventana":   {"gender": "F", "singular": "ventana",   "plural": "ventanas",   "meaning": "window"},
    "puerta":    {"gender": "F", "singular": "puerta",    "plural": "puertas",    "meaning": "door"},
    "luz":       {"gender": "F", "singular": "luz",       "plural": "luces",      "meaning": "light"},
    "canción":   {"gender": "F", "singular": "canción",   "plural": "canciones",  "meaning": "song"},
    "amiga":     {"gender": "F", "singular": "amiga",     "plural": "amigas",     "meaning": "friend (f)"},
    "profesora": {"gender": "F", "singular": "profesora", "plural": "profesoras", "meaning": "teacher (f)"},
    "leche":     {"gender": "F", "singular": "leche",     "plural": "leches",     "meaning": "milk"},
    "noche":     {"gender": "F", "singular": "noche",     "plural": "noches",     "meaning": "night"},
    "carta":     {"gender": "F", "singular": "carta",     "plural": "cartas",     "meaning": "letter"},
}

# ──────────────────────────── ADJECTIVES ──────────────────────────

ADJECTIVES = {
    # -o class (4 forms: -o/-a/-os/-as)
    "rojo":      {"base": "rojo",      "meaning": "red",        "irregular_forms": None},
    "blanco":    {"base": "blanco",    "meaning": "white",      "irregular_forms": None},
    "negro":     {"base": "negro",     "meaning": "black",      "irregular_forms": None},
    "bonito":    {"base": "bonito",    "meaning": "pretty",     "irregular_forms": None},
    "pequeño":   {"base": "pequeño",   "meaning": "small",      "irregular_forms": None},
    "alto":      {"base": "alto",      "meaning": "tall",       "irregular_forms": None},
    "bajo":      {"base": "bajo",      "meaning": "short",      "irregular_forms": None},
    "nuevo":     {"base": "nuevo",     "meaning": "new",        "irregular_forms": None},
    "viejo":     {"base": "viejo",     "meaning": "old",        "irregular_forms": None},
    "rico":      {"base": "rico",      "meaning": "rich",       "irregular_forms": None},
    "largo":     {"base": "largo",     "meaning": "long",       "irregular_forms": None},
    "amarillo":  {"base": "amarillo",  "meaning": "yellow",     "irregular_forms": None},
    "feo":       {"base": "feo",       "meaning": "ugly",       "irregular_forms": None},
    "delgado":   {"base": "delgado",   "meaning": "thin",       "irregular_forms": None},
    "gordo":     {"base": "gordo",     "meaning": "fat",        "irregular_forms": None},
    "barato":    {"base": "barato",    "meaning": "cheap",      "irregular_forms": None},
    "caro":      {"base": "caro",      "meaning": "expensive",  "irregular_forms": None},
    # -e class (2 forms: -e / -es)
    "grande":    {"base": "grande",    "meaning": "big",        "irregular_forms": None},
    "triste":    {"base": "triste",    "meaning": "sad",        "irregular_forms": None},
    "fuerte":    {"base": "fuerte",    "meaning": "strong",     "irregular_forms": None},
    "importante":{"base": "importante","meaning": "important",  "irregular_forms": None},
    "interesante":{"base":"interesante","meaning":"interesting", "irregular_forms": None},
    "inteligente":{"base":"inteligente","meaning":"intelligent", "irregular_forms": None},
    "elegante":  {"base": "elegante",  "meaning": "elegant",    "irregular_forms": None},
    "valiente":  {"base": "valiente",  "meaning": "brave",      "irregular_forms": None},
    # Consonant class (2 forms: base / base+es, special: -z -> -ces)
    "feliz":     {"base": "feliz",     "meaning": "happy",      "irregular_forms": None},
    "azul":      {"base": "azul",      "meaning": "blue",       "irregular_forms": None},
    "joven":     {"base": "joven",     "meaning": "young",      "irregular_forms": None},
    "fácil":     {"base": "fácil",     "meaning": "easy",       "irregular_forms": None},
    "difícil":   {"base": "difícil",   "meaning": "difficult",  "irregular_forms": None},
    "popular":   {"base": "popular",   "meaning": "popular",    "irregular_forms": None},
    "común":     {"base": "común",     "meaning": "common",     "irregular_forms": None},
    "gris":      {"base": "gris",      "meaning": "grey",       "irregular_forms": None},
    # Irregular
    "bueno": {
        "base": "bueno", "meaning": "good",
        "irregular_forms": {
            ("M", "singular"): "bueno",
            ("F", "singular"): "buena",
            ("M", "plural"):   "buenos",
            ("F", "plural"):   "buenas",
        },
    },
    "malo": {
        "base": "malo", "meaning": "bad",
        "irregular_forms": {
            ("M", "singular"): "malo",
            ("F", "singular"): "mala",
            ("M", "plural"):   "malos",
            ("F", "plural"):   "malas",
        },
    },
}

# ──────────────────────────── VERBS ───────────────────────────────

VERBS = {
    # ── Regular -ar ──
    "hablar":    {"group": "ar", "meaning": "to speak",  "irregular": None},
    "caminar":   {"group": "ar", "meaning": "to walk",   "irregular": None},
    "comprar":   {"group": "ar", "meaning": "to buy",    "irregular": None},
    "cocinar":   {"group": "ar", "meaning": "to cook",   "irregular": None},
    "estudiar":  {"group": "ar", "meaning": "to study",  "irregular": None},
    "trabajar":  {"group": "ar", "meaning": "to work",   "irregular": None},
    "cantar":    {"group": "ar", "meaning": "to sing",   "irregular": None},
    "bailar":    {"group": "ar", "meaning": "to dance",  "irregular": None},
    "mirar":     {"group": "ar", "meaning": "to look",   "irregular": None},
    "tomar":     {"group": "ar", "meaning": "to take",   "irregular": None},
    "llevar":    {"group": "ar", "meaning": "to carry",  "irregular": None},
    "pintar":    {"group": "ar", "meaning": "to paint",  "irregular": None},
    # ── Regular -er ──
    "comer":     {"group": "er", "meaning": "to eat",    "irregular": None},
    "beber":     {"group": "er", "meaning": "to drink",  "irregular": None},
    "correr":    {"group": "er", "meaning": "to run",    "irregular": None},
    "leer":      {"group": "er", "meaning": "to read",   "irregular": None},
    "aprender":  {"group": "er", "meaning": "to learn",  "irregular": None},
    "vender":    {"group": "er", "meaning": "to sell",   "irregular": None},
    "creer":     {"group": "er", "meaning": "to believe","irregular": None},
    # ── Regular -ir ──
    "vivir":     {"group": "ir", "meaning": "to live",   "irregular": None},
    "escribir":  {"group": "ir", "meaning": "to write",  "irregular": None},
    "abrir":     {"group": "ir", "meaning": "to open",   "irregular": None},
    "subir":     {"group": "ir", "meaning": "to go up",  "irregular": None},
    "recibir":   {"group": "ir", "meaning": "to receive","irregular": None},
    # ── Irregular ──
    "ser": {
        "group": "er", "meaning": "to be (essence)",
        "irregular": {
            "presente":    {"1s": "soy",    "2s": "eres",    "3s": "es",      "1p": "somos",   "2p": "sois",    "3p": "son"},
            "pretérito":   {"1s": "fui",    "2s": "fuiste",  "3s": "fue",     "1p": "fuimos",  "2p": "fuisteis","3p": "fueron"},
            "futuro":      {"1s": "seré",   "2s": "serás",   "3s": "será",    "1p": "seremos", "2p": "seréis",  "3p": "serán"},
            "condicional": {"1s": "sería",  "2s": "serías",  "3s": "sería",   "1p": "seríamos","2p": "seríais", "3p": "serían"},
            "imperativo":  {"tú": "sé",     "usted": "sea",  "nosotros": "seamos", "vosotros": "sed", "ustedes": "sean"},
        },
    },
    "estar": {
        "group": "ar", "meaning": "to be (state)",
        "irregular": {
            "presente":    {"1s": "estoy",  "2s": "estás",   "3s": "está",    "1p": "estamos", "2p": "estáis",  "3p": "están"},
            "pretérito":   {"1s": "estuve", "2s": "estuviste","3s": "estuvo",  "1p": "estuvimos","2p":"estuvisteis","3p":"estuvieron"},
            "futuro":      {"1s": "estaré", "2s": "estarás", "3s": "estará",  "1p": "estaremos","2p":"estaréis","3p": "estarán"},
            "condicional": {"1s": "estaría","2s": "estarías","3s": "estaría", "1p": "estaríamos","2p":"estaríais","3p":"estarían"},
            "imperativo":  {"tú": "está",   "usted": "esté", "nosotros": "estemos", "vosotros": "estad", "ustedes": "estén"},
        },
    },
    "ir": {
        "group": "ir", "meaning": "to go",
        "irregular": {
            "presente":    {"1s": "voy",    "2s": "vas",     "3s": "va",      "1p": "vamos",   "2p": "vais",    "3p": "van"},
            "pretérito":   {"1s": "fui",    "2s": "fuiste",  "3s": "fue",     "1p": "fuimos",  "2p": "fuisteis","3p": "fueron"},
            "futuro":      {"1s": "iré",    "2s": "irás",    "3s": "irá",     "1p": "iremos",  "2p": "iréis",   "3p": "irán"},
            "condicional": {"1s": "iría",   "2s": "irías",   "3s": "iría",    "1p": "iríamos", "2p": "iríais",  "3p": "irían"},
            "imperativo":  {"tú": "ve",     "usted": "vaya", "nosotros": "vayamos", "vosotros": "id", "ustedes": "vayan"},
        },
    },
    "tener": {
        "group": "er", "meaning": "to have",
        "irregular": {
            "presente":    {"1s": "tengo",  "2s": "tienes",  "3s": "tiene",   "1p": "tenemos", "2p": "tenéis",  "3p": "tienen"},
            "pretérito":   {"1s": "tuve",   "2s": "tuviste", "3s": "tuvo",    "1p": "tuvimos", "2p": "tuvisteis","3p":"tuvieron"},
            "futuro":      {"1s": "tendré", "2s": "tendrás", "3s": "tendrá",  "1p": "tendremos","2p":"tendréis","3p": "tendrán"},
            "condicional": {"1s": "tendría","2s": "tendrías","3s": "tendría", "1p": "tendríamos","2p":"tendríais","3p":"tendrían"},
            "imperativo":  {"tú": "ten",    "usted": "tenga","nosotros": "tengamos","vosotros": "tened","ustedes": "tengan"},
        },
    },
    "hacer": {
        "group": "er", "meaning": "to do/make",
        "irregular": {
            "presente":    {"1s": "hago",   "2s": "haces",   "3s": "hace",    "1p": "hacemos", "2p": "hacéis",  "3p": "hacen"},
            "pretérito":   {"1s": "hice",   "2s": "hiciste", "3s": "hizo",    "1p": "hicimos", "2p": "hicisteis","3p":"hicieron"},
            "futuro":      {"1s": "haré",   "2s": "harás",   "3s": "hará",    "1p": "haremos", "2p": "haréis",  "3p": "harán"},
            "condicional": {"1s": "haría",  "2s": "harías",  "3s": "haría",   "1p": "haríamos","2p": "haríais", "3p": "harían"},
            "imperativo":  {"tú": "haz",    "usted": "haga", "nosotros": "hagamos", "vosotros": "haced", "ustedes": "hagan"},
        },
    },
    "poder": {
        "group": "er", "meaning": "to be able to",
        "irregular": {
            "presente":    {"1s": "puedo",  "2s": "puedes",  "3s": "puede",   "1p": "podemos", "2p": "podéis",  "3p": "pueden"},
            "pretérito":   {"1s": "pude",   "2s": "pudiste", "3s": "pudo",    "1p": "pudimos", "2p": "pudisteis","3p":"pudieron"},
            "futuro":      {"1s": "podré",  "2s": "podrás",  "3s": "podrá",   "1p": "podremos","2p": "podréis", "3p": "podrán"},
            "condicional": {"1s": "podría", "2s": "podrías", "3s": "podría",  "1p": "podríamos","2p":"podríais","3p": "podrían"},
            "imperativo":  {"tú": "puede",  "usted": "pueda","nosotros": "podamos","vosotros": "poded","ustedes": "puedan"},
        },
    },
    "querer": {
        "group": "er", "meaning": "to want",
        "irregular": {
            "presente":    {"1s": "quiero", "2s": "quieres", "3s": "quiere",  "1p": "queremos","2p": "queréis", "3p": "quieren"},
            "pretérito":   {"1s": "quise",  "2s": "quisiste","3s": "quiso",   "1p": "quisimos","2p":"quisisteis","3p":"quisieron"},
            "futuro":      {"1s": "querré", "2s": "querrás", "3s": "querrá",  "1p": "querremos","2p":"querréis","3p": "querrán"},
            "condicional": {"1s": "querría","2s": "querrías","3s": "querría", "1p": "querríamos","2p":"querríais","3p":"querrían"},
            "imperativo":  {"tú": "quiere", "usted": "quiera","nosotros":"queramos","vosotros":"quered","ustedes":"quieran"},
        },
    },
    "decir": {
        "group": "ir", "meaning": "to say",
        "irregular": {
            "presente":    {"1s": "digo",   "2s": "dices",   "3s": "dice",    "1p": "decimos", "2p": "decís",   "3p": "dicen"},
            "pretérito":   {"1s": "dije",   "2s": "dijiste", "3s": "dijo",    "1p": "dijimos", "2p": "dijisteis","3p":"dijeron"},
            "futuro":      {"1s": "diré",   "2s": "dirás",   "3s": "dirá",    "1p": "diremos", "2p": "diréis",  "3p": "dirán"},
            "condicional": {"1s": "diría",  "2s": "dirías",  "3s": "diría",   "1p": "diríamos","2p": "diríais", "3p": "dirían"},
            "imperativo":  {"tú": "di",     "usted": "diga", "nosotros": "digamos", "vosotros": "decid", "ustedes": "digan"},
        },
    },
    "saber": {
        "group": "er", "meaning": "to know (facts)",
        "irregular": {
            "presente":    {"1s": "sé",     "2s": "sabes",   "3s": "sabe",    "1p": "sabemos", "2p": "sabéis",  "3p": "saben"},
            "pretérito":   {"1s": "supe",   "2s": "supiste", "3s": "supo",    "1p": "supimos", "2p": "supisteis","3p":"supieron"},
            "futuro":      {"1s": "sabré",  "2s": "sabrás",  "3s": "sabrá",   "1p": "sabremos","2p": "sabréis", "3p": "sabrán"},
            "condicional": {"1s": "sabría", "2s": "sabrías", "3s": "sabría",  "1p": "sabríamos","2p":"sabríais","3p": "sabrían"},
            "imperativo":  {"tú": "sabe",   "usted": "sepa", "nosotros": "sepamos", "vosotros": "sabed", "ustedes": "sepan"},
        },
    },
    "venir": {
        "group": "ir", "meaning": "to come",
        "irregular": {
            "presente":    {"1s": "vengo",  "2s": "vienes",  "3s": "viene",   "1p": "venimos", "2p": "venís",   "3p": "vienen"},
            "pretérito":   {"1s": "vine",   "2s": "viniste", "3s": "vino",    "1p": "vinimos", "2p": "vinisteis","3p":"vinieron"},
            "futuro":      {"1s": "vendré", "2s": "vendrás", "3s": "vendrá",  "1p": "vendremos","2p":"vendréis","3p": "vendrán"},
            "condicional": {"1s": "vendría","2s": "vendrías","3s": "vendría", "1p": "vendríamos","2p":"vendríais","3p":"vendrían"},
            "imperativo":  {"tú": "ven",    "usted": "venga","nosotros": "vengamos","vosotros": "venid","ustedes": "vengan"},
        },
    },
}

# ──────────────────────────── DETERMINERS ─────────────────────────

DETERMINERS = {
    "Definido": {
        ("M", "singular"): "el",
        ("F", "singular"): "la",
        ("M", "plural"):   "los",
        ("F", "plural"):   "las",
    },
    "Indefinido": {
        ("M", "singular"): "un",
        ("F", "singular"): "una",
        ("M", "plural"):   "unos",
        ("F", "plural"):   "unas",
    },
    "Demostrativo (este)": {
        ("M", "singular"): "este",
        ("F", "singular"): "esta",
        ("M", "plural"):   "estos",
        ("F", "plural"):   "estas",
    },
    "Demostrativo (ese)": {
        ("M", "singular"): "ese",
        ("F", "singular"): "esa",
        ("M", "plural"):   "esos",
        ("F", "plural"):   "esas",
    },
    "Posesivo (mi)": {
        ("M", "singular"): "mi",
        ("F", "singular"): "mi",
        ("M", "plural"):   "mis",
        ("F", "plural"):   "mis",
    },
    "Posesivo (tu)": {
        ("M", "singular"): "tu",
        ("F", "singular"): "tu",
        ("M", "plural"):   "tus",
        ("F", "plural"):   "tus",
    },
    "Ninguno": {},
}

# ──────────────────── CONJUGATION ENDING TABLES ───────────────────

# Presente & Pretérito: stem + ending
# Futuro & Condicional: infinitive + ending

REGULAR_ENDINGS = {
    "ar": {
        "presente":  {"1s": "o",  "2s": "as",  "3s": "a",   "1p": "amos",  "2p": "áis",  "3p": "an"},
        "pretérito": {"1s": "é",  "2s": "aste","3s": "ó",   "1p": "amos",  "2p": "asteis","3p": "aron"},
    },
    "er": {
        "presente":  {"1s": "o",  "2s": "es",  "3s": "e",   "1p": "emos",  "2p": "éis",  "3p": "en"},
        "pretérito": {"1s": "í",  "2s": "iste","3s": "ió",  "1p": "imos",  "2p": "isteis","3p": "ieron"},
    },
    "ir": {
        "presente":  {"1s": "o",  "2s": "es",  "3s": "e",   "1p": "imos",  "2p": "ís",   "3p": "en"},
        "pretérito": {"1s": "í",  "2s": "iste","3s": "ió",  "1p": "imos",  "2p": "isteis","3p": "ieron"},
    },
}

FUTURO_ENDINGS =      {"1s": "é",  "2s": "ás",  "3s": "á",   "1p": "emos",  "2p": "éis",  "3p": "án"}
CONDICIONAL_ENDINGS = {"1s": "ía", "2s": "ías", "3s": "ía",  "1p": "íamos", "2p": "íais", "3p": "ían"}

IMPERATIVE_ENDINGS = {
    "ar": {"tú": "a",  "usted": "e",  "nosotros": "emos", "vosotros": "ad",  "ustedes": "en"},
    "er": {"tú": "e",  "usted": "a",  "nosotros": "amos", "vosotros": "ed",  "ustedes": "an"},
    "ir": {"tú": "e",  "usted": "a",  "nosotros": "amos", "vosotros": "id",  "ustedes": "an"},
}
