from fastapi import FastAPI, Depends, HTTPException, Response, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from helper import check_menu, check_inventory, purchase_ice_cream, restock_ice_cream, give_user_feedback, get_all_feedback, feedback_report

app = FastAPI()
security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != "1337":
        raise HTTPException(status_code=401, detail="Invalid token")
    return credentials

@app.get("/menu",
         summary="Retrieve the current menu",
         description="Retrieves the current menu of ice cream flavors.")
def menu(token: HTTPAuthorizationCredentials = Depends(verify_token)):
    return Response(content=check_menu(), media_type="application/json")

@app.get("/orders",
         summary="Place an ice cream order",
         description="Places an order for a specific ice cream flavor.")
def orders(flavor: str = Query(...,
                            title="Flavor to purchase",
                            description="Specific ice cream flavor to purchase."),
        quantity: int = Query(...,
                            title="Quantity to purchase",
                            description="Quantity of the flavor to purchase."),
        token: HTTPAuthorizationCredentials = Depends(verify_token)):
    # Call the purchase_ice_cream function with the provided parameters
    result = purchase_ice_cream(flavor, quantity)
    return Response(content=result, media_type="application/json")

@app.get("/inventory",
         summary="Get inventory details",
         description="Gets details of the current ice cream invetory.")
def inventory(token: HTTPAuthorizationCredentials = Depends(verify_token)):
    return Response(content=check_inventory(), media_type="application/json")

@app.get("/restock",
         summary="Restock ice cream flavors",
         description="Restocks specific ice cream flavors.")
def restock(flavor: str = Query(..., 
                                title="Flavor to restock",
                                description="Specific flavor to restock"),
            quantity: int = Query(...,
                                  title="Quantitiy to restock",
                                  description="Quantity of a specific flavor to restock"),
            token: HTTPAuthorizationCredentials = Depends(verify_token)):
    # Call the restock_ice_cream function with the provided parameters
    result = restock_ice_cream(flavor, quantity)
    return Response(content=result, media_type="application/json")

@app.get("/give_feedback",
         summary="Submit feedback",
         description="Submits feedback for the ice cream service.")
def give_feedback(feedback: str = Query(...,
                                        title="Feedback",
                                        description="The feedback to be given"),
                rating: int = Query(...,
                                    title="Rating",
                                    description="The rating to be given"),
                token: HTTPAuthorizationCredentials = Depends(verify_token)):
    # Call the give_feedback function with the provided parameters
    result = give_user_feedback(feedback, rating)
    return Response(content=result, media_type="application/json")

@app.get("/get_feedback",
         summary="Retrieve feedback",
         description="Retrieves all feedback submitted by customers.")
def get_feedback(token: HTTPAuthorizationCredentials = Depends(verify_token)):
    return Response(content=get_all_feedback(), media_type="application/json")

@app.get("/report",
         summary="Submit customer satisfaction report",
         description="Submits a report to management based on the satisfaction report.")
def report(token: HTTPAuthorizationCredentials = Depends(verify_token)):
    return Response(content=feedback_report(), media_type="application/json")
