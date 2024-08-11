from datetime import datetime
from pytz import timezone
from typing import List

from modules.llm import Tone


def generate_newsletter_title(
    context,
) -> str:
    return f"""
"Context":
"{context}"

"Content Focus":

- "Context" 정보는 다양한 소스에서 수집한 피드의 제목들입니다.
- 여러 제목을 포괄할 수 있는 제목을 생성해야 합니다.
- 생성된 제목은 블로그 포스트의 제목으로 활용될 것입니다.

"!IMPORTANT":
- 관련 없는 정보는 반드시 제외하십시오!
- 반드시 여러 제목을 포괄할 수 있는 제목을 생성해야 합니다.
- 한글로 작성되어야 합니다.
"""


def generate_newsletter_main_body(
    context,
    topics: List = [],
    report_format: str = "apa",
    total_words=2000,
    tone: Tone = Tone.Objective,
) -> str:
    return f"""
"Context":
"{context}"

"Content Focus":

- "Context" 정보는 다양한 소스에서 수집한 피드입니다.
- 보고서는 "Context" 정보에서 title, summary를 잘 설명하는 데 초점을 맞추어야 하며, 잘 구조화되고, 정보가 풍부하고, 깊이 있으며, 가능하면 사실과 숫자를 포함해야 합니다.
- Markdown 문법을 사용하고 {report_format.upper()} 형식을 따르십시오.

"Structure and Formatting":
- 이 보고서는 Newsletter를 구성하는 데 목적이 있으므로, 소개나 결론 섹션 없이 적절한 하위 주제로 나누어진 본문만 포함하십시오.
- 이 보고서가 작성된 시간(published)과 작성자(publisher)를 Markdown 형식으로 표현하십시오.
- 이 보고서의 태그(tags) 정보도 Markdown 형식으로 표현하십시오. 단, 국가와 관련된 태그 정보는 노출하지 마십시오.
- 작성된 시간, 작성자, 태그 그리고 출처 URL은 Markdown 형식으로 표현되어야 합니다. 예를 들어:

  # Report Header
  이것은 샘플 텍스트입니다. 

  - 출처: [url website](url)
  - 발행자: Engadget
  - 발행일: 2024년 8월 7일
  - 태그: 인터넷 및 네트워킹 기술
  
"날짜":
필요할 경우 현재 날짜는 {datetime.now(timezone("Asia/Seoul")).strftime('%Y%m%d')}로 가정하십시오.

"!IMPORTANT":
- 주요 주제에 초점을 맞춰야 합니다! 관련 없는 정보는 반드시 제외하십시오!
- 소개 섹션이 없어야 합니다.
- 제목이 없어야 합니다.
- 보고서에 포함되는 내용은 {",".join(topics)}와 관련된 내용만 포함되어야 합니다.
- 보고서에서 참조된 관련 문장에 Markdown 문법([url website](url))을 사용하여 하이퍼링크를 반드시 포함하십시오.
- 보고서의 길이는 최소 {total_words} 단어 이상이어야 합니다.
- 보고서 전반에 걸쳐 {tone.value} 어조를 사용하십시오.
- 한글로 작성되어야 합니다.
"""
