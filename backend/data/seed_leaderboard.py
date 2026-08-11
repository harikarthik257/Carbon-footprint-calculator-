"""Synthetic leaderboard data. Per PRD.md §5, a live leaderboard is cut for
Round 1 — this is deliberately labeled is_synthetic so the UI never presents
it as real usage data."""

SEED_LEADERBOARD = {
    "is_synthetic": True,
    "entries": [
        {"group_name": "Brahmaputra Hostel", "avg_kg_co2e_saved_per_day": 4.2},
        {"group_name": "Kapili Hostel", "avg_kg_co2e_saved_per_day": 3.8},
        {"group_name": "Dihing Hostel", "avg_kg_co2e_saved_per_day": 3.1},
        {"group_name": "Manas Hostel", "avg_kg_co2e_saved_per_day": 2.6},
        {"group_name": "Umiam Hostel", "avg_kg_co2e_saved_per_day": 1.9},
    ],
}
