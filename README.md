# GMxLRC
<img src="icon.png" height="128"><br>
A simple GUI for [MxLRC](https://github.com/fashni/MxLRC) by [fashni](https://github.com/fashni)

## Song List
Here's an example<br>
```text
The Killers, Mr. Brightside
Michael Jackson, The Girl Is Mine
<artist>, <title>
```

## Config File
- Auto-Generate/Read settings from `config.json`<Br>
Example Config File:<Br>
```json
{
    "token": "",
    "darkmode": "1",
    "quiet": "0",
    "update": "0",
    "bfs": "0",
    "sleep": "30",
    "depth": "100",
    "output": "lyrics"
}
```

## Requirements
- Python 3.8+
- pyqt5
- tinytag

## Build
1. clone this repo
2. cd to folder
3. run `pyinstaller build.spec` in terminal

## LICENSE
[The MIT License](LICENSE)
