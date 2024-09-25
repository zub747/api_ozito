from typing import Annotated, Optional
from pydantic import BaseModel
from database import Role, ProductStatus
from datetime import date

class SProductAdd(BaseModel):
    product_name : str
    product_description : str
    price : int
    creator_id : int
    status: ProductStatus
    buyer_id : Optional[int] = None


class SProduct(SProductAdd):
    product_id : int
    created_at : date
          
class SUserAdd(BaseModel):
    email : str
    login : str 
    password : str 
    phone_number : Optional[int] = None
    mail_index : Optional[int] = None
    rating : Optional[float] = None
    region : str
    is_active : bool     
    role : Role

class SUser(SUserAdd):
    id : int 
    
class SProductRel(SProduct):
    creator : "SUser"
    buyer : "SUser"

class SUserRel(SUser):
    products_added : list["SProduct"]
    products_bought : list["SProduct"]