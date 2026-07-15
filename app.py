from flask import Flask, render_template, request, redirect, url_for, flash, abort
import os

app = Flask(__name__)
_secret = os.environ.get("SESSION_SECRET")
# if not _secret:
#     raise RuntimeError("SESSION_SECRET environment variable is not set. Set it before starting the app.")
# app.secret_key = _secret

# ─────────────────────────────────────────────
# Data
# ─────────────────────────────────────────────

CATEGORIES = {
    "tomato": {
        "name": "Tomato Paste & Mix",
        "icon": "",
        "color": "linear-gradient(135deg,#C8102E,#8b0000)",
        "description": "Africa's finest tomato paste — grown and processed right here in Nigeria.",
        "products": [
            {"name": "Erisco Tomato Paste (Classic)", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2024/09/tomatoes-erisco-1024x773.jpg"},
            {"name": "Ric-Giko Tomato Paste", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2024/09/tomatoes-ricko.jpg"},
            {"name": "Nagiko Tomato Mix", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2024/09/tomatoes-nagiko.jpg"},
            {"name": "Erisco Tomato Paste (Alternate)", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2024/09/tomatoes-erisco.jpg"},
        ]
    },
    "milk": {
        "name": "Milk & Chocolate Cubes",
        "icon": "",
        "color": "linear-gradient(135deg,#273272,#1a2255)",
        "description": "Rich, nourishing dairy products crafted to fuel Nigerian families every morning.",
        "products": [
            {"name": "Ricvita Fat-Filled Milk Powder (400g)", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/02/milks.jpg"},
            {"name": "Ricvita Fat-Filled Milk Powder (900g)", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/02/milks.jpg"},
            {"name": "Nagiko Chocolate Cubes", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/03/choco-cube.jpg"},
            {"name": "Nagiko Milk Cubes", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/03/milk-cube.jpg"},
        ]
    },
    "beverages": {
        "name": "Beverages",
        "icon": "",
        "color": "linear-gradient(135deg,#04681D,#023d12)",
        "description": "Refreshing, healthy drinks rooted in Nigerian flavours and natural ingredients.",
        "products": [
            {"name": "Ginger & Lemon Honey Drink", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2024/11/beverage_cat-1.jpg"},
            {"name": "Ginger & Honey Drink", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/02/tea.jpg"},
            {"name": "Ricvita Instant Drink", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2024/11/beverage_cat-1.jpg"},
            {"name": "Ricvita Milk Beverage", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/02/milks.jpg"},
        ]
    },
    "tea": {
        "name": "Erisco Tea",
        "icon": "",
        "color": "linear-gradient(135deg,#2ecc71,#1a8a47)",
        "description": "Premium Nigerian teas — smooth, aromatic, and steeped in natural goodness.",
        "products": [
            {"slug": "classic", "name": "Erisco Green Tea Classic", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/01/greentea.jpg"},
            {"slug": "ginger", "name": "Green Tea with Ginger", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/02/tea-1.jpg"},
            {"slug": "soursop", "name": "Green Tea with Soursop & Honey", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/02/tea-8.jpg"},
            {"slug": "turmeric", "name": "Green Tea with Turmeric & Honey", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/02/tea-7.jpg"},
            {"slug": "label", "name": "Label Tea", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/03/tea-10.jpg"},
            {"slug": "premium", "name": "Premium Grade Green Tea", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/02/tea-4.jpg"},
            {"slug": "life", "name": "Tea Life Green Tea", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/02/tea-5.jpg"},
            {"slug": "chinese", "name": "Traditional Chinese Green Tea", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/02/tea-6.jpg"},
            {"slug": "turmeric-herbal", "name": "Herbal Green Tea with Turmeric", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/03/tummmmm.jpg"},
            {"slug": "garlic-herbal", "name": "Herbal Green Tea with Garlic", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/03/garlic.jpg"},
            {"slug": "neem", "name": "Herbal Green Tea with Neem", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/03/neem-tea.jpg"},
            {"slug": "hibiscus", "name": "Herbal Green Tea with Hibiscus", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/03/herbal-green.jpg"},
            {"slug": "mint", "name": "Mint with Green Tea", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/03/mint-green-tea.jpg"},
            {"slug": "cinnamon", "name": "Cinnamon with Green Tea", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/03/cinnamon-tea.jpg"},
            {"slug": "moringa", "name": "Moringa with Green Tea", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/03/moringa-tea.jpg"},
            {"slug": "ginger-honey", "name": "Ginger with Honey", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/03/ginger-honey-tea.jpg"},
            {"slug": "ginger-lemon", "name": "Ginger with Lemon & Honey", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/03/ginger-lemon.jpg"},
            {"slug": "tea-9", "name": "Tea Variant 9", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/02/tea-9.jpg"},
            {"slug": "tea-3", "name": "Tea Variant 3", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/02/tea-3.jpg"},
            {"slug": "tea-2", "name": "Tea Variant 2", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/02/tea-2.jpg"},
            {"slug": "nem", "name": "Nem Tea Variant", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/03/nem.jpg"},
        ]
    },
    "seasoning": {
        "name": "Seasoning & Spice",
        "icon": "",
        "color": "linear-gradient(135deg,#e8a020,#b87a10)",
        "description": "Bold, authentic seasonings that bring the soul of Nigerian cooking to every pot.",
        "products": [
            {"name": "Ric-Giko Seasoning Cubes (Chicken)", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/01/2i.jpg"},
            {"name": "Ric-Giko Seasoning Cubes (7-1)", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/01/7-1.jpg"},
            {"name": "Ric-Giko Seasoning (2-2)", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/01/2-2.jpg"},
            {"name": "Ric-Giko Seasoning (2e)", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/01/2e.jpg"},
            {"name": "Ric-Giko Seasoning (2f)", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/01/2f.jpg"},
            {"name": "Ric-Giko Seasoning (2g)", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/01/2g.jpg"},
            {"name": "Ric-Giko Seasoning (21a)", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/01/21a.jpg"},
            {"name": "Ric-Giko Seasoning (32)", "desc": "Imported from live site.", "tag": "", "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/01/32.jpg"},
        ]
    },
}

TEA_DETAILS = {
    "classic": {
        "name": "Erisco Green Tea Classic",
        "tagline": "Pure. Smooth. Naturally Balanced.",
        "emoji": "",
        "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/01/greentea.jpg",
        "color_from": "#2ecc71", "color_to": "#1a8a47",
        "story": "Born from Nigeria's growing wellness movement, Erisco Green Tea Classic is our purest expression of what a great tea should be. Sourced from the finest leaves and blended in Nigeria, every cup is a moment of calm in a busy day. No artificial flavours. No shortcuts. Just real tea.",
        "benefits": [
            {"icon": "", "title": "Rich in Antioxidants", "desc": "Green tea is loaded with catechins — natural antioxidants that help fight oxidative stress and protect your cells."},
            {"icon": "", "title": "Mental Clarity", "desc": "The natural L-theanine in green tea promotes relaxed alertness — focus without the jittery caffeine crash."},
            {"icon": "", "title": "Heart Health", "desc": "Regular green tea consumption is linked to improved cholesterol levels and better cardiovascular health."},
            {"icon": "", "title": "Natural Energy", "desc": "A gentle caffeine lift that energises you without overstimulation — perfect as a morning or mid-afternoon drink."},
            {"icon": "", "title": "Supports Metabolism", "desc": "Green tea has been shown to support healthy metabolism and weight management when paired with an active lifestyle."},
            {"icon": "", "title": "Hydration", "desc": "A delicious way to stay hydrated throughout the day — your body thanks you for every cup."},
        ],
        "ingredients": ["Premium green tea leaves", "No artificial flavours", "No added sugar", "No artificial preservatives", "NAFDAC certified"],
        "brew_steps": [
            {"step": "1", "title": "Heat Your Water", "desc": "Use water heated to 80°C — not boiling. Boiling water can make green tea bitter."},
            {"step": "2", "title": "Add Your Tea Bag", "desc": "Place one Erisco Green Tea Classic bag into your cup or mug."},
            {"step": "3", "title": "Steep for 2–3 Minutes", "desc": "Let the bag steep for 2 to 3 minutes. Longer steeping increases bitterness."},
            {"step": "4", "title": "Remove & Enjoy", "desc": "Remove the bag, breathe in the aroma, and enjoy your cup as it is or with a slice of lemon."},
        ],
        "related_articles": ["5 Proven Benefits of Green Tea", "Healthy Ageing Tips", "Foods That Support Immunity"],
    },
    "ginger": {
        "name": "Erisco Green Tea & Ginger",
        "tagline": "The Fire and the Calm — In One Cup.",
        "emoji": "",
        "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/03/ginger-honey-tea.jpg",
        "color_from": "#e8a020", "color_to": "#2ecc71",
        "story": "Nigeria has always known the power of ginger. From pepper soup to agbo, ginger is woven into our healing traditions. Erisco Green Tea & Ginger combines this ancient root with the antioxidant power of green tea — creating a morning ritual that warms you from the inside out.",
        "benefits": [
            {"icon": "", "title": "Warming & Energising", "desc": "Ginger's natural compounds create a warming sensation that energises the body and improves circulation."},
            {"icon": "", "title": "Soothes the Stomach", "desc": "Ginger has been used for centuries to relieve nausea, bloating, and digestive discomfort."},
            {"icon": "", "title": "Anti-inflammatory", "desc": "Both ginger and green tea contain powerful anti-inflammatory compounds that help the body fight inflammation."},
            {"icon": "", "title": "Mental Alertness", "desc": "The combination of ginger's stimulating properties and green tea's L-theanine delivers clear, calm focus."},
            {"icon": "", "title": "Cold & Flu Fighter", "desc": "A traditional remedy backed by modern science — ginger and green tea together support your immune response."},
            {"icon": "", "title": "Detox Support", "desc": "This blend supports the body's natural detoxification processes, especially enjoyed first thing in the morning."},
        ],
        "ingredients": ["Premium green tea leaves", "Real Nigerian ginger extract", "No artificial flavours", "No added sugar", "NAFDAC certified"],
        "brew_steps": [
            {"step": "1", "title": "Boil & Cool Slightly", "desc": "Boil water and let it cool for 2 minutes to around 85°C — hot enough to extract the ginger, gentle on the tea."},
            {"step": "2", "title": "Steep for 3 Minutes", "desc": "Place the bag in your cup and steep for 3 minutes. For a stronger ginger kick, go up to 4 minutes."},
            {"step": "3", "title": "Optional: Add Honey", "desc": "A teaspoon of natural honey rounds out the ginger heat beautifully and adds extra wellness benefits."},
            {"step": "4", "title": "Sip & Energise", "desc": "Best enjoyed hot in the morning. Feel the warmth spread through you as you start your day."},
        ],
        "related_articles": ["Why Ginger & Honey Are Nigeria's Best-Kept Health Secret", "Foods That Support Immunity", "5 Proven Benefits of Green Tea"],
    },
    "lemon": {
        "name": "Erisco Green Tea & Lemon",
        "tagline": "Bright. Zesty. Refreshingly Alive.",
        "emoji": "",
        "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/03/ginger-lemon.jpg",
        "color_from": "#f7d060", "color_to": "#2ecc71",
        "story": "Sometimes a cup of tea should feel like sunshine in a mug. Erisco Green Tea & Lemon was crafted for those moments — a bright, citrus-forward blend that lifts your mood and refreshes your senses. The lemon not only adds flavour; it amplifies the antioxidant absorption of the green tea, making every sip more beneficial.",
        "benefits": [
            {"icon": "", "title": "Vitamin C Boost", "desc": "Lemon adds a natural dose of Vitamin C to your cup — supporting immunity, skin health, and iron absorption."},
            {"icon": "", "title": "Enhanced Antioxidants", "desc": "Lemon's acidity actually increases the bioavailability of green tea's catechins — you absorb more goodness."},
            {"icon": "", "title": "Digestive Aid", "desc": "Lemon stimulates bile production, supporting healthy digestion and reducing bloating after meals."},
            {"icon": "", "title": "Glowing Skin", "desc": "The Vitamin C and antioxidant combination supports collagen production and helps protect skin from oxidative damage."},
            {"icon": "", "title": "Hydration & Freshness", "desc": "The bright citrus taste makes it easy to drink more throughout the day — keeping you refreshed and hydrated."},
            {"icon": "", "title": "Mood Lifting", "desc": "Citrus aroma is scientifically linked to elevated mood and reduced cortisol. Just opening the sachet helps."},
        ],
        "ingredients": ["Premium green tea leaves", "Natural lemon flavour", "No artificial additives", "No added sugar", "NAFDAC certified"],
        "brew_steps": [
            {"step": "1", "title": "Use 80°C Water", "desc": "Lemon and green tea are both delicate — cooler water (80°C) preserves the bright flavour and prevents bitterness."},
            {"step": "2", "title": "Steep for 2 Minutes", "desc": "Two minutes is all it takes for this blend. The lemon notes are vibrant and don't need long to develop."},
            {"step": "3", "title": "Enjoy Hot or Iced", "desc": "This blend is spectacular iced. Brew double-strength and pour over ice for a refreshing cold drink."},
            {"step": "4", "title": "Garnish if You Like", "desc": "A fresh lemon slice on the rim takes it from everyday to elegant. Great for serving guests."},
        ],
        "related_articles": ["5 Proven Benefits of Green Tea", "Foods That Support Immunity", "Healthy Ageing Tips"],
    },
    "honey": {
        "name": "Erisco Green Tea & Honey",
        "tagline": "Nature's Sweetness. No Guilt. Just Goodness.",
        "emoji": "",
        "image": "https://eriscofoodsltd.com.ng/wp-content/uploads/2025/03/ginger-honey-tea.jpg",
        "color_from": "#f0a500", "color_to": "#2ecc71",
        "story": "Sweet doesn't have to mean unhealthy. Erisco Green Tea & Honey gives you the gentle sweetness you crave with none of the downsides of refined sugar. Natural honey adds its own antibacterial and antioxidant properties — turning your afternoon cup into a genuine wellness ritual. This is the tea for those who want to treat themselves, responsibly.",
        "benefits": [
            {"icon": "", "title": "Natural Sweetness", "desc": "Honey provides a gentle sweetness that doesn't spike blood sugar the way refined sugar does — a smarter sweet choice."},
            {"icon": "", "title": "Antibacterial Properties", "desc": "Honey contains natural hydrogen peroxide and other compounds that fight harmful bacteria in the body."},
            {"icon": "", "title": "Promotes Restful Sleep", "desc": "Honey raises insulin slightly, which releases tryptophan — the precursor to melatonin. Great as an evening drink."},
            {"icon": "", "title": "Immune Support", "desc": "The combination of green tea antioxidants and honey's natural compounds gives your immune system a powerful double boost."},
            {"icon": "", "title": "Soothes the Throat", "desc": "The classic honey-tea combination is one of the most effective natural remedies for sore throats and dry coughs."},
            {"icon": "", "title": "Gentle on the Body", "desc": "No artificial sweeteners, no refined sugar — just a naturally sweet, comforting cup that your body welcomes."},
        ],
        "ingredients": ["Premium green tea leaves", "Natural honey flavour", "No refined sugar", "No artificial sweeteners", "NAFDAC certified"],
        "brew_steps": [
            {"step": "1", "title": "Heat Water to 80°C", "desc": "Consistent with all green tea — slightly below boiling preserves the honey notes and prevents bitterness."},
            {"step": "2", "title": "Steep for 3 Minutes", "desc": "Let the honey flavour fully infuse. Three minutes delivers the perfect balance of sweetness and tea character."},
            {"step": "3", "title": "Add Real Honey if Desired", "desc": "For extra sweetness, add half a teaspoon of natural honey. The flavours layer beautifully together."},
            {"step": "4", "title": "Evening Ritual", "desc": "This is the perfect bedtime tea. Curl up, breathe in the warmth, and let the honey and tea calm you down."},
        ],
        "related_articles": ["Why Ginger & Honey Are Nigeria's Best-Kept Health Secret", "Healthy Ageing Tips", "5 Proven Benefits of Green Tea"],
    },
}

BLOG_ARTICLES = [
    {
        "slug": "green-tea-benefits",
        "title": "5 Proven Benefits of Green Tea for Your Health",
        "category": "Tea & Wellness",
        "category_color": "#2ecc71",
        "read_time": "4 min read",
        "excerpt": "Green tea has been consumed for thousands of years across Asia — and modern science is finally catching up with what traditional healers always knew. Here are five evidence-backed benefits of making green tea part of your daily routine.",
        "image": "img/green-tea-benefits.jpg",
        "emoji": "",
        "featured": True,
        "content_points": [
            ("Rich in Antioxidants", "Green tea is loaded with polyphenols — particularly EGCG (epigallocatechin gallate) — one of the most potent antioxidants found in any food. These compounds help neutralise free radicals that damage cells and accelerate ageing."),
            ("Supports Brain Function", "Green tea contains both caffeine and L-theanine. Together, they improve brain function synergistically — caffeine provides alertness while L-theanine promotes calm focus. No jitters. No crash."),
            ("May Reduce Risk of Heart Disease", "Green tea has been shown to improve LDL cholesterol levels and reduce oxidative damage in the blood — two key factors in cardiovascular health. Regular drinkers have a significantly lower risk of heart disease."),
            ("Supports Healthy Weight", "The catechins in green tea can boost metabolic rate and increase fat burning, particularly during exercise. It's not a miracle solution, but it genuinely helps when combined with an active lifestyle."),
            ("Antibacterial Properties", "The catechins in green tea inhibit the growth of bacteria like Streptococcus mutans — the bacteria that causes tooth decay. Green tea drinkers often report better oral health over time."),
        ],
        "product_link": "classic",
        "product_name": "Erisco Green Tea Classic",
    },
    {
        "slug": "healthy-ageing",
        "title": "Healthy Ageing Tips: Foods That Support Longevity",
        "category": "Healthy Ageing",
        "category_color": "#273272",
        "read_time": "6 min read",
        "excerpt": "Living longer is not just about genetics. Research consistently shows that what you eat, how you move, and how much you sleep have more impact on longevity than your DNA. Here's a practical Nigerian-focused guide to eating for a long, healthy life.",
        "emoji": "",
        "image": "img/healthy_aging.jpeg",
        "featured": True,
        "content_points": [
            ("Eat More Tomatoes", "Tomatoes are one of the richest sources of lycopene — a powerful antioxidant linked to reduced risk of prostate cancer, heart disease, and skin ageing. Cooked tomato paste actually has higher lycopene bioavailability than raw tomatoes. Erisco Tomato Paste is your ally here."),
            ("Make Tea a Daily Habit", "Green tea is one of the most comprehensively studied longevity foods in the world. The Japanese population — famous for extreme longevity — drinks green tea daily. Even two cups a day shows measurable benefits."),
            ("Prioritise Protein", "Muscle loss accelerates after 40. Ensure you are getting adequate protein at each meal — eggs, beans, fish, chicken, and milk products all count. Ricvita Milk Powder is a convenient protein and calcium boost."),
            ("Spice Up Your Food", "Ginger, turmeric, and herbs used in Nigerian cooking are packed with anti-inflammatory compounds. A diet full of spice is a diet that fights the inflammation underlying most age-related diseases."),
            ("Stay Hydrated", "Dehydration accelerates every ageing process in the body. Beyond plain water, herbal teas and natural drinks — like our Ginger & Honey range — keep you hydrated with added wellness benefits."),
        ],
        "product_link": None,
        "product_name": None,
    },
    {
        "slug": "immunity-foods",
        "title": "Foods That Support Immunity: A Nigerian Guide",
        "category": "Nutrition",
        "category_color": "#C8102E",
        "read_time": "5 min read",
        "excerpt": "Your immune system is your body's army — and like any army, it needs the right fuel. The good news? Nigerian cuisine is already packed with immune-supporting foods. Here's how to get more from your everyday meals.",
        "image": "img/immunity_foods.jpeg",
        "emoji": "",
        "featured": True,
        "content_points": [
            ("Tomatoes & Lycopene", "Lycopene — the compound that gives tomatoes their red colour — is a potent immune modulator. It activates natural killer cells and supports T-lymphocyte function. Regular tomato paste consumption genuinely supports immune resilience."),
            ("Ginger: Nigeria's Ancient Remedy", "Ginger contains gingerols and shogaols — compounds with powerful anti-inflammatory and antimicrobial properties. A daily ginger drink is one of the simplest and most effective things you can do for your immunity."),
            ("Green Tea Catechins", "EGCG (the primary antioxidant in green tea) has been shown to inhibit viral replication and stimulate immune cell production. During cold and flu season, green tea is one of your best defences."),
            ("Honey's Antimicrobial Power", "Raw honey contains hydrogen peroxide, bee defensin-1, and a low pH — all of which create a powerful antimicrobial environment. A teaspoon in your tea daily is ancient medicine backed by modern science."),
            ("Zinc from Seasoning Herbs", "The herbs and spices in Ric-Giko Mixed Herbs & Spices contain trace minerals including zinc — a critical nutrient for immune function. Every well-seasoned meal contributes to your immune health."),
        ],
        "product_link": "ginger",
        "product_name": "Erisco Green Tea & Ginger",
    },
    {
        "slug": "lycopene-tomatoes",
        "title": "How Tomatoes Power Your Body: The Science of Lycopene",
        "category": "Nutrition",
        "category_color": "#C8102E",
        "read_time": "4 min read",
        "excerpt": "You've been eating tomato stew your whole life. You probably didn't know it was also medicine. Lycopene — the pigment that makes tomatoes red — is one of the most powerful antioxidants in nature.",
        "emoji": "",
        "image": "img/tomatoes.jpeg",
        "featured": False,
        "content_points": [
            ("What is Lycopene?", "Lycopene is a carotenoid antioxidant found in red and pink foods — tomatoes, watermelon, guava. It's fat-soluble, meaning your body absorbs it best when eaten with oil. Your tomato stew (with palm oil or vegetable oil) is nutritionally perfect."),
            ("Why Tomato Paste is Better than Raw Tomatoes", "Cooking breaks down the cell walls in tomatoes, making lycopene up to 4x more bioavailable than in raw tomatoes. A tablespoon of Erisco Tomato Paste delivers more lycopene than a whole fresh tomato."),
            ("Prostate Health", "Lycopene has been extensively studied for its role in reducing prostate cancer risk. Men who consume tomato products regularly have consistently lower rates of prostate cancer in population studies."),
            ("Skin Protection", "Lycopene acts as an internal sunscreen — it helps protect your skin cells from UV damage, reducing the risk of premature ageing and skin cancer. Beauty really does start in the kitchen."),
            ("Heart Health", "Lycopene reduces LDL oxidation — the process that makes 'bad' cholesterol dangerous. Nigerian families eating tomato-rich diets are unknowingly protecting their hearts every single day."),
        ],
        "product_link": None,
        "product_name": None,
    },
    {
        "slug": "ginger-honey-secret",
        "title": "Why Ginger & Honey Are Nigeria's Best-Kept Health Secret",
        "category": "Wellness",
        "category_color": "#e8a020",
        "read_time": "5 min read",
        "excerpt": "Before antibiotics, there was ginger and honey. These two ingredients have been used across West Africa for centuries — not as folklore, but as effective, evidence-backed medicine. Here's why modern science now agrees with our grandmothers.",
        "image": "img/ginger_honey.jpeg",
        "emoji": "",
        "featured": False,
        "content_points": [
            ("Ginger's Bioactive Compounds", "The active ingredients in ginger — gingerols (raw) and shogaols (dried/cooked) — are among the most potent anti-inflammatory compounds found in any food. They work on the same molecular pathways as anti-inflammatory drugs, without the side effects."),
            ("Honey's Wound-Healing Power", "Medical-grade Manuka honey is used in hospitals worldwide to treat antibiotic-resistant wounds. The mechanism? Hydrogen peroxide, low pH, and osmotic effect that bacteria cannot adapt to. Your local natural honey shares these properties."),
            ("Together, They Amplify", "Ginger and honey have synergistic effects — ginger reduces inflammation while honey fights bacteria, and together they support gut health, immunity, and respiratory health simultaneously."),
            ("The Nigerian Cold Remedy", "Ginger tea with honey and lemon is Nigeria's most effective home remedy for colds and sore throats — and it's not anecdotal. All three ingredients have been shown to reduce cold duration and severity in clinical trials."),
            ("Daily Prevention, Not Just Cure", "You don't have to wait until you're sick. A daily Erisco Ginger & Honey drink keeps your immune system primed, your gut healthy, and your energy levels steady throughout the day."),
        ],
        "product_link": "honey",
        "product_name": "Erisco Green Tea & Honey",
    },
    {
        "slug": "seasoning-and-health",
        "title": "The Secret Weapon in Nigerian Soups: Why Seasoning Matters",
        "category": "Cooking Tips",
        "category_color": "#e8a020",
        "read_time": "3 min read",
        "excerpt": "Nigerian soups are some of the most nutritionally complex foods in the world. The secret isn't just the protein — it's the seasoning. Here's why what you put in your pot matters as much as what you put on the plate.",
        "image": "img/seasoning.jpeg",
        "emoji": "",
        "featured": False,
        "content_points": [
            ("Umami and Satiety", "Savoury, umami-rich seasoning doesn't just make food taste better — it increases satiety signals in the brain, meaning you feel fuller on less food. Good seasoning is actually a tool for healthy eating."),
            ("Herbs as Medicine", "The herbs in quality seasoning blends — thyme, basil, oregano — contain flavonoids, terpenes, and essential oils that have antimicrobial, anti-inflammatory, and antioxidant effects. Every pot of soup seasoned with Ric-Giko Mixed Herbs is a pot of functional food."),
            ("Glutamate and Brain Health", "Natural glutamates (from fish, chicken, and beef) provide the umami backbone of Nigerian cuisine. These are different from artificial MSG and support neurotransmitter function in the brain."),
            ("Reducing Salt Dependency", "Well-blended seasoning cubes carry so much flavour complexity that you naturally use less salt. For people managing blood pressure, switching from plain salt to flavourful, balanced seasoning can make a real difference."),
            ("The Quality Difference", "Not all seasoning cubes are equal. Ric-Giko cubes are produced under NAFDAC guidelines with consistent, balanced formulations — meaning every cube you use delivers predictable, safe, quality flavour."),
        ],
        "product_link": None,
        "product_name": None,
    },
]

RECIPES = [
    {
        "slug": "classic-tomato-stew",
        "title": "Classic Nigerian Tomato Stew",
        "subtitle": "The foundation of Nigerian cooking — done right.",
        "emoji": "",
        "category": "Main Dish",
        "time": "45 mins",
        "serves": "6–8",
        "difficulty": "Easy",
        "color_from": "#C8102E", "color_to": "#8b0000",
        "image": "img/tomatoes.jpeg",
        "product": "Erisco Tomato Paste 210g",
        "product_category": "tomato",
        "intro": "This is the stew that built a nation. Every Nigerian family has their version — this is ours. Rich, deeply flavoured, and endlessly versatile, it works as a base for rice, beans, yam, plantain, and more.",
        "ingredients": [
            "2 tins Erisco Tomato Paste 210g",
            "500g fresh peppers (tatashe + scotch bonnet)",
            "1 large onion, blended",
            "500ml vegetable or palm oil",
            "500g protein of choice (chicken, beef, or fish)",
            "2 Ric-Giko Chicken Seasoning Cubes",
            "Salt to taste",
            "1 tsp thyme",
            "1 bay leaf",
        ],
        "steps": [
            "Season and fry (or grill) your protein until cooked through. Set aside.",
            "In a large pot, heat the oil over medium-high heat until it shimmers.",
            "Add the blended onion and fry for 3 minutes until the raw smell disappears.",
            "Add the Erisco Tomato Paste and fry for 10–15 minutes, stirring frequently, until the paste darkens and the oil floats to the top.",
            "Add the blended peppers and fry for another 10 minutes.",
            "Add your seasoning cubes, thyme, and bay leaf. Stir well.",
            "Add the cooked protein and a splash of the protein's stock. Simmer for 10 minutes.",
            "Taste, adjust salt, and serve over rice or with any swallow.",
        ],
        "tip": "The key to a great tomato stew is patience during the frying stage. Don't rush it — the longer you fry out the tomato paste, the richer and sweeter the flavour.",
    },
    {
        "slug": "smoky-jollof-rice",
        "title": "Smoky Party Jollof Rice",
        "subtitle": "The legendary Nigerian party staple — perfected.",
        "emoji": "",
        "image": "img/jollof_rice.jpg",
        "category": "Main Dish",
        "time": "1 hr 15 mins",
        "serves": "8–10",
        "difficulty": "Medium",
        "color_from": "#e8a020", "color_to": "#C8102E",
        "product": "Ric-Giko Chicken Seasoning Cubes",
        "product_category": "seasoning",
        "intro": "Party jollof rice is in a class of its own. The smokiness comes from intentional bottom-burning — a technique Nigerian cooks have perfected over decades. This recipe gives you that distinctive smoky depth every time.",
        "ingredients": [
            "4 cups long-grain parboiled rice",
            "2 tins Erisco Tomato Paste 135g",
            "500g fresh blended peppers and tomatoes",
            "2 large onions (1 blended, 1 sliced for frying)",
            "500ml vegetable oil",
            "3 Ric-Giko Chicken Seasoning Cubes",
            "2 bay leaves",
            "1 tsp thyme",
            "1 tsp curry powder",
            "500ml chicken stock",
            "Salt to taste",
        ],
        "steps": [
            "Make your tomato base: fry the blended onion in hot oil for 3 minutes, add Erisco Tomato Paste, fry 10 minutes, then add blended peppers and fry another 10 minutes.",
            "Add seasoning cubes, thyme, curry, bay leaves, and stock. Stir to combine.",
            "Rinse your rice until the water runs clear. Add directly to the tomato base.",
            "The liquid should just cover the rice. Add more stock or water if needed.",
            "Cover tightly with foil, then a lid. Cook on medium heat for 20 minutes.",
            "Reduce heat to very low for 10–15 minutes — this is where the smokiness develops.",
            "For maximum smoky flavour, remove the lid and foil in the last 5 minutes and let the bottom catch slightly.",
            "Fluff with a fork, mix through, and serve immediately.",
        ],
        "tip": "The smoking at the end is not burning — it is 'the bottom pot'. Listen for the sizzle, trust the process, and remove from heat when you hear consistent crackling.",
    },
    {
        "slug": "green-tea-immunity-booster",
        "title": "Green Tea Immunity Booster",
        "subtitle": "Your daily defence — brewed in minutes.",
        "emoji": "",
        "image": "img/green_tea_immunity.jpeg",
        "category": "Wellness Drink",
        "time": "5 mins",
        "serves": "1",
        "difficulty": "Easy",
        "color_from": "#2ecc71", "color_to": "#1a8a47",
        "product": "Erisco Green Tea & Ginger",
        "product_category": "tea",
        "intro": "Three of nature's most powerful immune-supporting ingredients in a single cup. Takes five minutes. Tastes incredible. Your morning just got an upgrade.",
        "ingredients": [
            "1 Erisco Green Tea & Ginger tea bag",
            "1 tsp raw honey (or Erisco Ginger & Honey Drink as base)",
            "1 slice fresh lemon",
            "A small piece of fresh ginger (optional, for extra kick)",
            "250ml hot water (80–85°C — not boiling)",
        ],
        "steps": [
            "Heat your water to 80–85°C. If you don't have a thermometer, boil and wait 2 minutes.",
            "If using fresh ginger, muddle or slice it and add to the cup first.",
            "Pour the hot water over the ginger (if using) and let it steep for 1 minute.",
            "Add the Erisco Green Tea & Ginger tea bag and steep for 2–3 minutes.",
            "Remove the tea bag. Do not squeeze — it releases bitterness.",
            "Add the honey and stir until dissolved.",
            "Squeeze in the lemon slice, drop it in, and drink immediately.",
        ],
        "tip": "For a cold version: brew double-strength (2 tea bags) and pour over ice. Add honey and lemon. Sip through the day as an iced wellness drink.",
    },
    {
        "slug": "ginger-honey-cold-remedy",
        "title": "Ginger Honey Cold Remedy Drink",
        "subtitle": "Nigeria's most effective home remedy — scientifically validated.",
        "emoji": "",
        "image": "img/erisco_green_tea.jpeg",
        "category": "Wellness Drink",
        "time": "10 mins",
        "serves": "1",
        "difficulty": "Easy",
        "color_from": "#f0a500", "color_to": "#e8a020",
        "product": "Erisco Ginger & Honey Drink",
        "product_category": "beverages",
        "intro": "When the harmattan comes, this is what you reach for. Our grandmothers called it agbo. Scientists call it evidence-based. We call it delicious. Either way — it works.",
        "ingredients": [
            "1 sachet Erisco Ginger & Honey Drink",
            "250ml hot water",
            "1 tsp natural honey",
            "Half a fresh lemon",
            "1 clove of garlic (optional — for serious cold-fighting)",
            "A pinch of cayenne pepper (optional)",
        ],
        "steps": [
            "Heat the water to near-boiling (95°C).",
            "If using garlic, crush or slice and add to the water. Let steep 2 minutes.",
            "Pour the Erisco Ginger & Honey Drink sachet into your mug.",
            "Pour the hot water over and stir until fully dissolved.",
            "Add the honey and stir.",
            "Squeeze in the lemon.",
            "If using cayenne, add the smallest pinch — it adds warmth and helps clear congestion.",
            "Drink while hot. Repeat up to 3 times a day when fighting a cold.",
        ],
        "tip": "This drink is also excellent as a preventive — drink one cup every morning during harmattan season to keep your immune system primed.",
    },
    {
        "slug": "rich-egusi-soup",
        "title": "Rich & Flavourful Egusi Soup",
        "subtitle": "The king of Nigerian soups — elevated.",
        "emoji": "",
        "image": "img/egusi.jpeg",
        "category": "Soup",
        "time": "1 hr",
        "serves": "6",
        "difficulty": "Medium",
        "color_from": "#e8a020", "color_to": "#b87a10",
        "product": "Ric-Giko Fish Seasoning Cubes",
        "product_category": "seasoning",
        "intro": "Egusi soup is Nigeria's most beloved and complex soup — a dish that rewards patience and the right seasoning. The secret to exceptional egusi is layering flavour at every stage, and that starts with the seasoning.",
        "ingredients": [
            "2 cups ground egusi (melon seeds)",
            "500g beef (assorted cuts)",
            "200g stockfish, soaked and cleaned",
            "200g dried fish, cleaned",
            "2 Ric-Giko Fish Seasoning Cubes",
            "1 Ric-Giko Chicken Seasoning Cube",
            "300ml palm oil",
            "2 cups blended peppers",
            "1 tin Erisco Tomato Paste 70g",
            "Bitter leaf or spinach, washed",
            "Salt to taste",
        ],
        "steps": [
            "Season and cook your beef and stockfish in a pot with one fish seasoning cube until tender. Reserve the stock.",
            "Heat palm oil in a large pot on medium heat (do not allow to smoke).",
            "Add the blended peppers and fry for 10 minutes.",
            "Add the Erisco Tomato Paste and fry another 5 minutes.",
            "Mix the ground egusi with a little water to form a thick paste. Add in dollops to the pot.",
            "Do not stir — let the egusi clumps fry and set for 5 minutes, then carefully stir.",
            "Add the cooked meats, stockfish, dried fish, and the meat stock. Stir to combine.",
            "Add remaining seasoning cubes and salt. Simmer 15 minutes.",
            "Add the washed bitter leaf or spinach. Stir and cook 5 more minutes.",
            "Serve with pounded yam, eba, or amala.",
        ],
        "tip": "The key texture of egusi is achieved by frying the egusi paste in the oil before adding liquid. Patience here is what separates a good egusi from a great one.",
    },
    {
        "slug": "nagiko-hot-chocolate",
        "title": "Creamy Nagiko Hot Chocolate",
        "subtitle": "Rich, comforting, and made in Nigeria.",
        "emoji": "",
        "image": "img/hot_chocolate.jpeg",
        "category": "Drink",
        "time": "8 mins",
        "serves": "1–2",
        "difficulty": "Easy",
        "color_from": "#4a2c0a", "color_to": "#273272",
        "product": "Nagiko Chocolate Cubes",
        "product_category": "milk",
        "intro": "A hot chocolate that actually tastes like chocolate — rich, smooth, and deeply satisfying. Nagiko Chocolate Cubes dissolve beautifully in warm milk, creating a drink that feels indulgent but is grounded in simple, quality ingredients.",
        "ingredients": [
            "3 Nagiko Chocolate Cubes",
            "2 cups Ricvita Milk Powder (reconstituted) or fresh whole milk",
            "1 tsp natural honey (optional)",
            "A pinch of ground cinnamon",
            "A pinch of nutmeg",
            "Whipped cream to serve (optional)",
        ],
        "steps": [
            "Reconstitute Ricvita Milk Powder according to pack instructions, or warm fresh whole milk in a saucepan.",
            "Heat the milk gently over medium-low heat — do not boil.",
            "Add the Nagiko Chocolate Cubes and whisk continuously until fully melted and smooth.",
            "Add the pinch of cinnamon and nutmeg. Whisk again.",
            "If you like it sweeter, add the honey and stir.",
            "Pour into a mug through a small strainer for a perfectly smooth drink.",
            "Top with whipped cream and a dusting of cinnamon if serving to guests.",
        ],
        "tip": "For an extra-rich version, use equal parts milk and water when reconstituting the Ricvita Milk Powder. The higher fat content makes the hot chocolate significantly creamier.",
    },
]

FIND_US_STATES = [
    {"name": "Lagos", "stores": "12,000+", "anchor": "Ikeja, Victoria Island, Surulere, Lekki, Apapa"},
    {"name": "Abuja (FCT)", "stores": "4,500+", "anchor": "Wuse, Garki, Gwarinpa, Maitama"},
    {"name": "Ogun State", "stores": "3,200+", "anchor": "Sango-Otta (HQ), Abeokuta, Ijebu-Ode"},
    {"name": "Rivers State", "stores": "3,800+", "anchor": "Port Harcourt, Obio-Akpor"},
    {"name": "Kano State", "stores": "4,100+", "anchor": "Kano City, Nassarawa, Fagge"},
    {"name": "Oyo State", "stores": "3,600+", "anchor": "Ibadan, Ogbomosho, Oyo"},
    {"name": "Anambra State", "stores": "2,900+", "anchor": "Onitsha, Awka, Nnewi"},
    {"name": "Delta State", "stores": "2,400+", "anchor": "Asaba, Warri, Effurun"},
    {"name": "Enugu State", "stores": "2,100+", "anchor": "Enugu City, Nsukka"},
    {"name": "Cross River", "stores": "1,800+", "anchor": "Calabar, Ikom"},
    {"name": "Kaduna State", "stores": "2,800+", "anchor": "Kaduna City, Zaria"},
    {"name": "All Other States", "stores": "Nationwide", "anchor": "Available in all 36 states + FCT"},
]

# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@app.route("/")
def index():
    featured_articles = [a for a in BLOG_ARTICLES if a["featured"]][:3]
    featured_recipes  = RECIPES[:3]
    return render_template("index.html", featured_articles=featured_articles, featured_recipes=featured_recipes)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/products")
@app.route("/products/<category>")
def products(category=None):
    if category and category not in CATEGORIES:
        abort(404)
    active = CATEGORIES.get(category) if category else None
    return render_template("products.html", categories=CATEGORIES, active_key=category, active=active)

@app.route("/products/tea/<slug>")
def tea_detail(slug):
    detail = TEA_DETAILS.get(slug)
    if not detail:
        abort(404)
    related = [a for a in BLOG_ARTICLES if detail["name"] in a.get("related_articles", []) or any(detail["name"] in x for x in a.get("related_articles", []))][:2]
    return render_template("product_detail.html", tea=detail, slug=slug, related_articles=related)

@app.route("/brands")
def brands():
    return render_template("brands.html")

@app.route("/blog")
def blog():
    category_filter = request.args.get("category", "")
    articles = BLOG_ARTICLES
    categories = sorted({a["category"] for a in BLOG_ARTICLES})
    if category_filter:
        articles = [a for a in articles if a["category"] == category_filter]
    return render_template("blog.html", articles=articles, categories=categories, active_category=category_filter)

@app.route("/blog/<slug>")
def blog_article(slug):
    article = next((a for a in BLOG_ARTICLES if a["slug"] == slug), None)
    if not article:
        abort(404)
    tea_product = None
    if article.get("product_link"):
        tea_product = TEA_DETAILS.get(article["product_link"])
    related = [a for a in BLOG_ARTICLES if a["slug"] != slug][:3]
    return render_template("blog_article.html", article=article, tea_product=tea_product, related=related)

@app.route("/recipes")
def recipes():
    category_filter = request.args.get("category", "")
    all_recipes = RECIPES
    cat_options = sorted({r["category"] for r in RECIPES})
    if category_filter:
        all_recipes = [r for r in all_recipes if r["category"] == category_filter]
    return render_template("recipes.html", recipes=all_recipes, cat_options=cat_options, active_category=category_filter)

@app.route("/recipes/<slug>")
def recipe_detail(slug):
    recipe = next((r for r in RECIPES if r["slug"] == slug), None)
    if not recipe:
        abort(404)
    related = [r for r in RECIPES if r["slug"] != slug][:3]
    return render_template("recipe_detail.html", recipe=recipe, related=related)

@app.route("/find-us")
def find_us():
    return render_template("find_us.html", states=FIND_US_STATES)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name    = request.form.get("name", "").strip()
        email   = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not name or not email or not message:
            flash("Please fill in all required fields.", "error")
        else:
            flash(f"Thank you, {name}! Your message has been received. We'll respond within 2 business days.", "success")
            return redirect(url_for("contact"))
    return render_template("contact.html")

# ─────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
