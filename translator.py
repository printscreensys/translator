import sys
import requests
from exceptions import *
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': "Mozilla/5.0"}

LANG = ["arabic", "german", "english", "spanish", "french", "hebrew", "japanese", "dutch", "polish", "portuguese",
        "romanian", "russian", "turkish"]


def form_request(word, src_lang, trg_lang):
    return f"https://context.reverso.net/translation/{src_lang}-{trg_lang}/{word}"


def get_translations(r: requests.api) -> list:
    page = r.text
    soup = BeautifulSoup(page, "html.parser")
    terms = list(map(lambda x: x.text, soup.select(".display-term")))

    return terms


def get_examples(r: requests.api, trg_lang) -> list:
    page = r.text
    soup = BeautifulSoup(page, "html.parser")
    if trg_lang == "arabic":
        pairs = zip(soup.select(".src.ltr"), soup.select(".trg.rtl.arabic"))
    elif trg_lang == "hebrew":
        pairs = zip(soup.select(".src.ltr"), soup.select(".trg.rtl"))
    else:
        pairs = zip(soup.select(".src.ltr"), soup.select(".trg.ltr"))

    examples = list(map(lambda x: (x[0].text.strip(), x[1].text.strip()), pairs))

    return examples


def print_and_write(f, out: str):
    f.write(out+ "\n")
    print(out)


def file_output(f, word, trg_lang, src_lang, mode='w', encoding='utf-8'):
    r = requests.get(form_request(word, src_lang, trg_lang), headers=HEADERS)

    if "not found in Context" in r.text:
        print(UnknownWordException(word).message)
        exit(0)

    if r.status_code != 200:
        print(ConnectionProblemException().message)
        exit(0)

    print(f"{trg_lang} Translations:", file=f)
    translations = get_translations(r)
    print(translations[0], file=f)

    print(f"\n{trg_lang} Examples:", file=f)
    examples = get_examples(r, trg_lang)
    print(examples[0][0], file=f)
    print(examples[0][1], file=f)
    print("\n", file = f)


def main():
    src_lang, trg_lang, word = sys.argv[1:]

    if src_lang not in LANG:
        print(UnsupportedLanguageException(src_lang).message)
        exit(0)

    if trg_lang not in LANG and trg_lang != "all":
        print(UnsupportedLanguageException(trg_lang).message)
        exit(0)

    if trg_lang == "all":
        with open(f"{word}.txt", "w+", encoding="utf-8") as f:
            for i in range(len(LANG)):
                if LANG[i] == src_lang:
                    continue
                file_output(f, word, LANG[i], src_lang)
        f.close()
    else:
        with open(f"{word}.txt", "w", encoding="utf-8") as f:
            file_output(f, word, trg_lang, src_lang)
            f.close()

    with open(f"{word}.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            print(line.strip())
        f.close()


if __name__ == "__main__":
    main()
