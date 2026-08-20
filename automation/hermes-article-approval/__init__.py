"""Hermes gateway hook for deterministic personal-site article decisions."""

import asyncio
import re


_DECISION_RE = re.compile(r"^(APPROVE|REJECT) ([A-Za-z0-9_-]{6,64})$")
_FAILURE = "Article approval failed. Check the local pipeline log."
_TASKS = set()


def _coordinator_argv(raw_message: str) -> tuple[str, ...]:
    return (
        "/usr/bin/python3",
        "/root/dataengineergaurav.github.io/scripts/article_pipeline.py",
        "decision-hex",
        raw_message.encode("utf-8").hex(),
    )


async def _run_coordinator(raw_message):
    process = await asyncio.create_subprocess_exec(
        *_coordinator_argv(raw_message),
        cwd="/root/dataengineergaurav.github.io",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL,
    )
    try:
        stdout, _ = await asyncio.wait_for(process.communicate(), timeout=900)
    except TimeoutError:
        process.kill()
        await process.wait()
        return _FAILURE
    return stdout.decode("utf-8", errors="replace").strip() or _FAILURE


async def _dispatch(gateway, event, raw_message):
    try:
        response = await _run_coordinator(raw_message)
        await gateway._deliver_platform_notice(event.source, response)
    except Exception:
        try:
            await gateway._deliver_platform_notice(event.source, _FAILURE)
        except Exception:
            pass


def _pre_gateway_dispatch(*, event, gateway, session_store=None):
    source = getattr(event, "source", None)
    platform = getattr(getattr(source, "platform", None), "value", None)
    message_type = getattr(getattr(event, "message_type", None), "value", None)
    raw_message = getattr(event, "raw_message", None)
    raw_text = getattr(raw_message, "text", None)
    if (platform != "telegram" or message_type != "text"
            or not isinstance(raw_text, str) or event.text != raw_text
            or _DECISION_RE.fullmatch(raw_text) is None):
        return None
    try:
        if not gateway._is_user_authorized(source):
            return None
    except Exception:
        return {"action": "skip", "reason": "article approval authorization failed"}
    task = asyncio.get_running_loop().create_task(_dispatch(gateway, event, raw_text))
    _TASKS.add(task)
    task.add_done_callback(_TASKS.discard)
    return {"action": "skip", "reason": "article approval"}


def register(context):
    context.register_hook("pre_gateway_dispatch", _pre_gateway_dispatch)
