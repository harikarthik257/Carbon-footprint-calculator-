import { useRef, useState } from "react";
import { logMealPhoto, calculateMeal } from "../api/meal";
import type { MealItem } from "../types";

function fileToBase64(file: File): Promise<{ data: string; mediaType: string }> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result as string;
      const [, data] = result.split(",");
      resolve({ data, mediaType: file.type || "image/jpeg" });
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

export default function MealPhotoUpload({
  onLogged,
}: {
  onLogged: (kgCo2e: number) => void;
}) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [items, setItems] = useState<MealItem[] | null>(null);
  const [isMock, setIsMock] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [logged, setLogged] = useState(false);

  async function handleFile(file: File) {
    setLoading(true);
    setError(null);
    setLogged(false);
    setPreviewUrl(URL.createObjectURL(file));
    try {
      const { data, mediaType } = await fileToBase64(file);
      const result = await logMealPhoto(data, mediaType);
      setItems(result.items);
      setIsMock(result.is_mock);
    } catch (e) {
      setError("Couldn't read that photo — try again, or add items manually below.");
    } finally {
      setLoading(false);
    }
  }

  function updateItem(index: number, field: "name" | "quantity", value: string) {
    setItems((prev) => {
      if (!prev) return prev;
      const next = [...prev];
      next[index] = {
        ...next[index],
        [field]: field === "quantity" ? Number(value) : value,
      };
      return next;
    });
  }

  function removeItem(index: number) {
    setItems((prev) => (prev ? prev.filter((_, i) => i !== index) : prev));
  }

  function addManualItem() {
    setLogged(false);
    setItems((prev) => [...(prev ?? []), { name: "", quantity: 1 }]);
  }

  async function confirmAndLog() {
    if (!items || items.length === 0) return;
    const result = await calculateMeal(items);
    setLogged(true);
    onLogged(result.total_kg_co2e);
  }

  const itemsEditor = items && (
    <div className={previewUrl ? "flex-1" : ""}>
      {isMock && (
        <p className="text-xs font-data text-ochre mb-2">
          ⚠ mock response — connect ANTHROPIC_API_KEY for real extraction
        </p>
      )}
      <ul className="space-y-2">
        {items.map((item, i) => (
          <li key={i} className="flex items-center gap-2">
            <input
              className="flex-1 rounded-md border border-moss/20 px-2 py-1 text-sm"
              placeholder="Food item name"
              value={item.name}
              onChange={(e) => updateItem(i, "name", e.target.value)}
            />
            <input
              type="number"
              min={0}
              step={0.5}
              className="w-16 rounded-md border border-moss/20 px-2 py-1 text-sm font-data"
              value={item.quantity}
              onChange={(e) => updateItem(i, "quantity", e.target.value)}
            />
            <button
              className="text-xs text-alert"
              onClick={() => removeItem(i)}
              aria-label={`Remove ${item.name || "item"}`}
            >
              Remove
            </button>
          </li>
        ))}
      </ul>
      {items.length === 0 && (
        <p className="text-sm text-ink/50">Nothing confident enough to guess — add items manually.</p>
      )}
      <div className="flex items-center gap-3 mt-3">
        <button
          className="px-4 py-2 rounded-lg text-sm font-medium bg-moss text-paper hover:bg-moss-light disabled:opacity-40"
          onClick={confirmAndLog}
          disabled={items.length === 0 || items.some((it) => !it.name.trim())}
        >
          {logged ? "Logged ✓" : "Confirm and log"}
        </button>
        <button className="text-sm text-river underline" onClick={addManualItem}>
          + Add item
        </button>
      </div>
    </div>
  );

  return (
    <div className="bg-white/60 rounded-2xl p-6 border border-moss/10">
      <h3 className="font-display text-lg font-semibold mb-1">Log a meal</h3>
      <p className="text-sm text-ink/60 mb-4">
        Snap your tray and we'll guess what's on it, or type items in yourself —
        either way you confirm before anything's logged.
      </p>

      {!previewUrl && !items && (
        <div className="flex items-center gap-4">
          <button
            className="flex-1 py-8 rounded-xl border-2 border-dashed border-moss/30 text-moss font-medium hover:bg-moss/5"
            onClick={() => inputRef.current?.click()}
          >
            Choose a photo
          </button>
          <span className="text-xs font-data text-ink/40">or</span>
          <button
            className="flex-1 py-8 rounded-xl border-2 border-dashed border-river/30 text-river font-medium hover:bg-river/5"
            onClick={addManualItem}
          >
            Add a food item manually
          </button>
        </div>
      )}
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        capture="environment"
        className="hidden"
        onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
      />

      {previewUrl && (
        <div className="flex gap-4 items-start">
          <img
            src={previewUrl}
            alt="Meal tray"
            className="w-24 h-24 object-cover rounded-lg border border-moss/10 flex-shrink-0"
          />
          <div className="flex-1">
            {loading && <p className="text-sm text-ink/60">Reading the tray…</p>}
            {error && <p className="text-sm text-alert">{error}</p>}
            {itemsEditor}
          </div>
        </div>
      )}

      {!previewUrl && items && itemsEditor}
    </div>
  );
}
