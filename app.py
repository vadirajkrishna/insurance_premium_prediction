
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from uvicorn import run as app_run
import pandas as pd

from typing import Optional

from prem_pred.constants import APP_HOST, APP_PORT
from prem_pred.pipeline.prediction_pipeline import PremPredData, PremiumPredictor
from prem_pred.pipeline.training_pipeline import TrainPipeline

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.age: Optional[str] = None
        self.sex: Optional[str] = None
        self.bmi: Optional[str] = None
        self.children: Optional[int] = None
        self.smoker: Optional[str] = None
        self.region: Optional[str] = None        
        
    async def get_prempred_data(self):
        form = await self.request.form()
        self.age = form.get("age")
        self.sex = form.get("sex")
        self.bmi = form.get("bmi")
        self.children = form.get("children")
        self.smoker = form.get("smoker")
        self.region = form.get("region")

@app.get("/", tags=["authentication"])
async def index(request: Request):

    return templates.TemplateResponse(
            "prempred.html",{"request": request, "context": "Rendering"})


@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline = TrainPipeline()

        train_pipeline.run_pipeline()

        return Response("Training successful !!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.post("/")
async def predictRouteClient(request: Request):
    try:
        form = DataForm(request)
        await form.get_prempred_data()
        
        prempred_data = PremPredData(
                                age= form.age,
                                sex = form.sex,
                                bmi = form.bmi,
                                children = form.children,
                                smoker = form.smoker,
                                region= form.region,
                                )
        
        prempred_df = prempred_data.get_prempred_input_data_frame()
        # print("dataframe is", prempred_df) # for debugging
        prempred_df["children"] = pd.to_numeric(prempred_df["children"])
        # prempred_df.to_csv('testdf.csv')
        model_predictor = PremiumPredictor()

        value = model_predictor.predict(dataframe=prempred_df)[0]

        # status = None
        # if value == 1:
        #     status = "Visa-approved"
        # else:
        #     status = "Visa Not-Approved"

        #predicted_charge = value

        return templates.TemplateResponse(
            "prempred.html",
            {"request": request, "context": value},
        )
        
    except Exception as e:
        return {"status": False, "error": f"{e}"}


if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)