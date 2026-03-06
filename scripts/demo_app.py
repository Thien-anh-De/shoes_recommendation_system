import pandas as pd


# ==============================
# LOAD DATA
# ==============================

def load_data():

    products = pd.read_parquet(
        "data/processed/products_clean.parquet"
    )

    rec = pd.read_parquet(
        "data/feature_store/recommendations.parquet"
    )

    sim = pd.read_parquet(
        "data/feature_store/item_similarity.parquet"
    )

    # fallback popularity nếu chưa có
    if "popularity" not in products.columns:
        products["popularity"] = products.index[::-1]

    return products, rec, sim


# ==============================
# FORMAT PRICE
# ==============================

def format_price(v):

    try:
        return f"{int(v):,} VND"
    except:
        return "N/A"


# ==============================
# PRINT PRODUCT TABLE
# ==============================

def print_products(df):

    print("\n------------------------------------------------------------------------------------------------")
    print(f"{'ID':<6}{'NAME':<45}{'BRAND':<15}{'CATEGORY':<12}{'PRICE':>15}")
    print("------------------------------------------------------------------------------------------------")

    for _, r in df.iterrows():

        name = str(r.get("product_name", "unknown"))[:43]
        brand = str(r.get("brand", "-"))[:13]
        category = str(r.get("category", "-"))[:10]
        price = format_price(r.get("price_vnd", 0))

        print(
            f"{int(r['product_id']):<6}"
            f"{name:<45}"
            f"{brand:<15}"
            f"{category:<12}"
            f"{price:>15}"
        )

    print("------------------------------------------------------------------------------------------------")


# ==============================
# PRODUCT DETAIL
# ==============================

def show_product_detail(products, pid):

    p = products[products["product_id"] == pid]

    if p.empty:

        print("\n❌ Product not found")
        return False

    p = p.iloc[0]

    print("\n===================================================")
    print("📦 PRODUCT DETAIL")
    print("===================================================")

    print("ID       :", p["product_id"])
    print("Name     :", p.get("product_name", "-"))
    print("Brand    :", p.get("brand", "-"))
    print("Category :", p.get("category", "-"))
    print("Material :", p.get("material", "-"))
    print("Purpose  :", p.get("purpose", "-"))
    print("Price    :", format_price(p.get("price_vnd", 0)))

    return True


# ==============================
# RELATED PRODUCTS
# ==============================

def show_related(similarity, products, pid):

    print("\n🔗 RELATED PRODUCTS")

    sim = similarity[
        similarity["product_id"] == pid
    ].sort_values("rank").head(5)

    rows = []

    for _, r in sim.iterrows():

        spid = r["similar_product_id"]

        prod = products[
            products["product_id"] == spid
        ]

        if not prod.empty:
            rows.append(prod.iloc[0])

    if rows:

        df = pd.DataFrame(rows)
        print_products(df)

    else:

        print("No related products")


# ==============================
# USER RECOMMENDATIONS
# ==============================

def show_user_rec(rec, products, user_id):

    print("\n⭐ RECOMMENDED FOR YOU")

    r = rec[
        rec["user_id"] == user_id
    ].sort_values(
        "final_score",
        ascending=False
    ).head(10)

    rows = []

    for _, row in r.iterrows():

        pid = row["product_id"]

        prod = products[
            products["product_id"] == pid
        ]

        if not prod.empty:
            rows.append(prod.iloc[0])

    if rows:

        df = pd.DataFrame(rows)
        print_products(df)

    else:

        print("No recommendation")


# ==============================
# HOMEPAGE PAGINATION
# ==============================

def browse_homepage(products):

    page_size = 20
    page = 0

    sorted_products = products.sort_values(
        "popularity",
        ascending=False
    ).reset_index(drop=True)

    while True:

        start = page * page_size
        end = start + page_size

        page_df = sorted_products.iloc[start:end]

        print(f"\n🏠 HOMEPAGE — Page {page+1}")

        print_products(page_df)

        print("\nOptions:")
        print("n → next page")
        print("p → previous page")
        print("v → view product")
        print("q → menu")

        choice = input("\nSelect option: ").strip()

        if choice == "n":

            if end < len(sorted_products):
                page += 1
            else:
                print("No more pages")

        elif choice == "p":

            if page > 0:
                page -= 1

        elif choice == "v":

            try:
                pid = int(input("Enter product id: "))
                return pid
            except:
                print("Invalid product id")

        elif choice == "q":

            return None


# ==============================
# PRODUCT LOOP
# ==============================

def product_loop(products, rec, sim, user_id, pid):

    while True:

        ok = show_product_detail(products, pid)

        if not ok:
            return

        show_related(sim, products, pid)

        show_user_rec(rec, products, user_id)

        print("\nOptions:")
        print("1 → View another product")
        print("2 → Back to homepage")
        print("3 → Exit")

        choice = input("Select option: ")

        if choice == "1":

            try:
                pid = int(input("Enter product id: "))
                continue
            except:
                print("Invalid id")

        elif choice == "2":

            return

        elif choice == "3":

            print("\nExit demo")
            exit()


# ==============================
# MAIN
# ==============================

def main():

    products, rec, sim = load_data()

    print("\n🔐 LOGIN")

    try:
        user_id = int(input("Enter user id: "))
    except:
        print("Invalid user id")
        return

    while True:

        pid = browse_homepage(products)

        if pid is None:

            print("\nMenu:")
            print("1 → Recommended for you")
            print("2 → Back to homepage")
            print("3 → Exit")

            choice = input("Select option: ")

            if choice == "1":

                show_user_rec(rec, products, user_id)

            elif choice == "2":

                continue

            elif choice == "3":

                print("\nExit demo")
                break

        else:

            product_loop(products, rec, sim, user_id, pid)


if __name__ == "__main__":
    main()