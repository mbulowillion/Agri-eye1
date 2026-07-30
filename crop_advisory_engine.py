"""Crop advisory engine — Zambian-focused crop database with suitability scoring."""

ZAMBIAN_CROPS = [
    # ===== GRAINS & STAPLES =====
    {
        "id": "maize", "name": "Maize", "zambian_name": "Chimanga / Chimbwali",
        "climates": ["tropical", "subtropical", "temperate"],
        "min_ph": 5.5, "max_ph": 7.0, "suitable_soils": ["loamy", "silt", "clay"],
        "min_temp": 18, "max_temp": 32, "min_rainfall": 500, "max_rainfall": 1200,
        "yield_per_hectare": 6.5, "growth_days": 130,
        "description": "Primary Zambian cereal staple for Nshima. Grown nationwide with most production in Central, Eastern, and Southern provinces.",
        "stages": [("Seedbed Preparation", 10, "Deep tilling, basal D-Compound fertilizer application."), ("Germination & Emergence", 12, "Coleoptile emergence and root initiation."), ("Vegetative Stalk Elongation", 45, "Rapid stem extension, top-dressing with Urea."), ("Tasseling & Silking", 25, "Pollination stage; sensitive to moisture deficits."), ("Grain Filling & Maturity", 38, "Black layer formation and cob drying.")]},
    {
        "id": "cassava", "name": "Cassava", "zambian_name": "Chinangwa / Kalundwe",
        "climates": ["tropical", "subtropical", "semi-arid"],
        "min_ph": 4.5, "max_ph": 7.5, "suitable_soils": ["loamy", "sandy", "laterite"],
        "min_temp": 20, "max_temp": 35, "min_rainfall": 500, "max_rainfall": 1500,
        "yield_per_hectare": 15.0, "growth_days": 300,
        "description": "Drought-tolerant staple root crop critical for food security. Widely grown in Luapula, Northern, and Muchinga provinces.",
        "stages": [("Seedbed & Cuttings Selection", 14, "Selecting disease-free stem cuttings (20-25cm)."), ("Sprouting & Rooting", 30, "Early adventitious root formation and shoot sprouting."), ("Vegetative Canopy Growth", 120, "Rapid leaf canopy expansion and solar interception."), ("Tuberization & Bulking", 90, "Translocation of starches into storage roots."), ("Maturity & Harvest", 46, "Full root starch accumulation and manual lifting.")]},
    {
        "id": "rice", "name": "Rice", "zambian_name": "Mupunga",
        "climates": ["tropical", "subtropical"],
        "min_ph": 5.0, "max_ph": 6.5, "suitable_soils": ["clay", "silt", "loamy"],
        "min_temp": 20, "max_temp": 38, "min_rainfall": 1000, "max_rainfall": 2500,
        "yield_per_hectare": 4.5, "growth_days": 140,
        "description": "Staple crop in floodplains like Barotse Floodplain. Grown mainly in Western, Northern, and Luapula provinces.",
        "stages": [("Nursery / Puddled Field", 20, "Seed germination and nursery seedling growth."), ("Transplanting & Tillering", 35, "Setting seedlings in flooded puddled soil."), ("Panicle Initiation & Booting", 35, "Internode elongation and panicle formation."), ("Flowering & Grain Milk", 25, "Pollination and watery starch accumulation."), ("Field Drainage & Harvest", 25, "Drying paddy and sickle cutting.")]},
    {
        "id": "sorghum", "name": "Sorghum", "zambian_name": "Mapira",
        "climates": ["tropical", "semi-arid", "arid"],
        "min_ph": 5.5, "max_ph": 8.5, "suitable_soils": ["loamy", "clay", "sandy"],
        "min_temp": 22, "max_temp": 38, "min_rainfall": 400, "max_rainfall": 800,
        "yield_per_hectare": 3.8, "growth_days": 120,
        "description": "Resilient C4 grain crop with deep root system, ideal for drought-prone zones of Southern and Western provinces.",
        "stages": [("Seedbed Sowing", 8, "Fine seedbed planting at 2-3cm depth."), ("Seedling & Tillering", 25, "Development of primary tillers and crown roots."), ("Booting & Panicle Initiation", 35, "Flag leaf emergence holding developing panicle."), ("Grain Soft & Hard Dough", 32, "Starch filling in grain head."), ("Panicle Drying & Harvest", 20, "Clipping panicles and threshing.")]},
    {
        "id": "millet", "name": "Millet", "zambian_name": "Malezi",
        "climates": ["tropical", "semi-arid", "arid"],
        "min_ph": 5.0, "max_ph": 7.5, "suitable_soils": ["sandy", "loamy"],
        "min_temp": 22, "max_temp": 38, "min_rainfall": 300, "max_rainfall": 800,
        "yield_per_hectare": 2.5, "growth_days": 110,
        "description": "Drought-tolerant grain crop suited to poor sandy soils. Grown in Western, Southern and Central provinces.",
        "stages": [("Seedbed Sowing", 8, "Broadcast or drill seeding."), ("Seedling & Tillering", 20, "Fine grass-like tiller development."), ("Panicle Initiation", 30, "Seed head formation inside stem."), ("Grain Filling", 30, "Nutrient translocation to developing grain."), ("Harvest & Threshing", 22, "Head cutting and manual threshing.")]},
    {
        "id": "wheat", "name": "Wheat", "zambian_name": "Tirigu",
        "climates": ["temperate", "subtropical", "highland"],
        "min_ph": 5.5, "max_ph": 7.0, "suitable_soils": ["loamy", "clay", "silt"],
        "min_temp": 8, "max_temp": 28, "min_rainfall": 400, "max_rainfall": 900,
        "yield_per_hectare": 5.0, "growth_days": 120,
        "description": "Irrigated winter cereal grown on commercial farms in Central and Mkushi areas.",
        "stages": [("Seedbed Preparation", 10, "Fine seedbed with basal fertilizer."), ("Germination & Tillering", 25, "Seedling emergence and tiller development."), ("Stem Elongation & Booting", 35, "Rapid stem growth and head formation."), ("Flowering & Grain Fill", 30, "Anthesis and starch accumulation."), ("Combine Harvest", 20, "Mechanical harvesting at 14% moisture.")]},
    # ===== ROOT & TUBER CROPS =====
    {
        "id": "sweet_potato", "name": "Sweet Potato", "zambian_name": "Kandolo",
        "climates": ["tropical", "subtropical", "highland"],
        "min_ph": 5.5, "max_ph": 6.8, "suitable_soils": ["sandy", "loamy"],
        "min_temp": 18, "max_temp": 28, "min_rainfall": 750, "max_rainfall": 1250,
        "yield_per_hectare": 12.0, "growth_days": 110,
        "description": "Nutritious orange-fleshed tuber high in Vitamin A. Grown nationwide in smallholder gardens.",
        "stages": [("Mound/Ridge Planting", 10, "Planting vine cuttings on raised ridges."), ("Vine Establishment", 20, "Adventitious root anchoring and vine spreading."), ("Root Initiation & Canopy", 35, "Rapid vine extension and leaf carpet."), ("Storage Root Enlargement", 30, "Carbohydrate storage in modified roots."), ("Harvest & Curing", 15, "Manual digging and skin curing.")]},
    {
        "id": "potato", "name": "Irish Potato", "zambian_name": "Mbatata / Viazi",
        "climates": ["temperate", "highland", "subtropical"],
        "min_ph": 5.0, "max_ph": 6.5, "suitable_soils": ["sandy", "loamy"],
        "min_temp": 12, "max_temp": 24, "min_rainfall": 500, "max_rainfall": 1000,
        "yield_per_hectare": 20.0, "growth_days": 90,
        "description": "Cool-season tuber crop grown in high-altitude areas of Northern, Muchinga, and parts of Central province.",
        "stages": [("Seed Bed Preparation", 10, "Chitting seed potatoes in diffused light."), ("Planting & Emergence", 20, "Planting in ridges at 30cm spacing."), ("Vegetative Growth & Tuber Initiation", 25, "Stolon formation and early tuber set."), ("Tuber Bulking", 25, "Starch accumulation in expanding tubers."), ("Senescence & Harvest", 10, "Haulm killing and tuber lifting.")]},
    # ===== LEGUMES =====
    {
        "id": "groundnuts", "name": "Groundnuts", "zambian_name": "Mbalala / Syawala",
        "climates": ["tropical", "subtropical", "semi-arid"],
        "min_ph": 5.8, "max_ph": 6.8, "suitable_soils": ["sandy", "loamy"],
        "min_temp": 20, "max_temp": 30, "min_rainfall": 500, "max_rainfall": 1000,
        "yield_per_hectare": 2.2, "growth_days": 120,
        "description": "Key legume crop providing protein and soil nitrogen fixation. Grown in Eastern, Central, and Northern provinces.",
        "stages": [("Seedbed & Ridge Formation", 10, "Loose friable soil bed for easy pegging."), ("Germination & Seedling", 14, "Unfolding of trifoliate leaves."), ("Branching & Flowering", 30, "Yellow flower emergence and self-pollination."), ("Pegging & Pod Formation", 40, "Peg insertion into soil and pod enlargement."), ("Pod Ripening & Drying", 26, "Lifting, windrow curing, and stripping.")]},
    {
        "id": "soybean", "name": "Soybean", "zambian_name": "Soya Beans",
        "climates": ["subtropical", "temperate", "highland"],
        "min_ph": 6.0, "max_ph": 7.0, "suitable_soils": ["loamy", "silt", "clay"],
        "min_temp": 20, "max_temp": 30, "min_rainfall": 500, "max_rainfall": 900,
        "yield_per_hectare": 3.2, "growth_days": 115,
        "description": "High-value commercial legume for livestock feed and oil processing. Grown in Central, Eastern, and Mkushi regions.",
        "stages": [("Seedbed Inoculation", 8, "Inoculating seed with Bradyrhizobium."), ("Emergence", 15, "Unifoliate and trifoliate leaf expansion."), ("Vegetative Canopy Growth", 32, "Node development and leaf area accumulation."), ("Flowering & Pod Fill", 35, "Cluster pod formation and seed filling."), ("Defoliation & Harvest", 25, "Leaf drop, pod browning, combine harvesting.")]},
    {
        "id": "beans", "name": "Common Beans", "zambian_name": "Nyemba / Mahalaga",
        "climates": ["tropical", "subtropical", "highland"],
        "min_ph": 5.8, "max_ph": 7.0, "suitable_soils": ["loamy", "sandy", "silt"],
        "min_temp": 16, "max_temp": 28, "min_rainfall": 500, "max_rainfall": 1100,
        "yield_per_hectare": 2.0, "growth_days": 100,
        "description": "Important protein staple in Zambian diet. Grown in Northern, Muchinga, and Eastern provinces.",
        "stages": [("Seedbed Sowing", 8, "Direct seeding at 2-3cm depth."), ("Seedling & Vine Growth", 20, "Trifoliate leaf expansion and stem elongation."), ("Flowering", 20, "White/purple flower cluster formation."), ("Pod Filling", 30, "Green pod expansion and seed development."), ("Pod Drying & Harvest", 22, "Field drying and hand picking.")]},
    {
        "id": "cowpea", "name": "Cowpea", "zambian_name": "Nyemba / Nandolo",
        "climates": ["tropical", "semi-arid", "subtropical"],
        "min_ph": 5.5, "max_ph": 7.0, "suitable_soils": ["sandy", "loamy"],
        "min_temp": 20, "max_temp": 35, "min_rainfall": 350, "max_rainfall": 800,
        "yield_per_hectare": 1.8, "growth_days": 90,
        "description": "Drought-tolerant legume for grain and leaves. Grown in Western, Southern, and Eastern provinces.",
        "stages": [("Seedbed Planting", 8, "Direct seeding in moist soil."), ("Seedling & Vine Growth", 20, "Rapid vine spread and leaf development."), ("Flowering", 15, "Purple flower clusters."), ("Pod Formation & Filling", 30, "Green pod development and seed maturation."), ("Harvesting", 17, "Multiple pickings of mature pods.")]},
    {
        "id": "pigeon_pea", "name": "Pigeon Pea", "zambian_name": "Fwambila / Mwande",
        "climates": ["tropical", "semi-arid", "subtropical"],
        "min_ph": 5.5, "max_ph": 7.5, "suitable_soils": ["sandy", "loamy"],
        "min_temp": 18, "max_temp": 35, "min_rainfall": 350, "max_rainfall": 900,
        "yield_per_hectare": 2.5, "growth_days": 200,
        "description": "Perennial shrub legume providing food and soil improvement. Grown in Eastern and parts of Southern province.",
        "stages": [("Seedbed Sowing", 10, "Direct seeding at start of rains."), ("Seedling & Branching", 40, "Shrub establishment and branching."), ("Flowering Initiation", 60, "Photo-period sensitive flowering."), ("Pod Development & Fill", 60, "Multiple pod set and seed filling."), ("Sequential Harvest", 30, "Multiple pickings of mature pods.")]},
    {
        "id": "bambara", "name": "Bambara Groundnut", "zambian_name": "Mpama / Ndundu",
        "climates": ["tropical", "semi-arid"],
        "min_ph": 5.0, "max_ph": 7.0, "suitable_soils": ["sandy", "loamy"],
        "min_temp": 22, "max_temp": 35, "min_rainfall": 300, "max_rainfall": 700,
        "yield_per_hectare": 2.0, "growth_days": 150,
        "description": "Indigenous drought-tolerant legume with high protein. Grown in Western, Southern, and Eastern provinces.",
        "stages": [("Seedbed Planting", 10, "Plant seeds in well-drained sandy soil."), ("Seedling & Spreading", 25, "Prostrate growth and trifoliate leaf development."), ("Flowering & Pegging", 40, "Yellow flowers and peg insertion into soil."), ("Pod Development", 50, "Underground pod filling and maturation."), ("Harvest & Drying", 25, "Lifting plants and sun drying pods.")]},
    # ===== CASH / INDUSTRIAL CROPS =====
    {
        "id": "cotton", "name": "Cotton", "zambian_name": "Pamba",
        "climates": ["tropical", "subtropical", "arid", "semi-arid"],
        "min_ph": 5.8, "max_ph": 8.0, "suitable_soils": ["loamy", "clay", "laterite"],
        "min_temp": 22, "max_temp": 38, "min_rainfall": 500, "max_rainfall": 1000,
        "yield_per_hectare": 2.8, "growth_days": 160,
        "description": "Commercial lint crop suited for warmer valley regions. Grown in Eastern, Central, Lusaka, and Southern provinces.",
        "stages": [("Seedbed Planting", 10, "Delinted seed placement in moist warm soil."), ("Seedling & Square Formation", 35, "Appearance of triangular flower buds (squares)."), ("Bloom & Boll Development", 50, "White-to-pink flower transition and boll sizing."), ("Boll Opening", 40, "Lint fiber drying and fluffing."), ("Hand Picking Harvest", 25, "Selective lint harvesting in clean sacks.")]},
    {
        "id": "tobacco", "name": "Tobacco", "zambian_name": "Fwaka",
        "climates": ["subtropical", "tropical"],
        "min_ph": 5.5, "max_ph": 6.5, "suitable_soils": ["sandy", "loamy"],
        "min_temp": 20, "max_temp": 32, "min_rainfall": 600, "max_rainfall": 1200,
        "yield_per_hectare": 2.9, "growth_days": 120,
        "description": "High-value commercial industrial crop. Grown in Eastern, Central, and parts of Southern province.",
        "stages": [("Float Seedbed Nursery", 45, "Pelleted seed germination in floating trays."), ("Field Re-planting", 15, "Transplanting sturdy seedlings into ridges."), ("Rapid Leaf Expansion", 30, "Broad leaf development and topping."), ("Priming Harvest", 20, "Sequential harvesting of mature leaves."), ("Barn Curing", 10, "Temperature controlled flue curing.")]},
    {
        "id": "sugarcane", "name": "Sugarcane", "zambian_name": "Nsukali / Mizuwa",
        "climates": ["tropical", "subtropical"],
        "min_ph": 5.5, "max_ph": 7.5, "suitable_soils": ["loamy", "clay", "silt"],
        "min_temp": 22, "max_temp": 36, "min_rainfall": 1000, "max_rainfall": 2000,
        "yield_per_hectare": 80.0, "growth_days": 365,
        "description": "Commercial sugar crop grown under irrigation. Mostly cultivated in Mazabuka, Nakambala Sugar Estate.",
        "stages": [("Land Preparation & Planting", 30, "Furrow planting of cane setts."), ("Tillering & Stool Establishment", 60, "Multiple shoot formation from planted setts."), ("Grand Growth Phase", 150, "Rapid stalk elongation and sugar accumulation."), ("Ripening & Maturation", 90, "Sugar concentration increase in stalks."), ("Cane Harvest & Transport", 35, "Mechanical or manual cane cutting.")]},
    {
        "id": "sunflower", "name": "Sunflower", "zambian_name": "Sanamvula",
        "climates": ["subtropical", "semi-arid", "temperate"],
        "min_ph": 6.0, "max_ph": 7.5, "suitable_soils": ["loamy", "clay", "sandy"],
        "min_temp": 20, "max_temp": 32, "min_rainfall": 500, "max_rainfall": 1000,
        "yield_per_hectare": 2.5, "growth_days": 100,
        "description": "Oilseed cash crop widely cultivated in Central, Eastern, and Southern provinces.",
        "stages": [("Seedbed Sowing", 8, "Direct seeding into moist seedbed."), ("Vegetative Canopy", 30, "Broad leaf arrangement and stem thickening."), ("Budding & Flowering", 25, "Heliotropic head following sun path."), ("Seed Development", 22, "Achene filling and back-head yellowing."), ("Head Harvest & Threshing", 15, "Drying heads and mechanical or manual threshing.")]},
    {
        "id": "coffee", "name": "Arabica Coffee", "zambian_name": "Kofi",
        "climates": ["highland", "subtropical"],
        "min_ph": 5.5, "max_ph": 6.5, "suitable_soils": ["loamy", "laterite", "silt"],
        "min_temp": 15, "max_temp": 28, "min_rainfall": 1200, "max_rainfall": 2000,
        "yield_per_hectare": 3.5, "growth_days": 270,
        "description": "Premium export crop grown in Northern Province with sweet citrus acidity notes.",
        "stages": [("Nursery Seedling", 60, "Polythene bag nursery under shade."), ("Field Establishment", 30, "Planting in deep fertile pits with organic mulch."), ("Blossom & Berry Set", 60, "White jasmine-scented flowers and cherry formation."), ("Berry Ripening", 90, "Cherries turning deep red."), ("Selective Hand Picking & Wet Milling", 30, "Hand harvesting ripe cherries and pulping.")]},
    {
        "id": "tea", "name": "Tea", "zambian_name": "Tiyi",
        "climates": ["highland", "subtropical"],
        "min_ph": 4.5, "max_ph": 6.0, "suitable_soils": ["loamy", "laterite", "silt"],
        "min_temp": 12, "max_temp": 28, "min_rainfall": 1200, "max_rainfall": 2500,
        "yield_per_hectare": 3.0, "growth_days": 365,
        "description": "Highland beverage crop grown in Northern Province around Kawambwa and Mbala.",
        "stages": [("Nursery", 90, "Clonal propagation in polythene sleeves."), ("Field Planting", 60, "Planting in well-drained acidic soil on contours."), ("Establishment Phase", 180, "Shaping frame and building plucking table."), ("Plucking Cycle", 30, "Continuous shoot harvesting every 14-21 days."), ("Pruning & Maintenance", 5, "Annual pruning to maintain plucking table.")]},
    {
        "id": "cashew", "name": "Cashew", "zambian_name": "Mkanju / Kashew",
        "climates": ["tropical", "semi-arid"],
        "min_ph": 5.5, "max_ph": 7.5, "suitable_soils": ["sandy", "loamy", "laterite"],
        "min_temp": 22, "max_temp": 38, "min_rainfall": 500, "max_rainfall": 1200,
        "yield_per_hectare": 3.0, "growth_days": 365,
        "description": "Emerging nut cash crop in Western Province, especially around Mongu and Senanga.",
        "stages": [("Nursery", 60, "Seedling or grafted plant production."), ("Field Planting & Establishment", 365, "Transplanting and tree establishment phase."), ("Flowering", 60, "Panicle emergence and pollination."), ("Nut Development & Apple Maturation", 90, "Cashew apple swelling and nut hardening."), ("Harvest & Processing", 60, "Collecting fallen nuts and sun drying.")]},
    # ===== FRUITS =====
    {
        "id": "banana", "name": "Banana", "zambian_name": "Ntofu / Ndizi",
        "climates": ["tropical", "subtropical"],
        "min_ph": 5.5, "max_ph": 7.0, "suitable_soils": ["loamy", "sandy", "silt"],
        "min_temp": 22, "max_temp": 35, "min_rainfall": 1000, "max_rainfall": 2000,
        "yield_per_hectare": 25.0, "growth_days": 365,
        "description": "Staple fruit crop grown in homestead gardens nationwide and commercially in Luapula, Northern, and Copperbelt.",
        "stages": [("Sucker Planting", 15, "Planting disease-free tissue culture or suckers."), ("Vegetative Growth", 180, "Pseudostem elongation and leaf production (16-18 leaves)."), ("Bunch Initiation & Emergence", 90, "Flower bud emergence and hand formation."), ("Fruit Filling & Ripening", 70, "Banana finger expansion and yellow ripening."), ("Harvest & Marketing", 10, "Cutting bunches and ripening treatment.")]},
    {
        "id": "mango", "name": "Mango", "zambian_name": "Imango / Mango",
        "climates": ["tropical", "subtropical", "semi-arid"],
        "min_ph": 5.5, "max_ph": 7.5, "suitable_soils": ["loamy", "sandy"],
        "min_temp": 20, "max_temp": 38, "min_rainfall": 400, "max_rainfall": 1200,
        "yield_per_hectare": 15.0, "growth_days": 365,
        "description": "Popular fruit tree grown in homesteads and orchards nationwide, especially in Eastern and Lusaka provinces.",
        "stages": [("Tree Establishment", 365, "Planting grafted seedlings and tree development."), ("Flowering", 60, "Panicle emergence during dry winter months."), ("Fruit Set & Development", 90, "Fruit sizing and internal development."), ("Ripening & Harvest", 30, "Mature green to yellow transition."), ("Post-Harvest Handling", 10, "Careful handling and grading for market.")]},
    {
        "id": "citrus", "name": "Citrus (Orange / Lemon)", "zambian_name": "Malambe / Ndimu",
        "climates": ["subtropical", "tropical"],
        "min_ph": 5.5, "max_ph": 7.5, "suitable_soils": ["loamy", "sandy", "silt"],
        "min_temp": 15, "max_temp": 32, "min_rainfall": 600, "max_rainfall": 1500,
        "yield_per_hectare": 20.0, "growth_days": 365,
        "description": "Commercial fruit crop grown in Lusaka, Central, and Copperbelt provinces with irrigation.",
        "stages": [("Nursery & Grafting", 180, "Raising rootstock and budding scion varieties."), ("Field Planting & Establishment", 180, "Transplanting to well-drained orchard."), ("Flowering & Fruit Set", 60, "Spring blossom and small fruit development."), ("Fruit Growth & Ripening", 240, "Juice sac filling and color break."), ("Harvest & Packing", 30, "Hand picking and grading for market.")]},
    {
        "id": "pineapple", "name": "Pineapple", "zambian_name": "Chinafuta",
        "climates": ["tropical", "subtropical"],
        "min_ph": 4.5, "max_ph": 6.5, "suitable_soils": ["sandy", "loamy"],
        "min_temp": 22, "max_temp": 32, "min_rainfall": 800, "max_rainfall": 1500,
        "yield_per_hectare": 30.0, "growth_days": 360,
        "description": "Tropical fruit grown in Luapula, Northern, and parts of Copperbelt province.",
        "stages": [("Crown/Propagule Planting", 15, "Planting crown or slip propagules."), ("Vegetative Growth", 240, "Slow leaf rosette expansion and root establishment."), ("Flower Induction", 60, "Natural day-length or chemical induction."), ("Fruit Development", 120, "Multiple fruitlet fusion and pineapple formation."), ("Harvest & Trimming", 15, "Maturity harvest and crown trimming.")]},
    {
        "id": "papaya", "name": "Papaya", "zambian_name": "Mapwapwa / Pawpaw",
        "climates": ["tropical", "subtropical"],
        "min_ph": 5.5, "max_ph": 7.0, "suitable_soils": ["sandy", "loamy"],
        "min_temp": 22, "max_temp": 35, "min_rainfall": 800, "max_rainfall": 1500,
        "yield_per_hectare": 30.0, "growth_days": 240,
        "description": "Fast-growing fruit crop grown in homesteads nationwide.",
        "stages": [("Nursery", 30, "Seed germination in polythene tubes."), ("Field Planting & Growth", 120, "Transplanting and rapid vegetative growth."), ("Flowering", 60, "Dioecious or hermaphrodite flower production."), ("Fruit Development", 90, "Pepo fruit expansion and ripening."), ("Harvesting", 30, "Multiple harvests from single plant.")]},
    {
        "id": "avocado", "name": "Avocado", "zambian_name": "Mapapa",
        "climates": ["subtropical", "tropical", "highland"],
        "min_ph": 5.5, "max_ph": 7.0, "suitable_soils": ["loamy", "sandy", "silt"],
        "min_temp": 15, "max_temp": 30, "min_rainfall": 800, "max_rainfall": 1500,
        "yield_per_hectare": 12.0, "growth_days": 365,
        "description": "Emerging high-value fruit crop grown commercially in Lusaka, Central and Copperbelt provinces.",
        "stages": [("Nursery & Grafting", 180, "Raising Hass/Pinkerton grafted seedlings."), ("Field Planting", 30, "Planting in well-drained soils with windbreaks."), ("Tree Development", 540, "Vegetative growth and canopy formation."), ("Flowering & Fruit Set", 60, "Hundreds of flowers per panicle, low fruit set."), ("Fruit Maturation & Harvest", 180, "Oil accumulation and fruit softening.")]},
    {
        "id": "guava", "name": "Guava", "zambian_name": "Mapeyela / Guava",
        "climates": ["tropical", "subtropical"],
        "min_ph": 5.0, "max_ph": 7.0, "suitable_soils": ["sandy", "loamy"],
        "min_temp": 20, "max_temp": 35, "min_rainfall": 500, "max_rainfall": 1200,
        "yield_per_hectare": 18.0, "growth_days": 365,
        "description": "Hardy fruit tree common in village homesteads across Zambia.",
        "stages": [("Nursery", 60, "Seedling or cutting propagation."), ("Field Establishment", 180, "Tree canopy development."), ("Flowering", 60, "Multiple flowering cycles per year."), ("Fruit Development", 120, "Berry enlargement and ripening."), ("Harvesting", 30, "Multiple pickings of mature fruit.")]},
    {
        "id": "watermelon", "name": "Watermelon", "zambian_name": "Milikiti / Kalinga",
        "climates": ["tropical", "semi-arid", "subtropical"],
        "min_ph": 6.0, "max_ph": 7.5, "suitable_soils": ["sandy", "loamy"],
        "min_temp": 22, "max_temp": 36, "min_rainfall": 300, "max_rainfall": 800,
        "yield_per_hectare": 25.0, "growth_days": 85,
        "description": "Popular summer fruit grown in river valleys and market gardens across Zambia.",
        "stages": [("Seedbed Mounds", 8, "Planting 3-4 seeds per mound."), ("Seedling & Vine Growth", 25, "Runner development and leaf expansion."), ("Flowering", 15, "Male and female flower production."), ("Fruit Set & Sizing", 30, "Pollinated ovary expansion and ripening."), ("Harvest", 7, "Tendril drying indicates maturity.")]},
    {
        "id": "passion_fruit", "name": "Passion Fruit", "zambian_name": "Matundwa / Passion",
        "climates": ["tropical", "subtropical", "highland"],
        "min_ph": 6.0, "max_ph": 7.5, "suitable_soils": ["loamy", "sandy"],
        "min_temp": 18, "max_temp": 30, "min_rainfall": 700, "max_rainfall": 1500,
        "yield_per_hectare": 10.0, "growth_days": 240,
        "description": "Emerging high-value fruit for juice market. Grown in Central, Copperbelt, and Lusaka provinces.",
        "stages": [("Nursery", 45, "Seed germination or cutting propagation."), ("Field Planting & Trellis", 30, "Planting at base of trellis system."), ("Vegetative Growth", 120, "Rapid vine coverage on trellis."), ("Flowering & Fruiting", 90, "Fragrant flowers and fruit development."), ("Harvest & Re-planting", 30, "Collecting fallen ripe fruit.")]},
    {
        "id": "strawberry", "name": "Strawberry", "zambian_name": "Sitiroberi",
        "climates": ["highland", "temperate", "subtropical"],
        "min_ph": 5.5, "max_ph": 6.8, "suitable_soils": ["sandy", "loamy"],
        "min_temp": 10, "max_temp": 26, "min_rainfall": 500, "max_rainfall": 1000,
        "yield_per_hectare": 15.0, "growth_days": 120,
        "description": "High-value horticultural fruit grown in Central province and around Lusaka for fresh market and processing.",
        "stages": [("Runner Planting", 10, "Planting certified disease-free runners."), ("Vegetative Establishment", 30, "Crown development and leaf production."), ("Flowering", 20, "White flower cluster emergence."), ("Fruit Development", 30, "Receptacle swelling and red coloring."), ("Multiple Picking", 30, "Daily hand picking of ripe berries.")]},
    # ===== VEGETABLES =====
    {
        "id": "tomato", "name": "Tomato", "zambian_name": "Matimati",
        "climates": ["subtropical", "tropical", "temperate"],
        "min_ph": 6.0, "max_ph": 7.0, "suitable_soils": ["loamy", "silt", "sandy"],
        "min_temp": 18, "max_temp": 30, "min_rainfall": 400, "max_rainfall": 900,
        "yield_per_hectare": 35.0, "growth_days": 90,
        "description": "High-earning horticultural crop in urban market gardens nationwide. Fresh market and processing.",
        "stages": [("Nursery & Seedling Trays", 25, "Germination in seedling trays under shade."), ("Transplanting & Staking", 15, "Setting seedlings on raised beds with trellising."), ("Vegetative & Flowering", 20, "Pruning suckers, applying calcium nitrate."), ("Fruit Set & Sizing", 20, "Cluster fruit expansion and red pigment accumulation."), ("Multiple Harvest Pickings", 10, "Hand picking breaker-stage fruit.")]},
    {
        "id": "onion", "name": "Onion", "zambian_name": "Anyenye / Adyo",
        "climates": ["temperate", "subtropical", "highland"],
        "min_ph": 6.0, "max_ph": 7.0, "suitable_soils": ["sandy", "loamy", "silt"],
        "min_temp": 12, "max_temp": 28, "min_rainfall": 400, "max_rainfall": 900,
        "yield_per_hectare": 25.0, "growth_days": 150,
        "description": "Bulb crop requiring well-drained soil and long days. Grown in Lusaka, Central, and Copperbelt provinces.",
        "stages": [("Nursery", 35, "Seed germination in fine seedbeds."), ("Transplanting", 15, "Setting seedlings on raised beds."), ("Vegetative Growth", 50, "Leaf development and bulb initiation."), ("Bulb Swelling", 35, "Nutrient translocation to developing bulb."), ("Bulb Drying & Harvest", 15, "Neck softening, lifting and curing.")]},
    {
        "id": "cabbage", "name": "Cabbage", "zambian_name": "Kabichi",
        "climates": ["temperate", "subtropical", "highland"],
        "min_ph": 6.0, "max_ph": 7.5, "suitable_soils": ["loamy", "silt", "clay"],
        "min_temp": 10, "max_temp": 25, "min_rainfall": 500, "max_rainfall": 1000,
        "yield_per_hectare": 30.0, "growth_days": 90,
        "description": "Important leafy vegetable in urban markets. Grown nationwide in irrigated market gardens.",
        "stages": [("Nursery", 25, "Seed germination in seedling trays."), ("Transplanting", 10, "Hardening off and field planting."), ("Vegetative Leaf Growth", 30, "Wrapper leaf expansion and head initiation."), ("Head Formation & Firming", 20, "Cabbage head tightening and sizing."), ("Harvest & Trimming", 5, "Cutting at base and removing outer leaves.")]},
    {
        "id": "kale", "name": "Rape / Kale", "zambian_name": "Kanoni / Kale",
        "climates": ["temperate", "subtropical", "highland"],
        "min_ph": 6.0, "max_ph": 7.5, "suitable_soils": ["loamy", "silt"],
        "min_temp": 8, "max_temp": 26, "min_rainfall": 400, "max_rainfall": 900,
        "yield_per_hectare": 15.0, "growth_days": 60,
        "description": "Popular leafy green in urban Zambian diet. Grown in market gardens nationwide.",
        "stages": [("Seedbed", 15, "Direct seeding or transplanting."), ("Early Leaf Growth", 20, "Rapid leaf expansion."), ("Full Canopy", 15, "Dense leaf production."), ("Continuous Harvest", 10, "Leaf picking for fresh market.")]},
    {
        "id": "okra", "name": "Okra", "zambian_name": "Dete",
        "climates": ["tropical", "subtropical", "semi-arid"],
        "min_ph": 5.8, "max_ph": 7.0, "suitable_soils": ["loamy", "sandy"],
        "min_temp": 22, "max_temp": 35, "min_rainfall": 400, "max_rainfall": 900,
        "yield_per_hectare": 8.0, "growth_days": 70,
        "description": "Warm-season vegetable grown in village gardens and urban markets nationwide.",
        "stages": [("Direct Seeding", 8, "Sowing in moist warm soil."), ("Seedling & Vegetative", 25, "Rapid stem growth and leaf expansion."), ("Flowering", 15, "Yellow hibiscus-like flowers."), ("Pod Development", 15, "Green pod elongation (3-5 days to harvest)."), ("Multiple Picking", 7, "Continuous harvest of tender pods.")]},
    {
        "id": "eggplant", "name": "Eggplant", "zambian_name": "Entula / Bilingani",
        "climates": ["tropical", "subtropical"],
        "min_ph": 5.5, "max_ph": 7.0, "suitable_soils": ["loamy", "sandy"],
        "min_temp": 20, "max_temp": 32, "min_rainfall": 400, "max_rainfall": 900,
        "yield_per_hectare": 25.0, "growth_days": 85,
        "description": "Warm-season vegetable grown in market gardens nationwide.",
        "stages": [("Nursery", 25, "Seed germination in seedling trays."), ("Transplanting", 10, "Field planting on ridges."), ("Vegetative & Flowering", 20, "Branching growth and purple flower formation."), ("Fruit Development", 20, "Glossy purple fruit expansion."), ("Multiple Harvest", 10, "Cutting fruit with calyx attached.")]},
    {
        "id": "bell_pepper", "name": "Bell Pepper / Chili", "zambian_name": "Sabola / Pilipili",
        "climates": ["tropical", "subtropical", "temperate"],
        "min_ph": 5.5, "max_ph": 7.0, "suitable_soils": ["loamy", "sandy"],
        "min_temp": 18, "max_temp": 30, "min_rainfall": 400, "max_rainfall": 900,
        "yield_per_hectare": 20.0, "growth_days": 80,
        "description": "High-value horticultural crop for fresh market and processing. Grown in Lusaka, Copperbelt, and Central.",
        "stages": [("Nursery", 25, "Seedling tray germination."), ("Transplanting", 10, "Setting seedlings on beds."), ("Vegetative & Flowering", 20, "White flower emergence and branching."), ("Fruit Set & Development", 20, "Green-to-red pepper maturation."), ("Multiple Harvest", 5, "Hand harvesting at desired color stage.")]},
    {
        "id": "cucumber", "name": "Cucumber", "zambian_name": "Makaka",
        "climates": ["tropical", "subtropical"],
        "min_ph": 6.0, "max_ph": 7.0, "suitable_soils": ["loamy", "sandy"],
        "min_temp": 20, "max_temp": 32, "min_rainfall": 400, "max_rainfall": 900,
        "yield_per_hectare": 20.0, "growth_days": 65,
        "description": "Warm-season vegetable grown in market gardens for salad market.",
        "stages": [("Direct Seeding", 8, "Sowing on mounds or ridges."), ("Seedling & Vine Growth", 20, "Rapid runner development."), ("Flowering", 12, "Male and female yellow flowers."), ("Fruit Development", 15, "Cucumber elongation and sizing."), ("Multiple Harvest", 10, "Hand picking at marketable size.")]},
    {
        "id": "pumpkin", "name": "Pumpkin / Squash", "zambian_name": "Dzungu / Malangwa",
        "climates": ["tropical", "subtropical", "temperate"],
        "min_ph": 6.0, "max_ph": 7.5, "suitable_soils": ["loamy", "sandy"],
        "min_temp": 18, "max_temp": 32, "min_rainfall": 500, "max_rainfall": 1200,
        "yield_per_hectare": 15.0, "growth_days": 100,
        "description": "Multi-purpose crop for fruit and leaves, grown intercropped in smallholder fields nationwide.",
        "stages": [("Mound Seeding", 8, "Planting 3-4 seeds on mounds."), ("Vine Growth", 30, "Runner spread and large leaf development."), ("Flowering", 20, "Male and female flower production."), ("Fruit Development", 30, "Pumpkin sizing and rind hardening."), ("Harvest & Curing", 12, "Cutting mature fruit and field curing.")]},
    {
        "id": "carrot", "name": "Carrot", "zambian_name": "Kaloti / Karoti",
        "climates": ["temperate", "subtropical", "highland"],
        "min_ph": 5.5, "max_ph": 7.0, "suitable_soils": ["sandy", "loamy"],
        "min_temp": 10, "max_temp": 26, "min_rainfall": 400, "max_rainfall": 800,
        "yield_per_hectare": 25.0, "growth_days": 80,
        "description": "Root vegetable increasingly popular in urban markets. Grown in Lusaka, Copperbelt, and Central.",
        "stages": [("Seedbed Preparation", 10, "Fine tilth, deeply tilled sandy loam."), ("Germination & Seedling", 20, "Slow emergence, fine feathery leaves."), ("Taproot Development", 30, "Root elongation and thickening."), ("Root Maturation", 15, "Color development and sugar accumulation."), ("Harvest & Washing", 5, "Lifting, trimming tops, and washing.")]},
    {
        "id": "lettuce", "name": "Lettuce", "zambian_name": "Saladi / Letisi",
        "climates": ["temperate", "subtropical", "highland"],
        "min_ph": 6.0, "max_ph": 7.0, "suitable_soils": ["loamy", "sandy", "silt"],
        "min_temp": 8, "max_temp": 24, "min_rainfall": 300, "max_rainfall": 700,
        "yield_per_hectare": 15.0, "growth_days": 60,
        "description": "Salad vegetable for urban markets and institutions in Lusaka and Copperbelt.",
        "stages": [("Nursery", 15, "Germination in seedling trays."), ("Transplanting", 5, "Field planting on beds."), ("Head/Leaf Development", 25, "Rapid leaf expansion."), ("Harvest", 15, "Whole plant cutting at base.")]},
    {
        "id": "beetroot", "name": "Beetroot", "zambian_name": "Beetu",
        "climates": ["temperate", "subtropical", "highland"],
        "min_ph": 6.0, "max_ph": 7.5, "suitable_soils": ["sandy", "loamy"],
        "min_temp": 10, "max_temp": 26, "min_rainfall": 400, "max_rainfall": 800,
        "yield_per_hectare": 20.0, "growth_days": 70,
        "description": "Salad vegetable gaining popularity in urban supermarkets.",
        "stages": [("Direct Seeding", 10, "Sowing in loose, deep soil."), ("Seedling & Leaf Growth", 20, "Green-red leaf rosette expansion."), ("Root Swelling", 25, "Hypocotyl enlargement and sugar accumulation."), ("Root Maturation", 10, "Color development."), ("Harvest & Trimming", 5, "Lifting and leaf trimming.")]},
    # ===== OTHER =====
    {
        "id": "ginger", "name": "Ginger", "zambian_name": "Tsogolo / Ginger",
        "climates": ["tropical", "subtropical"],
        "min_ph": 5.5, "max_ph": 6.5, "suitable_soils": ["loamy", "sandy"],
        "min_temp": 20, "max_temp": 30, "min_rainfall": 1000, "max_rainfall": 2000,
        "yield_per_hectare": 8.0, "growth_days": 240,
        "description": "Spice and medicinal crop grown in Luapula, Northern, and parts of Copperbelt.",
        "stages": [("Seed Rhizome Preparation", 10, "Cutting and curing seed pieces."), ("Sprouting & Vegetative", 60, "Shoot emergence and pseudostem growth."), ("Rhizome Development", 120, "Underground rhizome branching and bulking."), ("Maturation", 35, "Leaf yellowing and rhizome skin setting."), ("Harvest & Curing", 15, "Lifting, washing, and sun drying.")]},
    {
        "id": "groundnuts_again", "name": "Bambara Groundnut", "zambian_name": "Mpama",
        "climates": ["tropical", "semi-arid"],
        "min_ph": 5.0, "max_ph": 7.0, "suitable_soils": ["sandy", "loamy"],
        "min_temp": 22, "max_temp": 35, "min_rainfall": 300, "max_rainfall": 700,
        "yield_per_hectare": 2.0, "growth_days": 150,
        "description": "Indigenous drought-tolerant legume. Grown in Western, Southern, Eastern provinces.",
        "stages": [("Seedbed Planting", 10, "Sowing in sandy soil."), ("Seedling & Spreading", 25, "Trifoliate leaf development."), ("Flowering & Pegging", 40, "Peg insertion into soil."), ("Pod Development", 50, "Underground pod filling."), ("Harvest", 25, "Lifting and sun drying.")]},
]


