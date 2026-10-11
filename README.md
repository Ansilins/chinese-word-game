# Chinese Word Game · 汉语

A small game for learning Mandarin Chinese: HSK 1 and HSK 2 vocabulary in bite-sized units, plus a Pinyin basics track for the sounds (4 tones, 23 initials, 24 finals and the 2 tone rules). A reels-style swipe feed, flashcards, a quiz, listening, matching pairs, a tone quiz, a searchable word list, and speaking practice with a pronunciation score.

**Play it:** https://ansilins.github.io/chinese-word-game/

## Put it on an iPhone home screen

1. Open the link above in **Safari**.
2. Tap **Share** (on iOS 26 it sits in the **⋯** menu), then **Add to Home Screen**.
3. Keep **Open as Web App** switched on and tap **Add**.

The game then opens full screen from its own icon. Open it once from the icon while you're online; after that it works offline.

**Progress is saved inside the Home Screen app on that device.** It is separate from Safari (progress you made in a Safari tab doesn't move over) and from other devices, and **removing the icon deletes it**.

For the voice, the phone needs a Mandarin voice: Settings, Accessibility, Spoken Content, Voices, Chinese (China mainland). No sound? Turn off silent mode.

Speaking practice uses a speech checker that runs on the phone. The first time you use it, it downloads about 80 MB (Wi-Fi is best); after that it works offline. The checker hears words, not pitch: a tone slip only shows when it hears a different character (for example "heard 买 mǎi, wanted 卖 mài").

## How the game works

- **刷词 Swipe** works like reels: full-screen cards, swipe up for the next one. New words are introduced, then come back as quick tests: a “do you remember?” card you swipe right if you knew it and left if you didn't, a meaning pick, a listening pick and a tone pick. Double-tap a card to ❤️ save the word (it's starred in the word list). It uses this unit, with some words from finished units mixed in.
- Each level is split into units of at most 12 words, with topics mixed. A word counts as learned after 3 right answers (a wrong answer moves it back one step) and is mastered after 5. When 80% of a unit is learned, the next unit opens. Practice only uses the current unit, finished units and a mixed review of them.
- Pinyin is coloured by tone everywhere: 1st red, 2nd orange, 3rd green, 4th blue, neutral grey. The **Pinyin hide** switch hides it in the games so you can test yourself on characters only.
- The tone quiz accepts both the written and the spoken tones where they change in speech (two 3rd tones like 你好 nǐ hǎo, said ní hǎo; 一 and 不) and explains why.
- Speaking is scored by comparing pinyin, not characters, so homophones and traditional characters aren't mistakes. 儿 is optional on words ending in r, and digits count when the value matches ("2" for 二 and 两).
- Progress is stored in this browser under keys starting with `cwg-`, and every cache name starts with `cwg-`, so it never touches the German game on the same address.

## Building

`index.html`, `sw.js`, `manifest.webmanifest` and `asr-worker.js` are generated. Edit the files in `src/` and run:

```
python3 src/build.py
```

Every build gives `sw.js` a new version (a hash of the app files), so phones pick up the change the next time the app comes to the front.

## Credits

- Word lists are based on the classic HSK 1 and HSK 2 (HSK 2.0) vocabulary lists, plus 你好; English meanings and topics were added for this game.
- `lib/pinyin-pro.min.js` is [pinyin-pro](https://github.com/zh-lx/pinyin-pro) 3.29.5 (MIT), bundled so speaking works offline.
- `vendor/` holds [transformers.js](https://github.com/huggingface/transformers.js) 3.5.1 and its ONNX Runtime files; the Whisper model (Xenova/whisper-base) is downloaded once from Hugging Face.
- The structure, home-screen setup and speech checker come from [Deutsch Wortspiel](https://github.com/Ansilins/deutsch-wortspiel).
