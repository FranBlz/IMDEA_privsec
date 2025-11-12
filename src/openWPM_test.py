from openwpm.task_manager import TaskManager # type: ignore
from openwpm.config import BrowserParams, ManagerParams # type: ignore

# Define the sites to visit
sites = [
    "https://elpais.com",
    "https://instagram.com",
    "https://lanacion.com"
]

# Setup parameters
manager_params = ManagerParams(num_browsers=1)
browser_params = BrowserParams(display_mode="native")

# Initialize manager
manager = TaskManager(manager_params, [browser_params])

# Visit sites
for site in sites:
    manager.get(site, sleep=5)

# Close
manager.close()
