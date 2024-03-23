from .enrollee import (
    EnrolleeBase,
    EnrolleeCreate,
    Enrollee,
    EnrolleeDetailed,
    EnrolleeForm,
    EnrolleeTemplate,
    EnrolleeUpdate,
    EnrolleeLogin
)
from .application import (
    Application,
    ApplicationBase,
    ApplicationCreate,
    ApplicationDetailed,
    ApplicationForm,
    ApplicationTemplate,
    ApplicationUpdate,
)
from .employee import (
    EmployeeBase,
    EmployeeUpdate,
    Employee,
    EmployeeCreate,
    EmployeeDetailed,
    EmployeeTemplate,
    EmployeeForm,
    EmployeeLogin
)
from .speciality import (
    SpecialityBase,
    Speciality,
    SpecialityCreate,
    SpecialityForm,
    SpecialityUpdate,
    SpecialityTemplate,
)
from .websocket import MessageWS, EventWS
