import base64
import streamlit as st
import pandas as pd
from pathlib import Path

# Page config
st.set_page_config(page_title="Your Table Awaits", page_icon="💒", layout="centered")

# Background image (PNG in repo)
_BG_IMAGE_PATH = Path(__file__).parent / "WEDDING DETAILS SAME SIZE INVI (5 x 7.5 in).png"


def _get_bg_base64():
    if _BG_IMAGE_PATH.exists():
        with open(_BG_IMAGE_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


# Center the whole layout and set background
_bg_b64 = _get_bg_base64()
_bg_css = ""
if _bg_b64:
    _bg_css = """
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .main .block-container {
        background: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 1rem;
    }
    """ % _bg_b64

st.markdown(
    f"""
    <style>
    .main .block-container {{ max-width: 42rem; margin-left: auto; margin-right: auto; text-align: center; }}
    .main .block-container > * {{ text-align: center; }}
    .stTextInput > div > div > input {{ text-align: center; }}
    {_bg_css}
    </style>
    """,
    unsafe_allow_html=True,
)


# Load guest data from the seating chart CSV (new columns)
@st.cache_data
def load_guests():
    csv_path = Path(__file__).parent / "wedding_seating_chart.csv"
    return pd.read_csv(csv_path)

def main():
    st.title("💒 Your Table Awaits")
    st.markdown(
        '<p style="font-size: 1.25rem; margin: 0.25rem 0;">Celebrating <strong>Jed</strong> & <strong>Clarisa</strong></p>',
        unsafe_allow_html=True,
    )
    st.markdown("Search by **first name**, **last name**, or **any part of your name** (e.g. either of two first names) to find your table and tablemates.")

    df = load_guests()

    # Normalize column names (strip whitespace)
    df.columns = df.columns.str.strip()

    search = st.text_input(
        "Search by any part of your name",
        placeholder="e.g. Jeremiah or Soliman",
        key="search",
    ).strip()

    if search:
        search_lower = search.lower()
        # Substring match: first_name and last_name (covers guests with two first names, e.g. "Clarisa Bianca" or "Jeremiah Dominic")
        mask_first = df["first_name"].astype(str).str.lower().str.contains(search_lower, na=False)
        mask_last = df["last_name"].astype(str).str.lower().str.contains(search_lower, na=False)
        matches = df[mask_first | mask_last].drop_duplicates()

        if matches.empty:
            st.info("No guest found with that name. Try a different spelling.")
            return

        # Multiple guests matched (same first name or same last name)
        if len(matches) > 1:
            st.warning(
                f"**{len(matches)} guests** match \"{search}\". Tap the person you mean:"
            )
            # One button per guest — easy to tap on phone
            selected_idx = None
            for i, (_, row) in enumerate(matches.iterrows()):
                label = f"{row['first_name']} {row['last_name']} — {row['table_number']}"
                if st.button(label, key=f"guest_btn_{search}_{i}", use_container_width=True):
                    selected_idx = i
            # Persist choice in session so we show only that guest after tap
            if "multi_guest_idx" not in st.session_state:
                st.session_state.multi_guest_idx = {}
            if selected_idx is not None:
                st.session_state.multi_guest_idx[search] = selected_idx
            idx = st.session_state.multi_guest_idx.get(search)
            if idx is not None and 0 <= idx < len(matches):
                if st.button("← Choose a different person", key=f"guest_back_{search}", use_container_width=True):
                    del st.session_state.multi_guest_idx[search]
                    st.rerun()
                matches = matches.iloc[[idx]]
            else:
                return  # wait for user to tap a button

        for _, guest in matches.iterrows():
            first = guest["first_name"]
            last = guest["last_name"]
            table_label = guest["table_number"]

            with st.container():
                st.markdown(
                    f'<p style="text-align: center; font-size: 1.5rem; font-weight: 600; margin: 0.5rem 0;">{first} {last}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p style="text-align: center; font-size: 4rem; font-weight: 700; margin: 0.5rem 0;">{table_label}</p>',
                    unsafe_allow_html=True,
                )

                # Tablemates: same table, excluding this guest
                tablemates = df[
                    (df["table_number"] == table_label)
                    & ~((df["first_name"] == first) & (df["last_name"] == last))
                ]

                if tablemates.empty:
                    st.markdown(
                        '<p style="text-align: center; color: #666;">No other guests at this table in the list.</p>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown('<p style="text-align: center; font-weight: 600;">Tablemates</p>', unsafe_allow_html=True)
                    names = [f"{tm['first_name']} {tm['last_name']}" for _, tm in tablemates.iterrows()]
                    st.markdown(
                        f'<p style="text-align: center; line-height: 1.8;">{"<br>".join(names)}</p>',
                        unsafe_allow_html=True,
                    )
                st.divider()

    else:
        st.caption("Enter a name above to look up a guest.")

if __name__ == "__main__":
    main()
