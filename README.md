# CSP-Compliant Russian Translator & Phonetic Guide

A lightweight JavaScript utility designed to bypass strict Content Security Policies (like Wikipedia's) by routing translation requests through Google's whitelisted endpoints. It displays the English translation and an instant, locally-computed pronunciation guide with word-final devoicing.

## Implementation Guide

1. **Copy the Code Block** below using the copy button in the top-right corner of the block.
2. Open your target webpage (works perfectly on Wikipedia/Wiktionary).
3. Press `F12` (or right-click and select **Inspect**) to open Developer Tools, then click the **Console** tab.
4. Paste the code into the command line and press `Enter`.
5. Highlight any Russian word or phrase.

```javascript
(function () {
    // ── Phonetic engine with word-final devoicing ──────────────────────────
    function getPronunciationGuide(text) {
        let adjusted = text
            .replace(/[бБ]([ьЬ]?)(?![а-яА-ЯёЁ])/g, (m, s) => (m[0] === m[0].toUpperCase() ? 'П' : 'п') + s)
            .replace(/[вВ]([ьЬ]?)(?![а-яА-ЯёЁ])/g, (m, s) => (m[0] === m[0].toUpperCase() ? 'Ф' : 'ф') + s)
            .replace(/[гГ]([ьЬ]?)(?![а-яА-ЯёЁ])/g, (m, s) => (m[0] === m[0].toUpperCase() ? 'К' : 'к') + s)
            .replace(/[дД]([ьЬ]?)(?![а-яА-ЯёЁ])/g, (m, s) => (m[0] === m[0].toUpperCase() ? 'Т' : 'т') + s)
            .replace(/[жЖ]([ьЬ]?)(?![а-яА-ЯёЁ])/g, (m, s) => (m[0] === m[0].toUpperCase() ? 'Ш' : 'ш') + s)
            .replace(/[зЗ]([ьЬ]?)(?![а-яА-ЯёЁ])/g, (m, s) => (m[0] === m[0].toUpperCase() ? 'С' : 'с') + s);

        const map = {
            'а':'a','б':'b','в':'v','г':'g','д':'d','е':'ye','ё':'yo','ж':'zh','з':'z',
            'и':'i','й':'y','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r',
            'с':'s','т':'t','у':'u','ф':'f','х':'kh','ц':'ts','ч':'ch','ш':'sh',
            'щ':'shch','ъ':'','ы':'y','ь':"'",'э':'e','ю':'yu','я':'ya',
            'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'Ye','Ё':'Yo','Ж':'Zh','З':'Z',
            'И':'I','Й':'Y','К':'K','Л':'L','М':'M','Н':'N','О':'O','П':'P','Р':'R',
            'С':'S','Т':'T','У':'U','Ф':'F','Х':'Kh','Ц':'Ts','Ч':'Ch','Ш':'Sh',
            'Щ':'Shch','Ъ':'','Ы':'Y','Ь':"'",'Э':'E','Ю':'Yu','Я':'Ya'
        };

        return adjusted.split('').map(c => c in map ? map[c] : c).join('');
    }

    // ── Voice pronunciation ────────────────────────────────────────────────
    let isSpeaking = false;

    function pronounce(text, btn) {
        if (!window.speechSynthesis) return;

        if (isSpeaking) {
            window.speechSynthesis.cancel();
            isSpeaking = false;
            btn.textContent = '🔊 Pronounce';
            btn.style.background = '#cba6f7';
            return;
        }

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'ru-RU';
        utterance.rate = 0.85;

        // Prefer a Russian voice if available, fall back to lang match
        const voices = window.speechSynthesis.getVoices();
        const ruVoice = voices.find(v => v.lang === 'ru-RU') || voices.find(v => v.lang.startsWith('ru'));
        if (ruVoice) utterance.voice = ruVoice;

        utterance.onstart = () => {
            isSpeaking = true;
            btn.textContent = '⏹ Stop';
            btn.style.background = '#f38ba8';
        };
        utterance.onend = utterance.onerror = () => {
            isSpeaking = false;
            btn.textContent = '🔊 Pronounce';
            btn.style.background = '#cba6f7';
        };

        window.speechSynthesis.speak(utterance);
    }

    // ── Floating tooltip ───────────────────────────────────────────────────
    const box = document.createElement('div');
    Object.assign(box.style, {
        position: 'fixed',
        zIndex: '2147483647',
        backgroundColor: '#1e1e2e',
        color: '#cdd6f4',
        padding: '12px',
        borderRadius: '8px',
        boxShadow: '0 4px 15px rgba(0,0,0,0.5)',
        fontFamily: 'sans-serif',
        fontSize: '14px',
        lineHeight: '1.4',
        display: 'none',
        maxWidth: '320px',
        minWidth: '220px',
    });
    document.body.appendChild(box);

    box.addEventListener('mousedown', e => e.stopPropagation());
    box.addEventListener('mouseup', e => e.stopPropagation());

    // ── Selection handler ──────────────────────────────────────────────────
    document.addEventListener('mouseup', async (e) => {
        if (box.contains(e.target)) return;

        const selectedText = window.getSelection().toString().trim();
        if (!selectedText || !/[Ѐ-ӿ]/.test(selectedText)) {
            box.style.display = 'none';
            return;
        }

        // Stop any ongoing speech when a new selection is made
        if (isSpeaking) {
            window.speechSynthesis.cancel();
            isSpeaking = false;
        }

        const pronunciation = getPronunciationGuide(selectedText);

        // Position box — keep it inside viewport
        const x = Math.min(e.clientX + 12, window.innerWidth - 335);
        const y = Math.min(e.clientY + 12, window.innerHeight - 200);
        box.style.left = `${x}px`;
        box.style.top = `${y}px`;

        box.innerHTML = '<span style="color:#a6e3a1;">Translating…</span>';
        box.style.display = 'block';

        try {
            const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=ru&tl=en&dt=t&q=${encodeURIComponent(selectedText)}`;
            const response = await fetch(url);
            const data = await response.json();

            if (data && data[0] && data[0][0] && data[0][0][0]) {
                const translation = data[0].map(x => x[0]).join('');

                box.innerHTML = `
                    <div style="margin-bottom:6px"><strong>Original:</strong> <span style="color:#f5c2e7">${selectedText}</span></div>
                    <div style="margin-bottom:6px"><strong>Pronunciation:</strong> <span style="color:#f9e2af;font-style:italic">${pronunciation}</span></div>
                    <div style="margin-bottom:10px"><strong>Translation:</strong> <span style="color:#a6e3a1">${translation}</span></div>
                    <div style="display:flex;gap:6px">
                        <button id="ext-pronounce-btn" style="flex:1;background:#cba6f7;color:#11111b;border:none;padding:6px 8px;border-radius:4px;cursor:pointer;font-weight:bold">🔊 Pronounce</button>
                        <button id="ext-copy-btn" style="flex:1;background:#89b4fa;color:#11111b;border:none;padding:6px 8px;border-radius:4px;cursor:pointer;font-weight:bold">Copy</button>
                    </div>
                `;

                const pronounceBtn = document.getElementById('ext-pronounce-btn');
                const copyBtn = document.getElementById('ext-copy-btn');

                pronounceBtn.addEventListener('click', (ev) => {
                    ev.stopPropagation();
                    pronounce(selectedText, pronounceBtn);
                });

                copyBtn.addEventListener('click', (ev) => {
                    ev.stopPropagation();
                    navigator.clipboard.writeText(selectedText).then(() => {
                        copyBtn.textContent = 'Copied!';
                        copyBtn.style.background = '#a6e3a1';
                        setTimeout(() => {
                            copyBtn.textContent = 'Copy';
                            copyBtn.style.background = '#89b4fa';
                        }, 1500);
                    });
                });

                // Trigger voice loading early so first click isn't delayed
                window.speechSynthesis.getVoices();

            } else {
                box.innerHTML = '<span style="color:#f38ba8">Translation parsing failed.</span>';
            }
        } catch (err) {
            box.innerHTML = '<span style="color:#f38ba8">Network error — check connection.</span>';
            console.error('[RU Translator]', err);
        }
    });

    document.addEventListener('mousedown', (e) => {
        if (!box.contains(e.target)) {
            box.style.display = 'none';
            if (isSpeaking) {
                window.speechSynthesis.cancel();
                isSpeaking = false;
            }
        }
    });

    console.log('%c🇷🇺 Russian Translator & Pronouncer loaded', 'color:#a6e3a1;font-weight:bold;font-size:13px');
})();
