# BookingProject

The BookingProject model represents a project for bookings within Easyverein.

## Fields

| Field Name | Type | Description |
| --- | --- | --- |
| `id` | `PositiveInt` | The unique identifier of the booking project |
| `org` | `EasyVereinReference` | Reference to the organization the booking project belongs to |
| `name` | `str` | The name of the booking project |
| `color` | `str` | The color code (hex) of the booking project |
| `short` | `str` | Short identifier for the booking project |
| `budget` | `str` | Budget allocated to the booking project |
| `completed` | `bool` | Whether the booking project is completed |
| `projectCostCentre` | `str` | Cost center code for the booking project |

## Models

### BookingProject

```python
class BookingProject(BookingProjectBase, EmptyStringsToNone):
    """
    Pydantic model representing a BookingProject
    """
    pass
```

### BookingProjectCreate

```python
class BookingProjectCreate(
    BookingProjectBase,
    required_mixin(["name"]),
):
    """
    Pydantic model for creating a BookingProject
    """
    pass
```

### BookingProjectUpdate

```python
class BookingProjectUpdate(BookingProjectBase):
    """
    Pydantic model used to patch a BookingProject
    """
    pass
```

### BookingProjectFilter

```python
class BookingProjectFilter(BaseModel):
    """
    Pydantic model used to filter booking projects
    """
    id__in: FilterIntList | None = None
    budget__lt: float | None = None
    budget__gt: float | None = None
    name: str | None = None
    short: str | None = None
    completed: bool | None = None
```

## Example

```python
from easyverein.api import EasyvereinAPI
from easyverein.models import BookingProject, BookingProjectCreate

# Initialize the API
api = EasyvereinAPI("your-api-key")

# Create a new booking project
new_project = BookingProjectCreate(
    name="Project Name",
    color="#23985d",
    short="5001",
    budget="0.00",
    completed=False,
    projectCostCentre="90001"
)
created_project = api.booking_project.create(new_project)
print(created_project)
