from fastapi import Depends
from typing import Annotated
from fastapi_pagination import Params

from core.base_UOW import IUnitOfWork, UnitOfWork


UOF_Depends = Annotated[IUnitOfWork, Depends(UnitOfWork)]
Params_Depends = Annotated[Params, Depends(Params)]
