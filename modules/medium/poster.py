from config import settings
from modules.clients import make_request


class MediumPoster(object):
    def __init__(self):
        pass

    async def get_user_id(self):
        data, status_code = await make_request(
            url=f"{settings.MEDIUM_API_BASE_URL}{settings.MEDIUM_API_GET_USER_URL}",
            headers={"Authorization": f"Bearer {settings.MEDIUM_ACCESS_TOKEN}"},
            method="get",
            is_json_resp=True,
        )

        assert status_code == 200
        return data["data"]["id"]

    async def post(
        self,
        user_id: str,
        title: str,
        content: str,
        tags=[],
        publish_status="draft",
    ):
        data, _ = await make_request(
            url=f"{settings.MEDIUM_API_BASE_URL}/v1/users/{user_id}/posts",
            headers={"Authorization": f"Bearer {settings.MEDIUM_ACCESS_TOKEN}"},
            method="post",
            data={
                "title": title,
                "contentFormat": "markdown",
                "content": content,
                "canonicalUrl": "",
                "tags": tags,
                "publishStatus": publish_status,
            },
            is_json_resp=True,
        )

        return data


medium_poster = MediumPoster()


def get_medium_poster() -> MediumPoster:
    return medium_poster
