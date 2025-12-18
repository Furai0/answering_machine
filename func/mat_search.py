import re
from typing import List, Tuple
from func.mats import mats

def levenshtein_with_limit(a: str, b: str, max_dist: int) -> int:
    """
    Возвращает расстояние Левенштейна между a и b.
    Если расстояние > max_dist, возвращает любое значение > max_dist (быстро).
    """
    # Быстрая проверка по длине
    if abs(len(a) - len(b)) > max_dist:
        return max_dist + 1

    if len(a) > len(b):
        a, b = b, a

    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        current = [i] + [0] * len(b)
        min_in_row = current[0]
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            insert = current[j - 1] + 1
            delete = previous[j] + 1
            replace = previous[j - 1] + cost
            current[j] = min(insert, delete, replace)
            if current[j] < min_in_row:
                min_in_row = current[j]
        # ранняя остановка: если в строке уже все > max_dist
        if min_in_row > max_dist:
            return max_dist + 1
        previous = current
    return previous[-1]

def find_fuzzy_matches(text: str, pattern_words: List[str], max_dist: int = 3
                      ) -> List[Tuple[str, str, int]]:
    """
    Ищет в тексте слова, которые совпадают с любым из pattern_words с допускаемым
    расстоянием Левенштейна <= max_dist.
    Возвращает список кортежей: (слово_в_тексте, шаблон, расстояние).
    """
    # Простая токенизация (слова из букв/цифр/подчёрки). Можно заменить на другую токенизацию.
    tokens = re.findall(r"\w+", text, flags=re.UNICODE)
    patterns_lower = [p.lower() for p in pattern_words]
    results = []

    for token in tokens:
        t = token.lower()
        for p in patterns_lower:
            dist = levenshtein_with_limit(t, p, max_dist)
            if dist <= max_dist:
                results.append((token, p, dist))
                # Если нужно только первое совпадение для слова — break
                # break
    return results

def mat_search(text):
    find = False
    patterns = mats
    matches = find_fuzzy_matches(text, patterns, max_dist=2)
    if matches:

        # print(f"{matches[0][0]}")
        # mat = matches[0][0]
        find = True
        return find

print(mat_search('хуй, конь, фывааывпп'))