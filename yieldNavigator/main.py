from starlette.middleware.cors import CORSMiddleware

from yieldNavigator.traker import *
from fastapi import FastAPI
import uvicorn

'''
stock {
  ticker
  price (현재주가)
  period (지급주기 월별/주별)
}

yield_history {
  ticker 
  date (지급일)
  amount (배당금)
}

user_stock {
  uid (유저 식별값)
  ticker  (티커)
  target_shares (목표수량)
  current_shares (보유수량)
}

'''

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''
-- 종목 정보 조회
{ 'ticker': 'NVDY',
    'price': 25.639999389648438,
    'period': 'monthly',
    'divinedHistories': [
      { 'divineDate': '2024-08-07', 'amount': 1.251 },
      { 'divineDate': '2024-07-06', 'amount': 2.576 },
    ],
    'totalAvg': xxx,
    'trendAvg': xxx
}
'''


@app.get("/stocks/{ticker}")
async def get_stock(ticker):
    return find_recent_dividends(ticker)


'''
-- 사용자 보유 정보 조회
GET /user-stocks?uid=1234
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


@app.get("/user-stocks/{uid}")
async def get_stock(uid):
    return get_user_stocks(uid)


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True)
