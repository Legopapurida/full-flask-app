from service import CreateProductionApplication
from configs import ProductionConfigs


production = CreateProductionApplication(ProductionConfigs())
app = production.create_app()
