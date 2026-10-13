"""Yangi ariza haqida Telegram va email orqali xabar berish."""
import json
import logging
import threading
import urllib.parse
import urllib.request

from django.conf import settings
from django.core.mail import send_mail

from apps.core.models import SiteSettings

log = logging.getLogger(__name__)


def _telegram(token, chat_id, text):
    try:
        data = urllib.parse.urlencode({"chat_id": chat_id, "text": text, "disable_web_page_preview": "true"}).encode()
        urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data=data, timeout=10).read()
    except Exception as exc:  # noqa: BLE001
        log.warning("Telegram notify failed: %s", exc)


def _email(recipients, subject, body):
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=False)
    except Exception as exc:  # noqa: BLE001
        log.warning("Email notify failed: %s", exc)


def _wa(phone):
    digits = "".join(ch for ch in phone if ch.isdigit())
    return f"https://wa.me/{digits}" if digits else ""


def inquiry_text(obj):
    rows = [
        "🆕 Новая заявка с сайта Rokate",
        f"Имя: {obj.name}",
        f"Телефон: {obj.phone}",
        f"WhatsApp: {_wa(obj.phone)}",
    ]
    if obj.event_date:
        rows.append(f"Дата: {obj.event_date:%d.%m.%Y}")
    if obj.event_type:
        rows.append(f"Тип: {obj.event_type}")
    if obj.guests:
        rows.append(f"Гостей: {obj.guests}")
    if obj.location_type:
        rows.append(f"Локация: {obj.get_location_type_display()}")
    if obj.package:
        rows.append(f"Пакет: {obj.package}")
    if obj.comment:
        rows.append(f"Комментарий: {obj.comment}")
    rows.append(f"Источник: {obj.source_label} · {obj.source_page} · {obj.language}")
    return "\n".join(rows)


def partner_text(obj):
    return "\n".join([
        "🤝 Новая заявка партнёра",
        f"Имя: {obj.name}",
        f"Компания: {obj.company}",
        f"Сфера: {obj.field}",
        f"Телефон: {obj.phone}",
        f"Email: {obj.email}",
        f"Сообщение: {obj.message}",
    ])


def notify(subject, text):
    cfg = SiteSettings.load()
    chat_id = cfg.telegram_chat_id or settings.TELEGRAM_CHAT_ID
    if settings.TELEGRAM_BOT_TOKEN and chat_id:
        threading.Thread(target=_telegram, args=(settings.TELEGRAM_BOT_TOKEN, chat_id, text), daemon=True).start()
    recipients = [x.strip() for x in (cfg.notify_emails or "").split(",") if x.strip()]
    if recipients:
        threading.Thread(target=_email, args=(recipients, subject, text), daemon=True).start()
