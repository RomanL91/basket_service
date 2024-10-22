from typing import Annotated
from fastapi import Depends, Header

from core.base_UOW import IUnitOfWork, UnitOfWork


UOF_Depends = Annotated[IUnitOfWork, Depends(UnitOfWork)]
Token_Depends = Annotated[str, Header()]
