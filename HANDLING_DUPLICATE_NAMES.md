# Handling Guests With the Same First or Last Name

## Examples in `guests.csv`

- **Same first name:** "Emma" → **Emma Johnson** (Table 1) and **Emma Lee** (Table 2).
- **Same last name:** "Johnson" → **Emma Johnson** (Table 1) and **Michael Johnson** (Table 3).
- **Same first name:** "James" → **James Wilson** (Table 1) and **James Taylor** (Table 2).

Searching by only first or last name can therefore return multiple guests.

---

## What the App Does

1. **Multiple matches:** When the search matches more than one guest, the app shows a warning and a **radio list** of all matches (with table numbers).
2. **User picks one:** The user selects the correct person; the app then shows that guest’s table and tablemates only.

---

## Suggested Action Steps (for you or your process)

| Step | Action |
|------|--------|
| **1. Encourage full name** | In your instructions or signage, ask guests to search by **first and last name** when possible (e.g. "Emma Johnson") so they get a single result. |
| **2. Add a second search mode (optional)** | In the app, add a "Full name" search that matches "First Last" and only returns one row when it’s unambiguous — and keep the current "First or last" search for quick lookups. |
| **3. Use table numbers on place cards** | Print table numbers on place cards or escort cards so guests can find their table even if they don’t use the app. |
| **4. Add a unique ID in the CSV (optional)** | If you need to support nicknames or many duplicates, add a column like `guest_id` or `display_name` and allow search by that as well. |
| **5. Review the guest list** | Before the event, search common first names (e.g. "Emma", "James") and last names (e.g. "Johnson") to confirm the app’s multiple-match flow is clear for your guests. |

---

## Quick Test in the App

- Search **"Emma"** → you should see 2 guests and a radio to choose Emma Johnson or Emma Lee.
- Search **"Johnson"** → you should see 2 guests and a radio to choose Emma Johnson or Michael Johnson.
- Search **"Emma Johnson"** → you can extend the app to treat this as full-name search and show a single result (see Step 2 above).
