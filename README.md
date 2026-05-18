# Russian Translator & Smart Phonetic Guide (with Word-Final Devoicing)

A zero-dependency JavaScript utility designed for your browser console. When you highlight Russian text, it displays the English translation and an advanced, locally-computed English pronunciation guide. This version intelligently accounts for **word-final devoicing**, swapping voiced consonants to their unvoiced counterparts if they appear at the end of a word.

## Implementation Guide

1. **Copy the Code Block** below using the copy button in the top-right corner of the block.
2. Open the webpage containing the Russian text.
3. Press `F12` (or right-click and select **Inspect**) to open Developer Tools, then click the **Console** tab.
4. Paste the code into the command line and press `Enter`.
5. Highlight any Russian word or phrase to see it in action.

```javascript
(function() {
    // Advanced phonetic engine with word-final devoicing rules built-in
    function getPronunciationGuide(text) {
        // 1. Handle Word-Final Devoicing (Point Numero Duo)
        // Maps voiced consonants to unvoiced equivalents when at the end of a word, 
        // or right before an optional soft sign (ь) at the end of a word.
        let adjustedText = text
            .replace(/[бБ]([ьЬ]?)(?![а-яА-ЯёЁ])/g, (match, p1) => (match === match.toUpperCase() ? 'П' : 'п') + p1)
            .replace(/[вВ]([ьЬ]?)(?![а-яА-ЯёЁ])/g, (match, p1) => (match === match.toUpperCase() ? 'Ф' : 'ф') + p1)
            .replace(/[гГ]([ьЬ]?)(?![а-яА-ЯёЁ])/g, (match, p1) => (match === match.toUpperCase() ? 'К' : 'к') + p1)
            .replace(/[дД]([ьЬ]?)(?![а-яА-ЯёЁ])/g, (match, p1) => (match === match.toUpperCase() ? 'Т' : 'т') + p1)
            .replace(/[жЖ]([ьЬ]?)(?![а-яА-ЯёЁ])/g, (match, p1) => (match === match.toUpperCase() ? 'Ш' : 'ш') + p1)
            .replace(/[зЗ]([ьЬ]?)(?![а-яА-ЯёЁ])/g, (match, p1) => (match === match.toUpperCase() ? 'С' : 'с') + p1);

        // 2. Standard Transliteration Map
        const cyrillicToPhonetic = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'ye', 'ё': 'yo', 
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 
            'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 
            'ъ': '', 'ы': 'y', 'ь': "'", 'э': 'e', 'ю': 'yu', 'я': 'ya',
            'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'Ye', 'Ё': 'Yo', 
            'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 
            'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 
            'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 
            'Ъ': '', 'Ы': 'Y', 'Ь': "'", 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
        };
        
        return adjustedText.split('').map(char => cyrillicToPhonetic[char] !== undefined ? cyrillicToPhonetic[char] : char).join('');
    }

    // Create a persistent floating UI element
    const box = document.createElement('div');
    box.style.position = 'fixed';
    box.style.zIndex = '10000';
    box.style.backgroundColor = '#1e1e2e';
    box.style.color = '#cdd6f4';
    box.style.padding = '12px';
    box.style.borderRadius = '8px';
    box.style.boxShadow = '0 4px 15px rgba(0,0,0,0.5)';
    box.style.fontFamily = 'sans-serif';
    box.style.fontSize = '14px';
    box.style.lineHeight = '1.4';
    box.style.display = 'none';
    box.style.maxWidth = '320px';
    document.body.appendChild(box);

    // Prevent popups from breaking on internal box interactions
    box.addEventListener('mousedown', (e) => e.stopPropagation());
    box.addEventListener('mouseup', (e) => e.stopPropagation());

    // Main text selection trigger
    document.addEventListener('mouseup', async (e) => {
        if (box.contains(e.target)) return;

        const selectedText = window.getSelection().toString().trim();
        const hasCyrillic = /[\u0400-\u04FF]/.test(selectedText);

        if (!selectedText || !hasCyrillic) {
            box.style.display = 'none';
            return;
        }

        // Generate the accurate phonetic guide locally
        const pronunciation = getPronunciationGuide(selectedText);

        box.style.left = `${e.clientX + 10}px`;
        box.style.top = `${e.clientY + 10}px`;
        box.innerHTML = '<span style="color: #a6e3a1;">Translating...</span>';
        box.style.display = 'block';

        try {
            const response = await fetch(`https://api.mymemory.translated.net/get?q=${encodeURIComponent(selectedText)}&langpair=ru|en`);
            const data = await response.json();
            
            if (data.responseData && data.responseData.translatedText) {
                const translation = data.responseData.translatedText;
                
                box.innerHTML = `
                    <div style="margin-bottom: 6px;"><strong>Original:</strong> <span style="color: #f5c2e7;">${selectedText}</span></div>
                    <div style="margin-bottom: 6px;"><strong>Pronunciation:</strong> <span style="color: #f9e2af; font-style: italic;">${pronunciation}</span></div>
                    <div style="margin-bottom: 10px;"><strong>Translation:</strong> <span style="color: #a6e3a1;">${translation}</span></div>
                    <button id="copy-btn-sticky" style="background: #89b4fa; color: #11111b; border: none; padding: 6px 8px; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%; display: block;">Copy Russian Text</button>
                `;

                const copyBtn = document.getElementById('copy-btn-sticky');
                copyBtn.addEventListener('click', (event) => {
                    event.stopPropagation();
                    navigator.clipboard.writeText(selectedText).then(() => {
                        copyBtn.innerText = 'Russian Copied!';
                        copyBtn.style.background = '#a6e3a1';
                    }).catch(err => {
                        console.error('Failed to copy text: ', err);
                    });
                });
            } else {
                box.innerHTML = '<span style="color: #f38ba8;">Translation failed.</span>';
            }
        } catch (error) {
            box.innerHTML = '<span style="color: #f38ba8;">Error fetching translation.</span>';
            console.error(error);
        }
    });

    document.addEventListener('mousedown', (e) => {
        if (!box.contains(e.target)) {
            box.style.display = 'none';
        }
    });

    console.log("%c🇷🇺 Smart Pronunciation Translator Loaded!", "color: #89b4fa; font-weight: bold; font-size: 14px;");
})();
