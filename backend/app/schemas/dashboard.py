from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_assets: int
    assigned_assets: int
    available_assets: int
    disposed_assets: int
    pending_disposals: int