def get_or_create_crop_data(plant_name):
    """Look up a crop by name/ID, or create a default profile."""
    lower = plant_name.strip().lower()
    for c in ZAMBIAN_CROPS:
        if lower in c["name"].lower() or lower == c["id"] or lower in c["zambian_name"].lower():
            return c
    return {
        "id": lower.replace(" ", "_"),
        "name": plant_name.strip().title(),
        "zambian_name": f"{plant_name.strip().title()} (Local Variety)",
        "climates": ["tropical", "subtropical", "temperate", "semi-arid", "highland"],
        "min_ph": 5.5, "max_ph": 7.2,
        "suitable_soils": ["loamy", "sandy", "silt", "clay"],
        "min_temp": 16, "max_temp": 34,
        "min_rainfall": 450, "max_rainfall": 1400,
        "yield_per_hectare": 12.5, "growth_days": 110,
        "description": f"Custom agronomic profile for {plant_name.strip().title()}.",
        "stages": [
            ("Seedbed & Germination", 12, "Seed germination and rootlet establishment."),
            ("Early Vegetative Growth", 28, "Leaf canopy expansion and root system anchoring."),
            ("Flowering Stage", 25, "Bud development, flowering, and reproductive cycle."),
            ("Fruit/Grain/Pod Sizing", 30, "Maturation and nutrient accumulation."),
            ("Harvest & Processing", 15, "Full maturity harvesting and post-harvest handling."),
        ],
    }


