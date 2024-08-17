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


더불어 위의 기술 뉴스 피드들이 게재되고 있는 미디엄 주소는 다음과 같습니다.

- https://medium.com/tag/y9yk-technews

---

# Architecture

medium_newsletter의 Architecture는 아래와 같습니다.

![Architecture](./Architecture.png)


# Getting Started

## Prerequisites

프로그램을 실행하기 위해 설치해야 하는 소프트웨어들은 다음과 같습니다.

- poetry
- virtualenv (pyenv, python 3.10)

## Local Development

로컬 환경에서 개발 및 실행하기 위한 환경 구성은 아래와 같습니다.

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

### Create Google Service Account and Get Google Application Credentials

프로그램을 실행하기 위해서는 Google Application Credentials가 있어야 하며, 해당 Credential은 Google Drive API 사용 권한이 있어야 합니다.

Google Application Credentials는 Google API에 접근하여 데이터를 인증하고 권한을 부여받기 위해 인간이 아닌 사용자(예: 애플리케이션)를 나타내도록 설계된 특별한 유형의 Google 계정입니다.

서비스 계정은 별도의 계정이므로, 기본적으로 이 계정은 해당 스프레드시트에 접근할 수 없습니다. 다른 Google 계정과 마찬가지로 해당 계정에 스프레드시트를 공유해야 접근할 수 있습니다.

서비스 계정을 생성하는 방법은 다음과 같습니다:

- 1. 프로젝트에 대해 API 액세스를 활성화합니다(아직 하지 않았다면).
- 2. "APIs & Services > Credentials"로 이동하여 "Create credentials > Service account key"를 선택합니다.
- 3. 양식을 작성합니다.
- 4. "Create"를 클릭한 후 "Done"을 클릭합니다.
- 5. "Service Accounts" 위에 있는 "Manage service accounts"를 클릭합니다.
- 6. 최근에 생성된 서비스 계정 옆에 있는 ⋮ 버튼을 누르고 "Manage keys"를 선택한 다음 "ADD KEY > Create new key"를 클릭합니다.
- 7. JSON 키 유형을 선택하고 "Create"를 클릭합니다.
- 8. 자동으로 자격 증명이 포함된 JSON 파일이 다운로드됩니다. 해당 파일은 다음과 비슷한 형태일 수 있습니다:

```json
{
    "type": "service_account",
    "project_id": "api-project-XXX",
    "private_key_id": "2cd … ba4",
    "private_key": "-----BEGIN PRIVATE KEY-----\nNrDyLw … jINQh/9\n-----END PRIVATE KEY-----\n",
    "client_email": "473000000000-yoursisdifferent@developer.gserviceaccount.com",
    "client_id": "473 … hd.apps.googleusercontent.com",
    ...
}
```

 - 9. 마지막으로 다운받은 JSON 파일을 `./credential/gcloud.json`으로 저장해주세요.

### Connect to Google Drive

**!Important**

프로그램을 수행하기 위해서는 아래의 Google Spreadsheet를 구성하고, 위에서 생성한 Google Application Credentials 내 `client_email`과 공유 설정이 되어있어야 합니다.

먼저, 생성되어야 하는 Google Spreadsheet는 다음과 같습니다.


| Google Spreadsheet     | 설명                                                     |
|------------------------|--------------------------------------------------------|
| awesome_research_sites | 수집해야 하는 기술 뉴스 피드 리스트가 있는 Google Spreadsheet            |
| reading_list           | 미디엄 포스트 생성에 사용된 피드 내 포스트들과 날짜를 기록하는 Google Spreadsheet |
| title_list             | 미디엄 포스트를 생성할 때 사용되었던 타이틀과 날짜를 기록하는 Google Spreadsheet  |

각 Spreadsheet의 예시는 다음과 같습니다.

#### awesom_research_sites

![awesome_research_sites](./awesome_research_sites.png)

#### reading_list

![reading_list](./reading_list.png)

#### title_list

![title_list](./title_list.png)


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