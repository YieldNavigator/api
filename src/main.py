from starlette.middleware.cors import CORSMiddleware
from src.traker import *
from fastapi import FastAPI, APIRouter
import uvicorn

app = FastAPI(docs_url="/yn/docs", redoc_url="/yn/redoc", openapi_url='/yn/openapi.json')
router = APIRouter(prefix="/yn")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@router.get("/stocks/{ticker}")
async def get_stock(ticker):
    '''
    종목 정보 조회

    :param ticker:
    :return: { 'ticker': 'NVDY',
            'price': 25.639999389648438,
            'period': 'monthly',
            'divinedHistories': [
              { 'divineDate': '2024-08-07', 'amount': 1.251 },
              { 'divineDate': '2024-07-06', 'amount': 2.576 },
            ],
            'totalAvg': xxx,
            'xxxxAvg': xxx
        }
    '''
    return find_recent_dividends(ticker)


@router.get("/user-stocks/{uid}")
async def get_stocks(uid):
    '''
     사용자 보유 정보 조회
    :param uid:
    :return:
        [
          { 'ticker': 'NVDY',
            'targetShares': 150,
            'currentShares': 90
          },
          { 'ticker': 'CONY',
            'targetShares': 150,
            'currentShares': 20
          }
        ]
    '''
    return get_user_stocks(uid)


# 라우터를 애플리케이션에 등록
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True)
