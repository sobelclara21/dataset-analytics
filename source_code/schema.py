from dataclasses import dataclass

@dataclass
class DatasetSpec:
    name: str
    date_col: str | None
    region_col: str | None
    product_col: str | None
    amount_col: str | None
    rating_col: str | None


def detect_dataset(cols: set[str]) -> DatasetSpec:

    # Dataset 11 — Consumer Behavior / Shopping
    if "location" in cols and "item_purchased" in cols:
        return DatasetSpec(
            name="shopping",
            date_col="purchase_date",
            region_col="location",
            product_col="item_purchased",
            amount_col="purchase_amount_usd",
            rating_col="review_rating" if "review_rating" in cols else None,
        )

    # Dataset 12 — Airbnb
    if "price" in cols and "room_type" in cols:
        return DatasetSpec(
            name="airbnb",
            date_col="last_review" if "last_review" in cols else None,
            region_col="neighbourhood_group" if "neighbourhood_group" in cols else "neighbourhood",
            product_col="room_type",
            amount_col="price",
            rating_col="review_rate_number" if "review_rate_number" in cols else None,
        )

    return DatasetSpec("unknown", None, None, None, None, None)
