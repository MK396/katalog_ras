#!/usr/bin/env python3
"""Uzupełnia opisy ras, które miały placeholder dog.ceo."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "breeds.json"

PLACEHOLDER = re.compile(r"^Rasa z katalogu dog\.ceo", re.I)

# id -> (description, optional origin, optional weight, optional lifespan)
UPDATES = {
    "african-wild": (
        "Afrykański pies dziki żyjący w stadach na sawannie. Nie jest typowym psem domowym — to gatunek dziki o silnej więzi stadnej i dużej wytrzymałości.",
        "Afryka subsaharyjska",
        "20–30 kg",
        "10–12 lat",
    ),
    "appenzeller": (
        "Szwajcarski pies pasterski i stróżujący o trójkolorowej sierści. Żywy, pewny siebie i bardzo związany z rodziną.",
        "Szwajcaria",
        "22–32 kg",
        "12–14 lat",
    ),
    "australian-kelpie": (
        "Australijski pies pasterski słynący z wytrzymałości w upale. Niezwykle pracowity, zwinny i wymagający dużo aktywności.",
        "Australia",
        "14–21 kg",
        "12–15 lat",
    ),
    "bakharwal-indian": (
        "Himalajski pies stróżujący i pasterski z Kaszmiru. Niezależny, ostrożny wobec obcych i lojalny wobec opiekuna.",
        "Indie",
        "30–38 kg",
        "10–12 lat",
    ),
    "brabancon": (
        "Bruselski griffon (brabancon) — mały pies towarzyszący o charakterystycznej brodawce. Ciekawski, towarzyski i przywiązany do człowieka.",
        "Belgia",
        "3–6 kg",
        "12–15 lat",
    ),
    "buhund-norwegian": (
        "Norweski buhund — sprytny pies pasterski i stróżujący. Przyjazny, energiczny i chętny do współpracy przy aktywności.",
        "Norwegia",
        "14–18 kg",
        "12–15 lat",
    ),
    "bulldog-boston": (
        "Buldog bostoński — kompaktowy pies z krótką sierścią i „frakowym” ubarwieniem. Wesoły, inteligentny i dobry towarzysz w domu.",
        "USA",
        "5–11 kg",
        "11–13 lat",
    ),
    "cattledog-australian": (
        "Australijski pies pasterski (blue lub red heeler) — wytrzymały pracownik na farmie. Czujny, zdecydowany i potrzebujący zadań.",
        "Australia",
        "16–23 kg",
        "12–16 lat",
    ),
    "cavapoo": (
        "Mieszaniec cavalier spaniela i pudla — mały, przyjazny pies domowy. Łagodny, towarzyski i często dobrze tolerowany przez alergików.",
        "Australia / Wielka Brytania",
        "5–12 kg",
        "12–15 lat",
    ),
    "chippiparai-indian": (
        "Indyjski chart z południa subkontynentu, wykorzystywany do polowań. Smukły, szybki i niezależny, ale wierny rodzinie.",
        "Indie",
        "15–20 kg",
        "12–15 lat",
    ),
    "cotondetulear": (
        "Coton de Tuléar z Madagaskaru — biały pies o puszystej, miękkiej sierści. Radosny, czuły i świetnie nadający się do towarzystwa.",
        "Madagaskar",
        "4–6 kg",
        "14–16 lat",
    ),
    "danishswedish-farmdog": (
        "Duńsko-szwedzki pies farmy — zwinny pomocnik i myśliwy. Żywy, uczuciowy i łatwy w szkoleniu przy konsekwentnym wychowaniu.",
        "Dania / Szwecja",
        "7–12 kg",
        "11–13 lat",
    ),
    "dhole": (
        "Dhole, azjatycki pies dziki, poluje w kooperacyjnych grupach. Nie jest rasą domową — to drapieżnik o silnym instynkcie łowieckim.",
        "Azja Południowa i Południowo-Wschodnia",
        "12–20 kg",
        "10–13 lat",
    ),
    "dingo": (
        "Dingo — dziki pies Australii, przystosowany do suchego klimatu. Samodzielny, ostrożny i trudny do udomowienia jak typowy pies domowy.",
        "Australia",
        "13–20 kg",
        "10–13 lat",
    ),
    "elkhound-norwegian": (
        "Norweski elkhund — pies myśliwski na łosie i jelenie. Odporny, odważny i przyjazny w rodzinie przy odpowiednim wychowaniu.",
        "Norwegia",
        "22–30 kg",
        "12–15 lat",
    ),
    "finnish-lapphund": (
        "Fiński lapphund — pies pasterski Samów z Laplandii. Łagodny, głośny przy alarmie i bardzo przywiązany do „stada”.",
        "Finlandia",
        "15–24 kg",
        "12–14 lat",
    ),
    "gaddi-indian": (
        "Gaddi — himalajski pies pastersko-stróżujący. Silny, odporny na zimno i czujny wobec intruzów.",
        "Indie",
        "32–45 kg",
        "10–12 lat",
    ),
    "greyhound-indian": (
        "Indyjski chart (często określany jako mudhol lub pokrewny typ) — szybki pies gończy. Smukły, wytrzymały i przywiązany do opiekuna.",
        "Indie",
        "20–28 kg",
        "10–12 lat",
    ),
    "greyhound-italian": (
        "Chart włoski — najmniejszy z chartów, elegancki i delikatny. Spokojny w domu, szybki na spacerze, lubi ciepło i bliskość człowieka.",
        "Włochy",
        "3–5 kg",
        "12–15 lat",
    ),
    "hound-english": (
        "English foxhound — pies gończy do polowania na lisa w sforze. Wytrzymały, towarzyski wśród psów i o spokojnym usposobieniu w domu.",
        "Wielka Brytania",
        "29–34 kg",
        "10–13 lat",
    ),
    "hound-ibizan": (
        "Chart ibizański — smukły pies myśliwski z dużymi uszami. Elegancki, niezależny i pełen energii na otwartej przestrzeni.",
        "Hiszpania (Ibiza)",
        "20–29 kg",
        "12–14 lat",
    ),
    "hound-plott": (
        "Plott hound — amerykański pies gończy o brązowej sierści. Odważny, wytrwały w tropieniu i lojalny wobec przewodnika.",
        "USA",
        "23–27 kg",
        "12–14 lat",
    ),
    "hound-walker": (
        "Treeing Walker coonhound — pies gończy na szopy i dziką zwierzynę. Energiczny, głośny w pracy i przyjazny w rodzinie.",
        "USA",
        "23–32 kg",
        "12–13 lat",
    ),
    "kelpie": (
        "Kelpie australijski — legendarny pies pasterski znany ze zwinności. Niezwykle pracowity, inteligentny i wymagający codziennego wysiłku.",
        "Australia",
        "14–21 kg",
        "12–15 lat",
    ),
    "kombai": (
        "Kombai z południowych Indii — pies stróżujący i myśliwski. Odważny, jednoosobowy w lojalności i czujny na własnym terenie.",
        "Indie",
        "20–26 kg",
        "13–15 lat",
    ),
    "mastiff-bull": (
        "Bullmastiff — potężny pies stróżujący wyhodowany do ochrony dóbr. Spokojny, pewny siebie i opiekuńczy wobec rodziny.",
        "Wielka Brytania",
        "41–59 kg",
        "8–10 lat",
    ),
    "mastiff-indian": (
        "Indyjski mastif (bully kutta) — duży pies stróżujący. Silny, dominujący i wymagający doświadczonego właściciela.",
        "Indie / Pakistan",
        "60–90 kg",
        "8–10 lat",
    ),
    "mix": (
        "Kundel lub mieszaniec — pies o zróżnicowanej budowie i charakterze. Często zdrowy genetycznie i wdzięczny za dom.",
        "różne",
        "różna",
        "10–14 lat",
    ),
    "mountain-swiss": (
        "Szwajcarski pies pasterski (szczygiec) — wszechstronny pomocnik na farmie. Spokojny, uczuciowy i dobrze współpracujący z dziećmi.",
        "Szwajcaria",
        "25–35 kg",
        "11–13 lat",
    ),
    "mudhol-indian": (
        "Mudhol hound — indyjski chart używany w polowaniach i na służbie. Szybki, smukły i bardzo zwinny.",
        "Indie",
        "20–28 kg",
        "10–12 lat",
    ),
    "ovcharka-caucasian": (
        "Owczarek kaukaski — potężny stróż stad i majątku. Niezależny, ostrożny wobec obcych i wymagający konsekwentnego prowadzenia.",
        "Kaukaz",
        "45–70 kg",
        "10–12 lat",
    ),
    "pariah-indian": (
        "Indyjski pies parijski — pierwotny typ psa wolno żyjącego w Azji Południowej. Odporny, czujny i łatwo adaptujący się do życia z człowiekiem.",
        "Indie",
        "15–25 kg",
        "13–16 lat",
    ),
    "pointer-germanlonghair": (
        "Wyżeł niemiecki długowłosy — wszechstronny pies myśliwski. Równy charakter, silny instynkt łowiecki i chęć do współpracy z człowiekiem.",
        "Niemcy",
        "27–32 kg",
        "12–14 lat",
    ),
    "poodle-medium": (
        "Pudel średni — inteligentny pies o kręconej, mało pękającej sierści. Żywy, łatwy w szkoleniu i dobry do sportów i towarzystwa.",
        "Francja / Niemcy",
        "14–18 kg",
        "12–15 lat",
    ),
    "poodle-miniature": (
        "Pudel miniaturowy — mniejsza odmiana pudla o wysokiej inteligencji. Wesoły, czujny i świetnie odnajdujący się w mieście.",
        "Francja / Niemcy",
        "4–7 kg",
        "12–15 lat",
    ),
    "poodle-toy": (
        "Pudel toy — najmniejsza odmiana pudla, pies towarzyszący. Przywiązany, elegancki i wymagający regularnej pielęgnacji sierści.",
        "Francja / Niemcy",
        "2–4 kg",
        "12–15 lat",
    ),
    "rajapalayam-indian": (
        "Rajapalayam — biały pies stróżujący z Tamil Nadu. Odważny, wierny jednej rodzinie i czujny na obcych.",
        "Indie",
        "25–32 kg",
        "10–12 lat",
    ),
    "segugio-italian": (
        "Segugio italiano — włoski pies gończy o krótkiej lub szorstkiej sierści. Wytrwały na tropie, spokojny i przyjazny w domu.",
        "Włochy",
        "18–28 kg",
        "11–13 lat",
    ),
    "sheepdog-indian": (
        "Indyjski pies pasterski (himalajski typ) — pomocnik przy trzodzie w górach. Odporny, pracowity i przywiązany do opiekuna.",
        "Indie",
        "25–40 kg",
        "10–12 lat",
    ),
    "spaniel-blenheim": (
        "Cavalier king charles spaniel w ubarwieniu blenheim — pies dworski o długich uszach. Łagodny, towarzyski i kochający bliskość ludzi.",
        "Wielka Brytania",
        "5–8 kg",
        "12–15 lat",
    ),
    "spaniel-japanese": (
        "Japoński spaniel (chin) — mały pies ozdobny z Azji. Dumny, czuły i spokojny w domowym zaciszu.",
        "Japonia / Chiny",
        "2–5 kg",
        "10–12 lat",
    ),
    "spaniel-sussex": (
        "Sussex spaniel — niski, masywny spaniel myśliwski. Spokojny, uparty w polu i bardzo lojalny wobec rodziny.",
        "Wielka Brytania",
        "20–25 kg",
        "13–15 lat",
    ),
    "spitz-indian": (
        "Indyjski spitz — mniejszy pies stróżujący i towarzyszący. Czujny, głośny przy alarmie i przyjazny w domu.",
        "Indie",
        "8–14 kg",
        "10–14 lat",
    ),
    "spitz-japanese": (
        "Japoński spitz — biały pies o puszystej sierści i lisim pysku. Wesoły, czysty w zachowaniu i dobry z dziećmi.",
        "Japonia",
        "5–10 kg",
        "12–16 lat",
    ),
    "terrier-american": (
        "American staffordshire terrier — silny, muskularny pies o wielkim przywiązaniu do ludzi. Pewny siebie, energiczny i wymagający socjalizacji.",
        "USA",
        "25–35 kg",
        "12–16 lat",
    ),
    "terrier-andalusian": (
        "Terier andaluzyjski (Ratonero Bodeguero) — hiszpański pies na szczury i myszy. Zwinny, odważny i żywy.",
        "Hiszpania",
        "5–8 kg",
        "12–16 lat",
    ),
    "terrier-australian": (
        "Terier australijski — mały, twardowłosy pies o zadziornym charakterze. Ciekawski, czujny i pełen energii.",
        "Australia",
        "6–7 kg",
        "11–15 lat",
    ),
    "terrier-bedlington": (
        "Bedlington terrier — pies przypominający baranka o miękkiej sierści. Łagodny w domu, szybki i odważny na zewnątrz.",
        "Wielka Brytania",
        "8–10 kg",
        "12–14 lat",
    ),
    "terrier-border": (
        "Border terrier — niewielki terier z pogranicza angielsko-szkockiego. Odporny, przyjazny i łatwo adaptujący się do różnych warunków.",
        "Wielka Brytania",
        "5–7 kg",
        "12–15 lat",
    ),
    "terrier-boston": (
        "Boston terrier — amerykański pies towarzyszący z krótką sierścią. Inteligentny, wesoły i lubiący być w centrum uwagi.",
        "USA",
        "5–11 kg",
        "11–13 lat",
    ),
    "terrier-dandie": (
        "Dandie dinmont terrier — niski terier z charakterystyczną „grzywą”. Niezależny, spokojny i lojalny wobec swojej rodziny.",
        "Wielka Brytania",
        "8–11 kg",
        "12–15 lat",
    ),
    "terrier-irish": (
        "Irish terrier — „daredevil” wśród terierów o rudym okrywie. Odważny, żywy i pełen humoru.",
        "Irlandia",
        "11–12 kg",
        "13–15 lat",
    ),
    "terrier-kerryblue": (
        "Kerry blue terrier — irlandzki terier o jedwabistej, szaro-niebieskiej sierści. Inteligentny, zabawowy i wymagający konsekwencji.",
        "Irlandia",
        "15–18 kg",
        "12–15 lat",
    ),
    "terrier-lakeland": (
        "Lakeland terrier — zwinny terier z jeziorowej Anglii. Pewny siebie, ciekawski i przyjazny po właściwym wychowaniu.",
        "Wielka Brytania",
        "7–8 kg",
        "12–16 lat",
    ),
    "terrier-norfolk": (
        "Norfolk terrier — mały terier z opuszczonymi uszami. Wesoły, twardy i świetny towarzysz do aktywnego życia.",
        "Wielka Brytania",
        "5–6 kg",
        "12–15 lat",
    ),
    "terrier-norwich": (
        "Norwich terrier — podobny do norfolka, lecz z uszami stojącymi. Odważny, towarzyski i pełen temperamentu.",
        "Wielka Brytania",
        "5–6 kg",
        "12–15 lat",
    ),
    "terrier-patterdale": (
        "Patterdale terrier — zwarty terier z północnej Anglii do pracy w norach. Wytrwały, energiczny i bardzo zdecydowany.",
        "Wielka Brytania",
        "5–6 kg",
        "11–13 lat",
    ),
    "terrier-sealyham": (
        "Sealyham terrier — biały terier z Walii, dawniej pies myśliwski. Spokojniejszy niż wiele terierów, ale nadal pewny siebie.",
        "Wielka Brytania",
        "9–10 kg",
        "12–14 lat",
    ),
    "terrier-silky": (
        "Silky terrier — australijski terier o jedwabistej sierści. Bystry, czujny i przywiązany do opiekuna.",
        "Australia",
        "4–5 kg",
        "12–15 lat",
    ),
    "terrier-tibetan": (
        "Terier tybetański — średni pies stróżujący z długą sierścią. Czujny, niezależny i przyjazny rodzinie.",
        "Tybet",
        "8–14 kg",
        "12–15 lat",
    ),
    "terrier-toy": (
        "Toy terrier (np. toy fox terrier) — miniaturowy terier o żywym temperamencie. Zwinny, odważny i lubiący zabawę.",
        "USA",
        "2–4 kg",
        "13–15 lat",
    ),
    "terrier-welsh": (
        "Welsh terrier — czarno-podpalany terier przypominający airedale w miniaturze. Przyjazny, zabawowy i energiczny.",
        "Walia",
        "9–10 kg",
        "12–15 lat",
    ),
    "terrier-wheaten": (
        "Soft coated wheaten terrier — irlandzki terier o miękkiej, pszennej sierści. Radosny, towarzyski i pełen życia.",
        "Irlandia",
        "14–20 kg",
        "12–14 lat",
    ),
    "tervuren": (
        "Owczarek belgijski tervueren — elegancki pies pasterski o długiej sierści. Inteligentny, czujny i bardzo chętny do pracy.",
        "Belgia",
        "20–30 kg",
        "12–14 lat",
    ),
    "waterdog-spanish": (
        "Hiszpański pies wodny — wszechstronny pies myśliwski i ratowniczy. Łagodny, łatwy w szkoleniu i lubiący wodę.",
        "Hiszpania",
        "14–22 kg",
        "12–14 lat",
    ),
}


def main() -> None:
    breeds = json.loads(PATH.read_text(encoding="utf-8"))
    updated = 0
    for breed in breeds:
        bid = breed["id"]
        if bid not in UPDATES:
            if PLACEHOLDER.match((breed.get("description") or "").strip()):
                raise SystemExit(f"Brak opisu w słowniku: {bid}")
            continue
        desc, origin, weight, lifespan = UPDATES[bid]
        breed["description"] = desc
        if origin:
            breed["origin"] = origin
        if weight:
            breed["weight"] = weight
        if lifespan:
            breed["lifespan"] = lifespan
        updated += 1

    PATH.write_text(json.dumps(breeds, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Zaktualizowano: {updated} ras")


if __name__ == "__main__":
    main()
