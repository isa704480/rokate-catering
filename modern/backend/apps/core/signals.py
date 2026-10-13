"""Kontent saqlanganda Next.js saytini yangilash (on-demand revalidate)."""
import json
import logging
import threading
import urllib.request

from django.conf import settings
from django.db.models.signals import m2m_changed, post_delete, post_save

log = logging.getLogger(__name__)

CONTENT_APPS = {"core", "services", "catering", "portfolio"}


def _post(url, secret):
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps({"tags": ["cms"]}).encode(),
            headers={"Content-Type": "application/json", "X-Revalidate-Secret": secret},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=5).read()
    except Exception as exc:  # noqa: BLE001
        # Frontend ishlamayotgan bo'lsa (lokal) — bu normal holat, shovqin qilmaymiz
        refused = isinstance(getattr(exc, "reason", exc), ConnectionRefusedError)
        (log.debug if refused else log.warning)("Revalidate failed: %s", exc)


SUSPENDED = False  # seed_demo kabi ommaviy yozishlarda vaqtincha o'chiriladi


def trigger_revalidate():
    if SUSPENDED:
        return
    if settings.REVALIDATE_URL and settings.REVALIDATE_SECRET:
        threading.Thread(target=_post, args=(settings.REVALIDATE_URL, settings.REVALIDATE_SECRET), daemon=True).start()


def _handler(sender, **kwargs):
    if getattr(sender._meta, "app_label", None) in CONTENT_APPS and not kwargs.get("raw"):
        trigger_revalidate()


post_save.connect(_handler, dispatch_uid="rk_revalidate_save")
post_delete.connect(_handler, dispatch_uid="rk_revalidate_delete")
m2m_changed.connect(_handler, dispatch_uid="rk_revalidate_m2m")
