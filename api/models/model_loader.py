# from . import orders, order_details, recipes, sandwiches, resources

# from ..dependencies.database import engine


# def index():
#     orders.Base.metadata.create_all(engine)
#     order_details.Base.metadata.create_all(engine)
#     recipes.Base.metadata.create_all(engine)
#     sandwiches.Base.metadata.create_all(engine)
#     resources.Base.metadata.create_all(engine)
from . import (
    orders,
    order_details,
    recipes,
    sandwiches,
    resources,
    customers,
    payments,
    reviews,
    promotions,
    order_promotions
)

from ..dependencies.database import engine
from ..dependencies.schema_migrate import apply_checklist_migrations


def index():
    orders.Base.metadata.create_all(bind=engine)
    apply_checklist_migrations(engine)