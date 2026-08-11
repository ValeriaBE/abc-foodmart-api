from fastapi import APIRouter, Query

from app.queries.dashboard_queries import (
    get_category_sales,
    get_database_connection_info,
    get_database_status,
    get_kpis,
    get_low_stock,
    get_monthly_sales,
    get_revenue_by_store,
    get_stores,
    get_top_products,
    get_vendor_performance,
)

router = APIRouter(
    prefix="/api",
    tags=["Dashboard"],
)


@router.get("/health")
def health():
    return {
        "status": "online",
        "service": "ABC Foodmart API",
    }


@router.get("/connection")
def database_connection():
    return get_database_connection_info()


@router.get("/kpis")
def kpis(store_id: int | None = None):
    return get_kpis(store_id)


@router.get("/revenue-by-store")
def revenue_by_store(store_id: int | None = None):
    return get_revenue_by_store(store_id)


@router.get("/monthly-sales")
def monthly_sales(store_id: int | None = None):
    return get_monthly_sales(store_id)


@router.get("/category-sales")
def category_sales(store_id: int | None = None):
    return get_category_sales(store_id)


@router.get("/top-products")
def top_products(
    store_id: int | None = None,
    limit: int = 10,
):
    return get_top_products(store_id, limit)


@router.get("/low-stock")
def low_stock(store_id: int | None = None):
    return get_low_stock(store_id)


@router.get("/vendor-performance")
def vendor_performance(store_id: int | None = None):
    return get_vendor_performance(store_id)

@router.get("/stores")
def stores():
    return get_stores()

@router.get("/database-status")
def database_status():
    return get_database_status()