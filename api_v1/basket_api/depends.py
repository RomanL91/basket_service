from typing import Annotated
from fastapi import Depends

from core.base_UOW import IUnitOfWork, UnitOfWork
from core.base_model import TokenSchema


UOF_Depends = Annotated[IUnitOfWork, Depends(UnitOfWork)]
Token_Depends = Annotated[TokenSchema, Depends(TokenSchema)]
