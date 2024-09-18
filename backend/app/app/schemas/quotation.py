from typing import List
from pydantic import BaseModel
from fastapi import File,UploadFile
from typing import Optional
from datetime import datetime




class ListTerms(BaseModel):
    terms_id:int

# class AccessoriesList(BaseModel):
#     quantity:int=0
#     act_sq:float=0
#     ch_sqft:Optional[float] = None
#     width:float=0
#     height:float=0
#     rate_sqft:float=0
#     accessories_id:Optional[int]=None
#     discount:Optional[int]=0
#     discounted_amount:float=0
#     accessories_tax_amount:float=0
#     total_amount:float=0
#     sub_total:float=0


# class OrderItems(BaseModel):
#     price_list_id:Optional[int]=None
#     quantity:int
#     location:str
#     drawing:int
#     width:str
#     height:str
#     h_add:Optional[str] =None
#     discount:Optional[int]=0
#     tax:Optional[int]=0
#     item_tax_amount:Optional[float]=0
#     extra_amount:Optional[float]=0
#     sub_total:float
#     discounted_amount:Optional[float]=0
#     ch_sqft:float
#     w_add:Optional[str] =None
#     act_sq:float
#     rate_sqft:float
#     total_amount:float=0
#     door_open:int
#     frame_color_id:int
#     frame_type_id:int
#     item_id:int
#     made_id:int
#     mesh_type_id:int
#     accessoriesList: Optional[List[AccessoriesList]] = None

# class UpdateOrder(BaseModel):
#     token:str
#     quotation_id:Optional[int]=None
#     order_item_id:Optional[int]=None
#     price_list_id:Optional[int]=None


#     quantity:int
#     tax:Optional[int]=0
#     item_tax_amount:Optional[float]=0
#     location:str
#     drawing:int
#     width:str
#     height:str
#     h_add:Optional[str] =None
#     discount:int=0
#     sub_total:float
#     discounted_amount:Optional[float]=0
#     extra_amount:Optional[float]=0
#     # advance_payment:Optional[float]=0
#     ch_sqft:float
#     w_add:Optional[str] =None
#     act_sq:float
#     rate_sqft:float
#     total_amount:float=0
#     door_open:int
#     frame_color_id:int
#     frame_type_id:int
#     item_id:int
#     made_id:int
#     mesh_type_id:int
#     accessoriesList: Optional[List[AccessoriesList]] = None


# class UpdateQuotation(BaseModel):
#     token:str
#     utr_no:Optional[str] =None
#     surname:Optional[str] =None
#     billing_address:Optional[str] =None
#     customer_id:Optional[int]=None
#     quotation_id : int
#     dealer_id:Optional[int] =None
#     correction_type:Optional[int] =None
#     correction_amount:Optional[float] = None


#     customer_name:Optional[str] =None
#     address:Optional[str] =None
#     phone:Optional[str] =None
#     alternative_no:Optional[str] =None
#     whatsapp_no:Optional[str] =None
#     email:Optional[str] =None
#     approx_fiting_hours:str
#     reference_no:Optional[str] =None
#     employee_id:Optional[int] =None
#     prepared_by:str
#     measured_by:str
#     transport_name:Optional[str] =None
#     deliver_area:Optional[str] =None
#     due_date:Optional[datetime]=None
#     qut_date:datetime
#     invoice_no:Optional[str] =None
#     remarks:Optional[str] =None
#     is_others:Optional[int]=None


#     # payment_mode:int
#     # advance_payment:Optional[float]=0

#     tax:int=18
#     installation_amount:Optional[float]=0
#     labour_charges:Optional[float]=0
#     rework_charges:Optional[float]=0
#     transport_charges:Optional[float]=0
#     service_charges:Optional[float]=0
#     packing_charges:Optional[float]=0
#     terms_list:List[ListTerms]

    

# class Quotations(BaseModel):
#     token:str
#     utr_no:Optional[str] =None
#     is_new:Optional[int] =None
#     customer_id:Optional[int] =None
#     approx_fiting_hours:str
#     reference_no:Optional[str] =None
#     lead_id:int
#     employee_id:Optional[int] =None
#     prepared_by:str
#     total_amount:Optional[float]=None
#     measured_by:str
#     remarks:Optional[str] =None
#     dealer_id:Optional[int] =None
#     surname:Optional[str] =None
#     customer_name:Optional[str] =None
#     address:Optional[str] =None
#     is_others:Optional[int]=None
#     billing_address:Optional[str] =None
#     phone:Optional[str] =None
#     alternative_no:Optional[str] =None
#     whatsapp_no:Optional[str] =None
#     transport_name:Optional[str] =None
#     deliver_area:Optional[str] =None
#     due_date:Optional[datetime]=None
#     qut_date:datetime
#     email:Optional[str] =None
#     invoice_no:Optional[str] =None
#     correction_type:Optional[int] =None
#     correction_amount:Optional[float] = None

#     terms_list:List[ListTerms]
#     # payment_mode:int
#     # advance_payment:Optional[float]=0

#     tax:int=18
#     installation_amount:Optional[float]=0
#     labour_charges:Optional[float]=0
#     rework_charges:Optional[float]=0
#     transport_charges:Optional[float]=0
#     service_charges:Optional[float]=0
#     packing_charges:Optional[float]=0

#     orderList:List[OrderItems]



# # class UploadFilesList(BaseModel):
# #     reason: str="-"
# #     upload_file: Optional[UploadFile] = None