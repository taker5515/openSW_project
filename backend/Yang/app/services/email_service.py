from app.external.email_provider import EmailProvider

_provider = EmailProvider()


def send_welcome(email: str) -> bool:
    body = (
        "<h2>주식 뉴스레터 구독 완료</h2>"
        "<p>관심 테마와 종목의 최신 뉴스를 받아보실 수 있습니다.</p>"
        "<p><small>이 서비스는 투자 추천이 아닌 참고용 정보 제공을 목적으로 합니다.</small></p>"
    )
    return _provider.send(to=email, subject="[StockLetter] 구독 확인", body_html=body)


def send_newsletter(email: str, news_items: list[dict]) -> bool:
    rows = "".join(
        f"<li><b>[{n.get('signal','?')}]</b> {n.get('title','')} — {n.get('source','')}</li>"
        for n in news_items
    )
    body = f"<h2>오늘의 주식 뉴스</h2><ul>{rows}</ul>"
    return _provider.send(to=email, subject="[StockLetter] 오늘의 뉴스", body_html=body)
