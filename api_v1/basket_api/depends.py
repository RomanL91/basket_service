from typing import Annotated
from fastapi import Depends

from core.base_UOW import IUnitOfWork, UnitOfWork


UOF_Depends = Annotated[IUnitOfWork, Depends(UnitOfWork)]
