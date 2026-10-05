import argparse
import random
import sys
from pathlib import Path

TEMPLATES = {
    "хоррор": {
        "hook": [
            "Никогда не ищи в интернете: {t}. Я пожалел.",
            "Это случилось в 3:07 ночи. Всё из-за темы «{t}».",
        ],
        "blocks": [
            "Всё началось с мелочи: в «{t}» что-то было не так, но никто не обращал внимания.",
            "Чем глубже я копал, тем больше странностей: звуки, тени, совпадения, связанные с «{t}».",
            "Когда я понял, в чём дело, было уже поздно: «{t}» смотрело прямо на меня.",
        ],
        "outro": "Если дошёл до конца — ты не один. Подпишись, чтобы не пропустить следующую историю. И не выключай свет.",
    },
    "мотивация": {
        "hook": [
            "Хватит ждать! Вот что «{t}» изменит в твоей жизни за 30 секунд.",
            "Все говорят про «{t}», но никто не говорит главного.",
        ],
        "blocks": [
            "Первое: начни с малого. Любой путь к «{t}» стартует с одного шага.",
            "Второе: не сравнивай себя с другими. Твой прогресс в «{t}» — только твой.",
            "Третье: не сдавайся, когда трудно. Именно в этот момент «{t}» начинает работать на тебя.",
        ],
        "outro": "Ты сильнее, чем думаешь. Подпишись, и мы пройдём этот путь вместе!",
    },
    "факты": {
        "hook": [
            "Ты не поверишь, но вот что известно про «{t}».",
            "5 секунд — и ты узнаешь о «{t}» то, чего не знает 90% людей.",
        ],
        "blocks": [
            "Факт первый: «{t}» появилось раньше, чем принято считать.",
            "Факт второй: у «{t}» есть неожиданная сторона, о которой редко говорят.",
            "Факт третий: даже эксперты до сих пор спорят о том, как устроено «{t}».",
        ],
        "outro": "Это были только самые интересные факты. Подпишись, чтобы узнать больше!",
    },
}


def build(topic, style):
    t = TEMPLATES[style]
    lines = [f"СЦЕНАРИЙ ({style}): {topic}", "", "ХУК (0–2 сек):", random.choice(t["hook"]).format(t=topic), ""]
    for i, block in enumerate(t["blocks"], 1):
        lines += [f"БЛОК {i}:", block.format(t=topic), ""]
    lines += ["ФИНАЛ:", t["outro"]]
    return "\n".join(lines)


ALIASES = {"horror": "хоррор", "motivation": "мотивация", "facts": "факты"}

parser = argparse.ArgumentParser(description="Генератор сценариев для коротких видео")
parser.add_argument("style", nargs="?", help="шаблон: " + ", ".join(f"{en}/{ru}" for en, ru in ALIASES.items()))
parser.add_argument("topic", nargs="*", help="тема видео (можно несколько слов)")
args = parser.parse_args()

style = ALIASES.get((args.style or "").lower(), (args.style or "").lower())
if style not in TEMPLATES:
    parser.error("укажите шаблон: " + ", ".join(ALIASES) + " (или " + ", ".join(TEMPLATES) + ")")

topic = " ".join(args.topic).strip()
if not topic and sys.stdin.isatty():
    topic = input("Тема видео: ").strip()
topic = topic or "неизвестная тема"

text = build(topic, style)
out = Path(__file__).resolve().parent / "scenario.txt"
out.write_text(text + "\n", encoding="utf-8")
print(text)
print(f"\nСохранено в {out}")
