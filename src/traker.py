import yfinance as yf


def find_recent_dividends(ticker) -> dict:
    '''
    티커를 받아 티커 이름, 현재 주가, 최근 10개의 배당일과 배당금액을 리스트로 리턴
    :param ticker: 배당주 티커
    :return: {"ticker": 티커 이름, "price": 현재 주가(float), "period": 배당 주기,
              "divinedHistories": [{"divineDate": 배당일("yyyy-mm-dd"), "amount": 배당금(float)}],
              "totalAvg": 전체 배당금 평균(float),
              "trendAvg": 최근 5번 배당금 평균(float)}
    '''
    stock = yf.Ticker(ticker)
    dividends = stock.dividends

    # 전체 배당금 평균 계산
    totalAvg = sum(dividends) / len(dividends) if len(dividends) > 0 else 0

    # 배당금이 10개 이상이라면 10개까지만 가져오기
    if len(dividends) > 10:
        dividends = dividends[-10:]

    # 배당일과 배당금을 리스트로 변환하여 divinedHistories에 담기 (날짜 순서를 역순으로)
    divinedHistories = [{"divineDate": date.strftime('%Y-%m-%d'), "amount": amount}
                        for date, amount in zip(dividends.index, dividends.tolist())][::-1]

    price = stock.history(period="1d")['Close'].iloc[-1]

    # 최근 5번 배당금 평균 계산
    if len(dividends) > 5:
        trendDividends = dividends[-5:]
    else:
        trendDividends = dividends
    trendAvg = sum(trendDividends) / len(trendDividends) if len(trendDividends) > 0 else 0

    # 배당금 지급 날짜 간의 차이를 계산
    date_diffs = dividends.index.to_series().diff().dropna()
    avg_frequency = date_diffs.mean().days if not date_diffs.empty else 0
    if 6 <= avg_frequency <= 8:
        period = "weekly"
    elif 28 <= avg_frequency <= 32:
        period = "monthly"
    elif 85 <= avg_frequency <= 95:
        period = "quarterly"
    elif 170 <= avg_frequency <= 190:
        period = "semiannual"
    elif 350 <= avg_frequency <= 380:
        period = "annual"
    else:
        period = "unknown"

    # 결과를 JSON 형태로 만듦
    result = {
        "ticker": ticker,
        "price": float(price),
        "period": period,
        "divinedHistories": divinedHistories,
        "totalAvg": totalAvg,
        "trendAvg": trendAvg
    }

    return result


def get_user_stocks(uid):
    res = [{'ticker': 'NVDY',
            'targetShares': 150,
            'currentShares': 90
            },
           {'ticker': 'CONY',
            'targetShares': 150,
            'currentShares': 20
            }]
    return res


def find_dividends_list(ticker_list) -> str:
    '''
    ticker_list를 스프레드시트의 셀 그대로 복붙해서 사용 가능하게 설정 \t 기준으로 스플릿 해서 사용함
    :param ticker_list:
    :return: 주가를 \t 간격으로 띄워서 문자열로 리턴
    '''
    res = []
    ticker_list = ticker_list.split('\t')
    for ticker in ticker_list:
        stock = yf.Ticker(ticker)
        dividends = stock.dividends
        res.append(dividends[-1])
    return '\t'.join([str(item) for item in res])