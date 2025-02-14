<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Immersive Chinese Reading</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f0f2f5;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }
        .search-bar {
            margin-bottom: 20px;
        }
        .search-bar input {
            width: 100%;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #ccc;
            font-size: 1em;
        }
        .sentence {
            margin: 20px 0;
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .sentence:hover {
            background-color: #e6f7ff;
        }
        .chinese {
            font-size: 1.5em;
            color: #333;
        }
        .pinyin {
            font-size: 1em;
            color: #888;
            margin-top: 5px;
        }
        .translation {
            margin-top: 5px;
            font-size: 1.2em;
            color: #555;
        }
        .tooltip {
            position: relative;
            display: inline-block;
        }
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 200px;
            background-color: #333;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
        }
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="search-bar">
            <input type="text" id="searchInput" placeholder="Search sentences...">
        </div>
        <div id="content"></div>
    </div>

    <script>
        const data = [
            {
                "sentences": "你好！",
                "pinyin": "nǐ hǎo",
                "translation": "Hello!",
                "meanings": "hello; hi",
                "hsk-tag": "HSK1"
            },
            {
                "sentences": "谢谢你！",
                "pinyin": "xièxiè nǐ",
                "translation": "Thank you!",
                "meanings": "thanks; thank you",
                "hsk-tag": "HSK1"
            },
            {
                "sentences": "你会说中文吗？",
                "pinyin": "nǐ huì shuō zhōngwén ma?",
                "translation": "Can you speak Chinese?",
                "meanings": "you; can; speak; Chinese; question",
                "hsk-tag": "HSK1"
            }
        ];

        const contentDiv = document.getElementById('content');
        const searchInput = document.getElementById('searchInput');

        function renderSentences(filteredData) {
            contentDiv.innerHTML = '';
            filteredData.forEach(item => {
                const sentenceDiv = document.createElement('div');
                sentenceDiv.className = 'sentence';

                const chinese = document.createElement('div');
                chinese.className = 'chinese';
                chinese.textContent = item.sentences;

                const pinyin = document.createElement('div');
                pinyin.className = 'pinyin';
                pinyin.textContent = item.pinyin;

                const translation = document.createElement('div');
                translation.className = 'translation';
                translation.textContent = item.translation;

                const tooltip = document.createElement('div');
                tooltip.className = 'tooltip';
                tooltip.textContent = '🔍';

                const tooltipText = document.createElement('span');
                tooltipText.className = 'tooltiptext';
                tooltipText.textContent = item.meanings;

                tooltip.appendChild(tooltipText);

                sentenceDiv.appendChild(chinese);
                sentenceDiv.appendChild(pinyin);
                sentenceDiv.appendChild(translation);
                sentenceDiv.appendChild(tooltip);

                contentDiv.appendChild(sentenceDiv);
            });
        }

        searchInput.addEventListener('input', () => {
            const searchTerm = searchInput.value.toLowerCase();
            const filtered = data.filter(item =>
                item.sentences.includes(searchTerm) ||
                item.pinyin.includes(searchTerm) ||
                item.translation.toLowerCase().includes(searchTerm)
            );
            renderSentences(filtered);
        });

        renderSentences(data);
    </script>
</body>
</html>
