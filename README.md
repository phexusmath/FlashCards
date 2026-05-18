# Inline Russian Text Grabber & Translator Script

A lightweight, zero-dependency JavaScript snippet designed to run directly in your browser's developer console. When you highlight any Russian text on a webpage, a floating tooltip instantly displays the English translation and provides a quick-copy utility to grab the **original Russian text** to your clipboard.

## Implementation Guide

1. **Copy the Code Block** below using the copy button in the top-right corner of the block.
2. Open the webpage containing the text you wish to translate and copy.
3. Press `F12` (or right-click and select **Inspect**) to open Developer Tools, then click the **Console** tab.
4. Paste the code into the command line and press `Enter`.
5. Highlight any Russian word or phrase to activate the utility.

```javascript
(function() {
    // Create a floating UI element for the translation hook
    const box = document.createElement('div');
    box.style.position = 'fixed';
    box.style.zIndex = '10000';
    box.style.backgroundColor = '#1e1e2e';
    box.style.color = '#cdd6f4';
    box.style.padding = '10px';
    box.style.borderRadius = '8px';
    box.style.boxShadow = '0 4px 15px rgba(0,0,0,0.5)';
    box.style.fontFamily = 'sans-serif';
    box.style.fontSize = '14px';
    box.style.display = 'none';
    box.style.maxWidth = '300px';
    document.body.appendChild(box);

    let currentTranslation = '';

    // Listen for text selection release
    document.addEventListener('mouseup', async (e) => {
        const selectedText = window.getSelection().toString().trim();
        
        // Only trigger if there is a selection and it contains Cyrillic/Russian characters
        const hasCyrillic = /[\u0400-\u04FF]/.test(selectedText);

        if (!selectedText || !hasCyrillic) {
            box.style.display = 'none';
            return;
        }

        // Position the box near the mouse pointer
        box.style.left = `${e.clientX + 10}px`;
        box.style.top = `${e.clientY + 10}px`;
        box.innerHTML = '<span style="color: #a6e3a1;">Translating...</span>';
        box.style.display = 'block';

        try {
            // Fetch translation from Russian (ru) to English (en) using the public MyMemory API
            const response = await fetch(`https://api.mymemory.translated.net/get?q=${encodeURIComponent(selectedText)}&langpair=ru|en`);
            const data = await response.json();
            
            if (data.responseData && data.responseData.translatedText) {
                currentTranslation = data.responseData.translatedText;
                
                // Update UI with translation and a button configured to copy the original Russian text
                box.innerHTML = `
                    <div style="margin-bottom: 8px;"><strong>Original:</strong> ${selectedText}</div>
                    <div style="margin-bottom: 8px;"><strong>Translation:</strong> ${currentTranslation}</div>
                    <button id="copy-btn" style="background: #89b4fa; color: #11111b; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%;">Copy Russian Text</button>
                `;

                // Add copy functionality targeting the original text
                document.getElementById('copy-btn').addEventListener('click', () => {
                    navigator.clipboard.writeText(selectedText).then(() => {
                        const btn = document.getElementById('copy-btn');
                        btn.innerText = 'Russian Copied!';
                        btn.style.background = '#a6e3a1';
                        setTimeout(() => box.style.display = 'none', 800);
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

    // Hide the box if clicking elsewhere without selecting new text
    document.addEventListener('mousedown', (e) => {
        if (!box.contains(e.target)) {
            box.style.display = 'none';
        }
    });

    console.log("%c🇷🇺 Russian Text Grabber Loaded! Highlight any Russian text to translate and copy.", "color: #89b4fa; font-weight: bold; font-size: 14px;");
})();
