# medium_newsletter

다양한 기술 뉴스 피드를 모아서 요약 -> 미디엄 블로그에 게재하는 서비스를 지원합니다.

아래의 기술 뉴스 피드를 지원하고 있습니다.

| 피드                 | URL                                          |
|--------------------|----------------------------------------------|
| wired              | https://www.wired.com/feed/tag/ai/latest/rss |
| theverge           | https://www.theverge.com/rss/full.xml        |
| engadget           | https://www.engadget.com/rss.xml             |
| techcrunch         | https://techcrunch.com/feed/                 |
| pragmaticeengineer | https://blog.pragmaticengineer.com/rss/      |


---

# Getting Started

## Prerequisites

- poetry
- virtualenv (pyenv, python 3.10)

## Local Development

로컬에서 개발하기 위한 환경 구성은 아래와 같습니다.

### Install Dependencies

```bash
$ poetry shell
$ poetry install --no-root
$ make install-pre-commit
```

### Configuration

- ./config/.env 파일을 구성해야 합니다.
- ./config/.env.sample 파일을 참고하세요.
- 활용되는 환경 변수는 다음과 같습니다.

| 환경변수                | 설명                             |
|---------------------|--------------------------------|
| MEDIUM_ACCESS_TOKEN | 미디엄 글을 올리기 위한 Access Token     |
| OPENAI_MODEL_NAME   | 사용되는 모델 이름 (e.g., gpt-4o-mini) |
| OPENAI_API_KEY      | 사용되는 모델 키                      |
| DEBUG               | 디버깅 여부 (e.g., True/False)      |

### Connect to Google Drive

**!important Google Spreadsheet와 연결되어야, 프로그램을 수행할 수 있습니다.**

- https://docs.gspread.org/en/latest/oauth2.html
- Google Drive API가 사용 가능한 상태가 되어야 합니다.
- credential은 ./credential/gcloud.json의 이름으로 저장되어야 합니다.
- 미리 만들어져야 하는 Google Spreadsheet의 파일명은 다음과 같습니다.
  - awesome_research_sites: 기술 피드 목록을 저장합니다.
  - reading_list
  - title_list

## Execution Program

- ./sbin.run.sh 스크립트를 통해 실행할 수 있습니다.
- 넘겨야 하는 argument는 아래 2가지 입니다.
  - topics: 해당 topics과 관련이 있는 글들만 피드에서 수집하여 요약합니다. comma separator로 구분합니다. (e.g., AI, Machine Learning)
  - publish_status: 미디엄에 게재할 상태를 의미합니다. `public, draft, unlisted` 세 가지 옵션이 있습니다.