def calculate_advisory(inputs, custom_crop_name=None):
    """Score all crops against user-supplied environmental inputs."""
    crops_to_evaluate = list(ZAMBIAN_CROPS)
    if custom_crop_name:
        custom = get_or_create_crop_data(custom_crop_name)
        if not any(c["id"] == custom["id"] for c in crops_to_evaluate):
            crops_to_evaluate.insert(0, custom)

    results = []
    for crop in crops_to_evaluate:
        try:
            climate_score = 100 if inputs.get("climate", "").lower() in crop["climates"] else 35
            ph = inputs.get("soil_ph", 6.5)
            ph_score = 100 if crop["min_ph"] <= ph <= crop["max_ph"] else max(
                0, 100 - min(abs(ph - crop["min_ph"]), abs(ph - crop["max_ph"])) * 30)
            soil_score = 100 if inputs.get("soil_type", "").lower() in crop["suitable_soils"] else 40
            avg_temp = (inputs.get("temp_min", 20) + inputs.get("temp_max", 30)) / 2.0
            temp_score = 100 if crop["min_temp"] <= avg_temp <= crop["max_temp"] else max(
                0, 100 - min(abs(avg_temp - crop["min_temp"]), abs(avg_temp - crop["max_temp"])) * 8)
            rain = inputs.get("rainfall", 800)
            rain_score = 100 if crop["min_rainfall"] <= rain <= crop["max_rainfall"] else max(
                0, 100 - min(abs(rain - crop["min_rainfall"]), abs(rain - crop["max_rainfall"])) / 10.0)
            total = int(climate_score * 0.20 + ph_score * 0.20 + soil_score * 0.15 + temp_score * 0.25 + rain_score * 0.20)
            total = max(0, min(100, total))
        except Exception:
            total, climate_score, ph_score, soil_score, temp_score, rain_score = 0, 0, 0, 0, 0, 0

        results.append({
            "crop": crop,
            "total_score": total,
            "climate_score": climate_score,
            "ph_score": int(ph_score),
            "soil_type_score": soil_score,
            "temp_score": int(temp_score),
            "rainfall_score": int(rain_score),
        })
    return sorted(results, key=lambda r: r["total_score"], reverse=True)
