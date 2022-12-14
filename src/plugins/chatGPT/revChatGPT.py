import json
import uuid
import asyncio
import httpx
from typing import List
from playwright.async_api import async_playwright
from utils.log import logger


def generate_uuid() -> str:
    """
    Generate a UUID for the session -- Internal use only

    :return: a random UUID
    :rtype: :obj:`str`
    """
    uid = str(uuid.uuid4())
    return uid


class AsyncChatbot:
    config: dict
    conversation_id: str | None
    parent_id: str
    base_url: str
    headers: dict
    conversation_id_prev_queue: List
    parent_id_prev_queue: List
    request_timeout: int
    captcha_solver: bool | None

    def __init__(self, config, conversation_id=None, parent_id=None, request_timeout=100, captcha_solver=None, base_url="https://chat.openai.com/", max_rollbacks=20):
        self.config = config
        self.conversation_id = conversation_id
        self.parent_id = parent_id if parent_id else generate_uuid()
        self.base_url = base_url
        self.request_timeout = request_timeout
        self.captcha_solver = captcha_solver
        self.max_rollbacks = max_rollbacks
        self.conversation_id_prev_queue = []
        self.parent_id_prev_queue = []
        self.config["accept_language"] = (self.config["accept_language"]
            if self.config.get("accept_language")
            else "en-US,en")
        self.config["user_agent"] = (self.config["user_agent"]
            if self.config.get("user_agent")
            else "Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0")
        self.headers = {
            "Accept": "text/event-stream",
            "Authorization": "Bearer ",
            "Content-Type": "application/json",
            "User-Agent": self.config["user_agent"],
            "X-Openai-Assistant-App-Id": "",
            "Connection": "close",
            "Accept-Language": self.config["accept_language"]+";q=0.9",
            "Referer": "https://chat.openai.com/chat",
        }

    def reset_chat(self) -> None:
        """
        Reset the conversation ID and parent ID.

        :return: None
        """
        self.conversation_id = None
        self.parent_id = generate_uuid()

    def __refresh_headers(self) -> None:
        """
        Refresh the headers -- Internal use only

        :return: None
        """
        if not self.config.get("Authorization"):
            self.config["Authorization"] = ""
        self.headers["Authorization"] = "Bearer " + \
            self.config["Authorization"]
        self.headers["User-Agent"] = self.config["user_agent"]

    async def __get_chat_text(self, data) -> dict | None:
        """
        Get the chat response as text -- Internal use only
        :param data: The data to send
        :type data: :obj:`dict`
        :return: The chat response
        :rtype: :obj:`dict`
        """
        # Create request session
        proxies = self.config["proxy"] if self.config.get("proxy") else None
        async with httpx.AsyncClient(proxies=proxies) as s:
            # set headers
            s.headers = self.headers
            # Set cloudflare cookies
            if "cf_clearance" in self.config:
                s.cookies.set(
                    "cf_clearance",
                    self.config["cf_clearance"],
                )
            response = await s.post(
                self.base_url + "backend-api/conversation",
                data=data,
                timeout=self.request_timeout,
            )
            try:
                response = response.text.splitlines()[-4]
                response = response[6:]
            except Exception as exc:
                logger.error("Incorrect response from OpenAI API")
                raise Exception("Incorrect response from OpenAI API") from exc
            # Check if it is JSON
            if response.startswith("{"):
                response = json.loads(response)
                self.parent_id = response["message"]["id"]
                self.conversation_id = response["conversation_id"]
                message = response["message"]["content"]["parts"][0]
                return {
                    "message": message,
                    "conversation_id": self.conversation_id,
                    "parent_id": self.parent_id,
                }
            else:
                return None

    async def get_chat_response(self, prompt: str, conversation_id=None, parent_id=None) -> dict | None:
        """
        Get the chat response.

        :param prompt: The message sent to the chatbot
        :type prompt: :obj:`str`

        :param output: The output type `text` or `stream`
        :type output: :obj:`str`, optional

        :return: The chat response `{"message": "Returned messages", "conversation_id": "conversation ID", "parent_id": "parent ID"}` or None
        :rtype: :obj:`dict` or :obj:`None`
        """
        await self.refresh_session()
        data = {
            "action": "next",
            "messages": [
                {
                    "id": str(generate_uuid()),
                    "role": "user",
                    "content": {"content_type": "text", "parts": [prompt]},
                },
            ],
            "conversation_id": conversation_id,
            "parent_message_id": parent_id,
            "model": "text-davinci-002-render",
        }
        self.conversation_id_prev_queue.append(
            data["conversation_id"])  # for rollback
        self.parent_id_prev_queue.append(data["parent_message_id"])
        while len(self.conversation_id_prev_queue) > self.max_rollbacks:  # LRU, remove oldest
            self.conversation_id_prev_queue.pop(0)
        while len(self.parent_id_prev_queue) > self.max_rollbacks:
            self.parent_id_prev_queue.pop(0)
        return await self.__get_chat_text(data)

    def rollback_conversation(self, num=1) -> None:
        """
        Rollback the conversation.
        :param num: The number of messages to rollback
        :return: None
        """
        for _ in range(num):
            self.conversation_id = self.conversation_id_prev_queue.pop()
            self.parent_id = self.parent_id_prev_queue.pop()

    async def refresh_session(self) -> None:
        """
        Refresh the session.

        :return: None
        """
        if self.config.get("session_token"):
            await self.__get_cf_cookies()
            proxies = self.config["proxy"] if self.config.get("proxy") else None
            async with httpx.AsyncClient(proxies=proxies) as s:
                # Set cookies
                s.cookies.set(
                    "__Secure-next-auth.callback-url",
                    "https%3A%2F%2Fchat.openai.com%2Fchat"
                )
                s.cookies.set(
                    "__Secure-next-auth.session-token",
                    self.config["session_token"],
                )

                s.cookies.set(
                    "cf_clearance",
                    self.config["cf_clearance"],
                )
                # s.cookies.set(
                #     "__Secure-next-auth.csrf-token",
                #     self.config["csrf_token"],
                # )
                response = await s.get(
                    self.base_url + "api/auth/session",
                    headers={
                        "User-Agent": self.config["user_agent"],
                    },
                )
            # Check the response code
            if response.status_code != 200:
                if response.status_code == 403:
                    await self.__get_cf_cookies()
                    await self.refresh_session()
                    return
                else:
                    logger.error(
                        f"Invalid status code: {response.status_code}")
                    raise Exception("Wrong response code")
            # Try to get new session token and Authorization
            try:
                if "error" in response.json():
                    logger.error("Error in response JSON")
                    logger.error(response.json()["error"])
                    raise Exception
                self.config["session_token"] = response.cookies.get(
                    "__Secure-next-auth.session-token",
                )
                self.config["Authorization"] = response.json()["accessToken"]
                self.__refresh_headers()
            # If it fails, try to login with email and password to get tokens
            except Exception as exc:
                # Check if response JSON is empty
                if response.json() == {}:
                    logger.error("Empty response")
                    logger.error("Probably invalid session token")
                # Check if ["detail"]["code"] == "token_expired" in response JSON
                # First check if detail is in response JSON
                elif "detail" in response.json():
                    # Check if code is in response JSON
                    if "code" in response.json()["detail"]:
                        # Check if code is token_expired
                        if response.json()["detail"]["code"] == "token_expired":
                            logger.error("Token expired")
                raise Exception("Failed to refresh session") from exc
            return
        else:
            logger.error(
                "No session_token, email and password or Authorization provided")
            raise ValueError(
                "No session_token, email and password or Authorization provided")

    async def __get_cf_cookies(self) -> None:
        """
        Get cloudflare cookies.

        :return: None
        """
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True)
            content = await browser.new_context(user_agent=self.config['user_agent'])
            page = await content.new_page()
            await page.add_init_script("Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});")
            await page.goto("https://chat.openai.com/")
            cf_clearance = None
            for _ in range(6):
                if cf_clearance:
                    break
                await asyncio.sleep(5)
                cookies = await content.cookies()
                for i in cookies:
                    if i["name"] == "cf_clearance":
                        cf_clearance = i
                        break
            else:
                logger.error("cf challenge fail")
                raise Exception("cf challenge fail")
            self.config["cf_clearance"] = cf_clearance["value"]
            await page.close()
            await content.close()
            await browser.close()

    def send_feedback(
        self,
        is_good: bool,
        is_harmful=False,
        is_not_true=False,
        is_not_helpful=False,
        description=None,
    ):
        from dataclasses import dataclass

        @ dataclass
        class ChatGPTTags:
            Harmful = "harmful"
            NotTrue = "false"
            NotHelpful = "not-helpful"

        url = self.base_url + "backend-api/conversation/message_feedback"

        data = {
            "conversation_id": self.conversation_id,
            "message_id": self.parent_id,
            "rating": "thumbsUp" if is_good else "thumbsDown",
        }

        if not is_good:
            tags = list()
            if is_harmful:
                tags.append(ChatGPTTags.Harmful)
            if is_not_true:
                tags.append(ChatGPTTags.NotTrue)
            if is_not_helpful:
                tags.append(ChatGPTTags.NotHelpful)
            data["tags"] = tags

        if description is not None:
            data["text"] = description

        response = httpx.post(
            url,
            headers=self.headers,
            data=data,
            timeout=self.request_timeout,
        )

        return response

