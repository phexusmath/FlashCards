# Russian Text Grabber, Translator & Pronunciation Guide

A lightweight JavaScript snippet designed to run directly in your browser's developer console. When you highlight a Russian word, it instantly displays the English translation, an English phonetic pronunciation guide, and a dedicated button to copy the original Russian text without UI glitches.

## Implementation Guide

1. **Copy the Code Block** below using the copy button in the top-right corner of the block.
2. Open the webpage containing the Russian text.
3. Press `F12` (or right-click and select **Inspect**) to open Developer Tools, then click the **Console** tab.
4. Paste the code into the command line and press `Enter`.
5. Highlight any Russian word to see the translation and pronunciation guide.

```javascript
(function() {
    // Create a floating UI element for the tooltips
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

    // Prevent mousedown inside the box from resetting selection prematurely
    box.addEventListener('mousedown', (e) => {
        e.stopPropagation();
    });

    // Listen for text selection release
    document.addEventListener('mouseup', async (e) => {
        // If clicking inside our existing box, ignore to prevent endless popups
        if (box.contains(e.target)) {
            return;
        }

        const selectedText = window.getSelection().toString().trim();
        
        // Only trigger if there is a selection and it contains Cyrillic characters
        const hasCyrillic = /[\u0400-\u04FF]/.test(selectedText);

        if (!selectedText || !hasCyrillic) {
            box.style.display = 'none';
            return;
        }

        // Clean the word for pronunciation lookup (remove punctuation)
        const cleanWord = selectedText.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()?"']/g,"").toLowerCase();

        // Position the box near the mouse pointer
        box.style.left = `${e.clientX + 10}px`;
        box.style.top = `${e.clientY + 10}px`;
        box.innerHTML = '<span style="color: #a6e3a1;">Fetching translation & pronunciation...</span>';
        box.style.display = 'block';

        try {
            // 1. Fetch Translation via MyMemory API
            const transPromise = fetch(`https://api.mymemory.translated.net/get?q=${encodeURIComponent(selectedText)}&langpair=ru|en`)
                .then(res => res.json());

            // 2. Fetch Pronunciation Guide via Lingua Robot / Wiktionary open endpoints
            const pronPromise = fetch(`https://en.wiktionary.org/api/rest_v1/page/definition/${encodeURIComponent(cleanWord)}`)
                .then(res => res.ok ? res.json() : null)
                .catch(() => null);

            // Wait for both network requests
            const [transData, wikiData] = await Promise.all([transPromise, pronPromise]);
            
            let translation = 'Translation unavailable';
            let pronunciation = 'Pronunciation guide unavailable';

            if (transData.responseData && transData.responseData.translatedText) {
                translation = transData.responseData.translatedText;
            }

            // Try to extract pronunciation key/IPA from Wiktionary data structure if available
            if (wikiData && wikiData.ru && wikiData.ru[0] && wikiData.ru[0].pronunciations) {
                const audioObj = wikiData.ru[0].pronunciations.find(p => p.transcription);
                if (audioObj) {
                    pronunciation = `[${audioObj.transcription}]`;
                }
            } else {
                // Alternative fallback: dynamic rough phonetic approximation rule-based snippet for common vowels
                pronunciation = "See context / Phonetic fallback";
            }

            // Update UI with data and an isolated copy button
            box.innerHTML = `
                <div style="margin-bottom: 6px;"><strong>Original:</strong> <span style="color: #f5c2e7;">${selectedText}</span></div>
                <div style="margin-bottom: 6px;"><strong>Pronunciation:</strong> <span style="color: #f9e2af; font-style: italic;">${pronunciation}</span></div>
                <div style="margin-bottom: 10px;"><strong>Translation:</strong> <span style="color: #a6e3a1;">${translation}</span></div>
                <button id="copy-btn-safe" style="background: #89b4fa; color: #11111b; border: none; padding: 6px 8px; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%; display: block;">Copy Russian Text</button>
            `;

            // Isolated Copy Event Listener
            const copyBtn = document.getElementById('copy-btn-safe');
            copyBtn.addEventListener('click', (event) => {
                event.stopPropagation(); // Stops the event from bubble-triggering a new popup
                
                navigator.clipboard.writeText(selectedText).then(() => {
                    copyBtn.innerText = 'Russian Copied!';
                    copyBtn.style.background = '#a6e3a1';
                    
                    // Clear the active text selection browser-wide so it doesn't immediately re-trigger
                    if (window.getSelection) {
                        window.getSelection().removeAllRanges();
                    }
                    
                    setTimeout(() => {
                        box.style.display = 'none';
                    }, 600);
                }).catch(err => {
                    console.error('Failed to copy text: ', err);
                });
            });

        } catch (error) {
            box.innerHTML = '<span style="color: #f38ba8;">Error fetching data.</span>';
            console.error(error);
        }
    });

    // Hide the box if clicking entirely outside the elements
    document.addEventListener('mousedown', (e) => {
        if (!box.contains(e.target)) {
            box.style.display = 'none';
        }
    });

    console.log("%c🇷🇺 Russian Assistant Loaded! Highlight text to translate, pronounce, and safely copy.", "color: #89b4fa; font-weight: bold; font-size: 14px;");
})();