```bash
$ ./sbin/run.sh AI draft
-----------------------------------------
CURR_DIR: /Users/y9yk/dev/medium_newsletter/sbin
PROJECT_ROOT: /Users/y9yk/dev/medium_newsletter
-----------------------------------------
2024-08-11 14:13:35.791 | DEBUG    | __main__:execute:13 - topics: ['AI']
/Users/y9yk/dev/medium_newsletter/main.py:16: DeprecationWarning: There is no current event loop
  loop = asyncio.get_event_loop()
2024-08-11 14:13:35.792 | INFO     | modules.utils.logger:log_step:11 - ----------
2024-08-11 14:13:35.792 | INFO     | modules.utils.logger:log_step:12 - get_seed_data
2024-08-11 14:13:35.792 | INFO     | modules.utils.logger:log_step:13 - ----------
2024-08-11 14:13:38.153 | DEBUG    | modules.processor:run:31 - [['wired', 'https://www.wired.com/feed/tag/ai/latest/rss'], ['theverge', 'https://www.theverge.com/rss/full.xml'], ['engadget', 'https://www.engadget.com/rss.xml'], ['techcrunch', 'https://techcrunch.com/feed/'], ['pragmaticeengineer', 'https://blog.pragmaticengineer.com/rss/']]
2024-08-11 14:13:38.153 | INFO     | modules.utils.logger:log_step:11 - ----------
2024-08-11 14:13:38.153 | INFO     | modules.utils.logger:log_step:12 - parse_feed_data
2024-08-11 14:13:38.153 | INFO     | modules.utils.logger:log_step:13 - ----------
2024-08-11 14:13:38.154 | DEBUG    | modules.processor:run:36 - parsing: wired
2024-08-11 14:13:40.426 | DEBUG    | modules.processor:run:36 - parsing: theverge
2024-08-11 14:13:41.223 | DEBUG    | modules.processor:run:36 - parsing: engadget
2024-08-11 14:13:47.044 | DEBUG    | modules.processor:run:36 - parsing: techcrunch
2024-08-11 14:13:48.037 | DEBUG    | modules.processor:run:36 - parsing: pragmaticeengineer
2024-08-11 14:13:48.227 | INFO     | modules.utils.logger:log_step:11 - ----------
2024-08-11 14:13:48.227 | INFO     | modules.utils.logger:log_step:12 - filter feeds not in reading_list -> sampling (TODO to extract favorate contents for me)
2024-08-11 14:13:48.227 | INFO     | modules.utils.logger:log_step:13 - ----------
2024-08-11 14:13:49.569 | INFO     | modules.utils.logger:log_step:11 - ----------
2024-08-11 14:13:49.569 | INFO     | modules.utils.logger:log_step:12 - filter feeds by summary length
2024-08-11 14:13:49.570 | INFO     | modules.utils.logger:log_step:13 - ----------
2024-08-11 14:13:49.570 | INFO     | modules.utils.logger:log_step:11 - ----------
2024-08-11 14:13:49.571 | INFO     | modules.utils.logger:log_step:12 - inspect filter length
2024-08-11 14:13:49.571 | INFO     | modules.utils.logger:log_step:13 - ----------
2024-08-11 14:13:49.572 | INFO     | modules.utils.logger:log_step:11 - ----------
2024-08-11 14:13:49.572 | INFO     | modules.utils.logger:log_step:12 - technews_generator
2024-08-11 14:13:49.572 | INFO     | modules.utils.logger:log_step:13 - ----------
2024-08-11 14:14:09.641 | INFO     | modules.utils.logger:log_step:11 - ----------
2024-08-11 14:14:09.641 | INFO     | modules.utils.logger:log_step:12 - append title to content
2024-08-11 14:14:09.641 | INFO     | modules.utils.logger:log_step:13 - ----------
2024-08-11 14:14:09.641 | INFO     | modules.utils.logger:log_step:11 - ----------
2024-08-11 14:14:09.641 | INFO     | modules.utils.logger:log_step:12 - medium posting
2024-08-11 14:14:09.641 | INFO     | modules.utils.logger:log_step:13 - ----------
2024-08-11 14:14:10.879 | DEBUG    | modules.processor:run:96 - {'data': {'id': '951bde44b251', 'title': '"2024년 기술 동향: AI, 스타트업, 그리고 산업 변화"', 'authorId': '1cdb9d0835223cb51fc98565cbcaab7a3faa5dd3ff3fdc15a29ba9c51d7ba3c7e', 'url': 'https://medium.com/@andrew.yk82/951bde44b251', 'canonicalUrl': '', 'publishStatus': 'draft', 'license': '', 'licenseUrl': 'https://policy.medium.com/medium-terms-of-service-9db0094a1e0f', 'tags': ['technews']}}
2024-08-11 14:14:10.880 | INFO     | modules.utils.logger:log_step:11 - ----------
2024-08-11 14:14:10.881 | INFO     | modules.utils.logger:log_step:12 - post-processing
2024-08-11 14:14:10.881 | INFO     | modules.utils.logger:log_step:13 - ----------
2024-08-11 14:14:10.882 | DEBUG    | modules.post_processor:record_reading_list:21 - updated links: [['https://www.wired.com/story/center-for-ai-safety-open-source-llm-safeguards/', '20240811'], ['https://www.engadget.com/apps/tiktok-will-make-it-easier-to-identify-movies-and-tv-shows-that-users-are-clipping-143449273.html?src=rss', '20240811'], ['https://www.engadget.com/social-media/turkey-unblocks-instagram-after-talks-to-address-its-concerns-about-crime-and-censorship-212231212.html?src=rss', '20240811'], ['https://www.wired.com/story/anduril-palmer-luckey-funding-ai-drones-arsenal-factory/', '20240811'], ['https://techcrunch.com/2024/08/09/anysphere-a-github-copilot-rival-has-raised-60m-series-a-at-400m-valuation-from-a16z-thrive-sources-say/', '20240811'], ['https://techcrunch.com/2024/08/10/the-tech-world-mourns-susan-wojcicki/', '20240811'], ['https://www.engadget.com/transportation/tenways-ago-t-is-a-well-equipped-but-heavy-e-bike-133005101.html?src=rss', '20240811'], ['https://blog.pragmaticengineer.com/the-software-engineering-industry-in-2024/', '20240811'], ['https://www.engadget.com/ai/uk-opens-antitrust-investigation-into-amazon-over-its-ties-to-ai-startup-anthropic-153026609.html?src=rss', '20240811'], ['https://www.wired.com/story/gadget-lab-podcast-654/', '20240811']]
2024-08-11 14:14:12.929 | DEBUG    | modules.post_processor:record_title_list:26 - updated title: "2024년 기술 동향: AI, 스타트업, 그리고 산업 변화"
```