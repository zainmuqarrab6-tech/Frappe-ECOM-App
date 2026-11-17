# Copyright (c) 2026, Zain and contributors
# For license information, please see license.txt

import itertools
import re
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cstr


class Product(Document):
    def validate(self):
        # 1. Sync is_active with Shopify status
        self.is_active = 1 if (self.status or "Active") == "Active" else 0

        # 2. Calculate Profit and Margin %
        price = float(self.price or 0)
        cost = float(self.cost_price or 0)
        if price > 0 and cost > 0:
            self.profit = round(price - cost, 2)
            self.margin_percent = round((self.profit / price) * 100, 2)
        else:
            self.profit = 0.0
            self.margin_percent = 0.0

        # 3. Auto-generate URL handle / slug if missing
        if not self.route_slug and self.title:
            self.route_slug = self.generate_slug(self.title)

        # 4. Default SEO title if empty
        if not self.seo_meta_title and self.title:
            self.seo_meta_title = self.title

        # 5. Handle Inventory & Stock
        if self.has_variants and self.variants:
            # When product has variants, total stock is the sum of active variants
            total_stock = sum(int(v.stock_quantity or 0) for v in self.variants if getattr(v, "is_active", 1))
            self.stock_quantity = total_stock
            self.is_in_stock = 1 if (total_stock > 0 or self.continue_selling_out_of_stock) else 0

            # Set starting price from minimum variant price if variants have prices
            active_variant_prices = [float(v.price) for v in self.variants if getattr(v, "is_active", 1) and float(v.price or 0) > 0]
            if active_variant_prices:
                min_price = min(active_variant_prices)
                if not self.price or self.price > min_price:
                    self.price = min_price
        else:
            self.is_in_stock = 1 if ((self.stock_quantity or 0) > 0 or self.continue_selling_out_of_stock) else 0

    def generate_slug(self, text):
        clean = re.sub(r"[^\w\s-]", "", cstr(text).lower()).strip()
        slug = re.sub(r"[-\s]+", "-", clean)
        # Ensure uniqueness
        base_slug = slug
        counter = 1
        filters = {"route_slug": slug}
        if not self.is_new():
            filters["name"] = ["!=", self.name]

        while frappe.db.exists("Product", filters):
            slug = f"{base_slug}-{counter}"
            filters["route_slug"] = slug
            counter += 1
        return slug

    @frappe.whitelist()
    def generate_variants_matrix(self):
        """
        Takes the options defined in the 'options' table and generates all combinations
        into the 'variants' table, preserving any existing variant prices and stocks.
        """
        if not self.options:
            frappe.throw(_("Please add at least one Option (e.g. Size or Color) with values before generating variants."))

        # Parse options
        option_lists = []
        for opt in self.options:
            opt_name = (opt.option_name or "").strip()
            raw_vals = (opt.option_values or "").strip()
            if not opt_name or not raw_vals:
                continue

            # Split comma-separated values
            vals = [v.strip() for v in raw_vals.split(",") if v.strip()]
            if vals:
                option_lists.append([(opt_name, v) for v in vals])

        if not option_lists:
            frappe.throw(_("Please provide valid option values (separated by commas)."))

        # Generate Cartesian product combinations
        all_combinations = list(itertools.product(*option_lists))

        # Index existing variants by combination title to preserve manual edits
        existing_variants = {}
        for v in (self.variants or []):
            existing_variants[v.title] = v

        # Rebuild variants table
        self.set("variants", [])
        for combo in all_combinations:
            combo_title = " / ".join(val for name, val in combo)
            sku_suffix = "-".join(re.sub(r"[^\w]", "", val).upper() for name, val in combo)
            default_sku = f"{self.sku or 'SKU'}-{sku_suffix}" if self.sku else f"PROD-{sku_suffix}"

            if combo_title in existing_variants:
                old_v = existing_variants[combo_title]
                self.append("variants", {
                    "doctype": "Product Variant",
                    "title": old_v.title,
                    "sku": old_v.sku or default_sku,
                    "price": old_v.price or self.price,
                    "compare_at_price": old_v.compare_at_price or self.compare_at_price,
                    "cost_price": old_v.cost_price or self.cost_price,
                    "stock_quantity": old_v.stock_quantity or 0,
                    "image": old_v.image,
                    "barcode": old_v.barcode,
                    "weight": old_v.weight,
                    "is_active": old_v.is_active
                })
            else:
                v_data = {
                    "doctype": "Product Variant",
                    "title": combo_title,
                    "sku": default_sku,
                    "price": self.price or 0.0,
                    "compare_at_price": self.compare_at_price or 0.0,
                    "cost_price": self.cost_price or 0.0,
                    "stock_quantity": 0,
                    "is_active": 1
                }
                for idx, (name, val) in enumerate(combo[:3], start=1):
                    v_data[f"option{idx}_name"] = name
                    v_data[f"option{idx}_value"] = val
                self.append("variants", v_data)

        self.has_variants = 1
        self.save()
        return {"status": "success", "count": len(self.variants)}
