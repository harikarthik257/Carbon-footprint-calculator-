// ~100 everyday Indian dishes for the manual meal-entry autocomplete list.
// Mirrors the primary display name for each factor key in
// backend/data/emission_factors.py + engine/calculator.py's
// FOOD_ITEM_TO_FACTOR_KEY — kept in sync manually since the frontend has no
// build-time access to the backend's Python data.
export const INDIAN_DISHES: string[] = [
  // Rice / grain
  "Rice", "Jeera rice", "Lemon rice", "Curd rice", "Pulao", "Veg biryani",
  "Chicken biryani", "Mutton biryani", "Khichdi", "Poha", "Upma",
  // Breads
  "Roti", "Naan", "Paratha", "Aloo paratha", "Poori", "Bhatura",
  // Dals / legumes
  "Dal", "Dal tadka", "Dal makhani", "Chana masala", "Rajma", "Sambar",
  "Moong dal", "Chole",
  // Vegetable curries
  "Mixed vegetables", "Aloo gobi", "Aloo matar", "Baingan bharta",
  "Bhindi masala", "Mixed vegetable curry", "Cabbage sabzi", "Capsicum sabzi",
  "Gobi manchurian", "Veg kofta", "Jeera aloo", "Karela sabzi",
  // Paneer
  "Paneer", "Paneer butter masala", "Palak paneer", "Shahi paneer",
  "Paneer tikka",
  // Non-veg
  "Chicken curry", "Chicken 65", "Tandoori chicken", "Butter chicken",
  "Chicken tikka", "Egg", "Egg curry", "Egg bhurji", "Mutton curry",
  "Mutton keema", "Fish curry", "Fish fry", "Prawn curry", "Chicken soup",
  // South Indian
  "Idli", "Dosa", "Masala dosa", "Uttapam", "Vada", "Rasam", "Medu vada",
  "Appam",
  // Snacks / street food
  "Samosa", "Pakora", "Vada pav", "Dhokla", "Bhel puri", "Pani puri",
  "Kachori", "Aloo tikki", "Sev puri", "Cutlet",
  // Dairy / sides
  "Curd", "Raita", "Lassi", "Buttermilk", "Papad", "Pickle", "Ghee", "Butter",
  // Sweets
  "Gulab jamun", "Jalebi", "Rasgulla", "Kheer", "Halwa", "Laddoo", "Barfi",
  "Kaju katli", "Rabri", "Shrikhand",
  // Soups / beverages
  "Veg soup", "Tomato soup", "Tea", "Coffee",
  // Combos / thali
  "Veg thali", "Non veg thali", "Mini meal",
];
