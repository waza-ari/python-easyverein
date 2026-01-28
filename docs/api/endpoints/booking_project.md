# BookingProject

The BookingProject API provides access to booking projects within Easyverein.

## Examples

### Get all booking projects

```python
from easyverein.api import EasyvereinAPI

# Initialize the API
api = EasyvereinAPI("your-api-key")

# Get all booking projects
booking_projects = api.booking_project.get_all()
print(booking_projects)
```

### Get a specific booking project

```python
from easyverein.api import EasyvereinAPI

# Initialize the API
api = EasyvereinAPI("your-api-key")

# Get a booking project by ID
booking_project = api.booking_project.get(123456)
print(booking_project)
```

### Create a booking project

```python
from easyverein.api import EasyvereinAPI

# Initialize the API
api = EasyvereinAPI("your-api-key")

# Create a new booking project
booking_project = api.booking_project.create({
    "name": "New Project",
    "color": "#23985d",
    "short": "5001",
    "budget": "0.00",
    "completed": False,
    "projectCostCentre": "90001"
})
print(booking_project)
```

### Update a booking project

```python
from easyverein.api import EasyvereinAPI

# Initialize the API
api = EasyvereinAPI("your-api-key")

# Update a booking project
booking_project = api.booking_project.update(123456, {
    "name": "Updated Project Name",
    "completed": True
})
print(booking_project)
```

### Delete a booking project

```python
from easyverein.api import EasyvereinAPI

# Initialize the API
api = EasyvereinAPI("your-api-key")

# Delete a booking project
api.booking_project.delete(123456)
```

### Filter booking projects

```python
from easyverein.api import EasyvereinAPI

# Initialize the API
api = EasyvereinAPI("your-api-key")

# Filter booking projects
filtered_projects = api.booking_project.filter({
    "name": "Project Name",
    "completed": False,
    "budget__lt": 1000.00
})
print(filtered_projects)
```
