"""
KDP listing data for the TOP 3 (EN = Amazon.com / .co.uk, FR = Amazon.fr) + validator + royalty estimator.

    python3 listings.py      -> writes out/<book>/KDP_LISTING_<LANG>.md and checks every KDP limit

KDP limits enforced here:
  * title + subtitle <= 200 characters
  * 7 keyword boxes, each <= 50 characters, no duplicates, no words already in title/subtitle
    (title words are indexed anyway - repeating them wastes slots), no banned terms
  * description <= 4000 characters (simple HTML allowed: <b> <i> <br> <ul> <li> <p>)
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
BANNED = ["bestseller", "best seller", "free", "kindle unlimited", "new", "disney", "pixar", "on sale", "#1"]

# Printing-cost estimates (USD, Amazon.com). Formula = fixed + pages x per_page.
# VERIFY in KDP's Printing Cost calculator before publishing - KDP updates these tables.
PRINT = {
    "bw_large_le108": lambda p: 2.84,               # black ink, large trim (8.5x11), 24-108 pages (estimate)
    "premium_color_large": lambda p: 1.00 + 0.08 * p if p > 40 else 3.60 + 0.5,  # 8.5x8.5 premium colour (estimate)
}

BOOKS = {
    "01_dino_quest": {
        "print_key": "bw_large_le108", "pages": 108,
        "en": {
            "title": "Dino Quest Activity Book for Kids Ages 4-8",
            "subtitle": "86 Fun Dinosaur Activities: Mazes, Dot-to-Dot, Word Search, Coloring, Counting, Tracing & Spot the Difference",
            "series": "Dino Quest (Book 1)",
            "author": "Dino Quest Kids Press (replace with your pen name)",
            "keywords": [
                "dinosaur gifts for boys and girls 4 5 6 7 8",
                "preschool kindergarten first grade workbook",
                "t rex triceratops puzzles games for children",
                "road trip travel activities unplugged quiet time",
                "connect the dots hidden picture color by number",
                "fine motor skills pencil control homeschool",
                "birthday stocking stuffer christmas present",
            ],
            "categories": [
                "Juvenile Nonfiction > Activity Books > General",
                "Juvenile Nonfiction > Animals > Dinosaurs & Prehistoric Creatures",
                "Juvenile Nonfiction > Games & Activities > Mazes",
            ],
            "age": "4-8", "grade": "Preschool - 3",
            "price": {"amazon.com": 9.99, "amazon.co.uk": 8.99, "amazon.de/fr/es/it": 9.99},
            "description": (
                "<p><b>Roar into hours of screen-free fun!</b> Join Rex, Trixie, Bitsy and the whole Dino Quest crew on a "
                "108-page prehistoric adventure that keeps kids ages 4-8 busy, happy and learning.</p>"
                "<p><b>What's inside:</b></p><ul>"
                "<li><b>86 activities that get gradually harder</b> - an easy win first, then a new challenge</li>"
                "<li>14 mazes (easy, medium, hard) - planning & pencil control</li>"
                "<li>12 dot-to-dots counting up to 50 - the dino appears as you connect!</li>"
                "<li>8 word searches + tracing pages - letters, spelling & pre-writing strokes</li>"
                "<li>Count it, add it up, shadow match & odd-one-out - early math & visual skills</li>"
                "<li>Color-by-number, draw the other half & spot the difference</li>"
                "<li>10 coloring pages printed <b>single-sided</b> so markers don't bleed through</li>"
                "<li>A <b>Quest Map</b> to track progress, a full answer key and a <b>Junior Paleontologist certificate</b></li></ul>"
                "<p>Every dinosaur comes with a real fun fact, so kids learn while they play. Large 8.5 x 11 pages, "
                "original illustrations, and activities designed to build real skills.</p>"
                "<p><b>The perfect gift</b> for birthdays, Christmas, road trips, waiting rooms and rainy days. "
                "Scroll up and click <i>Add to Cart</i> to start the quest!</p>"),
        },
        "fr": {
            "title": "Dino Quest - Cahier d'activités Dinosaures 4-8 ans",
            "subtitle": "86 jeux : labyrinthes, points à relier, mots mêlés, coloriages magiques, calcul, graphisme et 5 différences, avec solutions",
            "series": "Dino Quest (Tome 1)",
            "author": "Dino Quest Kids Press (remplacez par votre nom de plume)",
            "keywords": [
                "cadeau dinosaure garçon fille 4 5 6 7 8 ans",
                "maternelle grande section cp ce1 cahier jeux",
                "tyrannosaure tricératops livre jeux enfant",
                "activité voyage voiture sans écran calme",
                "relier les points coloriage par numéro",
                "motricité fine montessori tenir le crayon",
                "idée cadeau noël anniversaire petit garçon",
            ],
            "categories": [
                "Livres pour enfants > Activités, jeux et loisirs créatifs > Jeux et activités",
                "Livres pour enfants > Animaux > Dinosaures",
                "Livres pour enfants > Activités > Labyrinthes",
            ],
            "age": "4-8", "grade": "Maternelle - CE2",
            "price": {"amazon.fr": 9.99},
            "description": (
                "<p><b>Des heures de jeux sans écran avec les dinosaures !</b> Rex, Trixie, Bitsy et toute l'équipe "
                "Dino Quest emmènent les enfants de 4 à 8 ans dans une grande aventure de 108 pages.</p>"
                "<p><b>À l'intérieur :</b></p><ul>"
                "<li><b>86 activités de difficulté progressive</b> : une réussite facile, puis un nouveau défi</li>"
                "<li>14 labyrinthes (facile, moyen, difficile)</li>"
                "<li>12 points à relier jusqu'à 50 : le dinosaure apparaît au fil des points</li>"
                "<li>8 mots mêlés + pages de graphisme</li>"
                "<li>Dénombrement, additions, ombres et intrus</li>"
                "<li>Coloriages magiques, symétrie et jeu des 5 différences</li>"
                "<li>10 coloriages imprimés au <b>recto seulement</b> : les feutres ne traversent pas</li>"
                "<li>Une <b>Carte de la Quête</b>, toutes les solutions et un <b>diplôme de Jeune Paléontologue</b></li></ul>"
                "<p>Chaque dinosaure est présenté avec une vraie anecdote : on apprend en s'amusant. Grand format, "
                "illustrations originales.</p>"
                "<p><b>L'idée cadeau parfaite</b> pour Noël, les anniversaires, les voyages et les jours de pluie !</p>"),
        },
    },
    "02_dino_abc": {
        "print_key": "bw_large_le108", "pages": 82,
        "en": {
            "title": "Dino Quest ABC: Letter Tracing Book for Preschoolers Ages 3-5",
            "subtitle": "Learn to Write Letters and Numbers with Stroke-Order Arrows - Handwriting Practice Workbook for Pre-K and Kindergarten",
            "series": "Dino Quest (Book 2)",
            "author": "Dino Quest Kids Press (replace with your pen name)",
            "keywords": [
                "alphabet handwriting practice toddlers",
                "pre k learning activities ages 4-5 homeschool",
                "abc writing book uppercase lowercase",
                "trace numbers 0-10 counting kids",
                "dinosaur gifts for 3 year old boy girl",
                "fine motor skills pencil control lines shapes",
                "back to school sight words name writing",
            ],
            "categories": [
                "Juvenile Nonfiction > Language Arts > Handwriting",
                "Juvenile Nonfiction > Concepts > Alphabet",
                "Juvenile Nonfiction > Activity Books > General",
            ],
            "age": "3-5", "grade": "Preschool - Kindergarten",
            "price": {"amazon.com": 9.99, "launch_option": 7.99, "amazon.co.uk": 7.99},
            "description": (
                "<p><b>Most tracing books only show dotted letters. Dino Quest ABC shows little hands exactly WHERE to start "
                "and WHICH WAY to go.</b></p>"
                "<p>Every model letter and number comes with <b>numbered strokes and direction arrows</b> - the way teachers "
                "teach it - so good habits start on day one.</p>"
                "<p><b>Inside this 82-page workbook:</b></p><ul>"
                "<li>8 warm-up pages: lines, curves, circles, zigzags, waves and loops</li>"
                "<li>26 letter spreads: uppercase + lowercase in 4 steps - trace the model, trace, start from the dot, write alone</li>"
                "<li>A picture to color + a word to trace for every letter (A is for avocado, B is for ball...)</li>"
                "<li>\"Find the letter\" games for letter recognition</li>"
                "<li>Numbers 0-10 with counting and number words</li>"
                "<li>ABC review, uppercase/lowercase matching, ABC dot-to-dot and name practice</li>"
                "<li>Star chart + Super Writer certificate</li></ul>"
                "<p>Large 8.5 x 11 pages with clear handwriting lines, friendly dinosaur guides and original art. "
                "Perfect for preschool, pre-K, kindergarten readiness and homeschool.</p>"),
        },
        "fr": {
            "title": "Dino Quest ABC - J'apprends à écrire les lettres et les chiffres",
            "subtitle": "Cahier d'écriture maternelle dès 3 ans : majuscules, minuscules et chiffres avec flèches et ordre des traits",
            "series": "Dino Quest (Tome 2)",
            "author": "Dino Quest Kids Press (remplacez par votre nom de plume)",
            "keywords": [
                "petite moyenne grande section exercices",
                "apprendre alphabet tracer lettres enfant",
                "graphisme maternelle 3 4 5 ans exercices",
                "lettres bâton script apprentissage lecture",
                "nombres 0 à 10 compter écrire maternelle",
                "cadeau dinosaure enfant 3 ans éducatif",
                "préparer le cp lecture écriture montessori",
            ],
            "categories": [
                "Livres pour enfants > Premières lectures et apprentissage > Écriture",
                "Livres pour enfants > Premiers apprentissages > Alphabet",
                "Livres pour enfants > Activités, jeux et loisirs créatifs",
            ],
            "age": "3-5", "grade": "Petite section - Grande section",
            "price": {"amazon.fr": 8.99},
            "description": (
                "<p><b>Dans la plupart des cahiers, il n'y a que des pointillés. Dino Quest ABC montre aux petites mains OÙ "
                "commencer et DANS QUEL SENS tracer.</b></p>"
                "<p>Chaque lettre et chaque chiffre modèle est accompagné de <b>traits numérotés et de flèches</b>, "
                "comme le montre la maîtresse : les bonnes habitudes dès le premier jour.</p>"
                "<ul><li>8 pages d'échauffement graphique : traits, ponts, ronds, zigzags, vagues, boucles</li>"
                "<li>26 doubles pages : majuscules + minuscules en 4 étapes</li>"
                "<li>Un dessin à colorier et un mot à écrire pour chaque lettre (A comme avocat, B comme ballon...)</li>"
                "<li>Jeux « trouve la lettre », nombres de 0 à 10, révisions, points ABC, prénom</li>"
                "<li>Tableau d'étoiles et diplôme de Super Écrivain</li></ul>"
                "<p>Écriture script, idéale de la petite à la grande section. Grand format 21,6 x 27,9 cm.</p>"),
        },
    },
    "03_nova": {
        "print_key": "premium_color_large", "pages": 32,
        "en": {
            "title": "Nova's Calm Glow",
            "subtitle": "A Bedtime Story About Big Feelings and Calm Breathing",
            "series": "(optional) Little Lights - Book 1",
            "author": "Dino Quest Kids Press (replace with your pen name)",
            "keywords": [
                "toddler anxiety worry picture book bedtime",
                "emotions feelings book for kids ages 3-5",
                "mindfulness breathing exercises children",
                "self regulation anger tantrums preschool",
                "firefly night sleep story read aloud",
                "social emotional learning kindergarten",
                "baby shower gift calm down corner",
            ],
            "categories": [
                "Juvenile Fiction > Social Themes > Emotions & Feelings",
                "Juvenile Fiction > Bedtime & Dreams",
                "Juvenile Fiction > Animals > Insects, Spiders, etc.",
            ],
            "age": "3-6", "grade": "Preschool - 1",
            "price": {"amazon.com": 12.99, "ebook": 3.99, "amazon.co.uk": 10.99},
            "description": (
                "<p><b>Some nights, little lights feel BIG feelings.</b></p>"
                "<p>When thunder grumbles, her little brother bumps her wing and tomorrow's Moonlight Picnic feels SO exciting, "
                "Nova the firefly's light flashes worried blue, cross red and fizzy yellow. How will she ever fall asleep?</p>"
                "<p>With wise Grandma Owl, a jumpy little Frog and the kind Moon, Nova discovers three simple ways to calm her "
                "glow - and then shares them with her friends.</p>"
                "<ul><li>A gentle, rhythmic read-aloud for a calmer bedtime</li>"
                "<li>Feelings shown as colors that young children instantly understand</li>"
                "<li>3 easy calming tools: flower & candle breathing, the Frog Squeeze, counting five stars</li>"
                "<li>Bonus pages: star breathing, hill breathing, a feelings chart, a calm-down toolbox and tips for grown-ups</li></ul>"
                "<p>A perfect bedtime book for ages 3-6, and a thoughtful gift for preschool teachers, new siblings and calm-down corners.</p>"),
        },
        "fr": {
            "title": "La lumière douce de Nova",
            "subtitle": "Une histoire du soir pour apprivoiser les grandes émotions",
            "series": "(optionnel) Petites Lumières - Tome 1",
            "author": "Dino Quest Kids Press (remplacez par votre nom de plume)",
            "keywords": [
                "album jeunesse émotions 3 4 5 6 ans",
                "endormissement enfant doux sommeil apaisé",
                "gérer la colère et la peur maternelle",
                "respiration relaxation enfant calme",
                "luciole livre enfant nuit rituel coucher",
                "éducation bienveillante parentalité positive",
                "cadeau naissance anniversaire petite fille",
            ],
            "categories": [
                "Livres pour enfants > Thèmes sociaux > Émotions et sentiments",
                "Livres pour enfants > Histoires du soir",
                "Livres pour enfants > Albums",
            ],
            "age": "3-6", "grade": "Maternelle",
            "price": {"amazon.fr": 12.99, "ebook": 3.99},
            "description": (
                "<p><b>Certains soirs, les petites lumières ressentent de GRANDES émotions.</b></p>"
                "<p>Quand l'orage gronde, que son petit frère lui cogne l'aile et que le pique-nique de demain la rend si impatiente, "
                "la lumière de Nova la luciole clignote en bleu inquiet, en rouge fâché et en jaune pétillant. "
                "Comment va-t-elle réussir à dormir ?</p>"
                "<p>Avec Mamie Chouette, Grenouille et la gentille Lune, Nova découvre trois façons simples de retrouver son calme.</p>"
                "<ul><li>Une lecture douce et rythmée pour un coucher plus serein</li>"
                "<li>Des couleurs pour nommer les émotions</li>"
                "<li>3 outils : la fleur et la bougie, le serré de la grenouille, les cinq étoiles</li>"
                "<li>Bonus : respiration de l'étoile et des collines, roue des émotions, boîte à calme, conseils aux parents</li></ul>"),
        },
    },
}


def words(s):
    return {w for w in re.findall(r"[a-zà-ÿ0-9]+", s.lower()) if len(w) > 2}


def validate(book, lang, d):
    errs, warns = [], []
    ts = len(d["title"]) + len(d["subtitle"])
    if ts > 200:
        errs.append(f"title+subtitle {ts} > 200 chars")
    if len(d["keywords"]) != 7:
        errs.append("need exactly 7 keyword boxes")
    tw = words(d["title"] + " " + d["subtitle"])
    seen = set()
    for k in d["keywords"]:
        if len(k) > 50:
            errs.append(f"keyword > 50 chars: {k!r} ({len(k)})")
        if k in seen:
            errs.append(f"duplicate keyword {k!r}")
        seen.add(k)
        for b in BANNED:
            if re.search(r"\b" + re.escape(b) + r"\b", k.lower()):
                errs.append(f"banned term {b!r} in {k!r}")
        overlap = words(k) & tw
        if len(overlap) >= 3:
            warns.append(f"keyword repeats title words {sorted(overlap)}: {k!r}")
    if len(d["description"]) > 4000:
        errs.append(f"description {len(d['description'])} > 4000 chars")
    return errs, warns


def royalty(price, cost, rate=None):
    rate = rate or (0.60 if price >= 9.99 else 0.50)
    return round(rate * price - cost, 2), rate


def write_md(book, lang, data, cost):
    d = data[lang]
    fr = lang == "fr"
    L = []
    L.append(f"# {'Fiche KDP' if fr else 'KDP listing'} - {d['title']} ({lang.upper()})\n")
    L.append(f"| {'Champ' if fr else 'Field'} | {'Valeur (copier-coller)' if fr else 'Value (copy-paste)'} |\n|---|---|")
    L.append(f"| Title | {d['title']} |")
    L.append(f"| Subtitle | {d['subtitle']} |")
    L.append(f"| Series | {d['series']} |")
    L.append(f"| Author | {d['author']} |")
    L.append(f"| Reading age | {d['age']} |")
    L.append(f"| Grade | {d['grade']} |")
    L.append(f"| Title + subtitle length | {len(d['title']) + len(d['subtitle'])}/200 |")
    L.append("\n## " + ("7 mots-clés (un par case)" if fr else "7 keywords (one per box)") + "\n")
    for i, k in enumerate(d["keywords"], 1):
        L.append(f"{i}. `{k}` ({len(k)}/50)")
    L.append("\n## " + ("Catégories (3)" if fr else "Categories (3)") + "\n")
    for ccat in d["categories"]:
        L.append(f"- {ccat}")
    L.append("\n## " + ("Prix & royalties estimées" if fr else "Price & estimated royalties") + "\n")
    for mk, p in d["price"].items():
        if mk == "ebook":
            L.append(f"- eBook: {p} (70% royalty tier: 2.99-9.99)")
            continue
        r, rate = royalty(p, cost)
        L.append(f"- {mk}: {p} -> ~{r} {'par vente' if fr else 'per sale'} ({int(rate * 100)}% - "
                 f"{'impression estimée' if fr else 'est. printing'} {cost:.2f})")
    L.append(("\n> Coûts d'impression = estimations : vérifiez dans le calculateur KDP avec le fichier final. "
              "Depuis 2025, un livre broché sous 9,99 $ ne touche que 50 % (60 % à partir de 9,99 $).\n") if fr else
             ("\n> Printing costs are estimates: confirm in KDP's calculator with the final file. Paperbacks listed "
              "below $9.99 earn 50% instead of 60%.\n"))
    L.append("## " + ("Description (HTML, à coller dans KDP)" if fr else "Description (HTML, paste into KDP)") + "\n")
    L.append("```html\n" + d["description"].replace("</li>", "</li>\n").replace("</p>", "</p>\n") + "\n```")
    L.append(f"\n({len(d['description'])}/4000)\n")
    return "\n".join(L)


def main():
    ok = True
    for book, data in BOOKS.items():
        cost = PRINT[data["print_key"]](data["pages"])
        for lang in ("en", "fr"):
            errs, warns = validate(book, lang, data[lang])
            status = "OK" if not errs else "FAIL"
            ok &= not errs
            print(f"{book}/{lang}: {status} {errs} {warns}")
            md = write_md(book, lang, data, cost)
            p = os.path.join(ROOT, "out", book, f"KDP_LISTING_{lang.upper()}.md")
            open(p, "w").write(md)
    print("LISTINGS", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
